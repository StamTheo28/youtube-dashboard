from .youCom import get_most_frequent_words, get_emoji, get_comment_activity



def get_graph_data(data):
    # Sentiment Percentages (Pie Chart)
    print(data)
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

def get_tag_cloud_data(data):
    data_dict = {}
    for tag in data:
        data_dict[tag] = 1
    return data_dict