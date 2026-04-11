import streamlit as st
import pandas as pd
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="Crisis Alerts", page_icon="🚨", layout="wide")

st.title("🚨 Real-Time Crisis Monitoring")
st.markdown("Live feed of potential PR crises and negative sentiment spikes.")

# --- SIMULATE ACTIVE ALERTS ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Alert Feed")
    
    # Fake data for the demo
    alerts = [
        {"time": "2 mins ago", "status": "CRITICAL", "msg": "Spike in negative mentions detected for keyword 'Scam'", "sentiment": -0.85},
        {"time": "15 mins ago", "status": "WARNING", "msg": "Unusual volume of retweets from verified accounts.", "sentiment": -0.42},
        {"time": "1 hour ago", "status": "RESOLVED", "msg": "Server outage complaints have subsided.", "sentiment": 0.15},
    ]

    for alert in alerts:
        # Determine color based on status
        if alert["status"] == "CRITICAL":
            border_color = "red"
            icon = "🔴"
        elif alert["status"] == "WARNING":
            border_color = "orange"
            icon = "pV"
        else:
            border_color = "green"
            icon = "🟢"

        with st.container(border=True):
            c1, c2 = st.columns([0.1, 0.9])
            with c1:
                st.write(f"## {icon}")
            with c2:
                st.markdown(f"**{alert['status']}** | {alert['time']}")
                st.write(alert['msg'])
                st.caption(f"Sentiment Score: {alert['sentiment']}")

with col2:
    st.subheader("System Status")
    st.metric("Current Risk Level", "LOW", delta="- High Risk yesterday", delta_color="inverse")
    st.metric("Active Monitored Topics", "12")
    
    st.write("### Alert Thresholds")
    st.slider("Negative Sentiment Trigger", -1.0, 0.0, -0.6)
    st.slider("Volume Spike Trigger (Tweets/min)", 0, 1000, 200)
    
    st.button("Update Thresholds", type="primary")

st.info("ℹ️ Note: This module is running in 'Simulation Mode' for the demo.")