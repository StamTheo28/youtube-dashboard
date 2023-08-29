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


def index(request):
    if request.method == 'POST':
        url = request.POST.get('video_link')
        print('Gettign URL: ', url)
        video_id = url_to_videoId_parser(url)
        print('Current Video ID', video_id)
        # Display message if url is invalid
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

    results, meta = commentsAnalysis(video_id=video_id)
    if not isinstance(results, pd.DataFrame) and meta is None:
        messages.error(
            request,
            'Invalid URL. Please provide a valid YouTube video URL.',
        )
        context = {}
        return render(request, 'html/index.html', context)

    # Create paginator objects
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

        # Create graph data
        section_data = get_graph_data(results)
        if meta['tags'] is None:
            tag_cloud = None
        else:
            tag_cloud = get_tag_cloud_data(meta['tags'])

        # Create emoji plot

        emoji_graph = create_emoji_graph(section_data['emojis'], video_id)

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
    return render(request, 'errors/400.html', status=400)

# Error 403 view


def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)
# Error 404 view


def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)
# Error 500 view


def error_500(request):
    return render(request, 'errors/500.html', status=500)
