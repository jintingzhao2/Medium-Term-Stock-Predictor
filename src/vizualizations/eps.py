import pandas as pd
import altair as alt
import streamlit as st
from calculations.growth import calculate_percent_increase


def plot_eps_data(data: pd.DataFrame):
    df = data.reset_index()
    percent_change = calculate_percent_increase(df=df, y_col="Basic EPS")
    st.metric(
        "EPS Growth",
        delta=f"{percent_change:.2f}%",
        value=f"{df['Basic EPS'].iloc[-1]:.2f}",
        border=True,
    )
    base = alt.Chart(df).encode(x="index:T", y="Basic EPS")
    chart = base.mark_line() + base.transform_regression(
        "index", "Basic EPS"
    ).mark_line(color="red", strokeDash=[5, 5])
    st.altair_chart(chart.properties(title="Basic EPS"), width="stretch")
    if percent_change > 0:
        st.success(f"EPS has increased by {percent_change:.2f}%")
        st.session_state["is_eps_up"] = True
    elif percent_change < 0:
        st.error(f"EPS has decreased by {abs(percent_change):.2f}%")
        st.session_state["is_eps_up"] = False
    else:
        st.info("EPS is stable")
        st.session_state["is_eps_up"] = False

    st.dataframe(
        df.rename(columns={"index": "Quarter"}).assign(
            Quarter=lambda x: x["Quarter"].dt.strftime("%Y-%m-%d")
        ),
        hide_index=True,
    )
