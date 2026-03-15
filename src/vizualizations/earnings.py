import pandas as pd
import altair as alt
import streamlit as st


def earnings_met_expectations(df: pd.DataFrame, n_quarters: int = 2) -> bool:
    df = df.dropna(subset=["epsActual", "epsEstimate"])

    if df.empty:
        return False

    recent = df.tail(n_quarters)

    results = []
    for _, row in recent.iterrows():
        actual = row["epsActual"]
        estimate = row["epsEstimate"]

        # Allow a small tolerance for "meeting"
        if actual >= estimate * 0.98:
            results.append(True)
        else:
            results.append(False)

    return all(results)


def plot_earnings_history_data(data: pd.DataFrame):
    df = data.reset_index()

    # Check expectations
    meets_expectations = earnings_met_expectations(df)

    st.subheader("Recent Earnings and Expectations")

    # Chart logic
    df_long = df.melt(
        id_vars="quarter",
        value_vars=["epsActual", "epsEstimate"],
        var_name="Metric",
        value_name="EPS",
    )

    chart = (
        alt.Chart(df_long)
        .mark_line(point=True)
        .encode(
            x="quarter",
            y="EPS",
            color="Metric",
        )
        .properties(title="Earnings History")
    )

    st.altair_chart(chart, width="stretch")

    if meets_expectations:
        st.success("Recent earnings met or beat analyst expectations")
        st.session_state["earnings_met_expectations"] = True
    else:
        st.error("Recent earnings missed analyst expectations")
        st.session_state["earnings_met_expectations"] = False

    st.dataframe(df)
