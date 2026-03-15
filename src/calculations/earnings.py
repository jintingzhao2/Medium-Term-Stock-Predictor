import yfinance as yf
import pandas as pd


def get_earnings_history(ticker: yf.Ticker) -> pd.DataFrame:
    return ticker.earnings_history
