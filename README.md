![alt_text](Img/Headersentiment.png)

### **Twitter** 
Webapp developed with streamlit that allows to know the sentiment in the replies to banking tweets.

### **NLP with Huggingface**
The model used to analyze the comments of tweets has been bert-base-multilingual-uncased-sentiment that allows to have a classification of 1-5 stars
https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment

### **Streamlit Dataapp**
Thanks to streamlit, I was able to create an application that allows you to visualize the data in a very interactive way and with a very aesthetic look.
https://www.streamlit.io/gallery

### **Requirements**
pandas, numpy, streamlit, plotly, matplotlib, spacy, transformers, tweepy

### :file_folder: **Folder structure**
```
└── Webapp_streamlit_twtter_replies_sentiment
    ├── Data
    ├── Img
    ├── Notebooks
    |── Row_data
    |── Sentiment
    |   └── m_wrangling.py
    ├── Twitter_tweepy
    |   └── tweets_replies.py
    ├── .gitignore
    ├── webapp_classifier_sentiment.py
    ├── main.py
    ├── README.md
    └── requeriments.txt
```


