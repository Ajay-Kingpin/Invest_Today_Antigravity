import pytest
import asyncio
from app.graph.workflow import app
from app.graph.state import InvestTodayState
import time

# Configure pytest-asyncio to avoid the warning/error
pytestmark = pytest.mark.asyncio(loop_scope="function")

# Diverse set of stocks for evaluation
STOCKS_TO_TEST = [
    "RELIANCE",   # Large Cap (Energy)
    "TCS",        # Large Cap (IT)
    "HDFCBANK",   # Large Cap (Banking)
    "ADANIENT",   # Volatile/High Beta
    "SUZLON",     # Small Cap / Power
]

@pytest.mark.asyncio
async def test_full_analysis_workflow_diverse_stocks():
    """
    Evaluates the full LangGraph workflow for a diverse set of Indian stocks.
    Verifies that all analyst reports and the judge's verdict are generated.
    """
    for symbol in STOCKS_TO_TEST:
        print(f"\n🚀 Evaluating Symbol: {symbol}")
        start_time = time.time()
        
        # Initialize state
        initial_state = {
            "symbol": symbol,
            "query": f"Analyze {symbol}",
            "reports": {},
            "final_recommendation": "",
            "metadata": {}
        }
        
        # Run the graph
        try:
            # Using basic invoke since we aren't in a streaming context here
            result = await asyncio.to_thread(app.invoke, initial_state)
            
            end_time = time.time()
            duration = end_time - start_time
            print(f"✅ Completed in {duration:.2f}s")
            
            # Assertions
            assert result["symbol"] == symbol
            assert "technical" in result["reports"]
            assert "fundamental" in result["reports"]
            assert "sentiment" in result["reports"]
            assert "risk" in result["reports"]
            assert len(result["final_recommendation"]) > 50  # Ensure a substantial verdict
            
            # Check for generic errors in reports
            for report_type, content in result["reports"].items():
                assert "Error" not in content, f"{report_type} report for {symbol} contains an error: {content}"
                assert len(content) > 100, f"{report_type} report for {symbol} is too short."
                
        except Exception as e:
            pytest.fail(f"Workflow failed for {symbol}: {str(e)}")

if __name__ == "__main__":
    # For manual running
    async def run_manual_eval():
        await test_full_analysis_workflow_diverse_stocks()
    
    asyncio.run(run_manual_eval())
