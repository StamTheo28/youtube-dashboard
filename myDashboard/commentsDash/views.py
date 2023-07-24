from django.http import JsonResponse
from django.shortcuts import render, redirect
from .utils.utils import url_parser, get_all_video_ids_in_cache, get_paginator
from .utils.youCom import commentsAnalysis
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib import messages
import json


def index(request):
    if request.method == "POST":
        url = request.POST.get('video_link')
        video_id = url_parser(url)
        # Display message if url is invalid
        if video_id==False:
            messages.error(request, 'Invalid URL. Please provide a valid YouTube video URL.')
            cached_results = cache.get(video_id)
            if cached_results is not None:
                return redirect('index')
            else:
                video_id=get_all_video_ids_in_cache()[0]
                return redirect('analysis', video_id=video_id)
        
        return redirect('analysis', video_id=video_id)
    else:
        context = {}
        return render(request, 'html/index.html', context)


# Comment analysis view
def analysis(request, video_id):

    cached_results = cache.get(video_id)
    
    if cached_results is not None:
        results, meta, percentages = cached_results
    else:
        existing_ids = get_all_video_ids_in_cache()
        # Delete existing ids
        if len(existing_ids)==1:
            cache.delete(existing_ids[0])

        # If not cached, perform analysis and cache the results
        results, meta, percentages  = commentsAnalysis(video_id=video_id)
        cache.set(video_id, (results, meta, percentages))
    
    # Create paginator objects
    if meta['commentCount'] == None:
        comments_page = None
        context = { "video_id":video_id, 
            "meta":meta, 
            "comments_page":comments_page,
            }
    else:
        table_res = results[['index','comment_id', 'like_count','reply_count','type', 'comment']]
        comments_page = get_paginator(table_res, request, "comments_page")

        topics_page = get_paginator(percentages[1][['index','comment','emotion']], request, "topics_page", 10)

        # Create graph formats
        topics_results = json.dumps(percentages[1].to_dict())
        sorted_topics = percentages[2]
        topics_percentages = json.dumps(percentages[3])

        emotions_pages = {}
        for emotion, data in sorted_topics.items():
            page_name = emotion+"_page"
            page = get_paginator(data, request, page_name, 15)
            
            emotions_pages[emotion] = page

        # Retrieve the current emotion
        emotion = ""
        try:
            emotion = request.GET.get('topic-button')  # Get the selected button from the request
            emotion_page = emotions_pages[emotion]
        except:
            emotion = "anger"
            emotion_page = emotions_pages[emotion]

        # Create Graph Data
        emotion_data = json.dumps(percentages[1][['index','comment',emotion]].to_dict('records'))
        sentiment = json.dumps(percentages[0])
        context = { "video_id":video_id, 
                    "meta":meta, 
                    "comments_page":comments_page,
                    'sentiment':sentiment,
                    "emotion":emotion,
                    "emotion_page":emotion_page,
                    "emotion_data":emotion_data
                    }
        

    
    return render(request, 'html/dashboard.html', context)


    
