import streamlit as st
import preprocessor
import helper 
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    user_list=df['user'].unique().tolist()
    user_list.remove('group_notificaion')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Show Analysis"):
        
        #stats
        num_messages,words,media_messages,links=helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Messages")
            st.title(media_messages)
        with col4:
            st.header("Total Links Messages")
            st.title(links)

        # Monthly timeline
        st.title('Monthly Timeline')
        timeline=helper.timeline_monthly(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title('Daily Timeline')
        timelined=helper.timeline_daily(selected_user,df)
        fig,ax=plt.subplots(figsize=(18,10))
        ax.plot(timelined['date_only'],timelined['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        col1,col2=st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day['day_name'],busy_day['message'],color="#F5CB4C")
            plt.xticks(rotation='vertical')
            st.pyplot(fig) 
        with col2:
            st.header('Most Busy Month')
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month['month'],busy_month['message'],color="#F5CB4C")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)   

        # heatmap
        st.title('Weekly Heatmap')
        user_heatmap = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots(figsize=(10, 6)) 
        sns.heatmap(user_heatmap, ax=ax, cmap='Greens')  
        st.pyplot(fig)  

        # finding the busiest users in the group(Group level)
        if selected_user=='Overall':
            st.title('Most Busy Users')
            x,d=helper.busy(df)
            fig,ax=plt.subplots()
        
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color="#4CDEF5")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(d)
        
        #WordCloud
        st.title('WordCloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most Common Words')
        most=helper.most_common_words(selected_user,df)

        flg,ax=plt.subplots()
        ax.barh(most[0],most[1],color="#F5A94C")
        plt.xticks(rotation='vertical')
        st.pyplot(flg)
        # st.dataframe(most)

        #emojis
        st.title('Emojis Analysis')
        df_emojis=helper.emoji_extract(selected_user,df)
        
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(df_emojis)
        with col2:
            fig,ax=plt.subplots()
            emoji_font = fm.FontProperties(fname="C:\\Windows\\Fonts\\seguiemj.ttf")

            wedges,texts,autotexts=ax.pie(df_emojis['Count'],labels=df_emojis['Emoji'],autopct="%0.2f")
            for text in texts:
                text.set_fontproperties(emoji_font)
            
            # ax.bar(df_emojis['Emoji'].head(),df_emojis['Count'].head())

            st.pyplot(fig)

        
