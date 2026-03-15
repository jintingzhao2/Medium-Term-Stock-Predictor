import pandas as pd
import altair as alt
import streamlit as st
from calculations.growth import calculate_percent_increase


def plot_revenue_data(data: pd.DataFrame):
    df = data.reset_index()
    percent_change = calculate_percent_increase(
        df=df, y_col="Total Revenue (Billion $)"
    )
    st.metric(
        "Revenue Growth",
        delta=f"{percent_change:.2f}%",
        value=f"${df['Total Revenue (Billion $)'].iloc[-1]:.2f}B",
        border=True,
    )
    base = alt.Chart(df).encode(x="index:T", y="Total Revenue (Billion $)")
    chart = base.mark_bar() + base.transform_regression(
        "index", "Total Revenue (Billion $)"
    ).mark_line(color="red", strokeDash=[5, 5])
    st.altair_chart(chart.properties(title="Quarterly Revenue"), width="stretch")

    if percent_change > 0:
        st.success(f"Revenue has increased by {percent_change:.2f}%")
        st.session_state["is_revenue_up"] = True
    elif percent_change < 0:
        st.error(f"Revenue has decreased by {abs(percent_change):.2f}%")
        st.session_state["is_revenue_up"] = False
    else:
        st.info("Revenue is stable")
        st.session_state["is_revenue_up"] = False

    st.dataframe(
        df.rename(columns={"index": "Quarter"}).assign(
            Quarter=lambda x: x["Quarter"].dt.strftime("%Y-%m-%d")
        ),
        hide_index=True,
    )
