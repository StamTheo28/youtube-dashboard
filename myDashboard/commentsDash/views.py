from django.http import JsonResponse
from django.shortcuts import render, redirect
from .utils.utils import url_parser, get_all_video_ids_in_cache
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

    table_res = results[['index','comment_id', 'like_count','reply_count','type', 'comment']]
    
    # Create a paginator object, handle page request on front-end
    paginator = Paginator(table_res.to_dict('records'), 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Create graph formats
    sentiment = ''
    sentiment = json.dumps(percentages[0])
   
    columns = ['Id','Comment Id', 'Like Count', 'Reply Count','Type', 'Comment']
    context = { "video_id":video_id, "columns": columns,'comments': table_res.to_dict('records'), "meta":meta, "page_obj":page_obj, 'sentiment':sentiment}
    
    return render(request, 'html/dashboard.html', context)


    
