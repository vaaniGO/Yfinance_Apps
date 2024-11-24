import yfinance as yf
from prophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

model = Prophet()
ticker = "NVDA"
data = yf.download(ticker, start='2020-01-01', end='2024-01-01')
trendLinePrecision = 3 # Enter the required degree of approximation of the trend line
data.reset_index(inplace=True)
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label=f'{ticker} Close Price', color='#c9acfa')
plt.title(f'{ticker} Stock Close Price (2020-2024)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Close Price (USD)', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

data['DateNum'] = data['Date'].map(lambda x: x.toordinal())

x = data['DateNum'].values
y = data['Close'].values.ravel()
coeffs = np.polyfit(x, y, trendLinePrecision) 
trend_line = np.poly1d(coeffs)

plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], label='Close Price', color='#c9acfa')
plt.plot(data['Date'], trend_line(x), label='Trend Line', color='gray', linestyle='--')
plt.title(f'{ticker} Stock Close Price with Trend Line (2020-2024)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Close Price (USD)', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# Cleaning the dataframe, making it suitable for Prophet
# This process is based on constant inspection and adjustment and the below
# steps are good for achieving a clean df.
data.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
data.columns = data.columns.droplevel(1)
data.reset_index()
data.reset_index(inplace=True)
data.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
df = data[['ds', 'y']]
df['ds']=df['ds'].dt.tz_localize(None)

# Step 2: Train the Prophet model
model = Prophet()
model.fit(df)

# Step 3: Make predictions
# Create a future dataframe for the next day
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)

# Step 4: Compare today's close price with the prediction for the next day
today_close = df['y'].iloc[-1]
next_day_forecast = forecast[['ds', 'yhat']].iloc[-1]

print(f"Today's Close Price: {today_close}")
print(f"Predicted Next Day's Close Price: {next_day_forecast['yhat']}")

# Determine if the price will increase
if next_day_forecast['yhat'] > today_close:
    print("Prediction: The next day's close price will be higher.")
else:
    print("Prediction: The next day's close price will be lower or the same.")
    
forecast_next_7 = forecast[-7:]

plt.figure(figsize=(21, 6))

# Plot original data
plt.plot(data['ds'][-7:], data['y'][-7:], label='Actual Data', marker='o', color='purple')

# Plot predictions for the next 7 periods
plt.plot(forecast_next_7['ds'], forecast_next_7['yhat'], label='Forecast (Next 7 Days)', marker='x', color='navy')

plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Prophet Forecast for the Next 7 Days continuing from the previous 7 Days')
plt.legend()
plt.grid()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
plt.show()

