import streamlit as st


def show_news(news_data: list[dict], average_sentiment: float) -> None:
    if average_sentiment > 0.05:
        st.session_state["is_sent_pos"] = True
        st.success(f"Overall Average Positive Sentiment: {average_sentiment:.2f}")
    elif average_sentiment < -0.05:
        st.session_state["is_sent_pos"] = False
        st.error(f"Overall Average Negative Sentiment: {average_sentiment:.2f}")
    else:
        st.session_state["is_sent_pos"] = False
        st.info(f"Overall Average Neutral Sentiment: {average_sentiment:.2f}")

    cols = st.columns(3)
    for i, news_item in enumerate(news_data):
        with cols[i % 3]:
            if news_item["image_url"]:
                st.image(news_item["image_url"], width="stretch")
            # Label sentiment visually for the user
            s_color = (
                "green"
                if news_item["sentiment_score"] > 0.05
                else "red"
                if news_item["sentiment_score"] < -0.05
                else "gray"
            )
            st.markdown(
                f":{s_color}[Sentiment Score: {news_item['sentiment_score']:.2f}]"
            )
            st.markdown(f"**[{news_item['title']}]({news_item['url']})**")
            st.caption(f"Published: {news_item['published_date']}")
            st.divider()
