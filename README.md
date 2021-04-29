# CS-422-Informoation-Retrival-Systems
This repo is for the Information retrieval Systems Course CS422 Second Semester of 2020/2021.

Assignment #1 consisted of reading the "**Cranfield Docs**" and applying pre-processing on them. And then Construct an Inverted Index model of the terms in the Dataset.

"**data.tsv**__" is the documents dataset with only the Text and the Title. it was created with pandas and saved as a tab separated file for efficiency and speed.
"**Inverted_Index.json**__" is the postings-list of the terms in the dataset. it is a json file with **4334** terms. each term has the following format:
```json
"outweight": {
    "df": 1,
    "docs": [
      {
        "ID": 1380,
        "TF": 1
      }
    ]
  },
```
"**_df_**" is the "_**document frequency**_" for the term. "**_docs_**" is a list of the documents that contain the term. "**_ID_**" is the id of the document. "**_TF_**" is the "**_term frequency_**" of the term in the document. 

"**_Assignment1.py_**" is the code used to create "**data.tsv**__" and "**Inverted_Index.json**__"
There is a [colab notebook](https://colab.research.google.com/drive/1LgDM_C5xpNiZHO-J9WIOpoD9l4kHWGrM?usp=sharing) associated with this repo for the first Assignment.
