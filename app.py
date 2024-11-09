# app.py
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from single_ticker import run_single_ticker_analysis
from multi_ticker import run_multiple_ticker_analysis
from gemini import table_explaination, gemini_model

def main():
    st.title("Port4U")

    # Initialize session state variables to hold data across interactions
    if 'df_metrics' not in st.session_state:
        st.session_state.df_metrics = None

    if 'analysis_type' not in st.session_state:
        st.session_state.analysis_type = None

    # User selection for single ticker or multiple ticker analysis
    analysis_type = st.radio("Choose analysis type:", ('Single Ticker Analysis', 'Double Ticker Analysis'))
    st.session_state.analysis_type = analysis_type

    # Render input boxes conditionally based on analysis type
    if analysis_type == 'Single Ticker Analysis':
        ticker = st.text_input("Enter a stock ticker (e.g., AAPL):")
    
    elif analysis_type == 'Double Ticker Analysis':
        ticker_1 = st.text_input("Enter the first stock ticker (e.g., AAPL):")
        ticker_2 = st.text_input("Enter the second stock ticker (e.g., MSFT):")

    # Date range selection (common for both types of analysis)
    start_date = st.date_input("Start Date", value=pd.to_datetime("2018-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))

    # Run Analysis button
    if st.button("Run Analysis"):
        if analysis_type == 'Single Ticker Analysis' and ticker:
            # Perform analysis and store the results in session state
            st.session_state.df_metrics = run_single_ticker_analysis(ticker.strip().upper(), start_date, end_date)
        
        elif analysis_type == 'Double Ticker Analysis' and ticker_1 and ticker_2:
            tickers = [ticker_1.strip().upper(), ticker_2.strip().upper()]
            # Perform analysis and store the results in session state
            st.session_state.df_metrics = run_multiple_ticker_analysis(tickers, start_date, end_date)
        else:
            st.error("Please enter valid stock tickers for the selected analysis type.")

    # Display the analysis results if available in session state
    if st.session_state.df_metrics is not None:
        st.dataframe(st.session_state.df_metrics)

        # Button to generate the explanation
        if st.button("Explain Analysis"):
            with st.spinner("Generating explanation..."):
                explanation = table_explaination(st.session_state.df_metrics)
                st.write(explanation)

if __name__ == '__main__':
    main()
