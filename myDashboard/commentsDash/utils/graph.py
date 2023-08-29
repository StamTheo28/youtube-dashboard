from __future__ import annotations

import emoji
import pandas as pd
import plotly.express as px
import plotly.offline as pyo

from .youCom import get_comment_activity
from .youCom import get_emoji
from .youCom import get_most_frequent_words


def get_graph_data(data):
    # Sentiment Percentages (Pie Chart)
    sentiment_data = {}
    percentages = data['sentiment'].value_counts()/len(data)*100
    sentiment_data['positive'] = percentages['positive']
    sentiment_data['neutral'] = percentages['neutral']
    sentiment_data['negative'] = percentages['negative']

    # Comments Length (Histogram)
    comment_length = data['word_length'].to_list()

    # Top K most used words (Bar Chart)
    most_frequent_words = get_most_frequent_words(data)

    # Top K most used emojis (horizontal Bar chart)
    emoji_counts = get_emoji(data)

    # Number of most famous comments per month (Scatter plot)
    month_count = get_comment_activity(data)
    graph_dict = {
        'length': comment_length,
        'frequency': most_frequent_words,
        'emojis': emoji_counts,
        'activity': month_count,
        'sentiment': sentiment_data,
    }
    return graph_dict

# Function to get emoji names


def get_emoji_names(emojis):
    emoji_names = []
    for e in emojis:
        emoji_names.append(emoji.demojize(e).replace(':', ''))
    return emoji_names

# Function to create an emoji count bar chart


def create_emoji_graph(data, video_id):
    if len(data) == 0:
        return False
    else:
        # Extract emoji and count data

        emojis = list(data.keys())
        counts = list(data.values())
        emojis_names = get_emoji_names(emojis)
        emojis_dict = {
            'emoji': emojis,
            'count': counts,
            'emoji name': emojis_names,
        }
        df = pd.DataFrame(emojis_dict)
        # Create a bar chart using plotly
        fig = px.bar(
            df,
            x='emoji',
            y='count',
            hover_data=['emoji name'],
        )

        # Customize the layout (optional)
        fig.update_layout(
            xaxis_title='Emoji',
            yaxis_title='Count',
            xaxis_tickangle=-45,
            showlegend=False,
        )

        # Save the plot as an HTML file
        plot_filename = 'commentsDash/templates/html/emoji_chart.html'
        pyo.plot(fig, filename=plot_filename, auto_open=False)
        return True


def get_tag_cloud_data(data):
    data_dict = {}
    for tag in data:
        data_dict[tag] = 1
    return data_dict
