"""
author: Aiden Lewington
project: Binance Arbitrage Trading Bot
aim: using triangular arbitrage, automate trades that are guaranteed to return a specified profit or more.
"""

from binance.client import Client
from decimal import *
import time

api_key = "18YtfZfxwuBEN1V4fupoJakkuWvy1cwlNCPaWNKopjxkJkAoDeZdUNtfPk1cBdeY"
api_secret = "IWckkJsFQCGONzFzz9CWJaapgpM2BSOiGxKWLqpHoIk1lJ8G2OlPWBwEio4eDihI"

# initialise a client
client = Client(api_key, api_secret, {"timeout": 600})


# BTC -> ETH -> XRP -> BTC
def trade_forward(eth_btc, xrp_btc, xrp_eth):
    # BTC -> ETH : eth/btc -> buy eth with btc
    q1 = "{:0.0{}f}".format((0.01 / float(eth_btc)), 5)
    order_one = client.order_market_buy(symbol='ETHBTC', quantity=q1)
    print("btc -> eth done")

    # ETH -> XRP : xrp/eth -> buy xrp with eth
    q2 = "{:0.0{}f}".format((float(q1) / float(xrp_eth)), 5)
    order_two = client.order_market_buy(symbol='XRPETH', quantity=q2)
    print("eth -> xrp done")

    # XRP -> BTC : xrp/btc -> sell xrp for btc
    q3 = "{:0.0{}f}".format(float(q2) * float(xrp_btc), 5)
    order_three = client.order_market_sell(symbol='XRPBTC', quantity=q3)
    print("xrp -> btc done")


# print out a backward trade
def trade_backward(eth_btc, xrp_btc, xrp_eth):
    # BTC -> XRP : xrp/btc -> buy xrp with btc
    q1 = "{:0.0{}f}".format((0.01 / float(xrp_btc)), 5)
    order_one = client.order_market_buy(symbol='XRPBTC', quantity=q1)
    print("btc -> xrp done")

    # XRP -> ETH : xrp/eth -> sell xrp for eth
    q2 = "{:0.0{}f}".format(float(q1) * float(xrp_eth), 5)
    order_three = client.order_market_sell(symbol='XRPETH', quantity=q2)
    print("xrp -> eth done")

    # ETH -> BTC : eth/btc -> sell eth for btc
    q3 = "{:0.0{}f}".format(float(q2) * float(eth_btc), 5)
    order_three = client.order_market_sell(symbol='ETHBTC', quantity=q3)
    print("eth -> btc done")


lot_sizes = {
    "ETHBTC": 0.00100000,
    "XRPETH": 1.00000000,
    "XRPBTC": 1.00000000
}


def forward(pricelist):
    eth_btc = pricelist[0]
    xrp_eth = pricelist[1]
    xrp_btc = pricelist[2]

    # buy eth with 0.01 btc
    eth_amount = Decimal(0.01) / Decimal(eth_btc)
    print("0.01 BTC to ETH ->" + str(eth_amount) + " ETH")
    eth_amount = eth_amount - (eth_amount % lot_sizes["ETHBTC"])
    print("trimmed to " + str(eth_amount))
    # buy eth here

    # buy xrp with eth
    xrp_amount = eth_amount * Decimal(xrp_eth)
    print(str(eth_amount) + " ETH to XRP -> " + str(xrp_amount) + " XRP")
    xrp_amount = xrp_amount - (xrp_amount % lot_sizes["XRPBTC"])
    print("trimmed to " + str(xrp_amount))

    # sell xrp amount for btc
    btc_amount = xrp_amount * Decimal(xrp_btc)
    print(str(xrp_amount) + " XRP to BTC ->" + str(btc_amount) + " BTC")
    print("========================================")
    print("0.01 BTC to " + str(btc_amount))
    print("========================================")


def backward(pricelist):
    eth_btc = pricelist[0]
    xrp_eth = pricelist[1]
    xrp_btc = pricelist[2]

    # buy xrp with 0.01 btc
    xrp_amount = Decimal(0.01) / Decimal(xrp_btc)
    print("0.01 BTC to XRP -> " + str(xrp_amount) + " XRP")
    xrp_amount = xrp_amount - (xrp_amount % Decimal(lot_sizes["XRPBTC"]))
    print("trimmed to " + str(xrp_amount))
    # buy xrp here

    # sell xrp amount for eth
    eth_amount = xrp_amount * Decimal(xrp_eth)
    print(str(xrp_amount) + " XRP to ETH -> " + str(eth_amount) + " ETH")
    eth_amount = eth_amount - (eth_amount % Decimal(lot_sizes["ETHBTC"]))
    print("trimmed to " + str(eth_amount))
    # sell here

    # sell eth amount for btc
    btc_amount = eth_amount * Decimal(eth_btc)
    print(str(eth_amount) + " ETH to BTC ->" + str(btc_amount) + " BTC")
    print("========================================")
    print("0.01 BTC to " + str(btc_amount))
    print("========================================")


# prints the real change in the exchange wallet
# include all three values in case residuals left aside
def report(wallet):
    result = [client.get_asset_balance(asset='BTC')["free"],
              client.get_asset_balance(asset='XRP')["free"],
              client.get_asset_balance(asset='ETH')["free"]]

    # results
    btc_result = Decimal(result[0]) - Decimal(wallet[0])
    xrp_result = Decimal(result[1]) - Decimal(wallet[1])
    eth_result = Decimal(result[2]) - Decimal(wallet[2])

    print("BTC: " + str(btc_result))
    print("ETH: " + str(eth_result))
    print("XRP: " + str(xrp_result))


def main():
    wallet = [client.get_asset_balance(asset='BTC')["free"],
              client.get_asset_balance(asset='XRP')["free"],
              client.get_asset_balance(asset='ETH')["free"]]

    tickers = client.get_ticker()
    eth_btc = tickers[0]['askPrice']
    xrp_eth = tickers[91]['askPrice']
    xrp_btc = tickers[90]['askPrice']

    pricelist = [eth_btc, xrp_eth, xrp_btc]

    # 0.01 BTC -> ETH -> XRP -> BTC
    fwd= Decimal(0.01) / Decimal(eth_btc) / Decimal(xrp_eth) * Decimal(xrp_btc)

    # 0.01 BTC -> XRP -> ETH -> BTC
    bwd = Decimal(0.01) / Decimal(xrp_btc) * Decimal(xrp_eth) * Decimal(eth_btc)

    if fwd > 0.01:
        print("Forward: 0.01 BTC to " + str(fwd))
        # condition for trade
        if fwd / Decimal(0.01) > Decimal(1.00015):
            print("trade worthy forward")
            forward(pricelist)
            report(wallet)
    elif bwd > 0.01:
        print("Backward: 0.01 BTC to " + str(bwd))
        # condition for trade
        if bwd / Decimal(0.01) > Decimal(1.00015):
            print("trade worthy backward")
            backward(pricelist)
            report(wallet)
        else:
            print("trade not worth backward")
    else:
        print("No trade")


for i in range(50):
    main()
    time.sleep(3)

