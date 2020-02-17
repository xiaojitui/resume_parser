
def check_similar_word(df):
    
    droprow = []
    
    if 'time-series' in df['Keyword'].values and 'time series' in df['Keyword'].values:
        df[df['Keyword'] == 'time-series']['Count'] = max(df[df['Keyword'] == 'time-series']['Count'].values, df[df['Keyword'] == 'time series']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'time series'].index.values[0])
    if 'pca' in df['Keyword'].values and 'principal component analysis' in df['Keyword'].values:
        df[df['Keyword'] == 'pca']['Count'] = max(df[df['Keyword'] == 'pca']['Count'].values, df[df['Keyword'] == 'principal component analysis']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'principal component analysis'].index.values[0])
    if 'svm' in df['Keyword'].values and 'support vector machine' in df['Keyword'].values:
        df[df['Keyword'] == 'svm']['Count'] = max(df[df['Keyword'] == 'svm']['Count'].values, df[df['Keyword'] == 'support vector machine']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'support vector machine'].index.values[0])
    if 'k means' in df['Keyword'].values and 'k-means' in df['Keyword'].values:
        df[df['Keyword'] == 'k means']['Count'] = max(df[df['Keyword'] == 'k means']['Count'].values, df[df['Keyword'] == 'k-means']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'k-means'].index.values[0])
    if 'k means' in df['Keyword'].values and 'k-means clustering' in df['Keyword'].values:
        df[df['Keyword'] == 'k means']['Count'] = max(df[df['Keyword'] == 'k means']['Count'].values, df[df['Keyword'] == 'k-means clustering']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'k-means clustering'].index.values[0])
    if 'neural network' in df['Keyword'].values and 'neural networks' in df['Keyword'].values:
        df[df['Keyword'] == 'neural network']['Count'] = max(df[df['Keyword'] == 'neural network']['Count'].values, df[df['Keyword'] == 'neural networks']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'neural networks'].index.values[0])
    if 'cnn' in df['Keyword'].values and 'convolutional neural' in df['Keyword'].values:
        df[df['Keyword'] == 'cnn']['Count'] = max(df[df['Keyword'] == 'cnn']['Count'].values, df[df['Keyword'] == 'convolutional neural']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'convolutional neural'].index.values[0])
    if 'rnn' in df['Keyword'].values and 'recurrent neural' in df['Keyword'].values:
        df[df['Keyword'] == 'rnn']['Count'] = max(df[df['Keyword'] == 'rnn']['Count'].values, df[df['Keyword'] == 'recurrent neural']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'recurrent neural'].index.values[0])
    if 'handwritten recognition' in df['Keyword'].values and 'handwriting recognition' in df['Keyword'].values:
        df[df['Keyword'] == 'handwritten recognition']['Count'] = max(df[df['Keyword'] == 'handwritten recognition']['Count'].values, df[df['Keyword'] == 'handwriting recognition']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'handwriting recognition'].index.values[0])
    if 'nlp' in df['Keyword'].values and 'natural language processing' in df['Keyword'].values:
        df[df['Keyword'] == 'nlp']['Count'] = max(df[df['Keyword'] == 'nlp']['Count'].values, df[df['Keyword'] == 'natural language processing']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'natural language processing'].index.values[0])
    if 'ner' in df['Keyword'].values and 'named entity recoginition' in df['Keyword'].values:
        df[df['Keyword'] == 'ner']['Count'] = max(df[df['Keyword'] == 'ner']['Count'].values, df[df['Keyword'] == 'named entity recoginition']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'named entity recoginition'].index.values[0])
    if 'pos' in df['Keyword'].values and 'pos tagging' in df['Keyword'].values:
        df[df['Keyword'] == 'pos']['Count'] = max(df[df['Keyword'] == 'pos']['Count'].values, df[df['Keyword'] == 'pos tagging']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'pos tagging'].index.values[0])
    if 'statistical models' in df['Keyword'].values and 'statistical modeling' in df['Keyword'].values:
        df[df['Keyword'] == 'statistical models']['Count'] = max(df[df['Keyword'] == 'statistical models']['Count'].values, df[df['Keyword'] == 'statistical modeling']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'statistical modeling'].index.values[0])
    if 'r' in df['Keyword'].values and 'r programming' in df['Keyword'].values:
        df[df['Keyword'] == 'r']['Count'] = max(df[df['Keyword'] == 'r']['Count'].values, df[df['Keyword'] == 'r programming']['Count'].values)[0]
        droprow.append(df[df['Keyword'] == 'r programming'].index.values[0])
        
    return droprow







import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

#text1 = 'IBM Watson'#'This is a foo bar sentence .'
#text2 = 'IBM' #'This sentence is similar to a foo bar sentence .'



#print('Cosine:', cosine)

def get_similarity(text1, text2):
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine = get_cosine(vector1, vector2)
    
    return cosine


