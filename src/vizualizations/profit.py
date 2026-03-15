import pandas as pd
import altair as alt
import streamlit as st

from calculations.growth import calculate_percent_increase


def plot_profit_margin_data(data: pd.DataFrame):
    percent_change = calculate_percent_increase(data, "operating_margin")
    st.metric(
        "Margin Growth",
        delta=f"{percent_change:.2f}%",
        value=f"{data['operating_margin'].iloc[-1]:.2f}%",
        border=True,
    )

    base = alt.Chart(data).encode(x="index:T", y="operating_margin")
    chart = base.mark_line() + base.transform_regression(
        "index", "operating_margin"
    ).mark_line(color="red", strokeDash=[5, 5])
    st.altair_chart(chart.properties(title="Operating Margin (%)"), width="stretch")
    if percent_change > 0:
        st.success(f"Operating margin has increased by {percent_change:.2f}%")
        st.session_state["is_margin_up"] = True
    elif percent_change < 0:
        st.error(f"Operating margin has decreased by {abs(percent_change):.2f}%")
        st.session_state["is_margin_up"] = False
    else:
        st.info("Operating margin is stable")
        st.session_state["is_margin_up"] = False

    st.dataframe(
        data.rename(columns={"index": "Quarter"}).assign(
            Quarter=lambda x: x["Quarter"].dt.strftime("%Y-%m-%d")
        ),
        hide_index=True,
    )