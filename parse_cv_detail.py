#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from similar_word import get_similarity
import os
from parsetext import *


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


def load_all_data():

    location = pd.read_csv('./data/city_list.csv', encoding = 'ISO-8859-1') 
    #city and state
    sections = pd.read_csv('./data/sectionwords.csv', encoding = 'ISO-8859-1') 
    #sections: [Experience, Education, Project, Publication, Skill, Degree]
    ### experience: Professional Experience, EXPERIENCES, WORK EXPERIENCE, ...
    ### degree: BS, B.S, BE, B.E, ....
    ### project: ACADEMIC PROJECTS, INDUSTRIAL PROJECTS.....
    positions = pd.read_csv('./data/positionwords.csv', header = None, encoding = 'ISO-8859-1')
    # scientist, engineer, ...
    us_company = pd.read_excel('./data/us_company.xlsx', sheet_name = 'top')
    # company names
    school = pd.read_excel('./data/List of US Universities_D.xlsx')
    # school names


    return location, sections, positions, us_company, school


# In[ ]:


def detect_digit(ele):
    return np.sum([k.isdigit() for k in ele])


# In[ ]:


def detect_loc(ele, location):
    city = location.City.dropna().values
    state = location.State.dropna().values
    locs = np.append(city, state)
    if np.any([k.lower() == ele.lower() for k in locs]):
        return 1
    
    if ',' in ele and np.any([k.lower() in ele.lower() for k in locs]):
        return 1
 
    return 0


# In[ ]:


def find_loc(ele, location):
    city = location.City.dropna().values
    state = location.State.dropna().values
    locs = np.append(city, state)
    
    for k in locs:
        if k.lower() == ele.lower():
            return k
    
    if ',' in ele:
        for k in locs:
            if k.lower() in ele.lower():
                return k
 
    return 0


# In[ ]:


#from fuzzywuzzy import fuzz

def detect_company(ele, company):
    com_names = company.company.dropna().values
    
    if np.any([k.lower() == ele.lower().strip().strip(',') for k in com_names]):
        return 1
    
    if np.any([k.lower() in [m.strip().strip(',') for m in ele.lower().split()] for k in com_names]): # or  np.any([ele.lower() in k.lower() for k in com_names]):
        if len(ele.lower()) > 2: 
            return 1
    
    for k in com_names:
        for m in ele.lower().split(','):
            if k.lower() == m.strip():
                return 1
            
    for k in com_names:
        if len(k.split()) > 1:
            if np.any([k.lower() in n for n in [m.strip() for m in ele.lower().split(',')]]):
                if len(ele.lower()) > 2:
                    return 1
            
    if np.any([get_similarity(ele.lower().strip().strip(','), k.lower()) >= 0.7 for k in com_names]): 
        if len(ele.lower()) > 2: 
            return 1
        
    if 'inc.' in ele.lower() or 'co.' in ele.lower() or 'LLC' in ele.split() or 'LLP' in ele.split() or 'Ltd' in ele.split():
        return 1
    
    return 0


# In[ ]:


def find_company(ele, company):
    com_names = company.company.dropna().values
    
    for k in com_names:
        if k.lower() == ele.lower().strip().strip(','):
            return k
    
    for k in com_names:
        k = k.strip()
        if k.lower() in [m.strip() for m in ele.strip('|').lower().split(',')] or            k.lower() in [m.strip() for m in ele.strip('|').lower().split('–')] or            k.lower() in [m.strip() for m in ele.strip('|').lower().split('-')] or            k.lower() in [m.strip() for m in ele.strip('|').lower().split('|')] or            k.lower() in [m.strip() for m in ele.strip('|').lower().split('@')]:
            if len(ele.lower()) > 2:
                return k
            
    for k in com_names:
        k = k.strip()
        if len(k.split()) > 1:
            if np.any([k.lower() in n for n in [m.strip() for m in ele.lower().split(',')]]):
                if len(ele.lower()) > 2:
                    return k
    
    for k in com_names:
        k = k.strip()
        for m in ele.lower().split(','):
            if k.lower() == m.strip():
                return k
            
    for k in com_names:
        k = k.strip()
        if get_similarity(ele.lower().strip().strip(','), k.lower()) >= 0.7:
            return k
        
    if 'inc.' in ele.lower() or 'co.' in ele.lower() or 'llc' in ele.lower().split() or        'llp' in ele.lower().split() or 'ltd' in ele.lower().split() or 'ltd.' in ele.lower().split() or        'inc' in ele.lower().split():
        coms = ele.lower().split(',')
        for i in range(len(coms)):
            com = coms[i]
            if 'inc.' in com or 'co.' in com or 'llc' in com or 'llp' in com or 'ltd' in com or 'inc' in com:
                if 'inc.' == com.strip() or 'co.' == com.strip() or 'llc' == com.strip() or                    'llp' == com.strip() or 'ltd' == com.strip() or 'ltd.' == com.strip() or                    'inc' == com.strip():
                    return (coms[i-1].strip() + ' ' + com.strip())
                else:
                    return com.strip()
        
    
    return 0
    


# In[ ]:


def detect_school(ele, school):
    schools = school.University.dropna().values
    
    if np.any([k.lower() == ele.lower() for k in schools]):
        return 1
    
    if np.any([k in ele for k in schools]):
        return 1
    
    if 'university' in ele.lower() or 'school' in ele.lower() or 'institute' in ele.lower() or 'college' in ele.lower():
        return 1
 
    return 0


# In[ ]:


def find_school(ele, school):
    schools = school.University.dropna().values
    
    for k in schools:
        if k.lower() == ele.lower():
            return k
    
    for k in schools:
        if k in ele:
            return k
    
    if 'university' in ele.lower() or 'school' in ele.lower() or 'institute' in ele.lower() or 'college' in ele.lower():
        for uni in ele.lower().split(','):
            if 'university' in uni or 'school' in uni or 'institute' in uni or 'college' in uni:
                return uni.strip()
 
    return 0


# In[ ]:


def detect_degree(ele, sections):
    if np.any([k == ele for k in sections['Degree'].dropna().values]) or     np.any([k in [m.strip().strip(',') for m in ele.split()] for k in sections['Degree'].dropna().values]):
        return 1
    
    return 0


# In[ ]:


def find_degree(ele, sections):
    
    for k in sections['Degree'].dropna().values:
        if k == ele or (k in [m.strip().strip(',') for m in ele.split()]) or            np.any([k == n for n in [m.strip() for m in ele.split(',')]]):
            return k
    
    return 0


# In[ ]:


def detect_position(ele, positions):
    if np.any([k.lower() in [m.strip().strip(',') for m in ele.lower().split()] for k in positions[0].dropna().values]):
        return 1
    return 0


# In[ ]:


def find_position(ele, positions):
    
    for k in positions[0].dropna().values:
        if k.lower() in [m.strip().strip(',') for m in ele.lower().split()]:
            for m in ele.lower().split(','):
                if k.lower() in m:
                    return m.strip()

    return 0


# In[ ]:


def get_entity(sub_header_tracker, school, sections, positions, us_company):
    
    entity = {}
    entity['school'] = {'contents': [], 'cor': []}
    entity['degree'] = {'contents': [], 'cor': []}
    entity['company'] = {'contents': [], 'cor': []}
    entity['position'] = {'contents': [], 'cor': []}
    entity['location'] = {'contents': [], 'cor': []}
    entity['header'] = {'contents': [], 'cor': []}
    entity['others'] = {'contents': [], 'cor': []}
    
    for page in sub_header_tracker:
        for headers in sub_header_tracker[page]:
            row = headers[0]
            eles = headers[1]

            for ele in eles:
                flags = 0

                if find_school(ele, school):
                    entity['school']['contents'].append(ele)
                    entity['school']['cor'].append([page, row])
                    #print(page, row, '\t', 'School', '\t', ele)
                    #flags = 1
                    #continue

                if find_degree(ele, sections):
                    entity['degree']['contents'].append(ele)
                    entity['degree']['cor'].append([page, row])
                    #print(page, row, '\t', 'Degree', '\t', ele)
                    #flags = 1
                    #continue

                if find_position(ele, positions):
                    entity['position']['contents'].append(ele)
                    entity['position']['cor'].append([page, row])
                    #print(page, row, '\t', 'position', '\t', ele)
                    #flags = 1
                    #continue

                for col in sections.columns[:-1]:
                    
                    # section words
                    if np.any([k.lower() in ele.lower() for k in sections[col].dropna().values]) and                        len(ele.split()) <=10:
                        entity['header']['contents'].append(ele)
                        entity['header']['cor'].append([page, row])
                        #print(page, row, '\t', col, '\t', ele)
                        flags = 1
                        break

                    if find_company(ele, us_company):
                        entity['company']['contents'].append(ele)
                        entity['company']['cor'].append([page, row])
                        #print(page, row, '\t', 'company', '\t', ele)
                        flags = 1
                        break
                        
                    # location word
                    if find_loc(ele, location):
                        #print(page, row, '\t', 'location', '\t', ele)
                        entity['location']['contents'].append(ele)
                        entity['location']['cor'].append([page, row])
                        flags = 1
                        break
                    
                    # time words
                    if detect_digit(ele) >= 2:
                        #print(page, row, '\t', 'time', '\t\t', ele)
                        flags = 1
                        break

                if flags == 0:
                    if ele not in entity['school']['contents'] and                        ele not in entity['degree']['contents'] and                        ele not in entity['position']['contents'] and                        ele not in entity['company']['contents']:
                        entity['others']['contents'].append(ele)
                        entity['others']['cor'].append([page, row])
                    #print(page, row, '\t', 'others', '\t', ele)
    return entity


# In[ ]:


def refine_entity(entity, school, sections, positions, us_company):

    non_com_list = ['systems', 'system', 'technology', 'technologies', 'research', 'data']
    results = {}

    results['name'] = []
    others = entity['others']['contents']
    for i in range(len(others)):
        ele = others[i]
        if len(ele.split())<=4 and ele not in entity['header']['contents'] and '|' not in ele:
            if len(ele.split()) == 1 and len(others[i+1].split()) == 1:
                results['name'] = ele + ' ' + others[i+1]
            else:
                results['name'] = ele
            break

    results['school'] = []
    for ele in entity['school']['contents']:
        sch = find_school(ele, school)
        if sch not in results['school']:
            results['school'].append(sch)
    
    results['degree'] = []
    for ele in entity['degree']['contents']:
        degree = find_degree(ele, sections)
        if degree not in results['degree'] and ele not in entity['header']['contents']:
            results['degree'].append(degree)
    
    results['company'] = []
    for ele in entity['company']['contents']:
        com = find_company(ele, us_company)
        if ele.lower().strip() != 'microsoft office' and ele.lower().strip() not in non_com_list and            'skill' not in ele.lower().strip() and 'skills' not in ele.lower().strip():
            if com not in results['company'] and len(ele) >2:
                results['company'].append(com)
            
    results['position'] = []
    for ele in entity['position']['contents']:
        posi = find_position(ele, positions)
        if posi not in results['position'] and ele not in entity['location']['contents']:
            results['position'].append(posi)
        
    return results


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


## test

if __name__ == '__main__':
    location, sections, positions, us_company, school = load_all_data()

    alltext, allwords = getpdf_raw(file)
    allwords = groupwords(allwords)
    header_tracker = get_headers(allwords, tol = 6)
    sub_header_tracker = get_sub_headers(allwords, tol = 13)
    sub_header_tracker = add_sub_headers(allwords, sub_header_tracker, tol = 80)

    entity = get_entity(sub_header_tracker, school, sections, positions, us_company)
    results = refine_entity(entity, school, sections, positions, us_company)

    with open('./parsed_data/record.pkl', 'wb') as f:
        pickle.dump(results, f)


# In[ ]:
