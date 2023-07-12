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
            text = full_comment['items'][0]['snippet']['textDisplay']
            comment['comment'] = clean(text)
            comments_list.append(comment)
        except Exception as e:
            print(f"An error occurred while retrieving comment {comment_id}: {e}")
    comments_df = pd.DataFrame(comments_list)
    
    return comments_df, meta

def get_model_results(data):
    pine = SentimentTopicModel(data,
                           sentiment_model_path='D:\youtube-dashboard\youtube-dashboard\model\comment',
                           topic_model_path='j-hartmann/emotion-english-distilroberta-base',
                           num_labels=3)

    sentiments, sentiment_prob = pine.predict_sentiments(data)
    sent_df = pd.DataFrame(sentiment_prob)

    sent_df = sent_df[['negative','neutral','positive']].apply(pd.to_numeric)
    return sentiments, sentiment_prob


# Perform Comments classification 
def commentsAnalysis(video_id):
        # Retrieve the most famous comments of the video
        start = time.time()
        comments, meta = get_most_famous_comments(video_id)
        end = time.time()

        print("Retrieving the top 10 most famous comments took: ", end-start)

        start = time.time()
        results = get_model_results(comments)
        end = time.time()

        print("Predictions fort he top 10 most famous comments took: ", end-start)
        results_df= pd.DataFrame(results[1])


        # Return the comment type
        results_df['type'] = results_df[['negative','neutral','positive']].idxmax(axis=1)


        # Concatinate and remove duplicate columns
        df = pd.concat([comments, results_df], axis=1)
        df = df.loc[:, ~df.columns.duplicated()]

       
        print(df.head(2))
        return df, meta