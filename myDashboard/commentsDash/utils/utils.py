from __future__ import annotations

import re

from bs4 import BeautifulSoup


def url_to_videoId_parser(url):
    """
    Parses a YouTube video URL to extract the video's unique identifier (video ID).

    Args:
        url (str): The YouTube video URL.

    Returns:
        str or False: The extracted video ID if the URL is valid and of the YouTube format,
        otherwise False.
    """
    regex = r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*'
    # Check if the URL matches the YouTube video format
    match = re.match(regex, url)
    return match.group(7) if match and len(match.group(7)) == 11 else False


# Remove tags and hashtags from comments
def clean(text):
    """
    Removes HTML tags and hashtags from a given text.

    Args:
        text (str): The input text containing HTML tags and hashtags.

    Returns:
        str: The text with HTML tags and hashtags removed.
    """
    # Remove <a> HTML tags using BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all('a'):
        tag.unwrap()
    text = str(soup)

    # Remove hashtags using regular expression
    text = re.sub(r'#\w+', '', text)

    return text


# Get the dd/mm/yyyy from the datetime variables
def clean_date(date):
    """
    Extracts the date portion (dd/mm/yyyy) from a datetime variable.

    Args:
        date (str): The datetime variable in 'yyyy-mm-ddThh:mm:ssZ' format.

    Returns:
        str: The date in 'dd/mm/yyyy' format.
    """
    return date[:10]


# Function that converts the video duration format to 'h m s' format
def convert_duration(duration):
    """
    Converts a video duration from 'PT#H#M#S' format to 'h m s' format.

    Args:
        duration (str): The video duration in 'PT#H#M#S' format.

    Returns:
        str: The video duration in 'h m s' format.
    """
    # Check if the duration is in the right format
    if not duration.startswith('PT'):
        raise ValueError('Invalid duration format')

    # Remove the 'PT' prefix and 'S' suffix from the duration
    duration = duration[2:-1]

    # Split the duration into minutes and seconds if the video is less than a minute
    if 'M' not in duration:
        hours = 0
        minutes = 0
        seconds = int(duration[:2].replace('S', ''))
    else:
        minutes, seconds = map(int, duration.split('M'))
        # Convert minutes to hours if necessary
        hours = minutes // 60
        minutes %= 60

    # Format the duration as a string
    if hours > 0:
        return f'{hours}h {minutes}m {seconds}s'
    elif minutes > 0:
        return f'{minutes}m {seconds}s'
    else:
        return f'{seconds}s'
