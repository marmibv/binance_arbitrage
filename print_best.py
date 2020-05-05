from binance.client import Client
import csv

api_key = "18YtfZfxwuBEN1V4fupoJakkuWvy1cwlNCPaWNKopjxkJkAoDeZdUNtfPk1cBdeY"
api_secret = "IWckkJsFQCGONzFzz9CWJaapgpM2BSOiGxKWLqpHoIk1lJ8G2OlPWBwEio4eDihI"

# initialise a client
client = Client(api_key, api_secret, {"timeout": 600})

tickers = client.get_ticker()

# eth_btc = tickers[0]['askPrice']


mylist = [pair['symbol'] for pair in tickers]

btc_list = [item for item in mylist if 'BTC' in item]
eth_list = [item for item in mylist if 'ETH' in item]

match_list = [item for item in btc_list if item[:3] in eth_list]

for item in btc_list:
    for match in eth_list:
        if item[:3] == match[:3]:
            match_list.append(item)

btc_match = list(set(match_list))
eth_match = []

for item in eth_list:
    for match in btc_list:
        if item[:3] == match[:3]:
            eth_match.append(item)

eth_match = list(set(eth_match))

set_list = []

for item in btc_match:
    for ethpair in eth_match:
        if item[:3] in ethpair[:3]:
            set_list.append((item,ethpair))

