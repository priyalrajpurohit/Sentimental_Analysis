import streamlit as st

# --- 1. SET UP THE PAGE ---
st.set_page_config(
    page_title="TrendSense | AI Sentiment Platform",
    page_icon="📊",
    layout="wide"
)

# --- 2. CUSTOM CSS (UPDATED FOR HUGE FONTS) ---
st.markdown("""
<style>
    /* GLOBAL FONT SIZE OVERRIDES */
    h1 { font-size: 3.8rem !important; }
    h2 { font-size: 3.0rem !important; }
    h3 { font-size: 2.2rem !important; }
    p, li, .stMarkdown { font-size: 1.4rem !important; line-height: 1.8 !important; }
    
    /* 1. FORCE BOXES TO BE SAME HEIGHT */
    div[data-testid="column"] {
        background-color: transparent;
    }
    
    /* 2. STYLE THE CARDS */
    div.css-card {
        background-color: white;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 0px; 
        height: 100%;
        min-height: 580px; /* Increased to fit larger text */
        display: flex;
        flex-direction: column;
        overflow: hidden; 
    }
    
    /* 3. TEXT CONTENT PADDING */
    div.card-content {
        padding: 25px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    /* 4. BUTTON STYLING (Bigger Buttons) */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.3rem !important; /* Larger Button Text */
        padding: 0.8rem !important;
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        color: #31333F;
    }
    div.stButton > button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
    }

    /* 5. HERO IMAGE Styling */
    div[data-testid="stImage"] img {
        border-radius: 12px;
    }
    
    /* 6. GENERAL PADDING */
    .block-container { padding-top: 2rem; }

</style>
""", unsafe_allow_html=True)

# --- 3. TOP NAVIGATION ---
col_logo, col_spacer, col_signin = st.columns([2, 5, 1.5])
with col_logo:
    st.markdown("### 📊 *TrendSense*")
with col_signin:
    with st.popover("Sign In 👤", use_container_width=True):
        st.markdown("*Account*")
        if st.button("Consumer Intelligence", key="nav_c", use_container_width=True):
            st.switch_page("pages/1_🔎_Sentiment_Search.py")
        if st.button("Social Media Management", key="nav_s", use_container_width=True):
            st.warning("Access Restricted (Demo)")
        st.divider()
        if st.button("Log Out", key="nav_l", type="primary", use_container_width=True):
            st.rerun()

st.divider()

# --- 4. HERO SECTION ---
hero_col1, hero_col2 = st.columns([2, 3], gap="large")
with hero_col1:
    st.title("Social Suite")
    st.markdown("### Leverage pioneering AI analytics to make better decisions.")
    st.write("Understand your audience, track historical trends, and prevent crises before they happen.")
    st.write("")
    c1, c2 = st.columns([1, 1.5])
    with c1:
        if st.button("Get started ➡", type="primary"):
            st.switch_page("pages/1_🔎_Sentiment_Search.py")
    with c2:
        st.button("Explore plans")

with hero_col2:
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop", use_container_width=True)

st.write("---")

# --- 5. SOLUTIONS CARDS (HTML/CSS IMPLEMENTATION) ---
st.subheader("Our Solutions")

col1, col2 = st.columns(2, gap="medium")

# Define the HTML Card Template (UPDATED WITH LARGER INLINE FONTS)
def create_card(image_url, title, desc, key):
    return f"""
    <div class="css-card">
        <img src="{image_url}" style="width:100%; height:250px; object-fit:cover;">
        <div class="card-content">
            <div>
                <h3 style="margin-top:0; font-size:2.0rem;">{title}</h3>
                <p style="color:#555; font-size:1.3rem; line-height: 1.6;">{desc}</p>
            </div>
        </div>
    </div>
    """

# --- CARD 1 ---
with col1:
    st.markdown(create_card(
        "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?q=80&w=1932&auto=format&fit=crop",
        "Consumer Intelligence",
        "Understand your consumers, your brand, and your market with instant AI analysis.",
        "card1"
    ), unsafe_allow_html=True)
    
    st.write("")
    if st.button("Explore Search ➡", key="b1"):
        st.switch_page("pages/1_🔎_Sentiment_Search.py")

# --- CARD 2 ---
with col2:
    st.markdown(create_card(
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2015&auto=format&fit=crop",
        "Market Trends",
        "Track sentiment changes over weeks or months to see brand perception growth.",
        "card2"
    ), unsafe_allow_html=True)
    
    st.write("")
    if st.button("View Trends ➡", key="b2"):
        st.switch_page("pages/3_📈_Historical_Trends.py")


# --- 6. ABOUT US & FOOTER (UPDATED FONTS) ---
st.markdown("""
<style>
.about-title {
    color: #111827;
    font-size: 2.8rem;
    margin: 2rem 0 1.5rem 0;
    font-weight: 700;
    text-align: left;
    padding-left: 1rem;
}
.about-column h3 {
    color: #111827;
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    font-weight: 600;
}
.about-links {
    list-style: none;
    padding: 0;
    margin: 0;
}
.about-links li {
    margin-bottom: 1.0rem;
}
.about-links a {
    color: #4b5563;
    text-decoration: none;
    font-size: 1.3rem;
    transition: color 0.2s;
}
.about-links a:hover {
    color: #111827;
    text-decoration: underline;
}
.footer {
    background-color: #f8f9fa;
    padding: 2rem 2rem 2rem;
    border-top: 1px solid #e5e7eb;
    margin-top: 2rem;
}
.footer-container {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
    color: #6b7280;
    font-size: 1.2rem;
}
</style>
""", unsafe_allow_html=True)

# About Us Section
st.markdown("<h2 class='about-title'>ABOUT US</h2>", unsafe_allow_html=True)

col1, pad, col2 = st.columns([1, 0.2, 1])

with col1:
    st.markdown("""
    <div class='about-column'>
        <h3>Our Suite</h3>
        <ul class='about-links'>
            <li><a href='#'>Consumer Intelligence</a></li>
            <li><a href='#'>Social Media Management</a></li>
            <li><a href='#'>Influencer Marketing</a></li>
            <li><a href='#'>Social Listening</a></li>
            <li><a href='#'>Analytics</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='about-column'>
        <h3>Resources</h3>
        <ul class='about-links'>
            <li><a href='#'>Blog</a></li>
            <li><a href='#'>Guides</a></li>
            <li><a href='#'>Webinars</a></li>
            <li><a href='#'>Help Center</a></li>
            <li><a href='#'>API Documentation</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer with Copyright
with st.container():
    st.markdown("<footer class='footer'>", unsafe_allow_html=True)
    st.markdown("<div class='footer-container'>© 2025 TrendSense. All rights reserved.</div>", unsafe_allow_html=True)
    st.markdown("</footer>", unsafe_allow_html=True)