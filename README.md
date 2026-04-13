 AI-Powered Sentiment Analysis Platform (TrendSense)

A comprehensive multi-source sentiment analysis platform that collects, analyzes, and visualizes public opinion from platforms like Twitter, Reddit, YouTube, and News APIs. Built with Python and Streamlit, this tool provides real-time insights, historical trends, and crisis detection using NLP techniques.

1. Features
Multi-Source Data Collection
Twitter (via Nitter scraping)
Reddit discussions
YouTube comments
News articles (NewsAPI)
Sentiment Analysis
VADER-based sentiment scoring
Classifies text into Positive, Negative, Neutral
2. Interactive Dashboard
Real-time sentiment visualization
Historical trend analysis
Plotly-powered charts
 Word Cloud Generation
Highlights frequently used keywords
Crisis Detection
Detects spikes in negative sentiment
3. Tech Stack
Frontend: Streamlit
Backend: Python
Visualization: Plotly, Matplotlib
NLP: NLTK (VADER Sentiment)
APIs & Scraping: NewsAPI, Nitter Scraper, Reddit API
Environment: Virtual Environment (.venv)


4. Project Structure
sentiment-analysis-platform/
│
├── Home.py                  # Main Streamlit app entry point
├── analysis_utils.py        # Data fetching & sentiment logic
├── requirements.txt         # Project dependencies
├── .env                     # API keys (not uploaded to GitHub)
├── .gitignore               # Ignore unnecessary files
│
├── pages/                   # Multi-page Streamlit app
│   ├── Sentiment_Search.py
│   ├── Historical_Trends.py
│   └── Crisis_Alerts.py
│
├── .streamlit/
│   └── config.toml          # Streamlit configuration
│
├── venv/ or .venv/          # Virtual environment (ignored)
├── __pycache__/             # Python cache (ignored)


⚙️ Installation & Setup
1️ Clone the repository
git clone https://github.com/priyalrajpurohit/Sentimental_Analysis/tree/main
cd sentiment-analysis-platform
2️ Create virtual environment
python -m venv .venv
3️ Activate environment
Windows:
.\.venv\Scripts\Activate
Mac/Linux:
source .venv/bin/activate
4️ Install dependencies
pip install -r requirements.txt
5️ Run the app
python -m streamlit run Home.py
 API Keys Required
NewsAPI
Get API key: https://newsapi.org/
(Optional) Reddit / YouTube APIs if extended
Store keys in a .env file:
NEWS_API_KEY=your_api_key_here
Use Cases
Brand reputation monitoring
Social media sentiment tracking
Crisis detection systems
Market research & public opinion analysis
 Limitations
Nitter-based Twitter scraping may be unstable
External APIs may have rate limits
Requires internet connection for data fetching
Author
Developed as an AI/ML project for real-time sentiment intelligence and analytics.
Contributing
Contributions are welcome! Feel free to fork the repo and submit a pull request.

📜License
This project is for educational and research purposes.
