import os 
from dotenv import load_dotenv
import google.generativeai as genai

def configure_gemini():
    """
    Load API key from .env file and configure the Gemini model.
    :return: A configured Gemini model instance.
    """
    load_dotenv()

    # Check if API key is loaded
    api_key = os.getenv('API_KEY')
    if api_key is None:
        raise ValueError("API_KEY not found! Please check your .env file.")
    
    # Configure and return Gemini model
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

gemini_model = configure_gemini()

def table_explaination(df_metrics):
    metrics_dict = df_metrics.to_dict(orient = 'records')
    prompt = f'''Please provide a clear and concise explanation of the following 
    financial metrics in the context of portfolio optimization: Expected Annual Return, 
    Annual Volatility (Risk), Sharpe Ratio,Sortino Ratio, and Value at Risk (VaR),Maximun Drawdown,Compound Annual Growth rate (CAGR).For each metric, define it, 
    interpret the provided values, and explain the implications for an individual investor
    considering an investment opportunity, in a way that is easy to understand for a non-financial expert.{metrics_dict}'''

    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error occurred while generating explanation: {str(e)}")
        
    
