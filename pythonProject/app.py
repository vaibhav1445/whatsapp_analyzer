import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor
import helper

# Sidebar
st.sidebar.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("📁 Choose a WhatsApp chat file")

if uploaded_file is not None:
    # Decode file
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # User selection
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("👤 Show analysis with respect to", user_list)

    # Button to trigger analysis
    if st.sidebar.button("📈 Show Analysis"):


        st.title("✨ Chat Summary")
        st.subheader(f"User: **{selected_user}**")

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_messages)
        with col4:
            st.metric("Links Shared", num_links)


        st.markdown("---")
        st.title("🧠 Sentiment Analysis")
        df_sentiment, sentiment_counts = helper.get_sentiment_analysis(selected_user, df)

        st.subheader("Sentiment Distribution")
        st.bar_chart(sentiment_counts)

        st.subheader("Messages with Sentiment")
        st.dataframe(df_sentiment[['date', 'user', 'message', 'sentiment']])


        st.markdown("---")
        st.title("📆 Timelines")

        # Monthly Timeline
        st.subheader("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.subheader("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='brown')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.markdown("---")
        st.title("📊 Activity Map")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Active Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='skyblue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Most Active Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='lightgreen')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        st.markdown("---")
        st.title("📌 Most Active Users (Group Level Only)")

        if selected_user == "Overall":
            x, new_df = helper.most_busy_user(df)
            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='crimson')
                plt.xticks(rotation='vertical', color='black')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        st.markdown("---")
        st.title("☁️ Word Cloud")
        df_wc = helper.create_wordCloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)


        st.markdown("---")
        st.title("🗣️ Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='teal')
        plt.xticks(color='black')
        st.pyplot(fig)


        st.markdown("---")
        st.title("😄 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%", colors=sns.color_palette("pastel"))
            st.pyplot(fig)


        st.markdown("---")
        st.title("🗓️ Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap='YlOrBr')
        st.pyplot(fig)


