Basic financial analysis in python using streamlit and the yfinance library. 
Developments include building apps to provide more nuanced insights with their qualitative implications for a wider user base (current trading platforms provide comprehensive quantitative metrics. 
This is an attempt to translate unique metrics)

Below is the preview of some of the analysis work done and interfaces built: 

1. A glimpse into a comparitive study of weather paramaters with stock prices. The below is the streamlit app (yfinance app 5 in the directory) that shows a comparitive view of the
rainfall in Texas in the specified dates and the price of an entered stock. While this in itself is not all that insightful, the plan is to extend this to a more robust and dynamic
comparitive view of weather parameters and commodity prices to study how it has been historically. The main constraints including fetching data across time and location.
<img width="1699" alt="Screenshot 2024-11-24 at 3 58 39 PM" src="https://github.com/user-attachments/assets/6b85cf6c-eb3e-41a3-8e47-9e233711e244">

2. A trading strategy tester where the user can enter the details as prompted and get a net P/L figure along with a graph. The extention of this app will include Prophet to predict
P/L based on its analysis and give figures accordingly.
<img width="853" alt="Screenshot 2024-11-24 at 4 01 47 PM" src="https://github.com/user-attachments/assets/ce0cb15a-311a-4184-8ea2-248d950df5dd">
Output:
<img width="801" alt="Screenshot 2024-11-24 at 4 01 51 PM" src="https://github.com/user-attachments/assets/1310add9-03d4-40c5-ad14-e99b412f8735">

3. A stock screener where user can enter thresholds for parameters and get the tickers of stocks that qualify. 
<img width="737" alt="Screenshot 2024-11-24 at 4 17 15 PM" src="https://github.com/user-attachments/assets/3aa18450-6ed8-44a2-b431-fdabe12eed43">

And the result is displayed as below: 
<img width="329" alt="Screenshot 2024-11-24 at 4 20 36 PM" src="https://github.com/user-attachments/assets/febb4cec-1933-43d4-83fa-e0d4bb3d9663">
<img width="333" alt="Screenshot 2024-11-24 at 4 20 31 PM" src="https://github.com/user-attachments/assets/fb7b3d32-c0cf-46dd-adc4-67c701695433">

4. Using prophet to predict NVIDIA stock prices, get a trend line of specified degree, and a graph continuing the previous record
with the next time frame of prediction as shown in the second image.
![01710171-235e-457a-9602-dc3df20392c8](https://github.com/user-attachments/assets/c94e8631-09f5-40fe-bc70-e7194d103f5e)
![d3fb143d-b429-4503-80dd-1e30a65284e3](https://github.com/user-attachments/assets/b1150b4c-138f-4e9e-a395-68265f8e22b4)
