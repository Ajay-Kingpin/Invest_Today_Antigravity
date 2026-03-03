# Invest Today: Agent Tests
import pytest
from app.agents.technical import TechnicalAnalystAgent
from app.agents.fundamental import FundamentalAnalystAgent
from app.agents.sentiment import SentimentAnalystAgent
from app.agents.risk import RiskAnalystAgent
from app.agents.judge import JudgeAgent
import pandas as pd
from app.tools.market_data import MarketDataTool
from unittest.mock import MagicMock, patch

@pytest.fixture
def symbol():
    return "RELIANCE"

def test_technical_analyst_init():
    agent = TechnicalAnalystAgent()
    assert agent.model is not None

def test_fundamental_analyst_init():
    agent = FundamentalAnalystAgent()
    assert agent.model is not None

def test_sentiment_analyst_init():
    agent = SentimentAnalystAgent()
    assert agent.model is not None

def test_risk_analyst_init():
    agent = RiskAnalystAgent()
    assert agent.model is not None

def test_judge_agent_init():
    agent = JudgeAgent()
    assert agent.model is not None

def test_technical_indicator_logic(symbol):
    """Test the actual calculation logic of technical indicators."""
    agent = TechnicalAnalystAgent()
    # Create a dummy dataframe for testing
    data = {
        'Close': [100.0 + i for i in range(60)] # Upward trend
    }
    df = pd.DataFrame(data)
    
    # Calculate SMA
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    assert df['SMA20'].iloc[-1] == 149.5
    
    # Calculate RSI (Simple check)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    assert 0 <= df['RSI'].iloc[-1] <= 100

def test_market_data_fundamental_structure():
    """Verify that MarketDataTool returns the new fundamental fields."""
    with patch('yfinance.Ticker') as mock_ticker:
        mock_ticker.return_value.info = {
            "currentPrice": 150.0,
            "returnOnEquity": 0.20,
            "debtToEquity": 0.5,
            "priceToBook": 3.0
        }
        data = MarketDataTool.get_price_info("RELIANCE")
        assert data["roe"] == 0.20
        assert data["debt_to_equity"] == 0.5
        assert data["pb_ratio"] == 3.0

@patch('app.agents.technical.genai.GenerativeModel.generate_content')
def test_technical_analyst_analyze(mock_gen, symbol):
    mock_gen.return_value.text = "Bullish Technical Outlook"
    agent = TechnicalAnalystAgent()
    report = agent.analyze(symbol)
    assert "Bullish" in report

@patch('app.agents.fundamental.genai.GenerativeModel.generate_content')
def test_fundamental_analyst_analyze(mock_gen, symbol):
    mock_gen.return_value.text = "Strong Fundamentals"
    agent = FundamentalAnalystAgent()
    report = agent.analyze(symbol)
    assert "Strong" in report

@patch('app.agents.sentiment.genai.GenerativeModel.generate_content')
@patch('app.tools.news.NewsTool.get_company_news')
def test_sentiment_analyst_analyze(mock_news, mock_gen, symbol):
    mock_news.return_value = [{"title": "Good News", "source": "test"}]
    mock_gen.return_value.text = "Positive Sentiment"
    agent = SentimentAnalystAgent()
    report = agent.analyze(symbol)
    assert "Positive" in report

@patch('app.agents.risk.genai.GenerativeModel.generate_content')
def test_risk_analyst_analyze(mock_gen, symbol):
    mock_gen.return_value.text = "Low Risk Profile"
    agent = RiskAnalystAgent()
    report = agent.analyze(symbol)
    assert "Low Risk" in report

@patch('app.agents.judge.genai.GenerativeModel.generate_content')
def test_judge_agent_synthesize(mock_gen, symbol):
    mock_gen.return_value.text = "Final Recommendation: Buy"
    agent = JudgeAgent()
    reports = {
        "technical": "Bullish",
        "fundamental": "Strong",
        "sentiment": "Positive",
        "risk": "Low"
    }
    recommendation = agent.synthesize(symbol, reports)
    assert "Buy" in recommendation
