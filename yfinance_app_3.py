import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Financial Analysis : Compare 2 stocks", layout="wide")
with st.sidebar:
    st.title("Financial Analysis")
    num = int(st.selectbox("Enter the number of stocks to compare", ("2", "3", "4", "5", "6", "7", "8")))
    tickers = []
    for i in range(int(num)):  # Convert num to int
        ticker = st.text_input(f"Enter a stock ticker - ticker ${i + 1} (e.g. AAPL)", "AAPL")
        tickers.append(ticker)
    
    period = st.selectbox("Enter a time frame", ("5D", "1M", "6M", "YTD", "1Y", "5Y"))
    button = st.button("Submit")

def format_value(value):
    if not isinstance(value, (int, float)):
        return value  # Return as-is if not a number
    suffixes = ["", "K", "M", "B", "T"]
    suffix_index = 0
    while value >= 1000 and suffix_index < len(suffixes) - 1:
        value /= 1000
        suffix_index += 1
    return f"${value:.1f}{suffixes[suffix_index]}"

def format_float(value):
    return f"${value:.2f}" if isinstance(value, (int, float)) else "N/A"

if button: 
    for i in range(num):
        if not (tickers[i].strip()):
            st.error("Please provide a valid stock ticker.")
    else: 
        try: 
            with st.spinner("Please wait..."):
                info = []
                stock = []
                for i in range(num):
                    stock.append(yf.Ticker(tickers[i]))
                    info.append(stock[i].info)
                
                histories = []   # List to store the history data for each stock

                for i in range(num):  # Run twice, once for each stock
                    current_stock = stock[i]  # Get the current stock
                    if period == "5D":
                        histories.append(current_stock.history(period="5d", interval="1d"))
                    elif period == "1M":
                        histories.append(current_stock.history(period="1mo", interval="1d"))
                    elif period == "6M":
                        histories.append(current_stock.history(period="6mo", interval="1wk"))
                    elif period == "YTD":
                        histories.append(current_stock.history(period="ytd", interval="1mo"))
                    elif period == "1Y":
                        histories.append(current_stock.history(period="1y", interval="1mo"))
                    elif period == "5Y":
                        histories.append(current_stock.history(period="5y", interval="3mo"))
                
                chart_data = pd.DataFrame()
                for ticker, history in zip(tickers, histories):
                    chart_data[f"{ticker} Close"] = history["Close"]
                
                # The below line will help you check if the trading hours are the same. For example: it is not same for AAPL and SMSN.IL
                # st.write("Chart Data", chart_data)
                st.line_chart(chart_data)

                for i in range(num):
                    with st.container():
                        st.subheader(f"{tickers[i]} - {info[i].get('longName', 'N/A')}")
                        col1, col2, col3 = st.columns(3)
                        # Display tables for ticker1
                        country = info[i].get('country', 'N/A')
                        sector = info[i].get('sector', 'N/A')
                        industry = info[i].get('industry', 'N/A')
                        market_cap = info[i].get('marketCap', 'N/A')
                        ent_value = info[i].get('enterpriseValue', 'N/A')
                        employees = info[i].get('fullTimeEmployees', 'N/A')

                        stock_info = [
                            ("Stock Info", "Value"),
                            ("Country", country),
                            ("Sector", sector),
                            ("Industry", industry),
                            ("Market Cap", format_value(market_cap)),
                            ("Enterprise Value", format_value(ent_value)),
                            ("Employees", employees)
                        ]

                        df = pd.DataFrame(stock_info[1:], columns=stock_info[0])
                        col1.dataframe(df, width=400, hide_index=True)

                        current_price = info[i].get('currentPrice', 'N/A')
                        prev_close = info[i].get('previousClose', 'N/A')
                        day_high = info[i].get('dayHigh', 'N/A')
                        day_low = info[i].get('dayLow', 'N/A')
                        ft_week_high = info[i].get('fiftyTwoWeekHigh', 'N/A')
                        ft_week_low = info[i].get('fiftyTwoWeekLow', 'N/A')

                        price_info = [
                            ("Price Info", "Value"),
                            ("Current Price", format_float(current_price)),
                            ("Previous Close", format_float(prev_close)),
                            ("Day High", format_float(day_high)),
                            ("Day Low", format_float(day_low)),
                            ("52 Week High", format_float(ft_week_high)),
                            ("52 Week Low", format_float(ft_week_low)),
                        ]

                        df = pd.DataFrame(price_info[1:], columns=price_info[0])
                        col2.dataframe(df, width=400, hide_index=True)

                        forward_eps = info[i].get('forwardEps', 'N/A')
                        forward_pe = info[i].get('forwardPE', 'N/A')
                        peg_ratio = info[i].get('pegRatio', 'N/A')
                        dividend_rate = info[i].get('dividendRate', 'N/A')
                        dividend_yield = info[i].get('dividendYield', 'N/A')
                        recommendation = info[i].get('recommendationKey', 'N/A')

                        biz_metrics = [
                            ("Business Metrics", "Value"),
                            ("EPS (FWD)", format_float(forward_eps)),
                            ("P/E (FWD)", format_float(forward_pe)),
                            ("PEG Ratio", format_float(peg_ratio)),
                            ("Div Rate (FWD)", format_float(dividend_rate)),
                            ("Div Yield (FWD)", f"{dividend_yield * 100:.2f}%" if isinstance(dividend_yield, (int, float)) else "N/A"),
                            ("Recommendation", recommendation.capitalize())
                        ]

                        df = pd.DataFrame(biz_metrics[1:], columns=biz_metrics[0])
                        col3.dataframe(df, width=400, hide_index=True)

        except Exception as e: 
            st.exception(f"An error occurred: {e}")
