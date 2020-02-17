#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pickle
from tqdm import tqdm
import matplotlib.pyplot as plt


# In[ ]:


def find_ngrams(input_list, n):
    n_gram = zip(*[input_list[i:] for i in range(n)])
    n_list = []
    for ele in n_gram:
        new_ele = ' '.join([k.strip() for k in ele])
        n_list.append(new_ele)
    return n_list


# In[ ]:


def generate_words(data, n = 2):
    s1 = []
    s2 = []

    for name in tqdm(data, total = len(data)):
        y = data[name]['y']
        text = data[name]['X']
        text = text.replace('\t', ' ').replace('\n', ' ').replace('-', ' ').lower()
        word = find_ngrams(text.split(), n)

        if y == 1:
            s1.extend(word)
        else:
            s2.extend(word)
    return s1, s2


# In[ ]:


def generate_words_v2(raw_sample):
    s1 = []
    s2 = []

    for i in range(len(raw_sample)):
        name = raw_sample.loc[i, 'Candidate Name']
        keyword = raw_sample.loc[i, 'Keyword']
        num = raw_sample.loc[i, 'Count']
        if sample[sample['Candidate Name'] == name]['target'].values[0] == 1:
            s1.extend([keyword]*num)
        else:
            s2.extend([keyword]*num)
    return s1, s2


# In[ ]:





# In[ ]:


def plot_wordclound(words):
    
    text = ['_'.join([k for k in m.split()]) for m in words]
    text = ' '.join([k for k in text])
    text = text.replace('_&_', '_').replace('._', '_').replace('-', '_')
    stopwords = set(STOPWORDS)
    #stopwords.update({'machine_learning',  'data_science', 'python', 'data_engineering', 'statistics'})
    #wordcloud = WordCloud().generate(text)
   
    # Display the generated image:
    wordcloud = WordCloud(stopwords=stopwords, collocations = False, max_font_size=50, max_words=100, background_color="white").generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


# In[ ]:





# In[ ]:





# In[ ]:


## test
if __name__ == '__main__':
    with open('final_record.pkl', 'rb') as f:
        data = pickle.load(f)
    # data[name]['X'] = resume's text, data[name]['y'] = 1/0 pass/not

    s1, s2 = generate_words(data)
    plot_wordclound(s1)
    plot_wordclound(s2)


# In[ ]:




