from .youCom import get_most_frequent_words, get_emoji


def get_sentiment_pie_data(data):
    result = {}
    percentages = data['sentiment'].value_counts()/len(data)*100
    # Maintain order
    result['positive'] = percentages['positive']
    result['neutral'] = percentages['neutral']
    result['negative'] = percentages['negative']
    return result


def get_graph_data(data):
    comment_length = data['word_length'].to_list()
    most_frequent_words = get_most_frequent_words(data)
    emoji_counts =  get_emoji(data)
    graph_dict = {'length':comment_length,
                  "frequency":most_frequent_words,
                  "emojis":emoji_counts}

    return graph_dict