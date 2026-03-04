# Invest Today: AI-powered Indian Stock Market Analysis
from app.graph.workflow import app
import sys
import io

# Force UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    if "--api" in sys.argv:
        import uvicorn
        print("Starting Invest Today API Server...")
        # Listen on 0.0.0.0 for better local resolution compatibility
        uvicorn.run("app.api.routes:app", host="0.0.0.0", port=8000, reload=True)
        return

    print("--- Invest Today: Indian Market Analyst ---")
    
    # Example Query
    query = "Analyze RELIANCE" if len(sys.argv) < 2 else " ".join(sys.argv[1:])
    print(f"User Query: {query}")
    print("-" * 40)
    
    # Run the Orchestrator
    try:
        initial_state = {
            "query": query,
            "reports": {},
            "errors": [],
            "metadata": {}
        }
        
        # Invoke the graph
        result = app.invoke(initial_state)
        
        # Debug: Uncomment to see full state
        # logger.debug(f"Final State: {result}")
        
        if result.get("errors") and len(result.get("errors", [])) > 0:
            print(f"ERROR: {result['errors'][0]}")
            return
    
        symbol = result.get("symbol", "N/A")
        print(f"\nFINAL ANALYSIS FOR: {symbol}")
        print("=" * 40)
        print(result.get("final_recommendation", "No recommendation generated."))
        print("=" * 40)
        
    except Exception as e:
        print(f"System Error: {str(e)}")

if __name__ == "__main__":
    main()
