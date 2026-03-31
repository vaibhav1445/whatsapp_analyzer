import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import preprocessor
import helper

# ── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="WhatsApp Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg:        #0d0d0d;
    --surface:   #161616;
    --surface2:  #1f1f1f;
    --border:    #2a2a2a;
    --accent:    #00e5a0;
    --accent2:   #7c3aed;
    --text:      #f0f0f0;
    --muted:     #888888;
    --danger:    #ff4d6d;
    --warn:      #ffb347;
}

/* ── BASE ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── HEADINGS ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

h1 { 
    font-size: 2.2rem !important; 
    font-weight: 800 !important;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem !important;
}

h2 { 
    font-size: 1.4rem !important; 
    font-weight: 600 !important;
    color: var(--text) !important;
}

h3 { 
    font-size: 1.1rem !important; 
    font-weight: 600 !important;
    color: var(--muted) !important;
}

/* ── METRIC CARDS ── */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    transition: border-color 0.2s ease, transform 0.2s ease !important;
}

[data-testid="metric-container"]:hover {
    border-color: var(--accent) !important;
    transform: translateY(-2px) !important;
}

[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* ── BUTTONS ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent), #00c483) !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0, 229, 160, 0.3) !important;
}

/* ── SIDEBAR BUTTON ── */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent2), #9f67ff) !important;
    color: white !important;
    margin-top: 12px !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    box-shadow: 0 8px 24px rgba(124, 58, 237, 0.4) !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    transition: border-color 0.2s !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── DIVIDER ── */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0 !important;
}

/* ── PLOTS ── */
[data-testid="stImage"], .stPlotlyChart {
    border-radius: 16px !important;
    overflow: hidden !important;
}

/* ── CAPTION ── */
[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] {
    color: var(--accent) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

</style>
""", unsafe_allow_html=True)

# ── MATPLOTLIB DARK THEME ──────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor':  '#161616',
    'axes.facecolor':    '#161616',
    'axes.edgecolor':    '#2a2a2a',
    'axes.labelcolor':   '#888888',
    'text.color':        '#f0f0f0',
    'xtick.color':       '#888888',
    'ytick.color':       '#888888',
    'grid.color':        '#2a2a2a',
    'grid.linestyle':    '--',
    'grid.alpha':        0.5,
    'figure.autolayout': True,
})

# Sidebar
st.sidebar.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("📁 Choose a WhatsApp chat file in TXT format")

# Initialize session state
if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False
if "summary_result" not in st.session_state:
    st.session_state.summary_result = None
if "selected_user" not in st.session_state:
    st.session_state.selected_user = "Overall"
if "df" not in st.session_state:
    st.session_state.df = None

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    if df.empty or 'user' not in df.columns:
        st.error("⚠️ Could not read this chat file. Please upload a valid WhatsApp chat export (.txt)")
        st.stop()

    # Store df in session state
    st.session_state.df = df

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("👤 Show analysis with respect to", user_list)
    st.session_state.selected_user = selected_user

    if st.sidebar.button("📈 Show Analysis"):
        st.session_state.show_analysis = True
        st.session_state.summary_result = None  # Reset summary on new analysis

if st.session_state.show_analysis and st.session_state.df is not None:
    df = st.session_state.df
    selected_user = st.session_state.selected_user

    # Hero Banner
    st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #161616, #1f1f1f);
            border: 1px solid #2a2a2a;
            border-radius: 20px;
            padding: 32px 40px;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
        '>
            <div style='
                position: absolute; top: 0; right: 0;
                width: 300px; height: 300px;
                background: radial-gradient(circle, rgba(0,229,160,0.08) 0%, transparent 70%);
                pointer-events: none;
            '></div>
            <p style='color:#888; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.15em; margin:0 0 8px 0;'>ANALYSIS REPORT</p>
            <h1 style='margin:0 0 8px 0; font-size:2.5rem;'>💬 WhatsApp Insights</h1>
            <p style='color:#888; margin:0; font-size:0.95rem;'>
                Analyzing chat for <strong style='color:#00e5a0;'>{selected_user}</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

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

    if df_wc is not None:
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Not enough words to generate a Word Cloud for this user.")

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
        if not emoji_df.empty:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%", colors=sns.color_palette("pastel"))
            st.pyplot(fig)
        else:
            st.warning("⚠️ No emojis found.")

    st.markdown("---")
    st.title("🗓️ Weekly Activity Heatmap")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap, cmap='YlOrBr')
    st.pyplot(fig)

    st.markdown("---")
    st.title("💞 Relationship Health Score")
    health_score, insights = helper.relationship_health_score(df)

    if health_score >= 75:
        color = "green"
        label = "Healthy 💚"
    elif health_score >= 50:
        color = "orange"
        label = "Moderate 🧡"
    else:
        color = "red"
        label = "Needs Attention ❤️"

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div style='
                text-align:center;
                padding: 32px 20px;
                border-radius: 20px;
                background: linear-gradient(135deg, #161616, #1f1f1f);
                border: 1px solid {color};
                box-shadow: 0 0 40px rgba(0,0,0,0.4);
            '>
                <p style='color:#888; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.15em; margin:0 0 8px 0;'>HEALTH SCORE</p>
                <h1 style='color:{color}; font-size: 5rem; margin: 0; font-family: Syne, sans-serif;'>{health_score}</h1>
                <p style='color:#888; margin: 4px 0 12px 0; font-size:0.9rem;'>out of 100</p>
                <div style='
                    background: #2a2a2a;
                    border-radius: 999px;
                    height: 8px;
                    margin: 0 auto;
                    width: 80%;
                    overflow: hidden;
                '>
                    <div style='
                        background: {color};
                        height: 100%;
                        width: {health_score}%;
                        border-radius: 999px;
                        transition: width 1s ease;
                    '></div>
                </div>
                <h3 style='color:{color}; margin: 16px 0 0 0; font-size:1.1rem;'>{label}</h3>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("📋 Insights")
        for insight in insights:
            st.write(insight)

    st.markdown("---")
    st.title("🤖 AI Chat Summary")
    st.caption("Powered by Groq AI")

    if st.button("✨ Generate AI Summary"):
        with st.spinner("🤖 AI is analyzing your chat..."):
            st.session_state.summary_result = helper.chat_summary_ai(selected_user, df)

    if st.session_state.summary_result is not None:
        st.success("✅ Summary Ready!")
        st.markdown(st.session_state.summary_result)