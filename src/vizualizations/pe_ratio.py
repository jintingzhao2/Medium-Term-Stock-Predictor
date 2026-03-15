import streamlit as st

from calculations.pe_ratio import compare_pe_ratio_vs_pe_average, calculate_peg_ratio


def show_pe_peg(stock):
    pe_col, peg_col = st.columns(2)

    # P/E Ratio Comparison
    with pe_col:
        st.subheader("📊 P/E Ratio Comparison")
        c_pe, a_pe = compare_pe_ratio_vs_pe_average(stock)
        if c_pe is not None and a_pe is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current P/E", f"{c_pe:.2f}")
            with col2:
                st.metric("5Y Avg P/E", f"{a_pe:.2f}")
            if c_pe < a_pe:
                st.session_state["is_pe_good"] = True
                st.success("Current P/E is below 5-year average")
            else:
                st.session_state["is_pe_good"] = False
                st.warning("Current P/E is above 5-year average")
        else:
            st.info("P/E data not available")
            st.session_state["is_pe_good"] = False

    # PEG Ratio
    with peg_col:
        st.subheader("📈 PEG Ratio")
        p_val, _, _, _ = calculate_peg_ratio(stock)
        if p_val is not None:
            st.metric(
                "PEG Ratio",
                f"{p_val:.2f}",
            )
        else:
            st.info("PEG data not available")

        if p_val is not None:
            if p_val < 2:
                st.session_state["is_peg_good"] = True
                st.success("PEG Ratio indicates fair valuation")
            else:
                st.session_state["is_peg_good"] = False
                st.error("PEG Ratio indicates overvaluation")

    st.divider()  # optional visual separation
