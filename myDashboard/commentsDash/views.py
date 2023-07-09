from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils.utils import video_parser
from .utils.youCom import commentsAnalysis


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
    results, meta = commentsAnalysis(video_id=video_id)
    table_res = results[['comment_id', 'comment', 'like_count','reply_count','type']]
    columns = ['Comment Id', 'Comment', 'Like Count', 'Reply Count','Type']
    context = { "columns": columns,'comments': table_res.to_dict('records'), "meta":meta}

    return render(request, 'html/dashboard.html', context)
