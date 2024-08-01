from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns

extractor = URLExtract()


def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    Words = []
    for message in df['message']:
        Words.extend(message.split())

    num_media_messages = df[df['message']== '<Media Omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(Words), num_media_messages, len(links)

def most_buzy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})

    return x,df

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    word = []
    for message in temp['message']:
        for words in message.lower().split():
            if words not in stop_words:
                word.extend(message.split())

    most_common_df = pd.DataFrame(Counter(word).most_common(25))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0)

    return  user_heatmap



