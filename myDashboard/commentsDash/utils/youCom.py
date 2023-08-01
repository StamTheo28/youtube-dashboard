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
from datetime import datetime
import spacy
from spacymoji import Emoji

from tqdm.auto import tqdm

# Youtube categories ids and their names
youtube_categories = {
    '1': 'Film & Animation',
    '2': 'Autos & Vehicles',
    '10': 'Music',
    '15': 'Pets & Animals',
    '17': 'Sports',
    '18': 'Short Movies',
    '19': 'Travel & Events',
    '20': 'Gaming',
    '21': 'Videoblogging',
    '22': 'People & Blogs',
    '23': 'Comedy',
    '24': 'Entertainment',
    '25': 'News & Politics',
    '26': 'Howto & Style',
    '27': 'Education',
    '28': 'Science & Technology',
    '29': 'Nonprofits & Activism',
    '30': 'Movies',
    '31': 'Anime/Animation',
    '32': 'Action/Adventure',
    '33': 'Classics',
    '34': 'Comedy',
    '35': 'Documentary',
    '36': 'Drama',
    '37': 'Family',
    '38': 'Foreign',
    '39': 'Horror',
    '40': 'Sci-Fi/Fantasy',
    '41': 'Thriller',
    '42': 'Shorts',
    '43': 'Shows',
    '44': 'Trailers'
}

def convert_duration(duration):
    # Check if the duration is in the right format
    if not duration.startswith("PT"):
        raise ValueError("Invalid duration format")

    # Remove the 'PT' prefix and 'S' suffix from the duration
    duration = duration[2:-1]

    # Split the duration into minutes and seconds
    minutes, seconds = map(int, duration.split("M"))

    # Convert minutes to hours if necessary
    hours = minutes // 60
    minutes %= 60

    # Format the duration as a string
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


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
    part='snippet,statistics,contentDetails',
    id=video_id
    ).execute()

    # Extract the video metadata
    meta = {}
    meta['category'] = youtube_categories[video['items'][0]['snippet']['categoryId']]
    meta['video_id'] = video_id
    meta['title'] = video['items'][0]['snippet']['title']
    meta['description'] = video['items'][0]['snippet']['description']
    if len(meta['description'])==0:
        meta['description'] = None
    meta['publishedAt'] = clean_date(video['items'][0]['snippet']['publishedAt'])
    meta['thumbnail'] = video['items'][0]['snippet']['thumbnails']['high']['url']
    meta['channelTitle'] = video['items'][0]['snippet']['channelTitle']
    meta['viewCount'] = video['items'][0]['statistics']['viewCount']
    try:
        meta['tags'] = video['items'][0]['snippet']['tags']
    except:
        meta['tags'] = None
    try:
        meta['commentCount'] = video['items'][0]['statistics']['commentCount']
        commentSection = True
    except:
        meta['commentCount'] = None
        commentSection = False
    meta['likeCount'] = video['items'][0]['statistics']['likeCount']
    meta['duration'] = convert_duration(video['items'][0]['contentDetails']['duration'])
    print(meta['duration'])

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
            comment_data['publishedAt'] = item['snippet']['topLevelComment']['snippet']['publishedAt']
            if 'like_count' not in comment_data.keys():
                comment_data["like_count"] = 0
            if 'reply_count' not in comment_data.keys():
                comment_data["reply_count"] = 0
            comments.append(comment_data)
        comments_list = []

        print(comments[0]['publishedAt'])
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

def get_month_count(data):
    dates = data['publishedAt']
    # Parse the datetimes into datetime objects
    datetimes = sorted([datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ') for dt_str in dates])

    # Create a dictionary to store the count of each month
    month_counts = {}

    # Group the datetimes by month and count occurrences
    for dt in datetimes:
        month = dt.strftime('%Y-%m')  # Extract the year-month part (e.g., '2009-01')
        if month not in month_counts:
            month_counts[month] = 0
        month_counts[month] += 1
        
    return month_counts