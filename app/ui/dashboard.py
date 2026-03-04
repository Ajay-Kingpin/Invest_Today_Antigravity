import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
from app.api.routes import AnalysisResponse
from app.tools.market_data import MarketDataTool

st.set_page_config(page_title="Invest Today", page_icon="📈", layout="wide")

# Groww Style Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background-color: #f9fbfb;
    }
    
    /* Primary Color & Buttons */
    .stButton>button {
        background-color: #00D09C !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #00b386 !important;
        box-shadow: 0 4px 12px rgba(0, 208, 156, 0.3);
    }
    
    /* Cards Concept */
    div.stMetric, div[data-testid="stExpander"], div.stTabs [data-baseweb="tab-list"] {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 8px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #eee;
    }
    
    /* Titles */
    h1, h2, h3 {
        color: #44475b;
        font-weight: 700 !important;
    }
    
    .disclaimer {
        font-size: 0.8rem;
        color: #7c7e8c;
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 1px solid #eee;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Invest Today: AI Indian Market Analyst")

# Sidebar for Search
st.sidebar.markdown("### 🔍 Search Stock")
query = st.sidebar.text_input("Enter Ticker (e.g., RELIANCE, TCS)", value="", placeholder="e.g. HDFCBANK")
analyze_btn = st.sidebar.button("Run Comprehensive Analysis")

def get_technical_chart(symbol):
    df = MarketDataTool.get_historical_data(symbol, period="3mo")
    if df is not None and not df.empty:
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        increasing_line_color='#00D09C', 
                        decreasing_line_color='#EB5B3C')])
        
        fig.update_layout(
            title=f"{symbol} Price History",
            template="plotly_white",
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_rangeslider_visible=False
        )
        return fig
    return None

if analyze_btn and query:
    query = query.strip().upper()
    with st.spinner(f"✨ Our AI analysts are researching {query}..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze", 
                json={"query": query},
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                symbol = data["symbol"]
                
                # Header Section
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.header(f" {symbol}")
                    fig = get_technical_chart(symbol)
                    if fig:
                        st.plotly_chart(fig, width='stretch')
                    else:
                        st.info("Technical chart not available for this symbol.")
                
                with col2:
                    st.subheader("Final Verdict")
                    # Use a custom styled box for verdict
                    st.markdown(f"""
                        <div style="background-color: #e6f9f5; border-left: 5px solid #00D09C; padding: 1.5rem; border-radius: 8px;">
                            <p style="color: #008767; font-weight: 600; font-size: 1.1rem; margin-bottom: 0;">{data["final_recommendation"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Reports Section
                st.markdown("---")
                st.subheader("Specialized Analyst Reports")
                tabs = st.tabs(["📊 Technical", "📉 Fundamental", "📰 Sentiment", "⚖️ Risk"])
                
                with tabs[0]:
                    st.markdown(data["reports"].get("technical", "N/A"))
                with tabs[1]:
                    st.markdown(data["reports"].get("fundamental", "N/A"))
                with tabs[2]:
                    st.markdown(data["reports"].get("sentiment", "N/A"))
                with tabs[3]:
                    st.markdown(data["reports"].get("risk", "N/A"))
            else:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                except:
                    error_detail = response.text
                st.error(f"Analysis Failed: {error_detail}")
        except requests.exceptions.Timeout:
            st.error("⏰ Analysis Timed Out: The request took too long.")
            st.info("💡 Tip: Try analyzing a different stock or check if the backend is busy.")
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}")
            st.info("Make sure the backend is running (python main.py --api).")

# Universal Footer Disclaimer
st.markdown("""
    <div class="disclaimer">
        Disclaimer: Content shared on or through our digital media channels are for information and education purposes only and should not be treated as investment or trading advice. 
        Investment in securities are subject to market risks, please carry out your due diligence before investing. 
        And last but not the least, past performance is not indicative of future returns.
    </div>
""", unsafe_allow_html=True)
