import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from analysis_utils import fetch_twitter_data, fetch_reddit_data, fetch_youtube_comments, fetch_news_data, get_ai_summary, analyze_data

st.set_page_config(page_title="Sentiment Search", page_icon="🔎", layout="wide")

# --- CUSTOM CSS FOR HUGE FONTS ON THIS PAGE ---
st.markdown("""
<style>
    /* Main Titles & Headers */
    h1 { font-size: 3.8rem !important; }
    h2 { font-size: 3.0rem !important; }
    h3 { font-size: 2.2rem !important; }
    
    /* Regular Text */
    p, li, .stMarkdown { font-size: 1.4rem !important; line-height: 1.8 !important;}
    
    /* Metrics (The Big Numbers and Labels like 40.0%) */
    [data-testid="stMetricValue"] { font-size: 4.5rem !important; }
    [data-testid="stMetricLabel"] { font-size: 1.8rem !important; }
    
    /* Big Tabs (Twitter, Reddit, etc.) */
    button[data-baseweb="tab"] { 
        font-size: 24px !important; 
        font-weight: bold !important; 
        margin: 0 15px !important; 
    }
</style>
""", unsafe_allow_html=True)

st.title("🔎 Multi-Source Sentiment Analyzer")

# 5 TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🐦 Twitter", "🔴 Reddit", "▶️ YouTube", "📰 News", "✍️ Custom"])

def show_results(results, key):
    if not results:
        st.warning("No data found.")
        return

    df = pd.DataFrame(results)
    st.session_state[f'data_{key}'] = df
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    total = len(df)
    pos = len(df[df['sentiment']=='Positive'])
    neg = len(df[df['sentiment']=='Negative'])
    neu = len(df[df['sentiment']=='Neutral'])
    
    c1.metric("Total", total)
    c2.metric("Positive", f"{(pos/total)*100:.1f}%")
    c3.metric("Negative", f"{(neg/total)*100:.1f}%")
    c4.metric("Neutral", f"{(neu/total)*100:.1f}%")
    
    st.divider()
    
    # AI Summary
    st.subheader("✨ AI Smart Summary")
    if st.button("Generate AI Insights", key=f"ai_{key}"):
        with st.spinner("Analyzing..."):
            s = get_ai_summary(df['text'].tolist())
            st.success("Done!")
            st.markdown(s)
            
    st.divider()
    
    # Charts
    cl1, cl2 = st.columns(2)
    with cl1:
        if not df.empty:
            fig = px.pie(names=df['sentiment'].value_counts().index, values=df['sentiment'].value_counts().values, title="Sentiment Distribution")
            fig.update_layout(font=dict(size=18), title_font=dict(size=26)) 
            st.plotly_chart(fig, use_container_width=True)
    with cl2:
        st.subheader("Word Cloud")
        text = " ".join(df['text'].astype(str))
        if text.strip():
            wc = WordCloud(width=800, height=400).generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
    st.dataframe(df)

# --- TAB LOGIC ---
with tab1:
    st.header("Analyze Twitter")
    q = st.text_input("Topic", key="tw_q")
    if st.button("Analyze Twitter"):
        with st.spinner("Fetching..."):
            res = fetch_twitter_data(q)
            show_results(res, "twitter")

with tab2:
    st.header("Analyze Reddit")
    q = st.text_input("Topic", key="rd_q")
    if st.button("Analyze Reddit"):
        with st.spinner("Fetching..."):
            res = fetch_reddit_data(q)
            show_results(res, "reddit")

with tab3:
    st.header("Analyze YouTube")
    url = st.text_input("Video URL")
    if st.button("Analyze YouTube"):
        with st.spinner("Fetching..."):
            res = fetch_youtube_comments(url)
            show_results(res, "youtube")

with tab4:
    st.header("Analyze News")
    q = st.text_input("Topic", key="nw_q")
    if st.button("Analyze News"):
        with st.spinner("Fetching..."):
            res = fetch_news_data(q)
            show_results(res, "news")

with tab5:
    st.header("Custom Text")
    txt = st.text_area("Paste text")
    if st.button("Analyze Text"):
        if txt:
            sentences = [s.strip() for s in txt.split('.') if s]
            res = analyze_data(sentences, "Custom")
            show_results(res, "custom")
        else:
            st.warning("Enter text first.")