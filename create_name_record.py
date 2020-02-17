#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import os
import pickle
from tqdm import tqdm
from parsetext import *


# In[ ]:





# In[ ]:





# In[ ]:


def match_use_filename(names, file_dict):
    # 1st run, check filename
    file_tracker = []
    name_dict = {}

    for name in names:
        name_0 = name.replace('PhD', '').replace('PHD', '').replace('phd', '').replace(',', '').lower()
        name_0 = ' '.join([k.strip() for k in name_0.split()])
        name_1 = ' '.join(name_0.split()[::-1])
        name_2 = name.replace('-', ' ').replace('(', ' ').replace(')', ' ').lower()
        name_2 = ' '.join([k.strip() for k in name_2.split()])
        name_3 = ' '.join(name_2.split()[::-1])

        name_s = ''.join(name.split())
        name_0_s = ''.join(name_0.split())
        name_1_s = ''.join(name_1.split())
        name_2_s = ''.join(name_2.split())
        name_3_s = ''.join(name_3.split())

        for file in file_dict:
            file_text = file.replace('_', ' ').replace('-', ' ').replace('+', ' ').lower()
            file_text = ' '.join([k.strip() for k in file_text.split()])
            text_s = ''.join(file_text.split())
            if name.lower() in file_text or name_0 in file_text or name_1 in file_text or name_2 in file_text or name_3 in file_text or                name_s.lower() in text_s or name_0_s in text_s or name_1_s in text_s or name_2_s in text_s or name_3_s in text_s:
                name_dict[name] = file
                file_tracker.append(file)
                break
    
    miss_names = []
    for name in names:
        if name not in name_dict:
            miss_names.append(name)
    return name_dict, file_tracker, miss_names


# In[ ]:


def match_use_text():
    # 2nd run, read text and search
    for name in miss_names:
        name_0 = name.replace('PhD', '').replace('PHD', '').replace('phd', '').replace(',', '').lower()
        name_0 = ' '.join([k.strip() for k in name_0.split()])
        name_1 = ' '.join(name_0.split()[::-1])
        name_2 = name.replace('-', ' ').replace('(', ' ').replace(')', ' ').lower()
        name_2 = ' '.join([k.strip() for k in name_2.split()])
        name_3 = ' '.join(name_2.split()[::-1])

        name_s = ''.join(name.split())
        name_0_s = ''.join(name_0.split())
        name_1_s = ''.join(name_1.split())
        name_2_s = ''.join(name_2.split())
        name_3_s = ''.join(name_3.split())

        for file in file_dict:
            if file not in file_tracker:
                text = file_dict[file]
                text = text.replace('\n', '').replace('\t', '').replace('·', '').lower()
                text = ' '.join([k.strip() for k in text.split()])
                text_s = ''.join(text.split())
                if name.lower() in text or name_0 in text or name_1 in text or name_2 in text or name_3 in text or                    name_s.lower() in text_s or name_0_s in text_s or name_1_s in text_s or name_2_s in text_s or name_3_s in text_s:
                    name_dict[name] = file
                    file_tracker.append(file)
                    break

    miss_names_1 = []                
    for name in names:
        if name not in name_dict:
            miss_names_1.append(name)
    return name_dict, file_tracker, miss_names_1


# In[ ]:


def get_interview_result(data, name_dict):
    target = {}
    for name in name_dict:
        if name in data['name'].values:
            y = data[data['name'] == name]['interview_result'].values[0] 
            if y == 'Y':
                target[name] = 1
            else:
                target[name] = 0
    return target


# In[ ]:


def generate_final_record(target, name_dict):
    record = {}
    for name in target:
        name_1 = name.replace(', ', ' ')
        record[name_1] = {}
        file = name_dict[name]
        record[name_1]['X'] = file_dict[file] # resume text
        record[name_1]['y'] = target[name] # pass or not
    return record


# In[ ]:





# In[ ]:





# In[ ]:


## test
if __name__ == '__main__':
    data = pd.read_excel('hiring.xlsx')
    # data's format = [name, round1_interview_pass(Y/N), round2_interview_pass(Y/N), ...]
    names = data['name']

    file_dict = file_to_text('./resumebooks/')
    name_dict, file_tracker, miss_names = match_use_filename(names, file_dict)
    name_dict, file_tracker, miss_names = match_use_text()
    target = get_interview_result(data, name_dict)
    final_record = generate_final_record(target, name_dict)

    with open('./name_map.pkl', 'wb') as f:
        pickle.dump(name_dict, f)
    with open('./no_resume.pkl', 'wb') as f:
        pickle.dump(miss_names, f)
    with open('./final_record.pkl', 'wb') as f:
        pickle.dump(final_record, f)



