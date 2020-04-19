"""
author: Aiden Lewington
project: Binance Arbitrage Trading Bot
aim: using triangular arbitrage, automate trades that are guaranteed to return a specified profit or more.
"""

from binance.client import Client
from binance.enums import *

api_key = "18YtfZfxwuBEN1V4fupoJakkuWvy1cwlNCPaWNKopjxkJkAoDeZdUNtfPk1cBdeY"
api_secret = "IWckkJsFQCGONzFzz9CWJaapgpM2BSOiGxKWLqpHoIk1lJ8G2OlPWBwEio4eDihI"

# initialise a client
client = Client(api_key, api_secret, {"timeout": 600})

lot_sizes = {
    "ETHBTC" : 0.00100000,
    "XRPETH" : 1.00000000,
    "XRPBTC" : 1.00000000
}


# BTC -> ETH -> XRP -> BTC
def trade_forward(eth_btc, xrp_btc, xrp_eth):
    # BTC -> ETH : eth/btc -> buy eth with btc
    q1 = "{:0.0{}f}".format((0.01 / float(eth_btc)), 5)
    order_one = client.order_market_buy(symbol='ETHBTC', quantity=q1)

    # ETH -> XRP : xrp/eth -> buy xrp with eth
    q2 = "{:0.0{}f}".format((float(q1) / float(xrp_eth)), 5)
    order_two = client.order_market_buy(symbol='XRPETH', quantity=q2)

    # XRP -> BTC : xrp/btc -> sell xrp for btc
    q3 = "{:0.0{}f}".format(float(q2) * float(xrp_btc), 5)
    order_three = client.order_market_sell(symbol='XRPBTC', quantity=q3)


# print out a backward trade
def trade_backward(eth_btc, xrp_btc, xrp_eth):
    # BTC -> XRP : xrp/btc -> buy xrp with btc
    q1 = "{:0.0{}f}".format((0.01 / float(xrp_btc)), 5)
    order_one = client.order_market_buy(symbol='XRPBTC', quantity=q1)

    # XRP -> ETH : xrp/eth -> sell xrp for eth
    q2 = "{:0.0{}f}".format(float(q1) * float(xrp_eth), 5)
    order_three = client.order_market_sell(symbol='XRPETH', quantity=q2)

    # ETH -> BTC : eth/btc -> sell eth for btc
    q3 = "{:0.0{}f}".format(float(q2) * float(eth_btc), 5)
    order_three = client.order_market_sell(symbol='ETHBTC', quantity=q3)


# Print out a forward trade
def print_forward(eth_btc, xrp_btc, xrp_eth):
    # BTC -> ETH : eth/btc -> buy eth with btc
    q1 = "{:0.0{}f}".format((0.01 / float(eth_btc)), 5)
    print(q1 + " ETH with 0.01 BTC\n")

    # ETH -> XRP : xrp/eth -> buy xrp with eth
    q2 = "{:0.0{}f}".format((float(q1) / float(xrp_eth)), 5)
    print(q2 + " XRP with " + q1 + " ETH\n")

    # XRP -> BTC : xrp/btc -> sell xrp for btc
    q3 = "{:0.0{}f}".format(float(q2) * float(xrp_btc), 5)
    print(q3 + " BTC with " + q2 + " XRP\n")



# print out a backward trade
def print_backward(eth_btc, xrp_btc, xrp_eth):
    # BTC -> XRP : xrp/btc -> buy xrp with btc
    q1 = "{:0.0{}f}".format((0.01 / float(xrp_btc)), 0)
    print(q1 + "XRP with 0.01 BTC\n")

    # XRP -> ETH : xrp/eth -> sell xrp for eth
    q2 = "{:0.0{}f}".format(float(q1) * float(xrp_eth), 5)
    print(q2 + " ETH with " + q1 + " XRP\n")

    # ETH -> BTC : eth/btc -> sell eth for btc
    q3 = "{:0.0{}f}".format(float(q2) * float(eth_btc), 5)
    print(q3 + " BTC with " + q2 + " XRP\n")


def main():
    # TODO Get Lot Sizes and Adjust for Each Order
    # step size info
    info = client.get_exchange_info()
    balance = client.get_asset_balance(asset='BTC')

    # get our three price indices
    # ETHBTC 000
    # XRPETH 091
    # XRPBTC 090
    tickers = client.get_ticker()
    eth_btc = tickers[0]['askPrice']
    xrp_eth = tickers[91]['askPrice']
    xrp_btc = tickers[90]['askPrice']

    # print("eth_btc:" + str(eth_btc) + "\nxrp_eth:" + str(xrp_eth) + "\nxrp_btc:" + str(xrp_btc))

    # 0.01 BTC -> ETH -> XRP -> BTC
    forward = 0.01 / float(eth_btc) / float(xrp_eth) * float(xrp_btc)

    # 0.01 BTC -> XRP -> ETH -> BTC
    backward = 0.01 / float(xrp_btc) * float(xrp_eth) * float(eth_btc)

    if forward > 0.01:
        print("Forward: 0.01 BTC to " + str(forward))
        # condition for trade
        if forward / 0.01 > 1.00015:
            print("trade worthy forward")
            print_forward(eth_btc, xrp_btc, xrp_eth)
    elif backward > 0.01:
        print("Backward: 0.01 BTC to " + str(backward))
        # condition for trade
        if backward / 0.01 > 1.00015:
            print("trade worthy backward")
            print_backward(eth_btc, xrp_btc, xrp_eth)
    else:
        print("No trade")


main()
