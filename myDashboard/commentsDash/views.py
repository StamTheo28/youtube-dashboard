from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):

    if request.method == "POST":
        video_link = request.POST['video_link']
        # Make video link validation
        data = getNegativeComments(video_link)
    else:
        data = ['Nothing is here bro']


    return render(request, 'html/index.html', {'data': data})


def getNegativeComments(video_link):
    # Use trained model
    return ['This is a list with negative commetns']