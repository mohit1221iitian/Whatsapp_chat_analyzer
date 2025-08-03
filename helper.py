from urlextract import URLExtract
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from wordcloud import WordCloud 
from collections import Counter
import emoji
import seaborn as sns

extractor=URLExtract()

def fetch_stats(user,df):

    if user!='Overall':
        df = df[df['user'] == user]

    num_messages=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())   

    # fetch number of media messages
    media_message=df[df['message']=='<Media omitted>\n'].shape[0]
    
    y=[]
    for message in df['message']:
        y.extend(extractor.find_urls(message))    

    return num_messages,len(words),media_message,len(y)

def busy(df):
    
    temp=df[df['user'] != 'group_notificaion']
    x = temp['user'].value_counts().head()
    df1 = pd.DataFrame({
        'name': temp['user'].value_counts().index,
        'percentage': np.round((temp['user'].value_counts().values / temp.shape[0]) * 100, 2)
    })

    return x,df1

def create_wordcloud(user,df):
    if user!='Overall':
        df = df[df['user'] == user]

    temp=df[df['user'] != 'group_notificaion']
    temp=temp[temp['message'] != '<Media omitted>\n']
    f=open('hinglish_stopword.txt','r')
    stop_words=f.read()

    def remove(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(user,df):
    if user!='Overall':
        df = df[df['user'] == user]
    temp=df[df['user'] != 'group_notificaion']
    temp=temp[temp['message'] != '<Media omitted>\n']
    f=open('hinglish_stopword.txt','r')
    stop_words=f.read()

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    from collections import Counter
    most_df=pd.DataFrame(Counter(words).most_common(25))

    return most_df

def emoji_extract(user,df):
    if user!='Overall':
        df = df[df['user'] == user]
    
    emoji1=[]
    for message in df['message']:
        emoji1.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    from collections import Counter
    emoji_df=pd.DataFrame(Counter(emoji1).most_common())
    emoji_df.columns = ['Emoji', 'Count']
    return emoji_df

def timeline_monthly(user,df):
    if user!='Overall':
        df = df[df['user'] == user]
   
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time

    return timeline

def timeline_daily(user,df):
    if user!='Overall':
        df = df[df['user'] == user]

    timeline=df.groupby(['date_only']).count()['message'].reset_index()
    
    return timeline

def month_activity_map(user,df):
    if user!='Overall':
        df = df[df['user'] == user]

    timeline=df.groupby(['month']).count()['message'].reset_index()

    return timeline

def week_activity_map(user,df):
    if user!='Overall':
        df = df[df['user'] == user]
    
    timeline=df.groupby(['day_name']).count()['message'].reset_index()

    return timeline

def activity_heatmap(user,df):
    if user!='Overall':
        df = df[df['user'] == user]

    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap