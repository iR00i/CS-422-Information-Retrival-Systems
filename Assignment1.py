import os
from xml.dom import minidom
import pandas as pd
from tqdm.notebook import tqdm

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import re
import operator
import json


def rmv_StopWords(text):
  stop_words = set(stopwords.words('english'))
  tokens = word_tokenize(text)
  new_text = [i for i in tokens if not i in stop_words]
  new_text = " ".join(new_text)
  return new_text

def rmv_Punctuations(text):
  tokenizer = nltk.RegexpTokenizer(r"\w+")
  new_text = tokenizer.tokenize(text)
  new_text = " ".join(new_text)
  new_text = new_text.rstrip("\n")
  return new_text

def rmv_Numbers(text):
  return ''.join([i for i in text if not i.isdigit()])

def Stemming(text):
  PS = PorterStemmer()
  tokens = word_tokenize(text)
  new_text = []
  for i in tokens:
    new_text.append(PS.stem(i))
  new_text = " ".join(new_text)
  return new_text

def rmv_ShortWords(text):
  tokens = word_tokenize(text)
  new_text = []
  for i in tokens:
    if len(i) > 2:
      new_text.append(i)
  new_text = " ".join(new_text)
  return new_text

check = input("Do you want to create a 'data.tsv' version ? (note there already exists one in the submission) \n(y/n): ")
if check == 'y':
  print("Reading Docs from cranfieldDocs and concatenating them into a pandas DataFrame...")
  path = 'cranfieldDocs'
  file_list = os.listdir(path)
  file_list.sort()
  data = []
  for i in tqdm(range(len(file_list))):
    doc = minidom.parse(path+"/"+file_list[i])
    title = doc.getElementsByTagName('TITLE')[0].firstChild.data
    text = doc.getElementsByTagName('TEXT')[0].firstChild.data
    temp = [text, title]
    data.append(temp)
  data = pd.DataFrame(data,columns=['Text','Title'])
  data.to_csv('data.tsv',sep='\t',index=False)

check = input("Do you want to create a 'Inverted_Index.json' version ? (note there already exists one in the submission) \n(y/n): ")
if check == 'y':
  Inverted_Index = {}
  for key, val in tqdm(token_dict.items()):
    Inverted_Index[key] = {}
    Inverted_Index[key]['df'] = 0
    Inverted_Index[key]['docs'] = []

    for idx, row in data.iterrows():
      tokens = word_tokenize(data['Text'][idx])
      if key in tokens:
        Inverted_Index[key]['df']+=1
        temp = {}
        temp['ID'] = idx + 1
        temp['TF'] = tokens.count(key)
        Inverted_Index[key]['docs'].append(temp)

  with open('Inverted_Index.json', 'w') as fp:
      json.dump(Inverted_Index, fp)

print("Preprocessing data......")
data = pd.read_csv('data.tsv',sep='\t')
data['Text'] = data['Text'].apply(lambda x: rmv_Punctuations(x))
data['Text'] = data['Text'].apply(lambda x: rmv_Numbers(x))
data['Text'] = data['Text'].apply(lambda x: rmv_StopWords(x))
data['Text'] = data['Text'].apply(lambda x: Stemming(x))
data['Text'] = data['Text'].apply(lambda x: rmv_ShortWords(x))

data['Title'] = data['Title'].apply(lambda x: rmv_Punctuations(x))
data['Title'] = data['Title'].apply(lambda x: rmv_Numbers(x))
data['Title'] = data['Title'].apply(lambda x: rmv_StopWords(x))
data['Title'] = data['Title'].apply(lambda x: Stemming(x))
data['Title'] = data['Title'].apply(lambda x: rmv_ShortWords(x))

num_of_tokens = 0
token_dict = {}
for idx, row in data.iterrows():
  tokens = word_tokenize(data['Text'][idx])
  num_of_tokens += len(tokens)
  for token in tokens:
    if token not in token_dict:
      token_dict[token] = 1
    else:
      token_dict[token] +=1

one_word = [i for i in token_dict if token_dict[i] == 1]
token_dict = dict( sorted(token_dict.items(), key=operator.itemgetter(1),reverse=True))
print(f"There are a total of {num_of_tokens} tokens in the dataset.\nThere are {len(token_dict)} unique tokens.\nThe number of tokens that appear once in the dataset is {len(one_word)}.\nThe average number of Tokens per doc is {num_of_tokens/1400}")
print("\nThe 30-top most frequent terms in the dataset:")
keys, values = list(token_dict.keys())[0:30], list(token_dict.values())[0:30]
for i in range(len(keys)):
  print(f"{i+1}) {keys[i]} ----> {values[i]}")