import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from crewai.tools import tool
import os
import requests

@tool("Stock News")
def stock_news(ticker: str):
    """
    Useful to get news about a stock.
    The input should be a ticker string and dont use dic, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.news

@tool("Macro Economic Data")
def macro_economic_data(series_id: str):
    """
    Useful to get macro economic data.
    series_id is the id of the data series in FRED.
    Following are some examples of series_id:
    - GDP: GDPC1
    - Unemployment Rate: UNRATE
    - 10 Year Treasury Rate: GS10
    - 10 Year Treasury Constant Maturity Minus 2 Year Treasury Constant Maturity: T10Y2Y
    - Money Supply: M2
    - Consumer Confidence Index: UMCSENT
    - Consumer Price Index: CPIAUCNS
    - Producer Price Index: PPIACO
    - Retail Sales: RSXFS
    - Industrial Production: INDPRO
    - Housing Starts: HOUST
    - New Home Sales: NHSLTOT
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": os.environ["FRED_API_KEY"],
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    df = pd.DataFrame(data["observations"])[["date", "value"]]
    df["value"] = pd.to_numeric(df["value"])
    df["date"] = pd.to_datetime(df["date"])
    
    return df

@tool("Stock Price - 1 Month")
def stock_price_1m(ticker: str):
    """
    Useful to get stock price data for the last month.
    The input should be a ticker str and dont use dic, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.history(period="1mo")

@tool("Stock Price - last 1 Year")
def stock_price_1y(ticker: str):
    """
    Useful to get stock price data for the last year.
    The input should be a ticker str and dont use dic, for example AAPL, NET.
    """
    ticker = yf.Ticker(ticker)
    return ticker.history(period="1y")

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