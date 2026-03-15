import yfinance as yf
import pandas as pd


def calculate_earnings_per_share(ticker: yf.Ticker) -> pd.DataFrame:
    eps = ticker.quarterly_financials.loc[["Basic EPS"]].T.dropna().sort_index()
    return eps
