from django.core.cache import cache
import re
import requests
from django.core.paginator import Paginator



# Check if the url is valid and is of the Youtube format
def url_parser(url):
    regex = r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
    match = re.match(regex, url)
    return match.group(7) if match and len(match.group(7)) == 11 else False


def clean_date(date):
    return date[:10]


def get_all_video_ids_in_cache():
    all_keys = cache._cache.keys()  # Get all keys stored in the cache
    video_ids = [key.replace(':1:', "") for key in all_keys if key.startswith(':1')]  # Filter out video_id keys
    return video_ids

# Create a paginator object
# data is a dataframe, django view request
def get_paginator(data, request, page_name, num_per_page=10):
    paginator = Paginator(data.to_dict('records'), num_per_page)
    page_number = request.GET.get(page_name)
    page_obj = paginator.get_page(page_number)
    return page_obj