import streamlit as st
import yfinance as yf
import pandas as pd

from stocks import get_stock_data
from calculations.revenue import calculate_revenue
from calculations.sentiment import get_news_with_sentiment
from calculations.eps import calculate_earnings_per_share
from calculations.profit import calculate_profit_margin
from calculations.earnings import get_earnings_history

from vizualizations.stock_price import plot_stock_data
from vizualizations.news import show_news
from vizualizations.revenue import plot_revenue_data
from vizualizations.profit import plot_profit_margin_data
from vizualizations.eps import plot_eps_data
from vizualizations.earnings import plot_earnings_history_data
from vizualizations.pe_ratio import show_pe_peg

st.set_page_config(
    page_title="Stock Predictor",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_ticker_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    return stock.info


@st.cache_data
def get_ticker_list() -> list[str]:
    df = pd.read_csv("data/ticker_symbols.csv")
    return df["ACT Symbol"].tolist()


def show_company_header(ticker: str, ticker_information: dict):
    company_name = ticker_information.get("longName", ticker)

    st.title(f"{company_name} ({ticker})")
    st.caption(
        "⚠️ Disclaimer: This dashboard is for educational purposes only and should not be used for financial decisions."
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.metric(
            label="Sector",
            value=ticker_information.get("sector", "N/A"),
        )

    with col2:
        st.metric(
            label="Industry",
            value=ticker_information.get("industry", "N/A"),
        )

    with col3:
        market_cap = ticker_information.get("marketCap", 0)
        st.metric(
            label="Market Cap",
            value=f"${market_cap / 1e9:.2f}B" if market_cap else "N/A",
        )


def main():

    # Create sidebar container
    sidebar_container = st.sidebar.container()

    with sidebar_container:
        st.title("Medium Term Stock Predictor")
        ticker = st.selectbox(
            "Select a stock ticker:",
            options=get_ticker_list(),
            index=0,
        )

    # -----------------------------
    # DATA COLLECTION
    # -----------------------------
    stock = yf.Ticker(ticker)

    ticker_information = get_ticker_info(ticker)
    news_data, average_sentiment = get_news_with_sentiment(stock)
    stock_df = get_stock_data(ticker=ticker)

    try:
        revenue_df = calculate_revenue(stock)
    except Exception:
        revenue_df = pd.DataFrame()

    try:
        eps_df = calculate_earnings_per_share(stock)
    except Exception:
        eps_df = pd.DataFrame()

    try:
        profit_margin_df = calculate_profit_margin(stock)
    except Exception:
        profit_margin_df = pd.DataFrame()

    try:
        earnings_df = get_earnings_history(stock)
    except Exception:
        earnings_df = pd.DataFrame()

    # -----------------------------
    # MAIN PAGE
    # -----------------------------
    show_company_header(ticker, ticker_information)

    tab1, tab2, tab3 = st.tabs(["Stock Price", "Earnings & Revenue", "News"])

    # Stock Price Tab
    with tab1:
        plot_stock_data(data=stock_df)

    # Earnings & Revenue Tab
    with tab2:
        revenue_column, eps_column, pm_column = st.columns(3)

        with revenue_column:
            try:
                plot_revenue_data(data=revenue_df)
            except Exception:
                st.info("Revenue data not available")

        with eps_column:
            try:
                plot_eps_data(data=eps_df)
            except Exception:
                st.info("EPS data not available")

        with pm_column:
            try:
                plot_profit_margin_data(data=profit_margin_df)
            except Exception:
                st.info("Profit margin data not available")

        st.divider()

        try:
            plot_earnings_history_data(data=earnings_df)
        except Exception:
            st.info("Earnings history data not available")

        show_pe_peg(stock=stock)

    # News Tab
    with tab3:
        show_news(news_data=news_data, average_sentiment=average_sentiment)

    # -----------------------------
    # SIDEBAR CHECKLIST (after calculations)
    # -----------------------------
    with sidebar_container:
        st.markdown("---")
        st.subheader("Checklist Evaluation")

        checklist = {
            "Price Trending Up": st.session_state.get("is_price_up", False),
            "Revenue Trending Up": st.session_state.get("is_revenue_up", False),
            "Basic EPS Trending Up": st.session_state.get("is_eps_up", False),
            "Margin Trending Up": st.session_state.get("is_margin_up", False),
            "Earnings Met Expectations": st.session_state.get(
                "earnings_met_expectations", False
            ),
            "P/E Below 5Y Avg": st.session_state.get("is_pe_good", False),
            "PEG Ratio < 2": st.session_state.get("is_peg_good", False),
            "Positive News Sentiment": st.session_state.get("is_sent_pos", False),
        }

        for label, value in checklist.items():
            st.checkbox(label, value=value, disabled=True)

        score = sum(bool(v) for v in checklist.values())

        st.markdown(f"### Score: {score}/8")

        if score >= 6:
            st.success("Verdict: BUY")
        elif score >= 4:
            st.warning("Verdict: HOLD")
        else:
            st.error("Verdict: AVOID")


if __name__ == "__main__":
    main()
