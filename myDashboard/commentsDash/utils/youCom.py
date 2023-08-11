# ADD TO ENVIROMENT VARIABLES
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from .utils import clean_date
from .sentiment import comment_analysis, get_clean_data
import pandas as pd
import re
import os
import time
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from datetime import datetime, timedelta
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

    # Split the duration into minutes and seconds if video is less than a minute
    if "M" not in duration:
        hours = 0
        minutes = 0
        seconds = int(duration[:2].replace("S",""))
    else:
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

def get_comment_threads(response, comments):
    print(len(response['items']))
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
    return comments

# Retrieves the top k most famous comments of a youtube video
def get_most_famous_comments( video_id, max_comments=200):
    youtube = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE-API-KEY'))
    
    # Retrieve video statistics
    video = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=video_id,
    ).execute()
    
    # Returns null if video_id does not exist
    if len(video['items'])==0:
        print('Video id does not exist in youtube')
        return None, None
    else:
        # Extract the video metadata
        meta = {}
        try:
            meta['category'] = youtube_categories[video['items'][0]['snippet']['categoryId']]
        except:
            meta['category'] = 'N/A'

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
        

        # Check the comment section is diabled
        if commentSection:
            # Retrieve the comment threads for the video
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                order="relevance",
                maxResults=101
                ).execute()
            
            comments = []
            comments = get_comment_threads(response, comments)
            
            if 'nextPageToken' in response:
                response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                order="relevance",
                pageToken=response['nextPageToken'],
                maxResults=101
                ).execute()
                
                # application code
                comments = get_comment_threads(response, comments)
            else:
                pass
            

            comments_list = []
            # Retrieve the full comments using the comment IDs
            for comment in comments:
                try:
                    comment_id = comment['comment_id']
                    full_comment = youtube.comments().list(
                        part="snippet",
                        id=comment_id,
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
        if not isinstance(comments, pd.DataFrame) and meta_data == None:
            print("Creating a sentemint analysis for the k comments took: ", end-start)
            return comments, meta_data
        elif comments.empty:
            print("Creating a sentemint analysis for the k comments took: ", end-start)
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


from datetime import datetime, timedelta

from datetime import datetime, timedelta
def get_comment_activity(data):
    dates = data['publishedAt']
    # Parse the datetimes into datetime objects
    datetimes = sorted([datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ') for dt_str in dates])

    # Create dictionaries to store the count of each month, trimester, and year
    month_counts = {}
    trimester_counts = {}
    year_counts = {}

    # Group the datetimes by month, trimester, and year and count occurrences
    for dt in datetimes:
        month = dt.strftime('%Y-%m')  # Extract the year-month part (e.g., '2009-01')
        trimester = f"{dt.year}-T{((dt.month-1) // 4) + 1}"  # Calculate the trimester based on the month
        year = str(dt.year)

        if month not in month_counts:
            month_counts[month] = 0
        if trimester not in trimester_counts:
            trimester_counts[trimester] = 0
        if year not in year_counts:
            year_counts[year] = 0

        month_counts[month] += 1
        trimester_counts[trimester] += 1
        year_counts[year] += 1

    # Step 2: Check for missing months, trimesters, and years and add them with a count of 0
    start_date = min(datetimes).replace(day=1)
    end_date = max(datetimes).replace(day=28) + timedelta(days=4)  # To make sure the last month is included

    current_date = start_date
    while current_date <= end_date:
        month = current_date.strftime('%Y-%m')
        trimester = f"{current_date.year}-T{((current_date.month-1) // 4) + 1}"
        year = str(current_date.year)

        if month not in month_counts:
            month_counts[month] = 0
        if trimester not in trimester_counts:
            trimester_counts[trimester] = 0
        if year not in year_counts:
            year_counts[year] = 0

        current_date += timedelta(days=32)  # Move to the next month

    # Check if there are only two dates in the month, semester, or year dictionaries
    if len(month_counts) <= 2:
        prev_date = min(datetimes) - timedelta(days=32)
        next_date = max(datetimes) + timedelta(days=32)
        month_counts[prev_date.strftime('%Y-%m')] = 0
        

    if len(trimester_counts) <= 2:
        prev_date = min(datetimes) - timedelta(days=140)
        next_date = max(datetimes) + timedelta(days=140)
        trimester_counts[prev_date.strftime('%Y-T1')] = 0
       

    if len(year_counts) <= 2:
        prev_date = min(datetimes) - timedelta(days=365)
        next_date = max(datetimes) + timedelta(days=365)
        year_counts[str(prev_date.year)] = 0
        

    # Sort the dictionaries by keys to have the data in chronological order
    month_counts = dict(sorted(month_counts.items()))
    trimester_counts = dict(sorted(trimester_counts.items()))
    year_counts = dict(sorted(year_counts.items()))

    return {
        'month': month_counts,
        'semester': trimester_counts,
        'year': year_counts
    }
