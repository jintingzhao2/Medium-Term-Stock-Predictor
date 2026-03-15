# DSCI 521 Final Project
**Author:** Jin Ting Zhao

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

Analysis:
A. Earnings and Revenue
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
     
B. Valuation and Expectations
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
    
C. News
- gets news articles directly from Yahoo Finance
- news articles in public eyes
- investigator news
- VADER model used to measure the sentiment of the news article
- VADER sentiment score range summary: 
    Score Range  |   Sentiment
  0.05 - 1.0     |   Positive
  -0.05 - 0.05   |   Neutral
  -1.0 - 0.05    |   Negative
  
  


Final Scoring Logic: 
No. Checked boxes:   |     Signal:
       6-8       |    likely rise 
       4-5       |    stay flat/volatile
     3 or less   |    negative outlook 



     
