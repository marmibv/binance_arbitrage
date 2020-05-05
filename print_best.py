from binance.client import Client
import json

api_key = "18YtfZfxwuBEN1V4fupoJakkuWvy1cwlNCPaWNKopjxkJkAoDeZdUNtfPk1cBdeY"
api_secret = "IWckkJsFQCGONzFzz9CWJaapgpM2BSOiGxKWLqpHoIk1lJ8G2OlPWBwEio4eDihI"

# initialise a client
client = Client(api_key, api_secret, {"timeout": 600})

with open('indices.json') as f:
    indices = json.load(f)


# Print out a forward trade
def print_forward(eth_btc, alt_btc, alt_eth):
    # BTC -> ETH : eth/btc -> buy eth with btc
    q1 = "{:0.0{}f}".format((0.01 / float(eth_btc)), 5)
    # print(q1 + " ETH with 0.01 BTC\n")

    # ETH -> XRP : xrp/eth -> buy xrp with eth
    q2 = "{:0.0{}f}".format((float(q1) / float(alt_eth)), 5)
    # print(q2 + " XRP with " + q1 + " ETH\n")

    # XRP -> BTC : xrp/btc -> sell xrp for btc
    q3 = "{:0.0{}f}".format(float(q2) * float(alt_btc), 5)
    # print(q3 + " BTC with " + q2 + " XRP\n")

    # q3 is the remaining BTC
    return q3


# print out a backward trade
def print_backward(eth_btc, alt_btc, alt_eth):
    # BTC -> XRP : xrp/btc -> buy xrp with btc
    q1 = "{:0.0{}f}".format((0.01 / float(alt_btc)), 5)
    # print(q1 + "XRP with 0.01 BTC\n")

    # XRP -> ETH : xrp/eth -> sell xrp for eth
    q2 = "{:0.0{}f}".format(float(q1) * float(alt_eth), 5)
    # print(q2 + " ETH with " + q1 + " XRP\n")

    # ETH -> BTC : eth/btc -> sell eth for btc
    q3 = "{:0.0{}f}".format(float(q2) * float(eth_btc), 5)
    # print(q3 + " BTC with " + q2 + " XRP\n")

    # q3 is the remaining BTC
    return q3


def main():

    # get all ticker data
    tickers = client.get_ticker()

    eth_btc = tickers[0]['askPrice']

    results = {}

    # for each coin in the indices dict
    for coin in indices:
        # get the ask price
        print(indices[coin][coin+'BTC'])
        #alt_btc = tickers[coin[coin+'BTC']]['askPrice']
        #alt_eth = tickers[coin[coin+'ETH']]['askPrice']
        # find the result of arbitrage
        #fwd = print_forward(eth_btc, alt_btc, alt_eth)
        #bwd = print_backward(eth_btc, alt_btc, alt_eth)
        # append the result (forward or backward)
        #results[coin] = 0.01 - fwd if fwd > bwd else 0.01 - bwd

main()


