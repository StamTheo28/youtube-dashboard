from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils.utils import video_parser
from .utils.youCom import commentsAnalysis


def index(request):

    if request.method == "POST":
        url = request.POST['video_link']
        # ADD Make video link validation
        
        video_id = video_parser(url)
        video_comments = commentsAnalysis(video_id=video_id)
        data = video_comments['text']

    else:
        data = ['Nothing is here bro']


    return render(request, 'html/index.html', {'data': data})


def getNegativeComments(video_link):
    # Use trained model
    return ['This is a list with negative commetns']