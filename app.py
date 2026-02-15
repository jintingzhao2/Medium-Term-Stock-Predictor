import streamlit as st
import yfinance as yf

st.title("Super Awesome DSCI 521 Project")

# Text input for the stock ticker
ticker = st.text_input("Enter a stock ticker (e.g. AAPL, MSFT, GOOGL):")

if ticker:
    # Download stock data for the past year
    stock_data = yf.download(ticker, period="1y")

    if not stock_data.empty:
        # Display only the closing prices
        st.line_chart(stock_data["Close"])
    else:
        st.error("No data found for that ticker. Please try a valid stock symbol.")

