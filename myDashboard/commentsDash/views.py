from django.http import JsonResponse
from django.shortcuts import render, redirect
from .utils.utils import url_parser, get_all_video_ids_in_cache, get_paginator
from .utils.youCom import commentsAnalysis
from .utils.graph import get_sentiment_pie_data, get_graph_data
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
        results, meta = cached_results
    else:
        existing_ids = get_all_video_ids_in_cache()
        # Delete existing ids
        if len(existing_ids)==1:
            cache.delete(existing_ids[0])

        # If not cached, perform analysis and cache the results
        results, meta  = commentsAnalysis(video_id=video_id)
        cache.set(video_id, (results, meta))
    
    # Create paginator objects
    if meta['commentCount'] == None:
        comments_page = None
        context = { "video_id":video_id, 
            "meta":meta, 
            "comments_page":comments_page,
            }
    else:
        table_res = results[['index','comment_id', 'like_count','reply_count','sentiment', 'comment','word_length']]
        comments_page = get_paginator(table_res, request, "comments_page")

        # Create graph data
        sentiment_percentages = get_sentiment_pie_data(table_res)
        section_data = get_graph_data(table_res)
        print(section_data)

        #section_page = section_page[section]

        
        context = { "video_id":video_id, 
                    "meta":meta, 
                    "comments_page":comments_page,
                    "sentiment_percentages": sentiment_percentages,
                    "section_data":section_data
                    }
        

    
    return render(request, 'html/dashboard.html', context)


    
