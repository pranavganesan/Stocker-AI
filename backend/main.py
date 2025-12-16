from dotenv import load_dotenv
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

import yfinance as yf

load_dotenv()

app = FastAPI()

model = ChatOpenAI(
    model_name="c1/openai/gpt-5/v-20250930", 
    base_url= "https://api.thesys.dev/v1/embed")

checkpointer = InMemorySaver()

@tool('get_stock_price', description="Get the current stock price for a given ticker symbol.")
def get_stock_price(ticker: str):
    print('get_stock_price tool is being used')
    stock = yf.Ticker(ticker)
    return stock.history()['Close'].iloc[-1]

@tool('get_historical_stock_price', description="Get the historical stock price for a given ticker symbol and a start and end date.")
def get_historical_stock_price(ticker: str, start_date: str, end_date: str):
    print('get_historical_stock_price tool is being used')
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date).to_dict()

@tool('get_balance_sheet', description="Get the balance sheet for the given ticker symbol and year.")
def get_balance_sheet(ticker: str):
    print('get_balance_sheet tool is being used')
    stock = yf.Ticker(ticker)
    return stock.balance_sheet.to_dict()

@tool('get_news', description="Get the latest news for a given ticker symbol.")
def get_news(ticker: str):
    print('get_news tool is being used')
    stock = yf.Ticker(ticker)
    return stock.news

agent = create_agent(
    model = model,
    checkpointer = checkpointer,
    tools = [get_stock_price, get_historical_stock_price, get_balance_sheet, get_news]
)

class PromptObject(BaseModel):
    content: str
    id: str
    role: str

class RequestObject(BaseModel):
    prompt: PromptObject
    threadId: str
    responseId: str

@app.post('/api/chat')
async def chat(request: RequestObject):
    config = {'configurable': {'thread_id': request.threadId}}

    def generate():
        for token, _ in agent.stream(
            {'messages': [
                SystemMessage("You are a stock analyssis assistant. You have the ability to get real-time stock prices, historical stock prices (given a date range), news and balance sheet data for a given ticker symbol."),
                HumanMessage(request.prompt.content)
            ]},
            stream_mode='messages', 
            config=config
        ): 
            yield token.content

    return StreamingResponse(generate(), media_type='text/event-stream',
                             headers={"Cache-Control": "no-cache, no-transform",
                                      "Connection": "keep-alive"
                                      })
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8888)
    


        