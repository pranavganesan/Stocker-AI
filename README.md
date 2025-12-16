# 📈 Stocker-AI: Agentic Financial Analyst

Stocker-AI is a full-stack investment assistant that uses **LangGraph** and **Thesys AI** to perform autonomous financial research. Unlike standard stock trackers, this agent can "reason" through complex queries by calling specialized tools to fetch live data, news, and fundamentals.



## 🧠 Intelligence & Architecture
* **LLM**: Powered by `gpt-5` via the **Thesys AI** endpoint (`api.thesys.dev`).
* **Orchestration**: Built with **LangGraph** to maintain conversation state and handle complex tool-calling loops.
* **Real-time Data**: Integrated with **Yahoo Finance** (`yfinance`) for live market updates.

## 🛠️ Features & Tools
The agent has access to several specialized Python tools:
* **Live Prices**: `get_stock_price` retrieves the latest closing data.
* **Historical Trends**: `get_historical_stock_price` fetches data across custom ranges.
* **Fundamentals**: `get_balance_sheet` extracts company financial health metrics.
* **Market Sentiment**: `get_news` summarizes recent headlines for a specific ticker.

## 🚀 Getting Started

### Backend (FastAPI)
1. Navigate to `/backend`.
2. Install dependencies: `uv pip install -r requirements.txt`.
3. Add your key to a `.env` file: `OPENAI_API_KEY=your_thesys_key`.
4. Start the server: `uv run main.py`.

### Frontend (React + Vite)
1. Navigate to `/frontend`.
2. Install dependencies: `npm install`.
3. Start the dev server: `npm run dev`.

## 🎯 Example Prompts
* "What is the current price of NVDA and what has the news been lately?"
* "Show me the balance sheet for AAPL for the last year."
* "Compare the performance of TSLA and MSFT over the last month."
