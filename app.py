# app.py
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from single_ticker import run_single_ticker_analysis
from multi_ticker import run_multiple_ticker_analysis
from gemini import table_explaination, gemini_model

# Set up the page config
st.set_page_config(page_title="Port4U", page_icon="/mnt/data/PORT4U.png", layout="wide")

# CSS for custom styling
st.markdown(
    """
    <style>
    /* Style the sidebar */
    .css-18e3th9 {
        background-color: #2B3467; /* Dark theme color */
        color: #FFFFFF;
    }
    .css-1d391kg {
        background-color: #2B3467; /* Sidebar color */
    }
    .css-1avcm0n {
        background-color: #2B3467;
    }
    /* Style the main title */
    .css-10trblm {
        font-size: 30px;
        color: #E8F6F3; /* Mint green for contrast */
        text-align: center;
    }
    /* Style the buttons and inputs */
    .stButton>button, .stTextInput>div>input {
        background-color: #14C38E;
        color: #FFFFFF;
        border-radius: 8px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #12A47D;
    }
    /* Center the Run Analysis button */
    .stButton {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with navigation
st.sidebar.title("Port4U")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Single Ticker Analysis", "Double Ticker Analysis"])

# Main content based on selection
if page == "Home":
    st.title("Welcome to Port4U")
    st.write(
        """
        Port4U is your one-stop financial analysis tool for in-depth stock insights. 
        Select an analysis option from the sidebar to get started.
        """
    )

elif page == "Single Ticker Analysis":
    st.title("Single Ticker Analysis")
    ticker = st.text_input("Enter a stock ticker (e.g., AAPL):", placeholder="Enter ticker symbol")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2018-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))

    if st.button("🚀 Run Analysis"):
        if ticker:
            st.session_state.df_metrics = run_single_ticker_analysis(ticker.strip().upper(), start_date, end_date)
        else:
            st.error("Please enter a valid stock ticker.")
    
    if st.session_state.get("df_metrics") is not None:
        st.write("### Analysis Results")
        st.dataframe(st.session_state.df_metrics)

        if st.button("📊 Explain Analysis"):
            with st.spinner("Generating explanation..."):
                explanation = table_explaination(st.session_state.df_metrics)
                st.write(explanation)

elif page == "Double Ticker Analysis":
    st.title("Double Ticker Analysis")
    ticker_1 = st.text_input("Enter the first stock ticker (e.g., AAPL):", placeholder="Enter first ticker symbol")
    ticker_2 = st.text_input("Enter the second stock ticker (e.g., MSFT):", placeholder="Enter second ticker symbol")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2018-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))

    if st.button("🚀 Run Analysis"):
        if ticker_1 and ticker_2:
            tickers = [ticker_1.strip().upper(), ticker_2.strip().upper()]
            st.session_state.df_metrics = run_multiple_ticker_analysis(tickers, start_date, end_date)
        else:
            st.error("Please enter valid stock tickers.")
    
    if st.session_state.get("df_metrics") is not None:
        st.write("### Analysis Results")
        st.dataframe(st.session_state.df_metrics)

        if st.button("📊 Explain Analysis"):
            with st.spinner("Generating explanation..."):
                explanation = table_explaination(st.session_state.df_metrics)
                st.write(explanation)
