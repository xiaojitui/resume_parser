#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import PyPDF2
import os
from io import StringIO
import pandas as pd
import numpy as np
from collections import Counter
import pickle
from tqdm import tqdm
import matplotlib.pyplot as plt
# python -m spacy download en_core_web_sm
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import PhraseMatcher

from similar_word import check_similar_word


# In[ ]:


#function that does phrase matching and builds a candidate profile
def create_profile(data, name):
    
    text = data['X']
    text = str(text)
    text = text.replace("\\n", "")
    text = text.lower()
    #below is the csv where we have all the keywords, you can customize your own
    keyword_dict = pd.read_csv('./keywords.csv', encoding = "ISO-8859-1")
    stats_words = [nlp(text.lower().strip()) for text in keyword_dict['Statistics'].dropna(axis = 0)]
    NLP_words = [nlp(text.lower().strip()) for text in keyword_dict['NLP'].dropna(axis = 0)]
    ML_words = [nlp(text.lower().strip()) for text in keyword_dict['Data Science'].dropna(axis = 0)]
    DL_words = [nlp(text.lower().strip()) for text in keyword_dict['Deep Learning'].dropna(axis = 0)]
    Fin_words = [nlp(text.lower().strip()) for text in keyword_dict['Finance'].dropna(axis = 0)]
    python_words = [nlp(text.lower().strip()) for text in keyword_dict['Python'].dropna(axis = 0)]
    Data_Engineering_words = [nlp(text.lower().strip()) for text in keyword_dict['Data Engineering'].dropna(axis = 0)]

    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('Stats', None, *stats_words)
    matcher.add('NLP', None, *NLP_words)
    matcher.add('DS', None, *ML_words) #ML
    matcher.add('DL', None, *DL_words)
    matcher.add('Fin', None, *Fin_words)
    matcher.add('Python', None, *python_words)
    matcher.add('DE', None, *Data_Engineering_words)
    doc = nlp(text)
    
    d = []  
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start : end]  # get the matched slice of the doc
        d.append((rule_id, span.text))      
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())
    
    ## convertimg string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    
    #base = os.path.basename(file)
    #filename = os.path.splitext(base)[0]
       
    #name = filename.split('_')
    #name2 = name[0]
    name2 = name.lower()
    ## converting str to dataframe
    name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
    
    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)

    return dataf


# In[ ]:


def create_raw_profile_database(data):
    final_database=pd.DataFrame()
    names = list(data.keys())
    #i = 0 
    for i in tqdm(range(len(data)), total = len(data)):
        cur_data = data[names[i]]
        dat = create_profile(cur_data, names[i])
        final_database = final_database.append(dat)
    return final_database


# In[ ]:


def clean_raw_profile_database(data, final_database):
    final_database_1 = final_database.reset_index().dropna(axis = 0)
    final_database_1['Keyword'] = final_database_1['Keyword'].apply(lambda x: x.strip())
    final_database_1['Count'] = final_database_1['Count'].astype(int)
    df = final_database_1[final_database_1['Candidate Name'] == names[0].lower()]
    
    names = list(data.keys())
    droprow = []
    for name in names:
        df = final_database_1[final_database_1['Candidate Name'] == name.lower()]
        cur_drop = check_similar_word(df)
        droprow.extend(cur_drop)
        
    final_database_2 = final_database_1.drop(droprow, axis = 0)
    final_database_2.index = np.arange(len(final_database_2))
    
    #final_database_2.to_csv('raw_profile_database.csv')
    
    return final_database_2


# In[ ]:


def detect_general_word(data, final_database, thresh = 5):
    general_words = ['machine learning', 'deep learning', 'data science', 'python', 'data engineering', 'statistics', 'nlp']

    name_general_words = {}
    g_tracker = 0
    names = list(data.keys()
    for name in names: 
        name_general_words[name.lower()] = 0
        df = final_database[final_database['Candidate Name'] == name.lower()]
        for word in general_words:
            if word in df['Keyword'].values and df[df['Keyword']== word]['Count'].values[0] >= thresh:
                name_general_words[name.lower()] = 1
                g_tracker += 1
                break
    return name_general_word


# In[ ]:


def create_final_profile_database(final_database, name_general_words):
    final_database2 = final_database['Keyword'].groupby([final_database['Candidate Name'], final_database['Subject']]).count().unstack()
    final_database2.reset_index(inplace = True)
    final_database2.fillna(0,inplace=True)
    for i in range(len(final_database2)):
        name = final_database2.loc[i, 'Candidate Name']
        g_word = name_general_words[name]
        final_database2.loc[i, 'Total_Score'] = np.sum(final_database2.iloc[i, 1:8].values)
        final_database2.loc[i, 'General_Word'] = g_word
        
    return final_database2


# In[ ]:


def visualize(final_database, sample_size = None):
    new_data = final_database.iloc[:,1:-2]
    new_data.index = final_database['Candidate Name']
    
    if sample_size is not None:
        new_data = new_data[:sample_size]
        
    plt.rcParams.update({'font.size': 40})
    ax = new_data.plot.barh(title="Resume keywords by category", legend=False, figsize=(80,40), stacked=True)
    labels = []
    for j in new_data.columns:
        for i in new_data.index:
            label = str(j)+": " + str(new_data.loc[i][j])
            labels.append(label)
    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width/2., y + height/2., label, ha='center', va='center')
    plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


### test
                 
if __name__ == '__main__':
    with open('./final_record.pkl', 'rb') as f:
        data = pickle.load(f)
    # data[name]['X'] = resume's text, data[name]['X'] = 1/0 pass/not 

    final_database = create_raw_profile_database(data)
    final_database = clean_raw_profile_database(data, final_database)
    name_general_words = detect_general_word(data, final_database, thresh = 5)
    final_database = create_final_profile_database(final_database, name_general_words)
    final_database.to_csv('skillset_profile.csv', index = False)
    visualize(final_database, sample_size = 10)

