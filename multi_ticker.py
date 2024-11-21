import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import streamlit as st
from scipy.stats import norm

# Fetch data for multiple tickers
def fetch_multiple_ticker_data(tickers, start, end):
    all_data = {}
    all_returns = {}
    for ticker in tickers:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            raise ValueError(f"No data fetched for the ticker: {ticker} and date range.")
        
        returns = data['Adj Close'].pct_change().dropna()
        all_data[ticker] = data
        all_returns[ticker] = returns
    return all_data, pd.DataFrame(all_returns)

# Calculate financial metrics for multiple tickers
def calculate_financial_metrics(returns, tickers, risk_free_rate=0.01, confidence_level=0.95):
    metrics = []
    for ticker in tickers:
        mean_return = returns[ticker].mean() * 252
        volatility = returns[ticker].std() * np.sqrt(252)
        sharpe_ratio = (mean_return - risk_free_rate) / volatility
        var = norm.ppf(1 - confidence_level) * returns[ticker].std() - returns[ticker].mean()
        
        metrics.append({
            'Ticker': ticker,
            'Expected Annual Return': mean_return,
            'Annual Volatility': volatility,
            'Sharpe Ratio': sharpe_ratio,
            'VaR (95%)': var
        })
    return pd.DataFrame(metrics)

# Monte Carlo simulation for efficient frontier
def monte_carlo_simulation(mean_returns, cov_matrix, num_portfolios=5000, risk_free_rate=0.01):
    num_assets = len(mean_returns)
    results = np.zeros((3, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)

        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_volatility

    return results, weights_record

# Plot efficient frontier
def plot_efficient_frontier(results):
    max_sharpe_idx = np.argmax(results[2])
    min_vol_idx = np.argmin(results[1])

    plt.figure(figsize=(10, 6))
    plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='viridis', marker='o', alpha=0.6)
    plt.colorbar(label='Sharpe Ratio')

    # Highlight max Sharpe ratio portfolio
    plt.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx], c='red', marker='*', s=200, label='Max Sharpe Ratio')
    # Highlight minimum volatility portfolio
    plt.scatter(results[1, min_vol_idx], results[0, min_vol_idx], c='blue', marker='*', s=200, label='Min Volatility')

    plt.title('Efficient Frontier')
    plt.xlabel('Volatility (Risk)')
    plt.ylabel('Expected Return')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt.gcf())

# Candlestick chart plotting
def plot_candlestick_charts_for_multiple_tickers(stock_data):
    for ticker, data in stock_data.items():
        st.write(f"**Candlestick Chart for {ticker}**")
        if "Volume" not in data.columns:
            st.error(f"Error: Volume data not available for {ticker}.")
            continue

        data_ohlc = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        mpf.plot(data_ohlc, type='candle', volume=True, title=f'Candlestick chart for {ticker}', style='yahoo')
        st.pyplot(plt.gcf())

# Display financial metrics
def display_financial_metrics(metrics_df):
    st.write("### Metrics Table for Multiple Ticker Analysis")
    st.table(metrics_df)

# Run multiple ticker analysis
def run_multiple_ticker_analysis(tickers, start_date, end_date):
    try:
        # Fetch data
        stock_data, stock_returns = fetch_multiple_ticker_data(tickers, start=start_date, end=end_date)

        # Calculate metrics
        metrics_df = calculate_financial_metrics(stock_returns, tickers)

        # Display financial metrics
        display_financial_metrics(metrics_df)

        # Monte Carlo Simulation
        mean_returns = stock_returns.mean() * 252
        cov_matrix = stock_returns.cov() * 252
        results, weights_record = monte_carlo_simulation(mean_returns, cov_matrix)

        # Plot Efficient Frontier
        plot_efficient_frontier(results)

        # Plot candlestick charts
        plot_candlestick_charts_for_multiple_tickers(stock_data)

        return metrics_df, stock_data
    
    except Exception as e:
        st.error(f"Error: {e}")
