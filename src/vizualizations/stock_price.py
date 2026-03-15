import streamlit as st
import altair as alt
import pandas as pd

from calculations.growth import calculate_percent_increase


def plot_stock_data(data: pd.DataFrame) -> None:
    df = data.reset_index()
    create_metrics(df=df)

    percent_change = calculate_percent_increase(df=df, y_col="Close")
    color = "green" if percent_change > 0 else "red" if percent_change < 0 else "gray"
    with st.container(border=True):
        graph_stock_price(df=df, color=color)

    if percent_change > 0:
        st.success(f"Stock price has increased by {percent_change:.2f}%")
        st.session_state["is_price_up"] = True
    elif percent_change < 0:
        st.error(f"Stock price has decreased by {abs(percent_change):.2f}%")
        st.session_state["is_price_up"] = False
    else:
        st.info("Stock price is stable")
        st.session_state["is_price_up"] = False
    st.dataframe(
        df.sort_values("Date", ascending=False).assign(
            Date=lambda x: x["Date"].dt.strftime("%Y-%m-%d")
        ),
        hide_index=True,
    )


def graph_stock_price(df: pd.DataFrame, color: str) -> None:
    base = alt.Chart(df).encode(x="Date", y="Close")

    # Gradient area under the price line
    gradient_area = base.mark_area(
        interpolate="monotone",
        color=alt.Gradient(
            gradient="linear",
            stops=[
                alt.GradientStop(color=color, offset=0),
                alt.GradientStop(color=f"{color}00", offset=1),
            ],
            x1=1,
            y1=1,
            x2=1,
            y2=0,
        ),
        opacity=0.4,
    )

    price_line = base.mark_line(interpolate="monotone", color=color)
    trend_line = base.transform_regression("Date", "Close").mark_line(
        color="red", strokeDash=[5, 5]
    )

    chart = (gradient_area + price_line + trend_line).properties(
        title="3-Year Stock Price"
    )
    st.altair_chart(chart, width="stretch")


def create_metrics(df: pd.DataFrame) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)

    price_growth = calculate_percent_increase(df, "Close")
    with col1:
        st.metric(
            "Current Price",
            value=f"${df['Close'].iloc[-1]:.2f}",
            delta=f"{price_growth:.2f}%",
            border=True,
        )
    with col2:
        daily_change = df["Close"].iloc[-1] - df["Close"].iloc[-2]
        st.metric(
            "Daily Change",
            value=f"${daily_change:.2f}",
            delta=f"{(daily_change / df['Close'].iloc[-2] * 100):.2f}%",
            border=True,
        )
    with col3:
        weekly_change = df["Close"].iloc[-1] - df["Close"].iloc[-6]
        st.metric(
            "Weekly Change",
            value=f"${weekly_change:.2f}",
            delta=f"{(weekly_change / df['Close'].iloc[-6] * 100):.2f}%",
            border=True,
        )
    with col4:
        low_52w = df.sort_values("Date").iloc[-52:]["Close"].min()
        st.metric(
            "52-Week Low",
            value=f"${low_52w:.2f}",
            delta=f"{((df['Close'].iloc[-1] - low_52w) / low_52w * 100):.2f}%",
            border=True,
        )
    with col5:
        high_52w = df.sort_values("Date").iloc[-52:]["Close"].max()
        st.metric(
            "52-Week High",
            value=f"${high_52w:.2f}",
            delta=f"{((high_52w - df['Close'].iloc[-1]) / df['Close'].iloc[-1] * 100):.2f}%",
            border=True,
        )
