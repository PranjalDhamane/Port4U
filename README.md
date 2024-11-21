# Port4U

The **Port4U** is a web-based tool built with Streamlit for analyzing and optimizing stock portfolios. It supports both single-ticker analysis and multi-ticker portfolio optimization, using key financial metrics to assess performance, manage risk, and enable informed investment decisions.

## Table of Contents
- [Features](#features)
- [Key Metrics](#key-metrics)
- [Installation](#installation)
- [Usage](#usage)
- [Financial Metrics Explained](#financial-metrics-explained)
- [References](#references)

---

## Features

### Single Ticker Analysis
- Calculate essential metrics, including Expected Annual Return, Volatility, Sharpe Ratio, Treynor Ratio, Jensen’s Alpha, and Value at Risk (VaR).
- Visualize stock price data with interactive candlestick and volume charts.

### Multi-Ticker Portfolio Optimization
- Optimize portfolios using Monte Carlo simulations to balance risk and return.
- Display the **Efficient Frontier** to visualize optimal risk-return profiles.
- Provide optimal portfolio weights for maximizing the Sharpe ratio.
- Show individual candlestick charts for each stock in the portfolio.

---

## Key Metrics

The app calculates and displays several critical financial metrics:
1. **Expected Annual Return**: Annualized return estimate based on historical data.
2. **Volatility**: Indicates the risk or variability of returns.
3. **Sharpe Ratio**: Measures return relative to risk using standard deviation.
4. **Treynor Ratio**: Risk-adjusted return metric using beta as the risk measure.
5. **Jensen’s Alpha**: Assesses excess return over expected return based on portfolio beta.
6. **Beta**: Measures sensitivity of the portfolio to market movements.
7. **Value at Risk (VaR)**: Estimates potential portfolio losses under normal market conditions.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Portfolio_Optimization_App.git
   cd Portfolio_Optimization_App
   ```

2. **Install Dependencies**:
   Ensure Python 3.7+ is installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the App**:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. **Launch the App**:
   From the root directory, use the Streamlit command:
   ```bash
   streamlit run app.py
   ```

2. **Choose Analysis Type**:
   - **Single Ticker Analysis**: Enter a ticker symbol, select a date range, and click "Run Analysis."
   - **Portfolio Optimization**: Enter multiple ticker symbols separated by commas, select a date range, and click "Run Analysis."

3. **View Results**:
   - **Metrics**: Displays Expected Annual Return, Volatility, Sharpe Ratio, Treynor Ratio, Jensen’s Alpha, Beta, and VaR.
   - **Visualization**:
     - **Candlestick Chart**: For each stock.
     - **Efficient Frontier** (for multiple tickers): Displays optimal portfolios maximizing the Sharpe ratio.
     - **Optimal Weights** (for multiple tickers): Allocation for achieving maximum Sharpe ratio.

---

## Financial Metrics Explained

### Performance Metrics
- **Expected Annual Return**: Annualized average of daily returns over the selected period.
- **Volatility**: Annualized standard deviation of daily returns, representing risk.

### Risk-Adjusted Metrics
1. **Sharpe Ratio**:
   \[
   \text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}
   \]
   Where \( R_p \) is portfolio return, \( R_f \) is the risk-free rate, and \( \sigma_p \) is portfolio volatility.
   
2. **Treynor Ratio**:
   \[
   \text{Treynor Ratio} = \frac{R_p - R_f}{\beta}
   \]
   Uses portfolio beta instead of volatility for risk.

3. **Jensen’s Alpha**:
   \[
   \text{Alpha} = R_p - [R_f + \beta \times (R_m - R_f)]
   \]
   Indicates excess returns over expected market-based returns.

### Volatility and Risk
1. **Standard Deviation**: Reflects portfolio return variability; higher values imply greater risk.
2. **Beta**: Measures sensitivity to market trends, with \( \beta > 1 \) indicating higher market volatility.
3. **Value at Risk (VaR)**: Estimates potential loss in portfolio value under normal market conditions.

### Portfolio Efficiency
- **Efficient Frontier**: Illustrates portfolios that maximize return for a given level of risk.

---

## References

1. [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
2. [Sharpe Ratio](https://www.investopedia.com/terms/s/sharperatio.asp)
3. [Treynor Ratio](https://www.investopedia.com/terms/t/treynorratio.asp)
4. [Jensen's Alpha](https://www.investopedia.com/terms/a/alphajensen.asp)
5. [Efficient Frontier](https://www.investopedia.com/terms/e/efficientfrontier.asp)
6. [Value at Risk (VaR)](https://www.investopedia.com/terms/v/var.asp)

---

## Conclusion

The **Portfolio Optimization App** provides valuable insights and visualizations for single-stock and multi-ticker portfolio analysis. Leveraging financial theories like Modern Portfolio Theory and risk-adjusted metrics, this tool helps investors make well-informed decisions to effectively manage and optimize their portfolios.

