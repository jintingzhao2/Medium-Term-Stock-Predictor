import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Stockify", layout="wide")

# -------------------------
# Spotify Styling
# -------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    h1, h2, h3 {
        color: #1DB954;
    }
    section[data-testid="stSidebar"] {
        background-color: #181818;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -------------------------
# Header
# -------------------------
st.title("🎵 Stockify Dashboard")
st.subheader("Your Market. Your Vibes.")

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("🎧 Choose Your Stock")

ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")

period = st.sidebar.selectbox(
    "Select Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)

# -------------------------
# Fetch Data
# -------------------------
stock = yf.Ticker(ticker)
data = stock.history(period=period)

if data.empty:
    st.error("No data found. Try another ticker.")
else:
    data.reset_index(inplace=True)

    # -------------------------
    # Metrics
    # -------------------------
    current_price = data["Close"].iloc[-1]
    prev_price = data["Close"].iloc[-2]
    change = current_price - prev_price
    pct_change = (change / prev_price) * 100

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Price", f"${current_price:.2f}")
    col2.metric("Daily Change", f"${change:.2f}", f"{pct_change:.2f}%")
    col3.metric("Volume", f"{int(data['Volume'].iloc[-1]):,}")

    # -------------------------
    # Altair Chart (Line)
    # -------------------------
    base = alt.Chart(data).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Close:Q", title="Price"),
        tooltip=["Date:T", "Close:Q"],
    )

    line = base.mark_line(color="#1DB954", strokeWidth=3)

    st.subheader("📈 Price Chart")

    st.altair_chart(
        line.properties(width="container", height=500).interactive(),
        use_container_width=True,
    )

    # -------------------------
    # Company Info
    # -------------------------
    st.subheader("🎼 Company Overview")
    info = stock.info

    st.write(f"**Company:** {info.get('longName', 'N/A')}")
    st.write(f"**Sector:** {info.get('sector', 'N/A')}")
    st.write(f"**Industry:** {info.get('industry', 'N/A')}")
    st.write(f"**Market Cap:** ${info.get('marketCap', 0):,}")
