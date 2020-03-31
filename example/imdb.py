import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import urllib.request 
import os
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

def loading_dataset(path,seed=123):
    
    imdb_data_path = os.path.join(path,'imdb')
    
    train_text = []
    train_label = []
    
    for category in ['pos','neg']: #category=pos
        #print(category)
        train_path = os.path.join(imdb_data_path,'train',category) #train_path=/Users/archana/learn-code/git-what/example/imdb/train/pos
        #print(train_path)
        for fname in sorted(os.listdir(train_path)): #fname=0_9.txt
            if fname.endswith('.txt'): #true
                with open(os.path.join(train_path, fname)) as f: #f=train_path=/Users/archana/learn-code/git-what/example/imdb/train/pos/0_9.txt
                    train_text.append(f.read()) #train_text = [positive text]
                if category == 'neg': #false
                    train_label.append(0)
                else:    #true 
                    train_label.append(1) #tain_label = [1]

    test_text = []
    test_label = []

    for category in ['pos','neg']:
        test_path = os.path.join(imdb_data_path,'test',category)
        for fname in sorted(os.listdir(test_path)):
            if fname.endswith('.txt'):
                with open(os.path.join(test_path, fname)) as f:
                    test_text.append(f.read())
                if category == 'neg': #false
                    test_label.append(0)
                else:    #true 
                    test_label.append(1) #tain_label = [1]

    random.seed(100)
    random.shuffle(test_text) #to ensure model is not affected by data order
    random.seed(100)
    random.shuffle(test_label)

    return ((train_text, np.array(train_label)),
            (test_text, np.array(test_label)))


def get_num_words_per_sample(sample_texts):
    for s in sample_texts:
        num_words = [len(s.split())]
    return np.median(num_words)

def plot_sample_length_distribution(sample_texts):
    plt.hist([len(s) for s in sample_texts], 50)
    plt.xlabel('Length of a sample')
    plt.ylabel('Number of samples')
    plt.title('Sample length distribution')
    plt.show()

# def plot_frequency_words(text):
#     dictionary={}
#     for s in text: 
#         words=s.split()
#         for w in words: 
#             if w in dictionary.keys(): 
#                 dictionary[w]=dictionary[w]+1 
#             else: 
#                 dictionary[w] = 1

#     x , y = zip(*sorted(dictionary.items()))
#     plt.plot(x,y)
#     plt.show()


((trainD,trainL1),(testD, testL)) =loading_dataset("/Users/archana/learn-code/git-what/example") 
#data=(([train],[labels]),([test],[labels]))

NGRAM_RANGE = (1,2) #n-gram sizes for tokenising text 
TOP_K = 20000 #no of features/words 
TOKEN_MODE = 'word' #text will be split into words
MIN_DOCUMENT_FREQUENCY = 2 #if a word is appearing in less than documents, it will be discarded 

def ngram_vectorise(train_texts, train_labels, val_texts): #train_text,train_label,test_text
    kwargs = {
            'ngram_range': NGRAM_RANGE,  #uni-gram + bi-gram (1,2)
            'dtype': 'int32', #from -2,147,483,648 to +2,147,483,648
            'strip_accents': 'unicode', #strips accent ‘unicode’: slower method, works on any characters.
            'decode_error': 'replace', # if the sequence contains characters not of the given encoding
            'analyzer': TOKEN_MODE, #'words' Whether the feature should be made of word or character n-grams
            'min_df': MIN_DOCUMENT_FREQUENCY, #cut=off
    }
    vectorizer = TfidfVectorizer(**kwargs) # many arguments can be passed in list or dict
    x_train = vectorizer.fit_transform(train_texts) #transforms the train_text (in the form mentioned in vectorizer) into numbers
    x_val = vectorizer.transform(val_texts) #transforms test_text into numbers[diff bet .fit_transform, .tranform]
    selector = SelectKBest(f_classif, k=min(TOP_K, x_train.shape[1])) #selects k best feature,removes all but the k highest scoring features
    selector.fit(x_train, train_labels) #???
    x_train = selector.transform(x_train).astype('float32') #converts the array into float values 
    x_val = selector.transform(x_val).astype('float32')
    return x_train, x_val

y,x=ngram_vectorise(trainD, trainL1,testD)
#get_num_words_per_sample(trainD)

#plot_sample_length_distribution(trainD)
#plot_frequency_words(td1)

