# DSCI 521 Final Project
**Author:** Jin Ting Zhao

## Table of Contents

- [Medium-Term Stock Predictor](#medium-term-stock-predictor)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Analysis](#analysis)
  - [A. Earnings and Revenue](#a-earnings-and-revenue)
  - [B. Valuation and Expectations](#b-valuation-and-expectations)
  - [C. News](#c-news)
- [Final Scoring Logic](#final-scoring-logic)

## Medium-Term Stock Predictor
This project is designed to assist investors in making informed decisions on whether to buy a stock. The prediction model considers the following factors:

1. **Stock Price**
2. **Earnings & Revenue**
3. **Earnings per Share (EPS)**
4. **Profit Margin**
5. **Recent Earnings and Expectations**
6. **P/E Ratio vs. Historical Range**
7. **PEG Ratio**
8. **News Sentiment**

These features are used collectively to provide a medium-term outlook on stock performance.

## Getting Started
To get started, run the provided bash script:

```bash
./start-here.sh
```
**Notes**: 
* These are MacOS-focused instructions
* This is dependent that the user has Python 3.14 and `uv` on their system. 
* I decided to use `uv` since it speeds up the package depedency process.


## Project Structure

The project is organized to separate data processing, visualization, and application logic for clarity and maintainability. The main content is located in the `/src` folder, which contains all the source code.

### Folder and Module Overview

- **`/src/calculations`**  
  Contains all modules for data processing and financial computations, including stock metrics and quarterly financial analysis.

- **`/src/visualizations`**  
  Contains modules that generate interactive charts using **Altair**, converting processed data into visual insights.

- **`stocks.py`**  
  Fetches historical stock data for a given ticker, currently set to retrieve **3 years of data**, which is used for analysis and visualization.

- **`main.py`**  
  The main entry point for the project. Integrates calculations, visualizations, and user interaction into a **Streamlit** application.

- **`/data`**  
  Stores supporting static data, such as a list of stock ticker symbols used for the dropdown menu in the UI.


## Analysis:
### A. Earnings and Revenue
1. Revenue
   - shows the total revenue (in billions $) over the past year in a line graph
   - percent change difference to determine the total revenue trend increasing or decreasing consistenly over the last 2-3 quarters
2. Earnings per Share (EPS)
   - line graph of the EPS over the past year
   - if th eEPS the last 4 quarters trend is imprving or going up, then it gets a checkmark
   - if EPS is shrinking or volatile, then no checkmark
   - percent change difference to determine the EPS trend
3. Profit Margin (operating margin) - needed to calculate
   - operating margin = (operating income/total revenue)*100 calculated for the stock ticker that user inputs
   - percent change difference determines if checkmark for profit margin or ot
   - if margins are flat or rising --> checkmark
   - if margins are shrinking consistenly --> no checkmark
4. Recent Earnings and Expectations
   - looks at the recent earnings for the last 1-2 earnings
   - if company beats or meets expectations --> checkmark
   - if company missed badly without explaination --> no checkmark
   - percent change difference determines if checkmark for recent earnings category or not
     
### B. Valuation and Expectations
1. P/E Ratio vs. Historical Range
   - looks at current P/E ratio and the historical P/E avg. for 3-5 years
   - if P/E ratio vs historical average is near or below historical avg --> checkmark
   - if P/E ratio vs historical average is far above without faster growth --> no checkmark
3. PEG Ratio (needed to calculate)
   - looks at the PEG ratio over the last year
   - PEG Ratio = (current PE/annual EPS growth)
   - if PEG ratio <2 --> checkbox
   - if PEG Ratio >= 2 --> check if stock price is overpriced for growth by historical prices:
     - if current P/E <=5 year average P/E , then reasonable --> gets a checkmark
     - if current P/E > 5 year average P/E , then means growth expectations --> no checkmark
    
### C. News
- Gets news articles directly from Yahoo Finance
- Includes publicly available financial and investor news
- Uses the VADER model to measure the sentiment of each news article
- VADER Sentiment Score Range:

   | Score Range | Sentiment |
   |-------------|-----------|
   | 0.05 – 1.0   | Positive  |
   | -0.05 – 0.05 | Neutral  |
   | -0.05 – -1.0  | Negative |


## Challenges
* When trying to find the best free version, there were a lot of services that required creating API keys, had restriction API limits, or required credit card information.
* The main challenge was discovering what data was available in YFinance since some methods were deprecated
* There are much more financial metrics that could have been analyzed, the top few were selected
* Since it is a prediction, anything could happen on the news, that could affect the stock price
   - Example: War, political tensions/regulations, job market, pandemic, etc


## Final Scoring Logic

Each category receives a checkmark if the condition is satisfied.

| No. Checked Boxes | Signal |
|-------------------|--------|
| 6–8 | Likely Rise |
| 4–5 | Stay Flat / Volatile |
| 3 or less | Negative Outlook |


     
