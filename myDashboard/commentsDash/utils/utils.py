from __future__ import annotations

import re


# Check if the url is valid and is of the Youtube format
def url_to_videoId_parser(url):
    regex = r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*'
    match = re.match(regex, url)
    return match.group(7) if match and len(match.group(7)) == 11 else False

# Get the dd/mm/yyyy from the datetime varaibles


def clean_date(date):
    return date[:10]
