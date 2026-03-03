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
        uvicorn.run("app.api.routes:app", host="127.0.0.1", port=8000, reload=True)
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
        
        if result.get("errors"):
            print(f"ERROR: {result['errors'][0]}")
            return

        print(f"\nFINAL ANALYSIS FOR: {result['symbol']}")
        print("=" * 40)
        print(result.get("final_recommendation", "No recommendation generated."))
        print("=" * 40)
        
    except Exception as e:
        print(f"System Error: {str(e)}")

if __name__ == "__main__":
    main()
