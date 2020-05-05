from binance.client import Client
import json
from decimal import *

api_key = "18YtfZfxwuBEN1V4fupoJakkuWvy1cwlNCPaWNKopjxkJkAoDeZdUNtfPk1cBdeY"
api_secret = "IWckkJsFQCGONzFzz9CWJaapgpM2BSOiGxKWLqpHoIk1lJ8G2OlPWBwEio4eDihI"

# initialise a client
client = Client(api_key, api_secret, {"timeout": 600})

results = {}

with open('indices.json') as f:
    indices = json.load(f)

getcontext().prec = 8

# Print out a forward trade
def print_forward(eth_btc, alt_btc, alt_eth, name):

    if Decimal(alt_btc) == 0.00000000:
        return 0
    elif Decimal(alt_eth) == 0.00000000:
        return 0

    # BTC -> ETH : eth/btc -> buy eth with btc
    q1 = "{:0.0{}f}".format((Decimal(0.01) / Decimal(eth_btc)), 5)
    print(q1 + " ETH with 0.01 BTC\n")

    # ETH -> ALT : alt/eth -> buy alt with eth
    q2 = "{:0.0{}f}".format((Decimal(q1) / Decimal(alt_eth)), 5)
    print(q2 + " " + name + " with " + q1 + " ETH\n")

    # ALT -> BTC : alt/btc -> sell alt for btc
    q3 = "{:0.0{}f}".format(Decimal(q2) * Decimal(alt_btc), 5)
    print(q3 + " BTC with " + q2 + " " + name +"\n")

    # q3 is the remaining BTC
    return Decimal(q3)


# print out a backward trade
def print_backward(eth_btc, alt_btc, alt_eth, name):

    if Decimal(alt_btc) == 0.00000000:
        return 0
    elif Decimal(alt_eth) == 0.00000000:
        return 0

    # BTC -> ALT : alt/btc -> buy alt with btc
    q1 = "{:0.0{}f}".format((Decimal(0.01) / Decimal(alt_btc)), 5)
    print(q1 + " " + name + " with 0.01 BTC\n")

    # ALT -> ETH : alt/eth -> sell alt for eth
    q2 = "{:0.0{}f}".format(Decimal(q1) * Decimal(alt_eth), 5)
    print(q2 + " ETH with " + q1 + " " + name + "\n")

    # ETH -> BTC : eth/btc -> sell eth for btc
    q3 = "{:0.0{}f}".format(Decimal(q2) * Decimal(eth_btc), 5)
    print(q3 + " BTC with " + q2 + " " + name + "\n")

    # q3 is the remaining BTC
    return Decimal(q3)


def main():

    # get all ticker data
    tickers = client.get_ticker()

    eth_btc = tickers[0]['askPrice']



    # for each coin in the indices dict
    for coin in indices:
        # get the ask price
        alt_btc = tickers[indices[coin][coin+'BTC']]['askPrice']
        alt_eth = tickers[indices[coin][coin+'BTC']]['askPrice']

        print("alt = " + coin + ", alt_btc = " + alt_btc + ", alt_eth = " + alt_eth)
        # find the result of arbitrage
        fwd = print_forward(eth_btc, alt_btc, alt_eth, coin)
        bwd = print_backward(eth_btc, alt_btc, alt_eth, coin)
        # append the result (forward or backward)
        if fwd > bwd:
            results[coin] = fwd
        else:
            results[coin] = bwd


main()


