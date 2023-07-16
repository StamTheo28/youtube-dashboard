# ADD TO ENVIROMENT VARIABLES
API_KEY = "AIzaSyCj_o0-0ej8EOa6tPYPKfhJyI3c-zPJ9Yc"

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
from .pipeline import SentimentTopicModel
from .utils import clean_date
import pandas as pd
import numpy as np
import re
import time

# Remove tags and hashhtags from comments
def clean(text):
    # Remove <a> HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all('a'):
        tag.unwrap()
    text = str(soup)
    
    # Remove hashtags
    text = re.sub(r'#\w+', '', text)

    return text

# Retrieves the top k most famous comments of a youtube video
def get_most_famous_comments( video_id, max_comments=20):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Retrieve the comment threads for the video
    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        order="relevance",
        maxResults=max_comments
    ).execute()

    comments = []
    for item in response['items']:
        comment_data = {}
        comment_data['comment_id'] = item['id']
        comment_data['comment'] = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comment_data["like_count"] = item['snippet']['topLevelComment']['snippet']['likeCount']
        comment_data["reply_count"] = item['snippet']['totalReplyCount']
        if 'like_count' not in comment_data.keys():
            comment_data["like_count"] = 0
        if 'reply_count' not in comment_data.keys():
            comment_data["reply_count"] = 0
        comments.append(comment_data)
    comments_list = []

    # Retrieve video statistics
    video = youtube.videos().list(
    part='snippet,statistics',
    id=video_id
    ).execute()

    # Extract the video metadata
    meta = {}
    meta['video_id'] = video_id
    meta['title'] = video['items'][0]['snippet']['title']
    meta['description'] = video['items'][0]['snippet']['description']
    meta['publishedAt'] = clean_date(video['items'][0]['snippet']['publishedAt'])
    meta['thumbnail'] = video['items'][0]['snippet']['thumbnails']['medium']['url']
    meta['channelTitle'] = video['items'][0]['snippet']['channelTitle']
    meta['viewCount'] = video['items'][0]['statistics']['viewCount']
    meta['commentCount'] = video['items'][0]['statistics']['commentCount']
    meta['likeCount'] = video['items'][0]['statistics']['likeCount']
    meta['favoriteCount'] = video['items'][0]['statistics']['favoriteCount']

	# Retrieve the full comments using the comment IDs
    for comment in comments:
        try:
            comment_id = comment['comment_id']
            full_comment = youtube.comments().list(
                part="snippet",
                id=comment_id
            ).execute()

            # Clean the text comment by removing html tags and hashtags
            try:
                text = clean(full_comment['items'][0]['snippet']['textDisplay'])
            except:
                text = False
            comment['comment'] = text
            comments_list.append(comment)
        except Exception as e:
            print(f"An error occurred while retrieving comment {comment_id}: {e}")
    comments_df = pd.DataFrame(comments_list)
    
    return comments_df, meta

def get_sentiment_percentages(sentiments):
    total = sum(sentiments.values())
    for key, val in sentiments.items():
        sentiments[key] = round(val/total * 100, 2)
    return sentiments

def get_emotion_topics_percentages(topics_dict):
    total = sum(topics_dict.values())
    for key, val in topics_dict.items():
        topics_dict[key] = str(round(val/total * 100, 2)) + '%'
    return topics_dict

def rank_emotion_topics(df):
    emotion_columns = df.columns[1:]  
    ranked_dataframes = []
    df['index'] = df.index
    for column in emotion_columns:
        ranked_df = df[['index','comment', column]].sort_values(by=column, ascending=False).reset_index(drop=True)
        
        ranked_dataframes.append(ranked_df)
    
    return ranked_dataframes


def get_model_results(data):
    pine = SentimentTopicModel(data,
                           sentiment_model_path='D:\youtube-dashboard\youtube-dashboard\model\comment',
                           topic_model_path='j-hartmann/emotion-english-distilroberta-base',
                           num_labels=3)

    sentiments, sentiment_prob = pine.predict_sentiments(data)

    topic, topic_prob = pine.predict_topics(data)

    return sentiments, sentiment_prob, topic, topic_prob


# Perform Comments classification 
def commentsAnalysis(video_id):
        # Retrieve the most famous comments of the video, using YouTube API
        start = time.time()
        comments, meta_data = get_most_famous_comments(video_id)
        end = time.time()

        print("Retrieving the top k most famous comments took: ", end-start)

        start = time.time()
        results = get_model_results(comments)
        end = time.time()

        sentimentPerc = get_sentiment_percentages(results[0])

        print("Predictions fort he top k most famous comments took: ", end-start)
        results_df= pd.DataFrame(results[1])

        results_df['type'] = results_df[['negative','neutral','positive']].idxmax(axis=1)

        comments_df = pd.concat([comments, results_df], axis=1)
        comments_df = comments_df.loc[:, ~comments_df.columns.duplicated()]
        comments_df['index'] = comments_df.index

        topic_df = pd.DataFrame(results[3])
        sorted_topic_categories = rank_emotion_topics(topic_df)
        topics_percentage = get_emotion_topics_percentages(results[2])
        print(topics_percentage)
        return comments_df, meta_data, [sentimentPerc, topic_df, sorted_topic_categories, topics_percentage]


