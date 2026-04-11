import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Historical Trends", page_icon="📈", layout="wide")

st.title("📈 Historical Sentiment Trends")
st.markdown("Analyze how sentiment for a topic has changed over time.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Analysis Settings")
    topic = st.text_input("Enter Topic to Track", "Artificial Intelligence")
    
    # Date range selection
    end_date = st.date_input("End Date", datetime.now())
    start_date = st.date_input("Start Date", end_date - timedelta(days=30))
    
    if start_date >= end_date:
        st.error("Start date must be before end date.")
    
    # Analysis parameters
    st.markdown("### Analysis Parameters")
    window_size = st.slider("Trend Smoothing Window", min_value=1, max_value=14, value=3)
    
    # Add a button to generate the report
    generate_report = st.button("Generate Trend Report", type="primary")

if generate_report and start_date < end_date:
    with st.spinner("Analyzing historical data..."):
        # Calculate number of days
        days = (end_date - start_date).days + 1
        
        # Generate more realistic time series data with trends and seasonality
        np.random.seed(42)  # For reproducibility
        
        # Base trend (upward, downward, or neutral)
        trend = np.linspace(-0.3, 0.3, days)  # Slight upward trend
        
        # Add some seasonality (weekly pattern)
        day_of_week = np.array([(start_date + timedelta(days=i)).weekday() for i in range(days)])
        seasonality = 0.1 * np.sin(2 * np.pi * day_of_week / 7)
        
        # Add some random noise
        noise = np.random.normal(0, 0.1, days)
        
        # Combine components
        sentiment_scores = 0.5 * trend + seasonality + noise
        
        # Clip to [-1, 1] range
        sentiment_scores = np.clip(sentiment_scores, -0.9, 0.9)
        
        # Generate dates
        dates = [start_date + timedelta(days=i) for i in range(days)]
        
        # Create DataFrame
        df = pd.DataFrame({
            "Date": dates,
            "Sentiment Score": sentiment_scores,
            "Day of Week": day_of_week
        })
        
        # Calculate moving average for trend line
        df['Trend Line'] = df['Sentiment Score'].rolling(window=window_size, min_periods=1).mean()
        
        # --- METRICS ---
        st.subheader(f"📊 Sentiment Analysis for: {topic}")
        
        col1, col2, col3, col4 = st.columns(4)
        avg_sent = df['Sentiment Score'].mean()
        peak_sent = df['Sentiment Score'].max()
        low_sent = df['Sentiment Score'].min()
        volatility = df['Sentiment Score'].std()
        
        # Determine sentiment label and color
        if avg_sent > 0.2:
            sent_label = "😊 Positive"
            delta_color = "normal"
        elif avg_sent < -0.2:
            sent_label = "😞 Negative"
            delta_color = "inverse"
        else:
            sent_label = "😐 Neutral"
            delta_color = "off"
        
        col1.metric("Average Sentiment", f"{avg_sent:.2f}", 
                   delta=sent_label, 
                   delta_color=delta_color)
        
        col2.metric("Peak Sentiment", f"{peak_sent:.2f}", 
                   delta=f"{((peak_sent - avg_sent)/abs(avg_sent)*100 if avg_sent != 0 else 0):.0f}% above avg" if peak_sent > 0 else "")
        
        col3.metric("Lowest Sentiment", f"{low_sent:.2f}", 
                   delta=f"{((low_sent - avg_sent)/abs(avg_sent)*100 if avg_sent != 0 else 0):.0f}% below avg" if low_sent < 0 else "")
        
        col4.metric("Volatility", f"{volatility:.2f}", 
                   "High" if volatility > 0.15 else "Medium" if volatility > 0.08 else "Low")
        
        st.divider()
        
        # --- MAIN CHART ---
        st.subheader("Sentiment Trend Over Time")
        
        # Create figure with secondary y-axis for volume
        fig = go.Figure()
        
        # Add sentiment score as scatter plot
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Sentiment Score'],
            name='Daily Sentiment',
            mode='lines+markers',
            line=dict(color='#636EFA', width=1),
            marker=dict(size=4)
        ))
        
        # Add trend line
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Trend Line'],
            name=f'{window_size}-Day Moving Avg',
            line=dict(color='#FF4B4B', width=3)
        ))
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        # Update layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Sentiment Score (-1 to +1)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            height=500,
            title=f"Sentiment Trend: {topic}"
        )
        
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # --- WEEKLY BREAKDOWN ---
        st.subheader("Weekly Pattern Analysis")
        
        # Group by day of week
        weekly_avg = df.groupby('Day of Week')['Sentiment Score'].mean().reset_index()
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_avg['Day'] = weekly_avg['Day of Week'].map(lambda x: day_names[x])
        
        fig_weekly = px.bar(
            weekly_avg, 
            x='Day', 
            y='Sentiment Score',
            title='Average Sentiment by Day of Week',
            color='Sentiment Score',
            color_continuous_scale='RdYlGn',
            range_color=[-1, 1]
        )
        
        fig_weekly.update_layout(
            xaxis_title="Day of Week",
            yaxis_title="Average Sentiment Score",
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig_weekly, use_container_width=True)
        
        # --- DATA TABLE ---
        st.subheader("Raw Data")
        st.dataframe(df[['Date', 'Sentiment Score', 'Trend Line']].rename(columns={
            'Sentiment Score': 'Score',
            'Trend Line': 'Trend'
        }).style.format({
            'Score': '{:.2f}',
            'Trend': '{:.2f}'
        }), use_container_width=True)
        
        st.success("✅ Historical data analysis complete.")
        
        # Add download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"sentiment_analysis_{topic.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )