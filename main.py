"""
The code below, that appears to be a script that retrieves stock data from the Alpha Vantage API, calculates the
difference and percentage difference between the closing prices of the last two months,
and if the percentage difference is greater than 1%, it retrieves news articles
about the company (Tesla Inc) from the News API.
Then it creates a message for each article, with the headline and brief of the article,
and sends it via Twilio's SMS service
to a specific phone number.
"""
import os
import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
account_sid = os.environ.get("ACC_SID")
auth_token = os.environ.get("AUTH_TOKEN")
stock_params = {
    "function": "TIME_SERIES_MONTHLY",
    "symbol": "IBM",
    "datatype": "json",
    "apikey": STOCK_API_KEY,
}
dove = Client(account_sid, auth_token)
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = response.json()['Monthly Time Series']
data_list = [value for (key, value) in data.items()]
yesterday_list = data_list[0]
yesterday_closing_price = yesterday_list['4. close']
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"
difference = abs(difference)
percentage_dif = (float(difference) / float(yesterday_closing_price)) * 100

if percentage_dif > 1:
    NEWS_PARAMS = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    messages = [f"Breaking news!!!\n {up_down}Headline: {article['title']}.\n Brief: {article['description']}"
                for article in three_articles]
    for msg in messages:
        dove.messages.create(body=up_down + msg,
                             from_="+13XXXXXXXX1",
                             to="+995XXXXXXXXX")

