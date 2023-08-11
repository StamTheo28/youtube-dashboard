from django.shortcuts import render, redirect
from .utils.utils import url_to_videoId_parser, get_all_video_ids_in_cache
from .utils.youCom import commentsAnalysis
from .utils.graph import get_graph_data, get_tag_cloud_data
from django.core.cache import cache
from django.contrib import messages
import pandas as pd




def index(request):
    if request.method == "POST":
        url = request.POST.get('video_link')
        print('Gettign URL: ',url)
        video_id = url_to_videoId_parser(url)
        print("Current Video ID",video_id)
        # Display message if url is invalid
        if video_id==False:
            messages.error(request, 'Invalid URL. Please provide a valid YouTube video URL.')
            cached_results = cache.get(video_id)
            if cached_results is None:
                context = {}
                return render(request, 'html/index.html', context)
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
        if not isinstance(results, pd.DataFrame) and meta==None:
            messages.error(request, 'Invalid URL. Please provide a valid YouTube video URL.')
            cached_results = cache.get(video_id)
            if cached_results is None:
                context = {}
                return render(request, 'html/index.html', context)
            else:
                video_id=get_all_video_ids_in_cache()[0]
                return redirect('analysis', video_id=video_id)
        else:
            cache.set(video_id, (results, meta))
    
    # Create paginator objects
    if meta['commentCount'] == None:
        context = { "video_id":video_id, 
            "meta":meta, 
            "comments":None,
            }
    else:
        table_res = results[['index','comment_id', 'like_count','reply_count','sentiment', 'comment','word_length']]

        # Create graph data
        section_data = get_graph_data(results)
        if meta['tags']==None:
            tag_cloud = None
        else:
            tag_cloud = get_tag_cloud_data(meta['tags'])

        context = { "video_id":video_id, 
                    "meta":meta, 
                    "section_data":section_data,
                    "tags":tag_cloud,
                    "comments":table_res.to_dict(orient='records')
                    }
        
    
    return render(request, 'html/dashboard.html', context)


def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)

def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_500(request, exception):
    return render(request, 'errors/500.html', status=500)