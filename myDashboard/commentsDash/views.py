from django.http import JsonResponse
from django.shortcuts import render, redirect
from .utils.utils import video_parser
from .utils.youCom import commentsAnalysis
from django.core.paginator import Paginator
from django.core.cache import cache

def index(request):

    if request.method == "POST":
        url = request.POST['video_link']
        # ADD Make video link validation
        video_id = video_parser(url)
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
        # If not cached, perform analysis and cache the results
        results, meta = commentsAnalysis(video_id=video_id)
        cache.set(video_id, (results, meta))

    table_res = results[['comment_id', 'comment', 'like_count','reply_count','type']]

    # Create a paginator object, handle page request on front-end
    paginator = Paginator(table_res.to_dict('records'), 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    columns = ['Comment Id', 'Comment', 'Like Count', 'Reply Count','Type']
    context = { "columns": columns,'comments': table_res.to_dict('records'), "meta":meta, "page_obj":page_obj}

    return render(request, 'html/dashboard.html', context)


    
