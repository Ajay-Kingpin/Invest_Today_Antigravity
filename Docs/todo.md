# Invest_Today Implementation TODO List

This list outlines the steps required to build the Invest_Today platform, following the phase-wise approach while prioritizing Gemini models and free Indian market tools.

## Phase 1: Environment Setup & Data Infrastructure
- [ ] **Infrastructure Setup**
    - [ ] Initialize a new Python project with `poetry` or `venv`.
    - [ ] Install dependencies: `langchain-google-genai`, `langgraph`, `chromadb`, `yfinance`, `nsepython`, `fastapi`, `streamlit`.
    - [ ] Configure environment variables for `GOOGLE_API_KEY`.
- [ ] **Data Tooling (MCP Layer)**
    - [ ] Implement a `MarketDataTool` using `yfinance` for price tracking.
    - [ ] Implement a `FundamentalDataTool` using `nsepython` for NSE stock details.
    - [ ] Implement a `NewsTool` wrapper for GNews API or direct scraping of Indian financial news sites.
    - [ ] Register tools with LangChain for agent usage.
- [ ] **RAG System**
    - [ ] Set up ChromaDB for local document storage.
    - [ ] Create a pipeline for ingesting SEBI corporate filings and annual reports.
    - [ ] Implement retrieval logic with state-of-the-art chunking for financial data.

## Phase 2: Specialist Agent Development
- [ ] **Technical Analyst Agent**
    - [ ] Design system prompt focused on Indian market price action.
    - [ ] Integrate technical indicator calculations (RSI, SMA, MACD).
- [ ] **Fundamental Analyst Agent**
    - [ ] Design system prompt for ratio analysis and valuation metrics.
    - [ ] Connect agent to real-time financial statements via MCP tools.
- [ ] **Sentiment Analyst Agent**
    - [ ] Design system prompt for detecting mood and news importance.
    - [ ] Implement scoring logic for news headlines.
- [ ] **Risk Analyst Agent**
    - [ ] Design system prompt for promoter pledge and regulatory risk detection.
    - [ ] Integrate economic data tools (inflation, GDP).
- [ ] **The Judge Agent**
    - [ ] Design a robust decision framework for synthesizing conflicting analyst views.

## Phase 3: LangGraph Orchestration
- [ ] **State Definition**
    - [ ] Define the `InvestTodayState` schema in Python.
- [ ] **Graph Construction**
    - [ ] Implement the `Query Router` node.
    - [ ] Implement the parallel execution logic for analysts.
    - [ ] Implement the synthesis and judgement nodes.
- [ ] **Error Handling & Resiliency**
    - [ ] Add retry logic for Gemini API calls.
    - [ ] Implement fallbacks for failed data retrieval.

## Phase 4: User Interface & API
- [ ] **Backend API (FastAPI)**
    - [ ] Create endpoints for analysis: `/analyze`, `/stocks/{symbol}`.
    - [ ] Implement rate limiting and request validation.
- [ ] **Frontend (Streamlit)**
    - [ ] Build the main search interface.
    - [ ] Create interactive charts (Plotly) for technical views.
    - [ ] Display agent reasoning in a clean, tabbed layout.

## Phase 5: Verification & Beta Testing
- [ ] **System Evaluation**
    - [ ] Test with a set of diverse NSE stocks (Adani, Reliance, ITC, small caps).
    - [ ] Verify recommendation accuracy against historical movements.
- [ ] **Documentation & Handover**
    - [ ] Finalize deployment guides (Docker instructions).
    - [ ] Create a user manual for the dashboard.
