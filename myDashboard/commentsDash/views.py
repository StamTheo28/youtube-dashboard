from __future__ import annotations

import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from .utils.graph import create_emoji_graph
from .utils.graph import get_graph_data
from .utils.graph import get_tag_cloud_data
from .utils.utils import url_to_videoId_parser
from .utils.youCom import commentsAnalysis


# Index view
def index(request):
    """
    Handles the homepage. Parses the video URL from the form and redirects to the analysis page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the index.html template or redirects to the analysis page.
    """
    if request.method == 'POST':
        url = request.POST.get('video_link')
        print('Getting URL:', url)
        video_id = url_to_videoId_parser(url)
        print('Current Video ID:', video_id)

        # Display error message if URL is invalid
        if video_id is False:
            messages.error(
                request,
                'Invalid URL. Please provide a valid YouTube video URL.',
            )
            context = {}
            return render(request, 'html/index.html', context)

        return redirect('analysis', video_id=video_id)
    else:
        context = {}
        return render(request, 'html/index.html', context)


# Comment analysis view
def analysis(request, video_id):
    """
    Handles analysis page. Retrieves comment analysis results and prepares data for visualization.

    Args:
        request (HttpRequest): The HTTP request object.
        video_id (str): The YouTube video ID.

    Returns:
        HttpResponse: Renders the dashboard.html template with analysis results and graphs.
    """
    results, meta = commentsAnalysis(video_id=video_id)

    # Display error message if analysis results are invalid
    if not isinstance(results, pd.DataFrame) and meta is None:
        messages.error(
            request,
            'Invalid URL. Please provide a valid YouTube video URL.',
        )
        context = {}
        return render(request, 'html/index.html', context)

    # Prepare analysis results and graph data
    if meta['commentCount'] is None:
        context = {
            'video_id': video_id,
            'meta': meta,
            'comments': None,
        }
    else:
        table_res = results[[
            'index',
            'comment_id',
            'like_count',
            'reply_count',
            'sentiment',
            'comment',
            'word_length',
        ]]

        section_data = get_graph_data(results)

        # Prepare tag cloud data
        if meta['tags'] is None:
            tag_cloud = None
        else:
            tag_cloud = get_tag_cloud_data(meta['tags'])

        # Create emoji plot
        emoji_graph = create_emoji_graph(section_data['emojis'])

        context = {
            'video_id': video_id,
            'meta': meta,
            'section_data': section_data,
            'tags': tag_cloud,
            'emoji_graph': emoji_graph,
            'comments': table_res.to_dict(orient='records'),
        }

    return render(request, 'html/dashboard.html', context)


# Error 400 view
def error_400(request, exception):
    """
    Handles the 400 Bad Request error page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that caused the error.

    Returns:
        HttpResponse: Renders the 400.html template with the error message.
    """
    return render(request, 'errors/400.html', status=400)


# Error 403 view
def error_403(request, exception):
    """
    Handles the 403 Forbidden error page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that caused the error.

    Returns:
        HttpResponse: Renders the 403.html template with the error message.
    """
    return render(request, 'errors/403.html', status=403)


# Error 404 view
def error_404(request, exception):
    """
    Handles the 404 Not Found error page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that caused the error.

    Returns:
        HttpResponse: Renders the 404.html template with the error message.
    """
    return render(request, 'errors/404.html', status=404)


# Error 500 view
def error_500(request):
    """
    Handles the 500 Internal Server Error page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 500.html template with the error message.
    """
    return render(request, 'errors/500.html', status=500)
