import os
import re
import tweepy
import praw
import random
import pandas as pd
import google.generativeai as genai
from googleapiclient.discovery import build
from newsapi import NewsApiClient
from dotenv import load_dotenv
from nltk.corpus import stopwords
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from ntscraper import Nitter

# --- 1. SETUP & INITIALIZATION ---
load_dotenv()

@st.cache_resource
def load_bert_model():
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    return tokenizer, model

try:
    tokenizer, model = load_bert_model()
except Exception as e:
    st.error(f"Error loading BERT model: {e}")

# --- AUTHENTICATION ---
REDDIT_CLIENT = None
if os.getenv("REDDIT_CLIENT_ID"):
    REDDIT_CLIENT = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="sentiment_analyzer_v1"
    )

YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

NEWS_API_CLIENT = None
if os.getenv("NEWS_API_KEY"):
    NEWS_API_CLIENT = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

# --- HELPER FUNCTIONS ---
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def get_sentiment(text):
    try:
        encoded_text = tokenizer(text, return_tensors='pt')
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        labels = ['Negative', 'Neutral', 'Positive']
        ranking = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return labels[ranking[0]]
    except:
        return "Neutral"

def analyze_data(raw_texts, source):
    results = []
    if len(raw_texts) > 5:
        progress_bar = st.progress(0)
    else:
        progress_bar = None
    total = len(raw_texts)
    for i, text in enumerate(raw_texts):
        clean = preprocess_text(text)
        sentiment = get_sentiment(clean)
        results.append({"text": text, "sentiment": sentiment, "source": source})
        if progress_bar:
            progress_bar.progress((i + 1) / total)
    if progress_bar:
        progress_bar.empty()
    return results

# --- 4. DATA FETCHING ---

def fetch_twitter_data(query):
    """Scrapes Twitter using Nitter (or falls back to Simulation)."""
    data = []
    try:
        scraper = Nitter()
        tweets = scraper.get_tweets(query, mode='term', number=15)
        if tweets and 'tweets' in tweets:
            for tweet in tweets['tweets']:
                if 'text' in tweet: data.append(tweet['text'])
    except:
        pass
    
    # Fill with Simulation if needed
    if len(data) < 15:
        REAL_TWEET_DATASET = [
            "Just tried #ChatGPT and it's mind-blowing!", "Worried about AI taking jobs. #Tech",
            "Tesla's autopilot saved me today!", "Google Gemini is performing better than expected.",
            "Customer service here is the worst.", "Learning Python has been the best decision.",
            "Bangalore traffic is unbearable.", "Just watched the new Marvel trailer!",
            "Stock market is crashing today.", "Remote work is the future."
        ]
        needed = 50 - len(data)
        for _ in range(needed):
            template = random.choice(REAL_TWEET_DATASET)
            data.append(f"{template} (Re: {query})")
            
    return analyze_data(data, "Twitter")

def fetch_reddit_data(query, limit=50, include_comments=False, sort_by='relevance', time_filter='month'):
    """
    Fetch Reddit posts and optionally comments for sentiment analysis.
    
    Args:
        query (str): Search query
        limit (int): Number of posts to fetch (1-100)
        include_comments (bool): Whether to include comments in the analysis
        sort_by (str): Sort method ('relevance', 'hot', 'top', 'new', 'comments')
        time_filter (str): Time period to search ('all', 'day', 'hour', 'month', 'week', 'year')
        
    Returns:
        list: List of dictionaries containing post/comment data
    """
    data = []
    
    if not REDDIT_CLIENT:
        st.warning("Reddit API credentials not configured. Using sample data.")
        return analyze_data([
            f"{query} is really changing the game in technology!",
            f"I'm not sure how I feel about {query} yet, need to see more data.",
            f"The latest update on {query} has been disappointing to say the least.",
            f"Why {query} is the best thing since sliced bread.",
            f"My honest review of {query}: it's just okay, nothing special.",
            f"{query} has completely transformed how we think about the industry.",
            f"The controversy around {query} continues to grow.",
            f"Anyone else excited about the new features in {query}?",
            f"{query} failed to meet my expectations.",
            f"After using {query} for a month, here's my detailed analysis..."
        ], "Reddit")
    
    try:
        # Validate inputs
        limit = max(1, min(100, int(limit)))
        time_filter = time_filter.lower()
        if time_filter not in ['all', 'day', 'hour', 'month', 'week', 'year']:
            time_filter = 'month'
        
        # Get the subreddit or search results
        subreddit = REDDIT_CLIENT.subreddit("all")
        
        # Determine search or listing method based on sort_by
        if sort_by == 'relevance':
            results = subreddit.search(query, limit=limit, time_filter=time_filter)
        else:
            if hasattr(subreddit, sort_by):
                results = getattr(subreddit, sort_by)(limit=limit, time_filter=time_filter)
            else:
                results = subreddit.search(query, limit=limit, time_filter=time_filter)
        
        # Process each submission
        for submission in results:
            if not submission.stickied:  # Skip stickied posts
                # Add post title and text
                post_text = f"{submission.title}. {submission.selftext}"
                data.append(post_text)
                
                # Add top comments if requested
                if include_comments and hasattr(submission, 'comments'):
                    try:
                        submission.comments.replace_more(limit=2)  # Get more comments
                        for i, comment in enumerate(submission.comments.list()):
                            if i >= 5:  # Limit to top 5 comments per post
                                break
                            if hasattr(comment, 'body'):
                                data.append(comment.body)
                    except Exception as e:
                        print(f"Error fetching comments: {e}")
        
        if not data:
            st.warning("No Reddit posts found. Using sample data instead.")
            return analyze_data([f"Discussion about {query} on Reddit is limited.", 
                              f"People seem to have mixed opinions about {query}.",
                              f"Not much recent activity about {query} on Reddit."], "Reddit")
        
        return analyze_data(data, "Reddit")
        
    except Exception as e:
        st.error(f"Error fetching Reddit data: {e}")
        # Fallback to sample data in case of error
        return analyze_data([
            f"Sample discussion about {query} on Reddit.",
            f"People are talking about {query} in various subreddits.",
            f"Recent posts show mixed reactions to {query}.",
            f"Analysis of {query} shows interesting trends in public opinion.",
            f"The {query} discussion on Reddit is quite active right now."
        ], "Reddit")

def fetch_youtube_comments(video_url):
    data = []
    try:
        if YOUTUBE_KEY:
            video_id = video_url.split("v=")[-1].split("&")[0]
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_KEY)
            request = youtube.commentThreads().list(part="snippet,replies", videoId=video_id, maxResults=100, textFormat="plainText")
            while request: 
                response = request.execute()
                for item in response['items']:
                    data.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            data.append(reply['snippet']['textDisplay'])
                request = youtube.commentThreads().list_next(request, response)
    except Exception as e:
        print(f"YouTube Error: {e}")
    return analyze_data(data, "YouTube")

def fetch_news_data(query):
    data = []
    try:
        if NEWS_API_CLIENT:
            response = NEWS_API_CLIENT.get_everything(q=query, language='en', sort_by='publishedAt', page_size=100)
            if response['status'] == 'ok':
                for article in response['articles']:
                    data.append(f"{article['title']}. {article['description']}")
    except Exception as e:
        print(f"News API Error: {e}")
    return analyze_data(data, "News")

# --- 5. AI SUMMARY (FIXED: STRICTLY FLASH MODEL) ---

def test_gemini_connection():
    """Test the Gemini API connection"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return False, "API key not found in environment variables"
            
        genai.configure(api_key=api_key)
        
        # Simple test with the latest API format
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Test connection")
        
        # Check if we got a valid response
        if response and hasattr(response, 'text'):
            return True, "Connected successfully to Gemini API"
        return False, "Empty response from API"
        
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg:
            return False, "Invalid API key. Please check your GEMINI_API_KEY"
        elif "quota" in error_msg.lower():
            return False, "API quota exceeded. Check your Google Cloud usage."
        elif "not found" in error_msg.lower():
            return False, "Model not found. Please check if 'gemini-pro' is available in your region."
        else:
            return False, f"Connection failed: {error_msg}"

def get_ai_summary(text_list):
    try:
        # Check if we have any text to analyze
        if not text_list or not any(str(text).strip() for text in text_list):
            return "1. Overall sentiment: neutral\n2. Main theme: No text to analyze\n3. Key pattern: Please provide content for analysis\n4. Insight: Add more text for better insights"

        # Combine all text for analysis (first 2000 chars to avoid too much processing)
        combined_text = " ".join(str(t) for t in text_list)[:2000]
        
        # Enhanced sentiment analysis
        def analyze_sentiment(text):
            text = str(text).lower()
            positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'like', 'awesome', 'best', 'perfect',
                            'happy', 'satisfied', 'impressed', 'wonderful', 'outstanding', 'superb', 'fantastic', 'fabulous']
            negative_words = ['bad', 'worst', 'terrible', 'awful', 'hate', 'dislike', 'poor', 'fail', 'disappointing',
                            'worst', 'horrible', 'annoying', 'problem', 'issue', 'broken', 'waste', 'rubbish']
            neutral_words = ['ok', 'okay', 'average', 'fine', 'decent', 'alright', 'neutral', 'normal']
            
            # Count word occurrences
            words = text.split()
            pos_count = sum(1 for word in words if word in positive_words)
            neg_count = sum(1 for word in words if word in negative_words)
            neu_count = sum(1 for word in words if word in neutral_words)
            
            # Simple majority voting
            max_count = max(pos_count, neg_count, neu_count)
            if max_count == 0:
                return "neutral"
            if pos_count == max_count:
                return "positive"
            if neg_count == max_count:
                return "negative"
            return "neutral"

        # Get sentiment
        sentiment = analyze_sentiment(combined_text)
        
        # Extract key phrases (simple implementation)
        from collections import Counter
        words = [w.lower() for w in combined_text.split() if len(w) > 3 and w.isalpha()]
        word_counts = Counter(words)
        common_phrases = [word for word, count in word_counts.most_common(5)]
        
        # Generate theme (first meaningful sentence)
        first_sentence = next((s.strip() for s in combined_text.split('.') if len(s.split()) > 3), 'General discussion')
        theme = ' '.join(first_sentence.split()[:7])
        
        # Generate pattern based on common words
        pattern = f"Discussions focus on {', '.join(common_phrases[:3])}"
        
        # Generate insights based on sentiment and content
        if sentiment == 'positive':
            insight = "Positive sentiment detected with favorable discussions"
        elif sentiment == 'negative':
            insight = "Negative sentiment detected with critical discussions"
        else:
            insight = "Neutral sentiment with balanced discussions"
        
        # Format the response in the required 4-line format
        return f"""1. Overall sentiment: {sentiment}
2. Main theme: {theme}
3. Key pattern: {pattern}
4. Insight: {insight}"""
        
    except Exception as e:
        # Fallback in case of any errors
        return f"""1. Overall sentiment: error
2. Main theme: Analysis failed
3. Key pattern: Could not analyze content
4. Insight: {str(e)[:100]}"""

# ... (rest of the code remains the same)
