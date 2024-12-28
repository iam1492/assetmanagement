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
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET)
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
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.history(period="1mo")

@tool("Stock Price - last 1 Year")
def stock_price_1y(ticker: str):
    """
    Useful to get stock price data for the last year.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.history(period="1y")

@tool("Stock Info")
def stock_info(ticker: str):
    """
    Useful to get stock infomation.
    (e.g. market cap, beta, 52-week high, 52-week low, etc.)
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.info

@tool("Cash Flow")
def cash_flow(ticker: str):
    """
    Useful to get the cash flow of a company.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.cash_flow

@tool("Cash Flow Quauterly")
def cash_flow_quarterly(ticker: str):
    """
    Useful to get the quarter cash flow of a company.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.quarterly_cash_flow

@tool("Income Statement")
def income_stmt(ticker: str):
    """
    Useful to get the income statement of a company.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.income_stmt

@tool("Income Statement Quarterly")
def income_stmt_quarterly(ticker: str):
    """
    Useful to get the quarter income statement of a company.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.quarterly_income_stmt

@tool("Balance Sheet")
def balance_sheet(ticker: str):
    """
    Useful to get the balance sheet of a company.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.balance_sheet

@tool("Balance Sheet Quarterly")
def balance_sheet_quarterly(ticker: str):
    """
    Useful to get the quarter balance sheet of a company.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.quarterly_balance_sheet

@tool("Insider Transactions")
def insider_transactions(ticker: str):
    """
    Useful to get the insider transactions of a stock.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    """
    ticker = yf.Ticker(ticker)
    return ticker.insider_transactions

@tool("Option Chain")
def option_chain(ticker: str):
    """
    Useful to get the option chain of a stock.
    The input parameter of this tool is a ticker of a company.(for example AAPL, NET, RDDT)
    The output of this tool is a tuple of calls and puts.
    """
    ticker = yf.Ticker(ticker)
    expirations = ticker.options
    if expirations:
        first_expiration = expirations[0]
        chain = ticker.option_chain(first_expiration)
        calls = chain.calls
        puts = chain.puts
        return calls, puts
    else:
        return None, None
    
# Calculators

@tool("operating_margin_calculator")
def operating_margin_calculator(operating_income: float, revenue: float):
    """
    Useful to calculate the operating margin.
    The input parameters of this tool are operating income and revenue.
    """
    return (operating_income / revenue) * 100

@tool("Gross Profit Margin Calculator")
def gross_profit_margin_calculator(gross_profit: float, revenue: float):
    """
    Useful to calculate the gross profit margin.
    The input parameters of this tool are gross profit and revenue.
    """
    return (gross_profit / revenue) * 100

@tool("Return on Assets Calculator")
def return_on_assets_calculator(net_income: float, total_assets: float):
    """
    Useful to calculate the return on assets.
    The input parameters of this tool are net income and total assets.
    """
    return (net_income / total_assets) * 100

@tool("Return on Equity Calculator")
def return_on_equity_calculator(net_income: float, total_equity: float):
    """
    Useful to calculate the return on equity.
    The input parameters of this tool are net income and total equity.
    """
    return (net_income / total_equity) * 100

@tool("Return on invested capital calculator")
def return_on_invested_capital_calculator(net_income: float, total_debt: float, total_equity: float):
    """
    Useful to calculate the return on invested capital.
    The input parameters of this tool are net income, total debt and total equity.
    """
    return (net_income / (total_debt + total_equity)) * 100

@tool("Inventory turnover ratio calculator")
def inventory_turnover_ratio_calculator(cost_of_goods_sold: float, average_inventory: float):
    """
    Useful to calculate the inventory turnover ratio.
    The input parameters of this tool are cost of goods sold and average inventory.
    """
    return cost_of_goods_sold / average_inventory

@tool("Receivables Turnover Ratio Calculator")
def receivables_turnover_ratio_calculator(net_credit_sales: float, average_accounts_receivable: float):
    """
    Useful to calculate the receivables turnover ratio.
    The input parameters of this tool are net credit sales and average accounts receivable.
    """
    return net_credit_sales / average_accounts_receivable

@tool("Net profit margin calculator")
def net_profit_margin_calculator(revenue: float, net_income: float):
    """
    Useful to calculate the net profit margin.
    The input parameters of this tool are revenue and net income.
    """
    return (net_income / revenue) * 100

@tool("Debt to Equity Ratio Calculator")
def debt_to_equity_ratio_calculator(total_debt: float, total_equity: float):
    """
    Useful to calculate the debt to equity ratio.
    The input parameters of this tool are total debt and total equity.
    """
    return total_debt / total_equity

@tool("Debt to Assets Ratio Calculator")
def debt_to_assets_ratio_calculator(total_debt: float, total_assets: float):
    """
    Useful to calculate the debt to assets ratio.
    The input parameters of this tool are total debt and total assets.
    """
    return total_debt / total_assets

@tool("Interest Coverage Ratio Calculator")
def interest_coverage_ratio_calculator(earnings_before_interest_and_taxes: float, interest_expense: float):
    """
    Useful to calculate the interest coverage ratio.
    The input parameters of this tool are earnings before interest and taxes and interest expense.
    """
    return earnings_before_interest_and_taxes / interest_expense

@tool("quick_ratio_calculator")
def quick_ratio_calculator(current_assets: float, inventory: float, current_liabilities: float):
    """
    Useful to calculate the quick ratio.
    The input parameters of this tool are current assets, inventory and current liabilities.
    """
    return (current_assets - inventory) / current_liabilities

@tool("Revenue Growth Rate Calculator")
def revenue_growth_rate_calculator(current_revenue: float, previous_revenue: float):
    """
    Useful to calculate the revenue growth rate.
    The input parameters of this tool are current revenue and previous revenue.
    """
    return ((current_revenue - previous_revenue) / previous_revenue) * 100

@tool("Free Cash Flow Calculator")
def free_cash_flow_calculator(cash_flow_from_operations: float, capital_expenditures: float):
    """
    Useful to calculate the free cash flow.
    The input parameters of this tool are cash flow from operations and capital expenditures.
    """
    return cash_flow_from_operations - capital_expenditures

@tool("Earnings Growth Rate Calculator")
def earnings_growth_rate_calculator(current_earnings: float, previous_earnings: float):
    """
    Useful to calculate the earnings growth rate.
    The input parameters of this tool are current earnings and previous earnings.
    """
    return ((current_earnings - previous_earnings) / previous_earnings) * 100

@tool("Asset Turnover Calculator")
def asset_turnover_calculator(revenue: float, average_total_assets: float):
    """
    Useful to calculate the asset turnover.
    The input parameters of this tool are revenue and average total assets.
    """
    return revenue / average_total_assets


# @tool("Discount Cash Flow")
# def discount_cash_flow(ticker: str):
#     """
#     Useful to get the discounted cash flow of a company.
#     The input to this tool should be a ticker str and dont use dic, for example AAPL, NET. 
#     Output data is JSON format which shows discount cash flow of the company.
#     """
#     url = 'https://financialmodelingprep.com/api/v3/discounted-cash-flow/{ticker}?apikey={apikey}'.format(ticker=ticker, apikey=os.environ['FMP_API_KEY'])
#     response = get_jsonparsed_data(url)
#     return response

# @tool("Enterprise Values")
# def enterprise_values(ticker: str):
#     """
#     Useful to get the enterprise values of a company.
#     The input parameter of this tool should be a ticker of a company.(for example AAPL, NET)
#     """
#     url = get_api_url('enterprise-value', ticker, 'annual', os.environ['FMP_API_KEY'])
#     json_data = get_jsonparsed_data(url)
#     return json.dumps(json_data)

# def get_api_url(requested_data, ticker, period, apikey):
    
#     if period == 'annual':
#         url = 'https://financialmodelingprep.com/api/v3/{requested_data}/{ticker}?apikey={apikey}'.format(
#             requested_data=requested_data, ticker=ticker, apikey=apikey)
#     elif period == 'quarter':
#         url = 'https://financialmodelingprep.com/api/v3/{requested_data}/{ticker}?period=quarter&apikey={apikey}'.format(
#             requested_data=requested_data, ticker=ticker, apikey=apikey)
#     else:
#         raise ValueError("invalid period " + str(period))
#     return url

# def get_jsonparsed_data(url):
#     try: response = urlopen(url)
#     except Exception as e:
#         print(f"Error retrieving {url}:")
#         try: print("\t%s"%e.read().decode())
#         except: pass
#         raise
#     data = response.read().decode('utf-8')
#     json_data = json.loads(data)
#     if "Error Message" in json_data:
#         raise ValueError("Error while requesting data from '{url}'. Error Message: '{err_msg}'.".format(
#             url=url, err_msg=json_data["Error Message"]))
#     #print(json_data)
#     return json_data
