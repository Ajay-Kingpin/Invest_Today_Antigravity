import pytest
import os
import shutil
from app.tools.market_data import MarketDataTool
from app.tools.news import NewsTool
from app.tools.economic import EconomicTool
from app.rag.ingestor import Ingestor
from app.core.config import settings

@pytest.fixture(autouse=True)
def setup_teardown():
    """Clean up the FAISS index after tests."""
    if os.path.exists("data/faiss_index"):
        os.remove("data/faiss_index")
    if os.path.exists("data/faiss_index.pkl"):
        os.remove("data/faiss_index.pkl")
    yield
    if os.path.exists("data/faiss_index"):
        os.remove("data/faiss_index")
    if os.path.exists("data/faiss_index.pkl"):
        os.remove("data/faiss_index.pkl")

def test_market_data_tool():
    """Test fetching price info for a known Indian stock."""
    # Using RELIANCE as a stable symbol
    data = MarketDataTool.get_price_info("RELIANCE")
    assert "symbol" in data
    assert "current_price" in data or "error" in data
    if "current_price" in data:
        assert data["current_price"] > 0

def test_news_tool_scrape():
    """Test the news scraper fallback."""
    tool = NewsTool()
    news = tool._scrape_google_news("RELIANCE")
    assert isinstance(news, list)
    if len(news) > 0:
        assert "title" in news[0]

def test_economic_tool():
    """Test fetching India macro data from World Bank."""
    data = EconomicTool.get_india_macro_data()
    assert "gdp_growth" in data
    assert "inflation" in data

def test_rag_ingestion_faiss():
    """Test ingesting text into the FAISS vector store."""
    if not os.path.exists("data"):
        os.makedirs("data")
        
    ingestor = Ingestor()
    success = ingestor.ingest_text(
        "Reliance Industries Limited is an Indian multinational conglomerate headquartered in Mumbai.",
        metadata={"company": "RELIANCE"}
    )
    assert success is True
    
    # Verify retrieval
    results = ingestor.db.query("Where is Reliance headquartered?")
    assert len(results["documents"][0]) > 0
    assert "Mumbai" in results["documents"][0][0]
