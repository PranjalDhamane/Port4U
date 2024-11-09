import streamlit as st
import pandas as pd
from single_ticker import run_single_ticker_analysis
from multi_ticker import run_multiple_ticker_analysis

def main():
    st.title(" Stock Portfolio Optimization App")

    # User selection for single ticker or multiple ticker analysis
    analysis_type = st.radio("Choose analysis type:", ('Single Ticker Analysis', 'Double Ticker Analysis'))

    # Render input boxes conditionally based on analysis type
    if analysis_type == 'Single Ticker Analysis':
        ticker = st.text_input("Enter a stock ticker (e.g., AAPL):")  # Single input for one ticker
    
    elif analysis_type == 'Double Ticker Analysis':
        ticker_1 = st.text_input("Enter the first stock ticker (e.g., AAPL):")
        ticker_2 = st.text_input("Enter the second stock ticker (e.g., MSFT):")

    # Date range selection (common for both types of analysis)
    start_date = st.date_input("Start Date", value=pd.to_datetime("2018-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))

    if st.button("Run Analysis"):
        if analysis_type == 'Single Ticker Analysis':
            if ticker:  # Check if a ticker is entered
                run_single_ticker_analysis(ticker.strip().upper(), start_date, end_date)
            else:
                st.error("Please enter a valid stock ticker.")
        
        elif analysis_type == 'Double Ticker Analysis':
            tickers = [ticker_1.strip().upper(), ticker_2.strip().upper()]
            if all(tickers):  # Check if both tickers are entered
                run_multiple_ticker_analysis(tickers, start_date, end_date)
            else:
                st.error("Please enter valid stock tickers for both inputs.")

if __name__ == '__main__':
    main()
