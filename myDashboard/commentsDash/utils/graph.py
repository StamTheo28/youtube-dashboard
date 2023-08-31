from __future__ import annotations

from datetime import datetime
from datetime import timedelta

import emoji
import pandas as pd
import plotly.express as px
import plotly.offline as pyo

from .youCom import get_emoji
from .youCom import get_most_frequent_words


def create_emoji_graph(data):
    """
    Creates a bar chart visualization for emoji frequencies using Plotly.

    Args:
        data (dict): A dictionary containing emojis as keys and their corresponding count as values.

    Returns:
        bool: True if the graph is successfully created, False if there are no emojis.
    """
    # If there aren't any emojis, return False
    if len(data) == 0:
        return False
    else:
        emojis = list(data.keys())  # Extract emojis from the dictionary
        counts = list(data.values())  # Extract counts from the dictionary
        # Get emoji names using a function (get_emoji_names)
        emojis_names = get_emoji_names(emojis)
        emojis_dict = {
            'emoji': emojis,
            'count': counts,
            'emoji name': emojis_names,
        }
        df = pd.DataFrame(emojis_dict)  # Create a DataFrame with emoji data
        # Create a bar chart using Plotly Express (px)
        fig = px.bar(
            df,
            x='emoji',
            y='count',
            hover_data=['emoji name'],  # Show emoji names on hover
        )

        # Customize the layout of the chart
        fig.update_layout(
            xaxis_title='Emoji',
            yaxis_title='Count',
            xaxis_tickangle=-45,
            showlegend=False,  # Hide the legend
        )

        # Save the plot as an HTML file
        plot_filename = 'commentsDash/templates/html/emoji_chart.html'
        pyo.plot(fig, filename=plot_filename, auto_open=False)
        return True  # Return True indicating the successful creation of the graph


def get_tag_cloud_data(data):
    """
    Generates a dictionary of video tags and their corresponding counts.

    Args:
        data (list): A list of video tags.

    Returns:
        dict: A dictionary containing video tags as keys and their corresponding counts.
    """
    data_dict = {}
    for tag in data:
        data_dict[tag] = 1  # Assign a count of 1 to each tag
    return data_dict


def get_comment_activity(data):
    """
    Analyzes comment activity over time and returns counts grouped by month, trimester, and year.

    Args:
        data (pd.DataFrame): A DataFrame containing comment data with 'publishedAt' column.

    Returns:
        dict: A dictionary containing comment counts grouped by month, trimester, and year.
    """
    dates = data['publishedAt']
    # Parse the datetimes into datetime objects ('%Y-%m-%dT%H:%M:%SZ')
    datetimes = sorted(
        [datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ') for dt_str in dates],
    )

    # Create dictionaries to store the count of each month, trimester, and year
    month_counts = {}
    trimester_counts = {}
    year_counts = {}

    # Group the datetimes by month, trimester, and year and count occurrences
    for dt in datetimes:
        # Extract the year-month part (e.g., '2009-01')
        month = dt.strftime('%Y-%m')
        # Calculate the trimester based on the month
        trimester = f'{dt.year}-T{((dt.month-1) // 4) + 1}'
        year = str(dt.year)

        # Initialize counts if not present in dictionaries
        if month not in month_counts:
            month_counts[month] = 0
        if trimester not in trimester_counts:
            trimester_counts[trimester] = 0
        if year not in year_counts:
            year_counts[year] = 0

        # Increment counts for each time period
        month_counts[month] += 1
        trimester_counts[trimester] += 1
        year_counts[year] += 1

    # Step 2: Check for missing months, trimesters, and years and add them with a count of 0
    start_date = min(datetimes).replace(day=1)
    end_date = max(datetimes).replace(day=28) + timedelta(days=4)

    current_date = start_date
    while current_date <= end_date:
        month = current_date.strftime('%Y-%m')
        trimester = f'{current_date.year}-T{((current_date.month-1) // 4) + 1}'
        year = str(current_date.year)

        if month not in month_counts:
            month_counts[month] = 0
        if trimester not in trimester_counts:
            trimester_counts[trimester] = 0
        if year not in year_counts:
            year_counts[year] = 0

        current_date += timedelta(days=32)  # Move to the next month

    # Check if there are only two dates in the month, semester, or year dictionaries
    if len(month_counts) <= 2:
        prev_date = min(datetimes) - timedelta(days=32)
        month_counts[prev_date.strftime('%Y-%m')] = 0

    if len(trimester_counts) <= 2:
        prev_date = min(datetimes) - timedelta(days=140)
        trimester_counts[prev_date.strftime('%Y-T1')] = 0

    if len(year_counts) <= 2:
        prev_date = min(datetimes) - timedelta(days=365)
        year_counts[str(prev_date.year)] = 0

    # Sort the dictionaries by keys to have the data in chronological order
    month_counts = dict(sorted(month_counts.items()))
    trimester_counts = dict(sorted(trimester_counts.items()))
    year_counts = dict(sorted(year_counts.items()))

    return {
        'month': month_counts,
        'semester': trimester_counts,
        'year': year_counts,
    }


def get_graph_data(data):
    """
    Processes a DataFrame containing comment data into a format suitable for graph plotting.

    Args:
        data (pd.DataFrame): A DataFrame containing comment data.

    Returns:
        dict: A dictionary containing data for various types of graphs.
    """
    # Sentiment Percentages (for Pie Chart)
    sentiment_data = {}
    percentages = data['sentiment'].value_counts() / len(data) * 100
    sentiment_data['positive'] = percentages['positive']
    sentiment_data['neutral'] = percentages['neutral']
    sentiment_data['negative'] = percentages['negative']

    # Comments Length (for Histogram)
    comment_length = data['word_length'].to_list()

    # Top K most used words (for Bar Chart)
    most_frequent_words = get_most_frequent_words(data)

    # Top K most used emojis (for horizontal Bar chart)
    emoji_counts = get_emoji(data)

    # Number of most famous comments per month (for Scatter plot)
    month_count = get_comment_activity(data)

    graph_dict = {
        'length': comment_length,
        'frequency': most_frequent_words,
        'emojis': emoji_counts,
        'activity': month_count,
        'sentiment': sentiment_data,
    }
    return graph_dict


def get_emoji_names(emojis):
    """
    Retrieve the text name of each emoji.

    Args:
        data (list): A list of emojis.

    Returns:
        list: A list contianing the text name of each emoji.
    """
    emoji_names = []
    for e in emojis:
        emoji_names.append(emoji.demojize(e).replace(':', ''))
    return emoji_names
