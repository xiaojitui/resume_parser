#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import os
import pdfplumber
import docx
import pickle
from tqdm import tqdm


# In[ ]:


def getpdf(pdffile):
    alltext = []

    with pdfplumber.open(pdffile) as pdf:
        pages = pdf.pages
        page_n = len(pages)
        for i in range(page_n):
            page = pdf.pages[i]
            text = page.extract_text()
            if text is not None:
                alltext.append(text)
    alltext = ''.join([k for k in alltext])       
    return alltext


# In[ ]:


def getpdf_raw(pdffile, x_tol = 2, y_tol = 0):
    alltext = []
    allwords = []
    with pdfplumber.open(pdffile) as pdf:
        pages = pdf.pages
        page_n = len(pages)
        for i in range(page_n):
            page = pdf.pages[i]
            text = page.extract_text(x_tolerance = x_tol, y_tolerance = y_tol)
            words = page.extract_words(x_tolerance = x_tol, y_tolerance = y_tol)
            if text is not None:
                alltext.append(text)
                allwords.append(words)
    #alltext = ''.join([k for k in alltext])
    
    return alltext, allwords


# In[ ]:


def getdoc(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    alltext = ''.join(fullText)
    
    return alltext


# In[ ]:


def file_to_text(folder):
    allfiles = os.listdir(folder)

    file_dict = {}
    for file in tqdm(allfiles, total = len(allfiles)):
        text = ''
        if file.endswith('pdf') or file.endswith('PDF'):
            text = getpdf(folder + file)
        if file.endswith('docx') or file.endswith('DOCX'):
            text = getdoc(folder + file)

        file_dict[file] = text


    with open('./parsed_text.pkl', 'wb') as f:
        pickle.dump(file_dict, f)
        
    return file_dict


# In[ ]:


def groupwords(allwords, row_tol = 3, col_tol = 6): #row_tol = 1.5, 
    
    allwords_clean = []
    
    for words in allwords:
        
        if words == []:
            allwords_clean.append([])
            continue
        
        # find rows first
        words[0]['row'] = 0
        for i in range(1, len(words)):
            ##### loose condition: use or; strict condition: use and
            if abs(words[i]['top'] - words[i-1]['top']) <= row_tol and abs(words[i]['bottom'] - words[i-1]['bottom']) <= row_tol:
                words[i]['row'] = words[i-1]['row']
            else:
                words[i]['row'] = words[i-1]['row'] + 1
                
        # then group words
        words_clean = []
        i = 0
        while i < len(words):

            x0 = words[i]['x0']  # need some tolerence?
            x1 = words[i]['x1']
            text = words[i]['text']
            top = words[i]['top']
            bottom = words[i]['bottom']
            row = words[i]['row']

            j = i + 1
            
            while j < len(words) and words[j]['row'] == words[j-1]['row'] and abs(words[j]['x0'] - words[j-1]['x1']) <= col_tol:
                x0 = min(x0, words[j-1]['x0'])
                x1 = max(x1, words[j]['x1'])
                text = text + ' ' + words[j]['text']
                j = j + 1
            
            # do some cleaning for $ sign
            #if words[j-1]['text'].strip() == '$':
                #x1 = min(x1, words[j-2]['x1'])
                #text = text.strip().strip('$').strip()
            
            words_clean.append({'x0': int(x0), 'x1': int(x1), 'top': int(top), 'bottom': int(bottom), 
                                 'text': text, 'row': int(row)})
            i = j
          
        allwords_clean.append(words_clean)
    
    return allwords_clean


# In[ ]:


def clean_row(vals):
    
    vals_clean = []
    for k in vals:
        if k.strip() in ['•', '·', '’']:
            continue
        else:
            vals_clean.append(k.replace('\u200b', ' '))
            
    return vals_clean


# In[ ]:


def get_headers(allwords, tol = 6):
    
    header_tracker = {}
    for page in range(len(allwords)):
        if allwords[page] == []:
            continue
        
        header_tracker[page] = []
        word_df = pd.DataFrame(allwords[page])
        text_count = word_df.groupby(['row'])['text'].count()
        for i in range(len(text_count)):
            if text_count[i] == 1:
                val = word_df[word_df['row'] == i]['text'].values[0]
                #height = s[s['row'] == i]['bottom'].values[0] - s[s['row'] == i]['top'].values[0]
                if val not in ['•', '·', '’'] and ',' not in val and not val.endswith('.') and                     '[' not in val and val[0].isupper() and len(val.strip().split()) <= tol:
                    header_tracker[page].append([i, val])
    return header_tracker


# In[ ]:


def get_sub_headers(allwords, tol = 6):
    header_tracker = {}
    for page in range(len(allwords)):
        if allwords[page] == []:
            continue
        header_tracker[page] = []
        word_df = pd.DataFrame(allwords[page])
        text_count = word_df.groupby(['row'])['text'].count()
        for i in range(len(text_count)):
            if text_count[i] <= 5:
                vals = word_df[word_df['row'] == i]['text'].values
                vals_clean = clean_row(vals)
                if len(vals_clean) < 1:
                    continue
                section_n = 0
                for val in vals:
                    if len(val.strip().split()) <= tol:
                        section_n += 1
                if section_n == len(vals) and np.any([k[0].isupper() for k in vals_clean]) and                     not np.all([k.endswith('.') for k in vals_clean]) and not np.all([('[' in k) for k in vals_clean]):
                    header_tracker[page].append([i, vals_clean])
    return header_tracker


# In[ ]:


def add_sub_headers(allwords, header_tracker, tol = 80):
    
    for page in header_tracker:
        if header_tracker[page] == []:
            continue
        
        add_rows = []
        allword = pd.DataFrame(allwords[page])
        rows = allword.row.max()
        row_sep_record = {}
        for i in range(rows):
            x0s = allword[allword['row'] == i]['x0'].values[1:]
            x1s = allword[allword['row'] == i]['x1'].values[:-1]
            if len(x0s) == 0 and len(x1s) == 0:
                add_rows.append(i)
            else:
                sep = max(x0s-x1s)
                if sep >= tol:
                    add_rows.append(i)
        for add_row in add_rows:
            if add_row not in [k[0] for k in header_tracker[page]]:
                vals = allword[allword['row'] == add_row]['text'].values
                vals_clean = clean_row(vals)
                
                header_tracker[page].append([add_row, vals_clean])
        
    return header_tracker


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




