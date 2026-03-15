import yfinance as yf
import pandas as pd


def calculate_profit_margin(ticker: yf.Ticker) -> pd.DataFrame:
    operating_income = ticker.quarterly_financials.loc[["Operating Income"]].T.dropna()
    total_revenue = ticker.quarterly_financials.loc[["Total Revenue"]].T.dropna()
    margin = operating_income.merge(total_revenue, left_index=True, right_index=True)
    margin["operating_margin"] = (
        margin["Operating Income"] / margin["Total Revenue"] * 100
    )
    return margin.reset_index().sort_values("index")
