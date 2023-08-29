from __future__ import annotations

import re

import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm.auto import tqdm
from unidecode import unidecode
nltk.download('sentiwordnet')

# Model used
"""
en-core-web-sm @
https://github.com/explosion/spacy-models/releases/download/
en_core_web_sm-3.0.0/en_core_web_sm-3.0.0-py3-none-any.wh
"""

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def sentiwordnet(text):
    tokens = nltk.word_tokenize(text)

    pos_score = 0
    neg_score = 0

    for token in tokens:
        synsets = list(swn.senti_synsets(token))
        if len(synsets) > 0:
            pos_score += synsets[0].pos_score()
            neg_score += synsets[0].neg_score()

    if pos_score > neg_score:
        return 'positive'
    elif pos_score < neg_score:
        return 'negative'
    else:
        return 'neutral'


def comment_analysis(data):
    tqdm.pandas(desc='Sentiment-Analysis')
    data['sentiment'] = data['comment'].progress_apply(sentiwordnet)
    return data


def replace_stylish_words(text):
    # Convert Unicode text to ASCII
    normalized_text = unidecode(text)

    return normalized_text


def preprocess_text(text):
    # remove links
    text = re.sub(r'http\S+', '', str(text))
    # Lowercase
    text = text.lower()
    # special characters
    text = re.sub(r'\W', ' ', text)
    # Remove stylish character
    text = replace_stylish_words(text)
    # single characters
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    # only single space
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    # remove special chars and numbers
    text = re.sub('[^A-Za-z]+', ' ', str(text))
    # tokenization
    tokens = nltk.word_tokenize(text)
    # stopwords and lemmatization
    tokens = [
        lemmatizer.lemmatize(
            word,
        ) for word in tokens if word not in stop_words if len(word) > 2
    ]
    return ' '.join(tokens)


def get_clean_data(data):
    clean_comment = [
        preprocess_text(resume)
        for resume in tqdm(data['comment'])
    ]
    data['clean_comment'] = clean_comment
    return data
