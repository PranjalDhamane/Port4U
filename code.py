import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import cvxpy as cp
import logging
import mplfinance as mpf  # For candlestick charts
from scipy.stats import norm  # For VaR calculation

# Set up logging
logging.basicConfig(level=logging.ERROR, filename="portfolio_optimization_errors.log")

# Enhanced function to fetch stock data including Volume for candlestick chart with detailed error handling
def fetch_data(tickers, start, end):
    all_data = {}
    all_returns = {}
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start, end=end)
            if data.empty:
                raise ValueError(f"No data fetched for the ticker: {ticker} and date range.")
            
            returns = data['Adj Close'].pct_change().dropna()
            all_data[ticker] = data
            all_returns[ticker] = returns
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
            raise ValueError(f"Error fetching data for {ticker}: {e}")
    return all_data, pd.DataFrame(all_returns)

# Function to calculate single asset performance
def single_asset_performance(returns):
    mean_returns = returns.mean() * 252  # Annualized return
    std_dev = returns.std() * np.sqrt(252)  # Annualized volatility
    return mean_returns, std_dev

# Function to calculate Sharpe Ratio for single ticker
def sharpe_ratio_single(mean_returns, std_dev, risk_free_rate=0.01):
    return (mean_returns - risk_free_rate) / std_dev

# Calculate Treynor Ratio
def treynor_ratio(returns, beta, risk_free_rate=0.01):
    return (returns - risk_free_rate) / beta

# Calculate Jensen's Alpha
def jensens_alpha(returns, beta, market_return, risk_free_rate=0.01):
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    return returns - expected_return

# Calculate Beta
def calculate_beta(stock_returns, market_returns):
    cov_matrix = np.cov(stock_returns, market_returns)
    beta = cov_matrix[0, 1] / cov_matrix[1, 1]  # cov(stock, market) / var(market)
    return beta

# Value at Risk (VaR) calculation
def calculate_var(returns, confidence_level=0.95):
    mean = np.mean(returns)
    std_dev = np.std(returns)
    var = norm.ppf(1 - confidence_level) * std_dev - mean
    return var

# Monte Carlo simulation for efficient frontier (multiple tickers)
def monte_carlo_simulation(mean_returns, cov_matrix, num_portfolios=5000, risk_free_rate=0.01):
    num_assets = len(mean_returns)
    results = np.zeros((3, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        # Generate random portfolio weights
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)

        # Calculate portfolio return and volatility
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        # Store results
        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = (portfolio_return - risk_free_rate) / portfolio_volatility

    return results, weights_record

# Plot efficient frontier for multiple ticker analysis
def plot_efficient_frontier(results):
    max_sharpe_idx = np.argmax(results[2])
    
    plt.figure(figsize=(10, 6))
    plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='viridis', marker='o', alpha=0.6)
    plt.colorbar(label='Sharpe Ratio')

    plt.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx], c='red', marker='*', s=200, label='Max Sharpe Ratio')
    plt.title('Efficient Frontier')
    plt.xlabel('Volatility (Risk)')
    plt.ylabel('Expected Return')
    plt.legend()
    st.pyplot(plt.gcf())

# Function to plot candlestick chart for single ticker
def plot_candlestick_chart(data, ticker):
    if "Volume" not in data.columns:
        st.error(f"Error: Volume data not available for {ticker}.")
        return
    
    data_ohlc = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    mpf.plot(data_ohlc, type='candle', volume=True, title=f'Candlestick chart for {ticker}', style='yahoo')
    st.pyplot(plt.gcf())

# Function to plot candlestick chart for multiple tickers
def plot_candlestick_charts_for_multiple_tickers(stock_data):
    for ticker, data in stock_data.items():
        st.write(f"**Candlestick Chart for {ticker}**")
        if "Volume" not in data.columns:
            st.error(f"Error: Volume data not available for {ticker}.")
            continue
        
        data_ohlc = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        mpf.plot(data_ohlc, type='candle', volume=True, title=f'Candlestick chart for {ticker}', style='yahoo')
        st.pyplot(plt.gcf())

# Display financial metrics (standardized for both single and multiple tickers)
def display_financial_metrics(mean_return, volatility, sharpe_ratio, beta=None, treynor=None, jensens_alpha=None, var=None):
    st.write(f"**Expected Annual Return:** {mean_return:.4f}")
    st.write(f"**Annual Volatility (Risk):** {volatility:.4f}")
    st.write(f"**Sharpe Ratio:** {sharpe_ratio:.4f}")
    if beta is not None:
        st.write(f"**Beta:** {beta:.4f}")
    if treynor is not None:
        st.write(f"**Treynor Ratio:** {treynor:.4f}")
    if jensens_alpha is not None:
        st.write(f"**Jensen's Alpha:** {jensens_alpha:.4f}")
    if var is not None:
        st.write(f"**Value at Risk (VaR):** {var:.4f}")

# Streamlit app function
def main():
    st.title("Portfolio Optimization App")
    
    # User selection for single ticker or multiple ticker analysis
    analysis_type = st.radio("Choose analysis type:", ('Single Ticker Analysis', 'Multiple Ticker Analysis'))

    # User input for tickers and date range
    tickers_input = st.text_input("Enter stock tickers separated by commas (e.g., AAPL, MSFT, GOOGL):")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2018-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))

    if st.button("Run Analysis"):
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]  # Ensure tickers are uppercase
        
        if tickers:
            try:
                # Fetch stock data and returns
                stock_data, stock_returns = fetch_data(tickers, start=start_date, end=end_date)
                
                # Single Ticker Analysis
                if analysis_type == 'Single Ticker Analysis' and len(tickers) == 1:
                    mean_return, volatility = single_asset_performance(stock_returns[tickers[0]])
                    sharpe = sharpe_ratio_single(mean_return, volatility)

                    # Calculate Beta, Treynor Ratio, Jensen's Alpha, and VaR
                    market_data = yf.download("^GSPC", start=start_date, end=end_date)['Adj Close'].pct_change().dropna()
                    beta = calculate_beta(stock_returns[tickers[0]], market_data)
                    treynor = treynor_ratio(mean_return, beta)
                    j_alpha = jensens_alpha(mean_return, beta, market_return=0.10)
                    var = calculate_var(stock_returns[tickers[0]])

                    # Display financial metrics
                    display_financial_metrics(mean_return, volatility, sharpe, beta, treynor, j_alpha, var)

                    # Display candlestick chart
                    plot_candlestick_chart(stock_data[tickers[0]], tickers[0])
                
                # Multiple Ticker Portfolio Optimization
                elif analysis_type == 'Multiple Ticker Analysis' and len(tickers) > 1:
                    mean_returns = stock_returns.mean() * 252
                    cov_matrix = stock_returns.cov() * 252

                    # Run Monte Carlo Simulation
                    results, weights_record = monte_carlo_simulation(mean_returns, cov_matrix)

                    # Display Efficient Frontier
                    plot_efficient_frontier(results)

                    # Display optimal weights for max Sharpe ratio portfolio
                    max_sharpe_idx = np.argmax(results[2])
                    st.write("Optimal Weights for Maximum Sharpe Ratio Portfolio:")
                    for i, ticker in enumerate(tickers):
                        st.write(f"{ticker}: {weights_record[max_sharpe_idx][i]:.4f}")

                    # Calculate Portfolio Expected Return, Volatility, and Sharpe Ratio
                    portfolio_return = results[0, max_sharpe_idx]
                    portfolio_volatility = results[1, max_sharpe_idx]
                    portfolio_sharpe = results[2, max_sharpe_idx]

                    # Display Portfolio Metrics
                    display_financial_metrics(portfolio_return, portfolio_volatility, portfolio_sharpe)

                    # Display candlestick charts for all tickers in the portfolio
                    plot_candlestick_charts_for_multiple_tickers(stock_data)
                
                else:
                    st.warning("Please enter a valid selection for analysis.")

            except ValueError as ve:
                st.error(f"Value Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}. Please check the error log for more details.")
                logging.error(f"Unhandled exception: {e}")
        else:
            st.warning("Please enter valid stock tickers.")

if __name__ == '__main__':
    main()
