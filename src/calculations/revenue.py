import yfinance as yf
import pandas as pd


def calculate_revenue(ticker: yf.Ticker) -> pd.DataFrame:
    revenue_billion = (
        ticker.quarterly_financials.loc[["Total Revenue"]].T.dropna() / 1_000_000_000
    ).rename(columns={"Total Revenue": "Total Revenue (Billion $)"})
    return revenue_billion.sort_index()
