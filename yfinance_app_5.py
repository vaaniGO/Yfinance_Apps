import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="Financial Analysis", layout="wide")
with st.sidebar:
    st.title("Financial Analysis with Texas Precipitation : We are in 2017-7-31")
    ticker = st.text_input("Enter a stock ticker (e.g. AAPL)", "AAPL")
    period = st.selectbox("Enter a time frame", ("5D", "1M", "6M"))
    button = st.button("Submit")

# Load the dataset
file_path = 'austin_weather.csv'
df_p = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df_p['Date'] = pd.to_datetime(df_p['Date'])

# Set the 'Date' column as the index
df_p.set_index('Date', inplace=True)

# Keep only the 'PrecipitationSumInches' column
df_p = df_p[['PrecipitationSumInches']]

def format_value(value):
    if isinstance(value, (int, float)):
        return f"${value:.2f}"
    return value  # Return as-is if not a number

if button: 
    if not ticker.strip():
        st.error("Please provide a valid stock ticker.")
    else: 
        try: 
            with st.spinner("Please wait..."):
                stock = yf.Ticker(ticker)
                info = stock.info

                st.subheader(f"{ticker} - {info.get('longName', 'N/A')}")
                
                start_date = datetime(2017, 7, 31)

                if period == "5D":
                    end_date = start_date - timedelta(days=5)
                    history = stock.history(start=end_date, end=start_date, interval="1d")
                    precipitation_data = df_p.last("5D")
                elif period == "1M":
                    end_date = start_date - timedelta(days=30)
                    history = stock.history(start=end_date, end=start_date, interval="1d")
                    precipitation_data = df_p.last("1M")
                elif period == "6M":
                    end_date = start_date - timedelta(days=180)
                    history = stock.history(start=end_date, end=start_date, interval="1wk")
                    precipitation_data = df_p.last("6M")

                # Plot with dual y-axes
                fig, ax1 = plt.subplots(figsize=(10, 5))

                # Plot Close Price on the first y-axis
                ax1.set_xlabel("Date")
                ax1.set_ylabel("Close Price", color="blue")
                ax1.plot(history["Close"], color="blue", label="Close Price")
                ax1.tick_params(axis="y", labelcolor="blue")

                # Plot Precipitation on the second y-axis
                ax2 = ax1.twinx()
                ax2.set_ylabel("Precipitation (Inches)", color="black")
                ax2.plot(precipitation_data["PrecipitationSumInches"], color="pink", label="Precipitation")
                ax2.tick_params(axis="y", labelcolor="pink")

                # Add a title and display the plot in Streamlit
                fig.suptitle(f"{ticker} Close Price and Precipitation Data")
                st.pyplot(fig)

                col1, col2, col3 = st.columns(3)

                # Stock Info Table
                stock_info = [
                    ("Stock Info", "Value"),
                    ("Country", info.get('country', 'N/A')),
                    ("Sector", info.get('sector', 'N/A')),
                    ("Industry", info.get('industry', 'N/A')),
                    ("Market Cap", format_value(info.get('marketCap', 'N/A'))),
                    ("Enterprise Value", format_value(info.get('enterpriseValue', 'N/A'))),
                    ("Employees", info.get('fullTimeEmployees', 'N/A'))
                ]
                col1.dataframe(pd.DataFrame(stock_info[1:], columns=stock_info[0]), width=400, hide_index=True)

                # Price Info Table
                price_info = [
                    ("Price Info", "Value"),
                    ("Current Price", format_value(info.get('currentPrice', 'N/A'))),
                    ("Previous Close", format_value(info.get('previousClose', 'N/A'))),
                    ("Day High", format_value(info.get('dayHigh', 'N/A'))),
                    ("Day Low", format_value(info.get('dayLow', 'N/A'))),
                    ("52 Week High", format_value(info.get('fiftyTwoWeekHigh', 'N/A'))),
                    ("52 Week Low", format_value(info.get('fiftyTwoWeekLow', 'N/A')))
                ]
                col2.dataframe(pd.DataFrame(price_info[1:], columns=price_info[0]), width=400, hide_index=True)

                # Business Metrics Table
                biz_metrics = [
                    ("Business Metrics", "Value"),
                    ("EPS (FWD)", format_value(info.get('forwardEps', 'N/A'))),
                    ("P/E (FWD)", format_value(info.get('forwardPE', 'N/A'))),
                    ("PEG Ratio", format_value(info.get('pegRatio', 'N/A'))),
                    ("Div Rate (FWD)", format_value(info.get('dividendRate', 'N/A'))),
                    ("Div Yield (FWD)", f"{info.get('dividendYield', 'N/A') * 100:.2f}%" if isinstance(info.get('dividendYield'), (int, float)) else "N/A"),
                    ("Recommendation", info.get('recommendationKey', 'N/A').capitalize() if info.get('recommendationKey') else "N/A")
                ]
                col3.dataframe(pd.DataFrame(biz_metrics[1:], columns=biz_metrics[0]), width=400, hide_index=True)
                
        except Exception as e: 
            st.exception(f"An error occurred: {e}")
