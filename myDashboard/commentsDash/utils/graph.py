from .youCom import get_most_frequent_words, get_emoji, get_comment_activity
import plotly.express as px
import plotly.offline as pyo








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
    emoji_counts =  get_emoji(data)

    # Number of most famous comments per month (Scatter plot)
    month_count = get_comment_activity(data)
    graph_dict = {'length':comment_length,
                  "frequency":most_frequent_words,
                  "emojis":emoji_counts,
                  "activity":month_count,
                  "sentiment":sentiment_data
                  }
    return graph_dict

def get_emoji_graph(data, video_id):

    # Extract emoji and count data
    emojis = list(data.keys())
    counts = list(data.values())

    # Create a bar chart using plotly
    fig = px.bar(
        x=emojis,
        y=counts,
        title="Emoji Counts",
        labels={"x": "Emoji", "y": "Count"},
        text=counts,
    )

    # Customize the layout (optional)
    fig.update_layout(
        xaxis_title="Emoji",
        yaxis_title="Count",
        xaxis_tickangle=-45,
        showlegend=False,
    )


    # Save the plot as an HTML file
    plot_filename = "commentsDash/templates/html/emoji_chart.html"
    pyo.plot(fig, filename=plot_filename, auto_open=False)
    return plot_filename
   

    """
    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    
    # Set emoji labels on the x-axis
    emoji_labels = [emoji.emojize(label) for label in x]
    plt.xticks(x, emoji_labels, rotation='vertical', fontsize=12)
    
    plt.xlabel('X-axis', fontname="Times New Roman")
    plt.ylabel('Y-axis')
    plt.title('Sample Plot')
    """

def get_tag_cloud_data(data):
    data_dict = {}
    for tag in data:
        data_dict[tag] = 1
    return data_dict