import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from scipy.stats import norm  # For VaR calculation
import streamlit as st

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

# Value at Risk (VaR) calculation
def calculate_var(returns, confidence_level=0.95):
    mean = np.mean(returns)
    std_dev = np.std(returns)
    var = norm.ppf(1 - confidence_level) * std_dev - mean
    return var

# Function to display financial metrics
def display_financial_metrics(mean_return, volatility, sharpe_ratio, var):
    metrics = {
        "Metric": ["Expected Annual Return", "Annual Volatility (Risk)", "Sharpe Ratio", "Value at Risk (VaR)"],
        "Value": [f"{mean_return:.4f}", f"{volatility:.4f}", f"{sharpe_ratio:.4f}", f"{var:.4f}"]
    }
    
    df_metrics = pd.DataFrame(metrics)
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
        stock_data, stock_returns = fetch_single_ticker_data(ticker, start=start_date, end=end_date)

        mean_return, volatility = single_asset_performance(stock_returns)
        sharpe = sharpe_ratio_single(mean_return, volatility)
        var = calculate_var(stock_returns)

        # Display financial metrics
        df_metrics = display_financial_metrics(mean_return, volatility, sharpe, var)
        
    
        # Display candlestick chart
        plot_candlestick_chart(stock_data, ticker)
        return df_metrics
    
    except Exception as e:
        st.error(f"Error: {e}")