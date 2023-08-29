from __future__ import annotations

import re

from bs4 import BeautifulSoup


# Check if the url is valid and is of the Youtube format
def url_to_videoId_parser(url):
    regex = r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*'
    match = re.match(regex, url)
    return match.group(7) if match and len(match.group(7)) == 11 else False


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


# Get the dd/mm/yyyy from the datetime varaibles
def clean_date(date):
    return date[:10]


# Function that converts the video duration format to 'h m s' format
def convert_duration(duration):
    # Check if the duration is in the right format
    if not duration.startswith('PT'):
        raise ValueError('Invalid duration format')

    # Remove the 'PT' prefix and 'S' suffix from the duration
    duration = duration[2:-1]

    # Split the duration into minutes and seconds if video is less than a minute
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
