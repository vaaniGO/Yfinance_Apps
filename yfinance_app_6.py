import streamlit as st
import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Custom CSS to change background and text colors
st.markdown(
    """
    <style>
    /* Set background color */
    .main {
        background-color: #000000;
    }
    """,
    unsafe_allow_html=True
)

# Paths
data_folder = 'Stock_data/Stocks'

# Helper function to load data for a specific stock
def load_stock_data(stock_file):
    file_path = os.path.join(data_folder, stock_file)
    return pd.read_csv(file_path, delimiter=',', parse_dates=['Date'])

# UI for selecting stock and dates
st.title("Stock Profit/Loss Calculator")

# Step 1: Select Stock
stock_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
stock_names = [f.replace('.txt', '') for f in stock_files]
selected_stock = st.selectbox("Select a stock to buy", stock_names)

# Fetch the company name using yfinance
ticker = yf.Ticker(selected_stock[:-3])
company_name = ticker.info.get('longName', 'Unknown Company')
st.write(f"**Selected Company**: {company_name}")

# Load selected stock data
stock_data = load_stock_data(f"{selected_stock}.txt")
stock_data['Year'] = stock_data['Date'].dt.year
stock_data['Month'] = stock_data['Date'].dt.month
stock_data['Day'] = stock_data['Date'].dt.day

# Step 2: Select Units
units = st.number_input("Enter the number of units to buy", min_value=1, step=1)
years = list(stock_data['Year'].unique())
min_year_index = years.index(min(years))

# Step 3: Select Purchase Date
purchase_year = st.selectbox("Select the purchase year", years, index = min_year_index)
purchase_month = st.selectbox("Select the purchase month", stock_data[stock_data['Year'] == purchase_year]['Month'].unique())
purchase_day = st.selectbox("Select the purchase day", stock_data[(stock_data['Year'] == purchase_year) & (stock_data['Month'] == purchase_month)]['Day'].unique())
purchase_date = datetime(purchase_year, purchase_month, purchase_day)

# Step 4: Select Selling Date
filtered_years = [year for year in years if year>=purchase_year]
max_year_index = filtered_years.index(max(filtered_years))
selling_year = st.selectbox("Select the selling year", filtered_years, max_year_index)
selling_month = st.selectbox("Select the selling month", stock_data[stock_data['Year'] == selling_year]['Month'].unique())
selling_day = st.selectbox("Select the selling day", stock_data[(stock_data['Year'] == selling_year) & (stock_data['Month'] == selling_month)]['Day'].unique())
selling_date = datetime(selling_year, selling_month, selling_day)

# Filter the data between purchase and selling dates
filtered_data = stock_data[(stock_data['Date'] >= purchase_date) & (stock_data['Date'] <= selling_date)]

# Calculate profit or loss
purchase_price = stock_data.loc[stock_data['Date'] == purchase_date, 'Close'].values[0]
selling_price = stock_data.loc[stock_data['Date'] == selling_date, 'Close'].values[0]
profit_loss = (selling_price - purchase_price) * units

st.write(f"**Purchase Price**: ${purchase_price}")
st.write(f"**Selling Price**: ${selling_price}")
st.write(f"**Units**: {units}")
st.write(f"**Net Profit/Loss** (in USD ($)): {profit_loss:.2f}")

# Display line chart for the stock performance between purchase and selling dates
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_data['Date'], filtered_data['Close'], color="blue", label="Close Price")
ax.axvline(purchase_date, color="green", linestyle="--", label="Purchase Date")
ax.axvline(selling_date, color="red", linestyle="--", label="Selling Date")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.set_title(f"{company_name} ({selected_stock}) Stock Performance")
ax.legend()
st.pyplot(fig)
