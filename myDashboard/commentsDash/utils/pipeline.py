import pandas as pd
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from langdetect import detect
import re
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import emoji
from sklearn.model_selection import train_test_split
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import pipeline
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore")


class SentimentTopicModel:
    def __init__(self, data, sentiment_model_path, topic_model_path, num_labels, id_col_name='Video ID', 
                 comment_col_name='comment'):
        self.data = data
        self.video_id_col_name = id_col_name
        self.comment_col_name = comment_col_name
        
        self.label_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
        
        self.topic_model = pipeline("text-classification", model=topic_model_path, return_all_scores=True)
        
        self.sentiment_model = TFBertForSequenceClassification.from_pretrained(sentiment_model_path, num_labels=num_labels)
        self.sentiment_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        
    def remove_emoji(self, text):
        return emoji.demojize(text, delimiters=("", ""))

    def preprocess_text(self, text):
        text = self.remove_emoji(text)
        text = re.sub(r'http\S+|www.\S+', '', text)
        text = re.sub(r'<.*?>', '', text)
        text = word_tokenize(text.lower())
        lemmatizer = WordNetLemmatizer()
        text = [lemmatizer.lemmatize(token) for token in text]
        text = [token for token in text if token.isalnum()]
        return ' '.join(text)
    
    def predict_sentiment(self, video_id):
        df_test = self.data[self.data[self.video_id_col_name]==video_id]
        results = []
        for text in df_test[self.comment_col_name].tolist():
            result = {
                'comment': text,
                'prediction': {}
            }
            processed_text = self.preprocess_text([text])
            input_ids = self.sentiment_tokenizer([processed_text], padding=True, truncation=True, max_length=128)

            logits = self.sentiment_model(input_ids)['logits']
            pred_prob = tf.nn.softmax(logits).numpy()[0]
            for i, pred in enumerate(pred_prob):
                result['prediction'][self.label_map[i]]=pred
            results.append(result)
        return results
    
    def predict_sentiments(self, data):
        comments_sentiment_resul_percentage = {
            'comment': data[self.comment_col_name],
            'negative': [],
            'neutral': [],
            'positive':[]
        }
        comments_sentiment_result = {
            'negative': 0,
            'neutral': 0,
            'positive':0
        }
        data[self.comment_col_name] = data[self.comment_col_name].apply(self.preprocess_text)
        batch_size = 100
        for i in range(0, len(data[self.comment_col_name]), batch_size):
            # Tokenize the current batch of comments
            input_ids = self.sentiment_tokenizer(data[self.comment_col_name].iloc[i:i+batch_size].tolist(), padding=True, truncation=True, max_length=256, return_tensors='tf')

            # Make sentiment predictions for the current batch
            logits = self.sentiment_model(input_ids)['logits']
            pred_prob = tf.nn.softmax(logits)
            for prob in pred_prob:
                comments_sentiment_resul_percentage['negative'].append(prob[0].numpy())
                comments_sentiment_resul_percentage['neutral'].append(prob[1].numpy())
                comments_sentiment_resul_percentage['positive'].append(prob[2].numpy())
            
            preds = tf.argmax(logits, axis=-1).numpy()
            for pred in preds:
                pred_class = list(self.label_map.values())[pred]
                comments_sentiment_result[pred_class]+=1
        return comments_sentiment_result, comments_sentiment_resul_percentage
    
    def predict_topic(self, video_id):
        df_test = self.data[self.data[self.video_id_col_name]==video_id]
        results = []
        for text in df_test[self.comment_col_name].tolist():
            result = {
                'comment': text,
                'prediction': {}
            }
            
            processed_text = self.preprocess_text([text])
            
            label = self.topic_model(processed_text)
            for v in label:
                result['prediction'][v['label']]=v['score']
            results.append(result)
        return results
    
    def predict_topics(self, data):
        comments_topic_result_percentage = {
            'comment': data[self.comment_col_name],
            'anger': [],
            'disgust': [],
            'fear': [],
            'joy':[],
            'neutral': [],
            'sadness': [],
            'surprise': []
        }
        
        comments_topic_result = {
            'anger': 0,
            'disgust': 0,
            'fear':0,
            'joy': 0,
            'neutral': 0,
            'sadness':0,
            'surprise': 0
        }
        
        data[self.comment_col_name] = data[self.comment_col_name].apply(self.preprocess_text)
        for text in data[self.comment_col_name]:
            try:
                preds = self.topic_model(text)
                score = []
                for v in preds:
                    score.append(v['score'])
                    comments_topic_result_percentage[v['label']].append(v['score'])
                comments_topic_result[list(comments_topic_result)[np.argmax(score)]] +=1
            except:
                for key in comments_topic_result_percentage.keys():
                    if key=='comment':
                        continue
                    comments_topic_result_percentage[key].append(0)
                pass
        return comments_topic_result, comments_topic_result_percentage
    

