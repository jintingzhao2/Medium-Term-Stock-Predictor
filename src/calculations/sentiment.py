import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import yfinance as yf
import nltk

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


def get_news_with_sentiment(ticker: yf.Ticker) -> tuple[list[dict], float]:
    sid = SentimentIntensityAnalyzer()
    try:
        news = ticker.news
    except Exception:
        return [], 0

    output = []
    sentiment_scores = []

    for item in news:
        content = item.get("content")
        if not isinstance(content, dict):
            # Skip if content is None or not a dict
            continue

        title = content.get("title", "")
        summary = content.get("summary", "")
        pub_date = content.get("pubDate", "")
        image_url = (content.get("thumbnail") or {}).get("originalUrl", "")
        url = (content.get("canonicalUrl") or {}).get("url", "")

        score = sid.polarity_scores(title)["compound"]
        sentiment_scores.append(score)

        output.append(
            {
                "title": title,
                "summary": summary,
                "published_date": pub_date,
                "image_url": image_url,
                "url": url,
                "sentiment_score": score,
            }
        )

    avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
    return output, avg_sentiment
