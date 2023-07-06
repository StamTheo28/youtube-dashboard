# ADD TO ENVIROMENT VARIABLES
API_KEY = "AIzaSyCj_o0-0ej8EOa6tPYPKfhJyI3c-zPJ9Yc"

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
from .pipeline import SentimentTopicModel
import pandas as pd
import re

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

def get_most_famous_comments( video_id, max_comments=2):
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
        comment_data['like_count'] = item['snippet']['topLevelComment']['snippet']['likeCount']
        comment_data['reply_count'] = item['snippet']['totalReplyCount']
        comments.append(comment_data)
    comments_list = []
	# Retrieve the full comments using the comment IDs
    for comment in comments:
        try:
            comment_id = comment['comment_id']
            full_comment = youtube.comments().list(
                part="snippet",
                id=comment_id
            ).execute()
            text = full_comment['items'][0]['snippet']['textDisplay']
            comment['comment'] = clean(text)
            comments_list.append(comment)
        except Exception as e:
            print(f"An error occurred while retrieving comment {comment_id}: {e}")

    comments_df = pd.DataFrame(comments)
    return comments_df

def get_model_results(data):
    pine = SentimentTopicModel(data,
                           sentiment_model_path='comment',
                           topic_model_path='j-hartmann/emotion-english-distilroberta-base',
                           num_labels=3)

    sentiments, sentiment_prob = pine.predict_sentiments(data)
    return sentiments, sentiment_prob

# Perform Comments classification 
def commentsAnalysis(video_id):
        # Retrieve the most famous comments of the video
        comments = get_most_famous_comments(video_id)['comment']
        results = get_model_results(comments)
        print(results[0])
        print(results[1])
        return results