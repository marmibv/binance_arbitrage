from binance.client import Client
import csv
import json

api_key = "18YtfZfxwuBEN1V4fupoJakkuWvy1cwlNCPaWNKopjxkJkAoDeZdUNtfPk1cBdeY"
api_secret = "IWckkJsFQCGONzFzz9CWJaapgpM2BSOiGxKWLqpHoIk1lJ8G2OlPWBwEio4eDihI"

# initialise a client
client = Client(api_key, api_secret, {"timeout": 600})

# get all ticker data
tickers = client.get_ticker()

# get all symbols on exchange
mylist = [pair['symbol'] for pair in tickers]

# get all btc and eth symbols into their own lists
btc_list = [item for item in mylist if 'BTC' in item]
eth_list = [item for item in mylist if 'ETH' in item]

# get all btc pairs in a list that exist in the eth list

match_list = []

for item in btc_list:
    for match in eth_list:
        if item[:3] == match[:3]:
            match_list.append(item)

btc_match = list(set(match_list))

# get all eth pairs in a list that exist in the btc list

eth_match = []
for item in eth_list:
    for match in btc_list:
        if item[:3] == match[:3]:
            eth_match.append(item)

eth_match = list(set(eth_match))

# make a list of sets with matching btc/eth pairs
set_list = []

for item in btc_match:
    for ethpair in eth_match:
        if item[:3] in ethpair[:3]:
            set_list.append((item,ethpair))

# get rid of errors
for item in set_list:
    if item[0].startswith('ETH'):
        set_list.remove(item)
set_list.remove(set_list[70])

# make into a json with the index in tickers
final = {}
for pair in set_list:
    temp_dict = {}

    for item in pair:
        # find index
        for count, ele in enumerate(tickers):
            # add entry to dict
            if ele['symbol'] == item:
                temp_dict[item] = count
    # add to final
    if len(item) == 7:
        final[pair[0][:4]] = temp_dict
    else:
        final[pair[0][:3]] = temp_dict

try1 = "ZRXBTC"
for element in tickers:
    if 'symbol' == try1:
        print(tickers)


for count, ele in enumerate(tickers):
    if ele['symbol'] == "ZRXBTC":
        print(count)

with open('indices.json', 'w') as fp:
    json.dump(final, fp)
