from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()
import pandas as pd
import os
from collections import Counter
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from groq import Groq
import streamlit as st
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def knn_train_and_predict(df, test_size=0.2, k=3):
    df = df[df['user'] != 'group_notification']
    df = df[df['message'].str.strip() != '']

    if df.empty:
        return None, None, None

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['message'])
    y = df['user']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))

    return model, vectorizer, acc


analyzer = SentimentIntensityAnalyzer()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def get_sentiment_analysis(user, df):
    if user != 'Overall':
        df = df[df['user'] == user]

    sentiments = df['message'].apply(lambda msg: analyzer.polarity_scores(msg)['compound'])

    df['sentiment_score'] = sentiments
    df['sentiment'] = df['sentiment_score'].apply(
        lambda x: 'Positive' if x > 0.05 else ('Negative' if x < -0.05 else 'Neutral'))

    sentiment_counts = df['sentiment'].value_counts()
    return df, sentiment_counts

def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100).reset_index().rename(
        columns={'index': 'name', 'count': 'percent'})
    return x, df

def create_wordCloud(selected_user, df):
    f = open(os.path.join(BASE_DIR, 'stop_hinglish.txt'), 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'].str.strip() != '']

    if temp.empty:
        return None

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp = temp.copy()
    temp['message'] = temp['message'].apply(remove_stopwords)
    temp = temp[temp['message'].str.strip() != '']

    # Fallback — use original messages if everything got filtered
    if temp.empty:
        temp = df[df['user'] != 'group_notification']
        temp = temp[temp['message'] != '<Media omitted>\n']
        temp = temp[temp['message'].str.strip() != '']

    if temp.empty:
        return None

    combined_text = " ".join(temp['message'].dropna()).strip()

    if not combined_text:
        return None

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    try:
        df_wc = wc.generate(combined_text)
        return df_wc
    except ValueError:
        return None

def most_common_words(selected_user, df):
    f = open(os.path.join(BASE_DIR, 'stop_hinglish.txt'), 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['day_name'] = df['date'].dt.day_name()
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

def relationship_health_score(df):
    score = 0
    insights = []

    # Remove group notifications and media
    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'].str.strip() != '']

    if df.empty:
        return 0, []

    users = df['user'].unique()

    # 1. CONVERSATION BALANCE (20 points)
    msg_counts = df['user'].value_counts()
    if len(msg_counts) >= 2:
        top2 = msg_counts.head(2)
        ratio = top2.iloc[1] / top2.iloc[0]
        balance_score = round(ratio * 20)
        score += balance_score
        if ratio > 0.7:
            insights.append("✅ Conversation is well balanced between users")
        else:
            insights.append("⚠️ One person dominates the conversation")

    # 2. SENTIMENT SCORE (25 points)
    analyzer = SentimentIntensityAnalyzer()
    df['compound'] = df['message'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
    avg_sentiment = df['compound'].mean()
    sentiment_score = round((avg_sentiment + 1) / 2 * 25)  # normalize -1/+1 to 0/25
    score += sentiment_score
    if avg_sentiment > 0.2:
        insights.append("✅ Overall chat tone is positive and healthy")
    elif avg_sentiment < -0.1:
        insights.append("⚠️ Chat has a lot of negative sentiment")
    else:
        insights.append("😐 Chat tone is mostly neutral")

    # 3. EMOJI USAGE (10 points)
    total_msgs = len(df)
    emoji_msgs = df['message'].apply(lambda x: any(emoji.is_emoji(c) for c in x)).sum()
    emoji_ratio = emoji_msgs / total_msgs if total_msgs > 0 else 0
    emoji_score = min(round(emoji_ratio * 50), 10)
    score += emoji_score
    if emoji_ratio > 0.2:
        insights.append("✅ Good emoji usage — shows emotional expression")
    else:
        insights.append("💬 Low emoji usage — chat is more text focused")

    # 4. RESPONSE CONSISTENCY (25 points)
    df = df.sort_values('date')
    df['prev_user'] = df['user'].shift(1)
    df['prev_time'] = df['date'].shift(1)
    df['response_time'] = (df['date'] - df['prev_time']).dt.total_seconds() / 60  # in minutes
    replies = df[df['user'] != df['prev_user']]
    avg_response = replies['response_time'].median()
    if avg_response < 5:
        response_score = 25
        insights.append("✅ Very fast reply time — both users are highly engaged")
    elif avg_response < 30:
        response_score = 20
        insights.append("✅ Good reply time — healthy engagement")
    elif avg_response < 120:
        response_score = 12
        insights.append("😐 Average reply time is a bit slow")
    else:
        response_score = 5
        insights.append("⚠️ Very slow reply time — low engagement")
    score += response_score

    # 5. CONVERSATION INITIATIONS (20 points)
    df['time_gap'] = (df['date'] - df['date'].shift(1)).dt.total_seconds() / 3600
    new_convos = df[df['time_gap'] > 4]  # new conversation if gap > 4 hours
    if len(new_convos) > 0:
        init_counts = new_convos['user'].value_counts()
        if len(init_counts) >= 2:
            init_ratio = init_counts.iloc[1] / init_counts.iloc[0]
            init_score = round(init_ratio * 20)
            score += init_score
            if init_ratio > 0.6:
                insights.append("✅ Both users initiate conversations equally")
            else:
                insights.append("⚠️ One person initiates most conversations")
        else:
            score += 10
            insights.append("⚠️ Only one person initiates conversations")

    score = min(score, 100)  # cap at 100

    return score, insights

def chat_summary_ai(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'].str.strip() != '']

    if df.empty:
        return "Not enough messages to summarize."

    recent_msgs = df.tail(200)

    chat_text = "\n".join(
        f"{row['user']}: {row['message'].strip()}"
        for _, row in recent_msgs.iterrows()
    )

    try:
        from groq import Groq
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert chat analyzer. Analyze WhatsApp chats and give clear concise insights."
                },
                {
                    "role": "user",
                    "content": f"""Analyze this WhatsApp chat and provide:
1. 📝 Short summary of what was discussed (3-5 lines)
2. 🔑 Key topics talked about (bullet points)
3. 😊 Overall mood of the conversation
4. 💡 One interesting insight about the chat

Chat:
{chat_text}"""
                }
            ],
            max_tokens=1024,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"
