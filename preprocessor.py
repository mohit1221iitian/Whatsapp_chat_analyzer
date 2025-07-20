import re
import pandas as pd
def preprocess(data):
    data = data.replace('\u202f', ' ')
    pattern=r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} (?:am|pm) -'
    timestamps = re.findall(pattern, data)
    messages=re.split(pattern, data)[1:]
    df=pd.DataFrame({'user_messages':messages,'date':timestamps})
    df['date']=pd.to_datetime(df['date'],format='%d/%m/%y, %I:%M %p -')
    users=[]
    messages=[]
    for message in df['user_messages']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notificaion')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_messages'],inplace=True)

    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df['date_only']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    df['month_num']=df['date'].dt.month

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else :
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period
    
    return df