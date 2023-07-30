# ADD TO ENVIROMENT VARIABLES
API_KEY = "AIzaSyCj_o0-0ej8EOa6tPYPKfhJyI3c-zPJ9Yc"

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
from .utils import clean_date
from .sentiment import comment_analysis, get_clean_data
import pandas as pd
import re
import time
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

import spacy
from spacymoji import Emoji

from tqdm.auto import tqdm






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
    try:
        meta['commentCount'] = video['items'][0]['statistics']['commentCount']
        commentSection = True
    except:
        meta['commentCount'] = None
        commentSection = False
    meta['likeCount'] = video['items'][0]['statistics']['likeCount']
    meta['favoriteCount'] = video['items'][0]['statistics']['favoriteCount']


    # Check the comment section is diabled
    if commentSection:
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
                comment['word_length'] = len(comment['comment'].split(' '))
                comments_list.append(comment)
            except Exception as e:
                print(f"An error occurred while retrieving comment {comment_id}: {e}")
        comments_df = pd.DataFrame(comments_list)
    else:
        comments_df = pd.DataFrame()
    
    return comments_df, meta


# Perform Comments classification 
def commentsAnalysis(video_id):
        # Retrieve the most famous comments of the video, using YouTube API
        start = time.time()
        comments, meta_data = get_most_famous_comments(video_id)
        end = time.time()

        print("Retrieving the top k most famous comments took: ", end-start)


        if comments.empty:
            return None, meta_data
        else:
            start = time.time()
            df = comment_analysis(comments)        
            end = time.time()

            df['index'] = df.index

            print("Creating a sentemint analysis for the k comments took: ", end-start)
            return df, meta_data
        
def get_most_frequent_words(data, word_number=10):
    df = get_clean_data(data)
    word_freq_dist = FreqDist(word_tokenize((" ").join(df['clean_comment'])))
    frequent_words = word_freq_dist.most_common(word_number)
    result_dict = {word: frequency for word, frequency in frequent_words}
    return result_dict



# Emoji Extraction
def get_emoji(data):
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("emoji", first=True)
    nlp.pipe_names

    def extract_emojies(x):
        doc = nlp(x['comment']) #with emojis
        emojis = [token.text for token in doc if token._.is_emoji]
        return emojis
    
    tqdm.pandas(desc="Detecting Emoji")
    emojies_df = data.progress_apply(extract_emojies,axis=1)
    emoji_counts = (emojies_df
                    .apply(pd.Series)  # breaks up the list into separate columns
                    .stack()  # collapses each column into one column
                    .value_counts()  # counts the frequency of each item
                    .rename('Count')
                    .sort_values(ascending=False)
                    .reset_index()
                    .rename(columns={'index': 'Emoji'}))
    
    emoji_counts_dict = emoji_counts.head(10).set_index('Emoji')['Count'].to_dict()
    return emoji_counts_dict
