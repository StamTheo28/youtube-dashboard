from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils import video_parser


def index(request):

    if request.method == "POST":
        url = request.POST['video_link']
        # ADD Make video link validation
        
        data = video_parser(url)
    else:
        data = ['Nothing is here bro']


    return render(request, 'html/index.html', {'data': data})


def getNegativeComments(video_link):
    # Use trained model
    return ['This is a list with negative commetns']