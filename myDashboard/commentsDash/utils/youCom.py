# ADD TO ENVIROMENT VARIABLES
from __future__ import annotations

import os
import time

import pandas as pd
import spacy
from googleapiclient.discovery import build
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from tqdm.auto import tqdm

from .sentiment import comment_analysis
from .sentiment import get_clean_data
from .utils import clean
from .utils import clean_date
from .utils import convert_duration


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
    '44': 'Trailers',
}


def get_comment_threads(response, comments):
    """
    Extracts relevant information from a YouTube API response and populates the comments list.

    Args:
        response (dict): The response obtained from the YouTube API containing comment thread data.
        comments (list): A list to store extracted comment data.

    Returns:
        list: The updated list of comments containing comment data from the API response.
    """
    for item in response['items']:
        comment_data = {}  # Create a dictionary to store extracted comment data
        comment_data['comment_id'] = item['id']  # Extract comment ID
        # Extract comment text
        comment_data['comment'] = item['snippet']['topLevelComment']['snippet']['textDisplay']
        # Extract comment's like count
        comment_data['like_count'] = item['snippet']['topLevelComment']['snippet']['likeCount']
        # Extract total reply count
        comment_data['reply_count'] = item['snippet']['totalReplyCount']
        # Extract comment's publish date
        comment_data['publishedAt'] = item['snippet']['topLevelComment']['snippet']['publishedAt']

        # Check if 'like_count' key is missing and set it to 0 if missing
        if 'like_count' not in comment_data.keys():
            comment_data['like_count'] = 0

        # Check if 'reply_count' key is missing and set it to 0 if missing
        if 'reply_count' not in comment_data.keys():
            comment_data['reply_count'] = 0

        # Add extracted comment data to the comments list
        comments.append(comment_data)

    return comments  # Return the updated list of comments


def get_most_famous_comments(video_id, max_comments=100):
    """
    Retrieves relevant information about a YouTube video and its comments.

    Args:
        video_id (str): The YouTube video's unique identifier.
        max_comments (int, optional): The maximum number of comments to retrieve. Defaults to 100.

    Returns:
        pandas.DataFrame: A DataFrame containing comments' data.
        dict: A dictionary containing video metadata.
    """
    youtube = build(
        'youtube', 'v3',
        developerKey=os.environ.get('YOUTUBE-API-KEY'),
    )

    # Retrieve video statistics
    video = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=video_id,
    ).execute()

    # Return null if video_id does not exist
    if len(video['items']) == 0:
        print('Video id does not exist on YouTube')
        return None, None
    else:
        # Extract video metadata
        meta = {}
        try:
            meta['category'] = youtube_categories[
                video['items']
                [0]['snippet']['categoryId']
            ]
        except Exception as e:
            # Handle any other exceptions that might occur
            print(f'An error occurred: {e}')
            meta['category'] = 'N/A'

        # Extract other video metadata
        meta['video_id'] = video_id
        meta['title'] = video['items'][0]['snippet']['title']
        meta['description'] = video['items'][0]['snippet']['description']
        if len(meta['description']) == 0:
            meta['description'] = None
        meta['publishedAt'] = clean_date(
            video['items'][0]['snippet']['publishedAt'],
        )
        meta['thumbnail'] = video['items'][0]['snippet']['thumbnails']['high']['url']
        meta['channelTitle'] = video['items'][0]['snippet']['channelTitle']
        meta['viewCount'] = video['items'][0]['statistics']['viewCount']
        try:
            meta['tags'] = video['items'][0]['snippet']['tags']
        except Exception as e:
            # Handle any other exceptions that might occur
            print(f'An error occurred: {e}')
            meta['tags'] = None
        try:
            meta['commentCount'] = video['items'][0]['statistics']['commentCount']
            commentSection = True
        except Exception as e:
            # Handle any other exceptions that might occur
            print(f'An error occurred: {e}')
            meta['commentCount'] = None
            commentSection = False
        meta['likeCount'] = video['items'][0]['statistics']['likeCount']
        meta['duration'] = convert_duration(
            video['items'][0]['contentDetails']['duration'],
        )

        # Check if the comment section is disabled
        if commentSection:
            # Retrieve the comment threads for the video
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                order='relevance',
                maxResults=max_comments,
            ).execute()

            comments = []
            comments = get_comment_threads(response, comments)

            comments_list = []
            # Retrieve the full comments using the comment IDs
            for comment in comments:
                try:
                    comment_id = comment['comment_id']
                    full_comment = youtube.comments().list(
                        part='snippet',
                        id=comment_id,
                    ).execute()

                    # Clean the text comment by removing HTML tags and hashtags
                    try:
                        text = clean(
                            full_comment['items'][0]['snippet']['textDisplay'],
                        )
                    except Exception as e:
                        # Handle any other exceptions that might occur
                        print(f'An error occurred: {e}')
                        text = False
                    comment['comment'] = text
                    comment['word_length'] = len(comment['comment'].split(' '))
                    comments_list.append(comment)
                except Exception as e:
                    print(
                        f'An error occurred while retrieving comment {comment_id}: {e}',
                    )

            comments_df = pd.DataFrame(comments_list)

        else:
            comments_df = pd.DataFrame()

        return comments_df, meta


def commentsAnalysis(video_id):
    """
    Perform sentiment analysis on the most famous comments of a given YouTube video.

    Args:
        video_id (str): The unique identifier of the YouTube video.

    Returns:
        pd.DataFrame or None: A DataFrame containing sentiment analysis results for comments,
        or None if no comments.
        dict: Metadata about the video.
    """
    # Retrieve the most famous comments of the video, using the YouTube API
    start = time.time()
    comments, meta_data = get_most_famous_comments(video_id)
    end = time.time()

    print('Retrieving the top k most famous comments took: ', end - start)

    # If comments are not in DataFrame format and metadata is None
    if not isinstance(comments, pd.DataFrame) and meta_data is None:
        print('Creating a sentiment analysis for the k comments took: ', end - start)
        return comments, meta_data

    # If there are no comments
    elif comments.empty:
        print('Creating a sentiment analysis for the k comments took: ', end - start)
        return None, meta_data

    # If there are comments
    else:
        start = time.time()
        # Perform sentiment analysis on comments
        df = comment_analysis(comments)
        end = time.time()

        df['index'] = df.index  # Add an index column for reference

        print('Creating a sentiment analysis for the k comments took: ', end - start)
        return df, meta_data


def get_most_frequent_words(data, word_number=10):
    """
    Get the most frequent words from cleaned comments.

    Args:
        data (pd.DataFrame): A DataFrame containing comment data.
        word_number (int, optional): The number of most frequent words to retrieve. Defaults to 10.

    Returns:
        dict: A dictionary containing the most frequent words and their frequencies.
    """
    df = get_clean_data(
        data,
    )  # Get cleaned comment data using a function (get_clean_data)
    # Create frequency distribution of words
    word_freq_dist = FreqDist(word_tokenize((' ').join(df['clean_comment'])))
    frequent_words = word_freq_dist.most_common(
        word_number,
    )  # Retrieve the most common words
    result_dict = {
        word: frequency for word,
        frequency in frequent_words
    }  # Convert to a dictionary
    # Return the dictionary containing most frequent words and their frequencies
    return result_dict


# Emoji Extraction
def get_emoji(data):
    """
    Extract and count emojis from comments using SpaCy.

    Args:
        data (pd.DataFrame): A DataFrame containing comment data.

    Returns:
        dict: A dictionary containing the top 10 emojis and their counts.
    """
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('emoji', first=True)
    nlp.pipe_names

    def extract_emojis(x):
        """
        Helper function to extract emojis from a comment using SpaCy.

        Args:
            x (pd.Series): A Series containing comment data.

        Returns:
            list: A list of emojis detected in the comment.
        """
        doc = nlp(x['comment'])  # Process the comment with emojis
        # Extract emojis
        emojis = [token.text for token in doc if token._.is_emoji]
        return emojis

    tqdm.pandas(desc='Detecting Emoji')
    # Apply emoji extraction to each comment
    emojies_df = data.progress_apply(extract_emojis, axis=1)
    emoji_counts = (
        emojies_df
        .apply(pd.Series)  # Breaks up the list into separate columns
        .stack()  # Collapses each column into one column
        .value_counts()  # Counts the frequency of each emoji
        .rename('Count')
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={'index': 'Emoji'})
    )

    emoji_counts_dict = emoji_counts.head(10).set_index(
        'Emoji',
    )['Count'].to_dict()  # Convert top 10 emojis to a dictionary
    return emoji_counts_dict
