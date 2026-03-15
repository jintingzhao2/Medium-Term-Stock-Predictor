import yfinance as yf

from calculations.eps import calculate_earnings_per_share


def compare_pe_ratio_vs_pe_average(stock: yf.Ticker, period="5y"):
    hist_prices = stock.history(period=period)["Close"]
    current_pe = stock.info.get("trailingPE")
    eps_ttm = stock.info.get("trailingEps")
    if current_pe is None or eps_ttm is None:
        return None, None
    avg_pe = (hist_prices / eps_ttm).mean()
    return current_pe, avg_pe


def calculate_peg_ratio(stock: yf.Ticker):
    try:
        eps_series = calculate_earnings_per_share(stock)["Basic EPS"]
        annual_eps_growth = (eps_series.pct_change() * 100)[-4:].sum()
        current_pe = stock.info.get("trailingPE")
        if current_pe and annual_eps_growth:
            return (
                current_pe / annual_eps_growth,
                annual_eps_growth,
                current_pe,
                eps_series,
            )
    except:
        pass
    return None, None, None, None
