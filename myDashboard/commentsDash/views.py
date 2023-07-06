from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils.utils import video_parser
from .utils.youCom import commentsAnalysis


def index(request):

    if request.method == "POST":
        url = request.POST['video_link']
        # ADD Make video link validation
        
        video_id = video_parser(url)
        data = commentsAnalysis(video_id=video_id)
        

    else:
        data = ['Nothing is here bro']


    return render(request, 'html/index.html', {'data': data})

