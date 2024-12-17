import yfinance as yf
from crewai.tools import tool

@tool("Stock News")
def stock_news(ticker: str):
    """
    Useful to get news about a stock.
    The input should be a ticker string and dont use dic, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.news

@tool("Stock Price")
def stock_price(ticker: str):
    """
    Useful to get stock price data.
    The input should be a ticker str and dont use dic, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.history(period="1mo")

@tool("Income Statement")
def income_stmt(ticker: str):
    """
    Useful to get the income statement of a company.
    The input to this tool should be a ticker str and dont use dic, for example AAPL, NET. 
    """
    ticker = yf.Ticker(ticker)
    return ticker.income_stmt

@tool("Balance Sheet")
def balance_sheet(ticker: str):
    """
    Useful to get the balance sheet of a company.
    The input to this tool should be a ticker str and dont use dic, for example AAPL, NET. 
    """
    ticker = yf.Ticker(ticker)
    return ticker.balance_sheet

@tool("Insider Transactions")
def insider_transactions(ticker: str):
    """
    Useful to get the insider transactions of a stock.
    The input to this tool should be a ticker str and dont use dic, for example AAPL, NET. 
    """
    ticker = yf.Ticker(ticker)
    return ticker.insider_transactions