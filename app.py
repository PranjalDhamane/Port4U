# app.py
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from single_ticker import run_single_ticker_analysis
from multi_ticker import run_multiple_ticker_analysis
from gemini import table_explaination, gemini_model

# Set up the page config
st.set_page_config(page_title="Port4U", layout="wide")

# CSS for custom styling
st.markdown(
    """
    <style>
    /* Custom styles here */
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with navigation
st.sidebar.image('PORT4U.png')
st.sidebar.header("Navigation")
# Sidebar with navigation
page = st.sidebar.radio("Go to", ["Home", "Single Ticker Analysis", "Multiple Ticker Analysis"])

# Main content based on selection
if page == "Home":
    st.title("Welcome to")
    st.image('PORT4U.png')
    st.write(
        """
        Port4U is your one-stop financial analysis tool for in-depth stock insights. 
        Select an analysis option from the sidebar to get started.
        """
    )

elif page == "Single Ticker Analysis":
    st.title("Single Ticker Analysis")
    ticker = st.text_input(
        "Enter a stock ticker (e.g., AAPL):",
        placeholder="Enter ticker symbol",
        help="Input the stock symbol for the company you wish to analyze (e.g., AAPL for Apple Inc.)."
    )
    start_date = st.date_input(
        "Start Date", value=pd.to_datetime("2018-01-01"),
        help="Choose the starting date for the analysis period."
    )
    end_date = st.date_input(
        "End Date", value=pd.to_datetime("2023-01-01"),
        help="Choose the end date for the analysis period."
    )

    # Button to trigger analysis
    if st.button("🚀 Run Analysis", help="Click to run the stock analysis based on the entered ticker and date range."):
        if ticker:
            st.session_state.df_metrics = run_single_ticker_analysis(ticker.strip().upper(), start_date, end_date)
            st.session_state.explain_analysis = False  # Reset explanation flag
        else:
            st.error("Please enter a valid stock ticker.")

    # Display financial metrics if available
    if st.session_state.get("df_metrics") is not None:
        

        # Button to trigger explanation
        if st.button("✨ Explain Analysis", help="Click to generate an explanation for the analysis results displayed above."):
            st.session_state.explain_analysis = True

    # Display explanation if triggered
    if st.session_state.get("explain_analysis", False):
        with st.spinner("Generating explanation..."):
            explanation = table_explaination(st.session_state.df_metrics)
            st.write(explanation)

elif page == "Multiple Ticker Analysis":
    st.title("Multiple Ticker Analysis")
    tickers = st.text_area(
        "Enter stock tickers (e.g., AAPL, MSFT, GOOG):",
        placeholder="Enter ticker symbols separated by commas",
        help="Input stock symbols for multiple companies separated by commas (e.g., AAPL, MSFT, GOOG)."
    )
    start_date = st.date_input(
        "Start Date", value=pd.to_datetime("2018-01-01"),
        help="Choose the starting date for the analysis period."
    )
    end_date = st.date_input(
        "End Date", value=pd.to_datetime("2023-01-01"),
        help="Choose the end date for the analysis period."
    )

    # Button to trigger analysis
    if st.button("🚀 Run Analysis", help="Click to run the analysis for the specified tickers within the chosen date range."):
        if tickers:
            # Split tickers by commas and strip whitespace
            ticker_list = [ticker.strip().upper() for ticker in tickers.split(",") if ticker.strip()]
            
            if len(ticker_list) > 1:  # Ensure at least two tickers are provided
                try:
                    df_metrics, *_ = run_multiple_ticker_analysis(ticker_list, start_date, end_date)
                    st.session_state.df_metrics = df_metrics  # Store only the DataFrame
                    st.session_state.explain_analysis = False  # Reset explanation flag
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
            else:
                st.error("Please enter at least two valid stock tickers.")
        else:
            st.error("Please enter stock tickers.")

    # Display financial metrics if available
    if "df_metrics" in st.session_state and isinstance(st.session_state.df_metrics, pd.DataFrame):
        

        # Button to trigger explanation
        if st.button("✨ Explain Analysis", help="Click to generate an explanation for the analysis results displayed above."):
            st.session_state.explain_analysis = True

    # Display explanation if triggered
    if st.session_state.get("explain_analysis", False):
        with st.spinner("Generating explanation..."):
            explanation = table_explaination(st.session_state.df_metrics)
            st.write(explanation)
