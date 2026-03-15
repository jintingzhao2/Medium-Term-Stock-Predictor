import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data
def get_stock_data(ticker: str, period: str = "3y") -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    return stock.history(period=period)
