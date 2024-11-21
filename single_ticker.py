import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import streamlit as st
from scipy.stats import norm  # For VaR calculation

# Fetch data for a single ticker
def fetch_single_ticker_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    if data.empty:
        raise ValueError(f"No data fetched for the ticker: {ticker} and date range.")
    
    returns = data['Adj Close'].pct_change().dropna()
    return data, returns

# Function to calculate single asset performance
def single_asset_performance(returns):
    mean_returns = returns.mean() * 252  # Annualized return
    std_dev = returns.std() * np.sqrt(252)  # Annualized volatility
    return mean_returns, std_dev

# Sharpe Ratio calculation
def sharpe_ratio_single(mean_returns, std_dev, risk_free_rate=0.01):
    return (mean_returns - risk_free_rate) / std_dev

# Sortino Ratio calculation
def sortino_ratio_single(returns, risk_free_rate=0.01):
    downside_deviation = np.std(returns[returns < 0]) * np.sqrt(252)
    annualized_return = returns.mean() * 252
    return (annualized_return - risk_free_rate) / downside_deviation

# Maximum Drawdown calculation
def calculate_max_drawdown(data):
    cumulative_return = (1 + data['Adj Close'].pct_change()).cumprod()
    drawdown = cumulative_return / cumulative_return.cummax() - 1
    max_drawdown = drawdown.min()
    return max_drawdown

# Compound Annual Growth Rate (CAGR)
def calculate_cagr(data):
    start_value = data['Adj Close'].iloc[0]
    end_value = data['Adj Close'].iloc[-1]
    num_years = len(data) / 252  # Approximation for trading days in a year
    cagr = (end_value / start_value) ** (1 / num_years) - 1
    return cagr

# Value at Risk (VaR) calculation
def calculate_var(returns, confidence_level=0.95):
    mean = np.mean(returns)
    std_dev = np.std(returns)
    var = norm.ppf(1 - confidence_level) * std_dev - mean
    return var

# Monte Carlo simulation for single asset
def monte_carlo_simulation_single(mean_return, std_dev, num_simulations=1000, initial_investment=10000):
    simulated_prices = []
    for _ in range(num_simulations):
        daily_return = np.random.normal(mean_return / 252, std_dev / np.sqrt(252), 252)
        price_series = [initial_investment * (1 + r) for r in np.cumprod(1 + daily_return)]
        simulated_prices.append(price_series[-1])
    return simulated_prices

# Function to display financial metrics
def display_financial_metrics(mean_return, volatility, sharpe_ratio, sortino, var, max_drawdown, cagr):
    metrics = {
        "Metric": [
            "Expected Annual Return", 
            "Annual Volatility (Risk)", 
            "Sharpe Ratio", 
            "Sortino Ratio",
            "Value at Risk (VaR)", 
            "Maximum Drawdown", 
            "Compound Annual Growth Rate (CAGR)"
        ],
        "Value": [
            f"{mean_return:.4f}", 
            f"{volatility:.4f}", 
            f"{sharpe_ratio:.4f}", 
            f"{sortino:.4f}", 
            f"{var:.4f}", 
            f"{max_drawdown:.4f}", 
            f"{cagr:.4f}"
        ]
    }
    
    df_metrics = pd.DataFrame(metrics)
    st.write("### Financial Metrics")
    st.table(df_metrics)
    return df_metrics

# Function to plot candlestick chart
def plot_candlestick_chart(data, ticker):
    if "Volume" not in data.columns:
        st.error(f"Error: Volume data not available for {ticker}.")
        return
    
    data_ohlc = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    mpf.plot(data_ohlc, type='candle', volume=True, title=f'Candlestick chart for {ticker}', style='yahoo')
    st.pyplot(plt.gcf())

# Function to run single ticker analysis
def run_single_ticker_analysis(ticker, start_date, end_date):
    try:
        # Fetch data and calculate returns
        stock_data, stock_returns = fetch_single_ticker_data(ticker, start=start_date, end=end_date)

        # Calculate financial metrics
        mean_return, volatility = single_asset_performance(stock_returns)
        sharpe = sharpe_ratio_single(mean_return, volatility)
        sortino = sortino_ratio_single(stock_returns)
        var = calculate_var(stock_returns)
        max_drawdown = calculate_max_drawdown(stock_data)
        cagr = calculate_cagr(stock_data)

        # Display financial metrics
        df_metrics = display_financial_metrics(mean_return, volatility, sharpe, sortino, var, max_drawdown, cagr)

        # Monte Carlo Simulation
        simulated_prices = monte_carlo_simulation_single(mean_return, volatility)
        

        # Plot candlestick chart
        plot_candlestick_chart(stock_data, ticker)

        return df_metrics

    except Exception as e:
        st.error(f"Error: {e}")

# Run the application
if __name__ == "__main__":
    st.title("Stock Portfolio Optimization")
    ticker = st.text_input("Enter Stock Ticker", "AAPL")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))
    
    if st.button("Analyze"):
        run_single_ticker_analysis(ticker, start_date, end_date)
