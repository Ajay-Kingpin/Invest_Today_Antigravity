import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
from app.api.routes import AnalysisResponse
from app.tools.market_data import MarketDataTool

st.set_page_config(page_title="Invest Today", page_icon="📈", layout="wide")

st.title("📈 Invest Today: AI Indian Market Analyst")
st.markdown("---")

# Sidebar for Search
query = st.sidebar.text_input("Analyze a Stock (e.g., RELIANCE, TCS, HDFCBank)", value="RELIANCE")
analyze_btn = st.sidebar.button("Run Comprehensive Analysis")

def get_technical_chart(symbol):
    df = MarketDataTool.get_historical_data(symbol, period="3mo")
    if df is not None and not df.empty:
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])])
        fig.update_layout(title=f"{symbol} Price History (3 Months)", template="plotly_dark")
        return fig
    return None

if analyze_btn or query:
    with st.spinner(f"Analyzing {query}..."):
        try:
            # For simplicity in local dev, we call the API or the graph directly
            # Here we simulate an API call to our own backend
            response = requests.post("http://127.0.0.1:8000/analyze", json={"query": query})
            
            if response.status_code == 200:
                data = response.json()
                symbol = data["symbol"]
                
                # Header Section
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.header(f"Analysis for {symbol}")
                    st.plotly_chart(get_technical_chart(symbol), use_container_width=True)
                
                with col2:
                    st.subheader("The Judge's Final Verdict")
                    st.success(data["final_recommendation"])
                
                # Reports Section
                st.markdown("### Specialized Analyst Reports")
                tabs = st.tabs(["Technical", "Fundamental", "Sentiment", "Risk"])
                
                with tabs[0]:
                    st.markdown(data["reports"].get("technical", "N/A"))
                with tabs[1]:
                    st.markdown(data["reports"].get("fundamental", "N/A"))
                with tabs[2]:
                    st.markdown(data["reports"].get("sentiment", "N/A"))
                with tabs[3]:
                    st.markdown(data["reports"].get("risk", "N/A"))
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}")
            st.info("Make sure the backend is running with: `python main.py --api`")
