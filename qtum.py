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

getcontext().prec = 8

lot_sizes = {
    "ETHBTC": 0.00100000,
    "QTUMETH": 0.01000000,
    "QTUMBTC": 0.01000000
}


# trade forward
# BTC -> ETH -> QTUM -> BTC
def forward(pricelist):
    eth_btc = pricelist[0]
    alt_eth = pricelist[1]
    alt_btc = pricelist[2]

    # buy eth with 0.01 btc
    eth_amount = Decimal(0.01) / Decimal(eth_btc)
    print("0.01 BTC to ETH ->" + str(eth_amount) + " ETH")
    eth_amount = eth_amount - (eth_amount % Decimal(lot_sizes["ETHBTC"]))
    print("trimmed to " + str(eth_amount))
    q1 = "{:0.0{}f}".format(eth_amount, 5)
    order_one = client.order_market_buy(symbol='ETHBTC', quantity=q1)

    # buy xrp with eth
    alt_amount = eth_amount / Decimal(alt_eth)
    print(str(eth_amount) + " ETH to QTUM -> " + str(alt_amount) + " QTUM")
    alt_amount = alt_amount - (alt_amount % Decimal(lot_sizes["QTUMBTC"]))
    print("trimmed to " + str(alt_amount))
    q2 = "{:0.0{}f}".format(alt_amount, 5)
    order_two = client.order_market_buy(symbol='QTUMETH', quantity=q2)
    print("trade two complete")

    # sell xrp amount for btc
    order_three = client.order_market_sell(symbol='QTUMBTC', quantity=q2)
    btc_amount = alt_amount * Decimal(alt_btc)
    print(str(alt_amount) + " QTUM to BTC ->" + str(btc_amount) + " BTC")
    print("========================================")
    print("0.01 BTC to " + str(btc_amount))
    print("========================================")


# trade backward
# BTC -> QTUM -> ETH -> BTC
def backward(pricelist):
    eth_btc = pricelist[0]
    alt_eth = pricelist[1]
    alt_btc = pricelist[2]

    # buy xrp with 0.01 btc
    alt_amount = Decimal(0.01) / Decimal(alt_btc)
    print("0.01 BTC to QTUM -> " + str(alt_amount) + " QTUM")
    alt_amount = alt_amount - (alt_amount % Decimal(lot_sizes["QTUMBTC"]))
    print("trimmed to " + str(alt_amount))
    q1 = "{:0.0{}f}".format(alt_amount, 5)
    order_one = client.order_market_buy(symbol='QTUMBTC', quantity=q1)

    # sell xrp amount for eth
    eth_amount = alt_amount * Decimal(alt_eth)
    print(str(alt_amount) + " QTUM to ETH -> " + str(eth_amount) + " ETH")
    eth_amount = eth_amount - (eth_amount % Decimal(lot_sizes["ETHBTC"]))
    print("trimmed to " + str(eth_amount))
    q2 = "{:0.0{}f}".format(eth_amount, 5)
    order_two = client.order_market_sell(symbol='QTUMETH', quantity=q1)
    print("trade two complete")

    order_three = client.order_market_sell(symbol='ETHBTC', quantity=q2)
    btc_amount = eth_amount * Decimal(eth_btc)
    print(str(eth_amount) + " ETH to BTC ->" + str(btc_amount) + " BTC")
    print('========================================')
    print("0.01 BTC to " + str(btc_amount))
    print("========================================")


# prints the real change in the exchange wallet
# include all three values in case residuals left aside
def report(wallet):
    result = [client.get_asset_balance(asset='BTC')["free"],
              client.get_asset_balance(asset='QTUM')["free"],
              client.get_asset_balance(asset='ETH')["free"]]

    # results
    btc_result = Decimal(result[0]) - Decimal(wallet[0])
    xrp_result = Decimal(result[1]) - Decimal(wallet[1])
    eth_result = Decimal(result[2]) - Decimal(wallet[2])

    print("BTC: " + str(btc_result))
    print("ETH: " + str(eth_result))
    print("QTUM: " + str(xrp_result))


def main():
    wallet = [client.get_asset_balance(asset='BTC')["free"],
              client.get_asset_balance(asset='QTUM')["free"],
              client.get_asset_balance(asset='ETH')["free"]]

    start = time.time()

    tickers = client.get_ticker()
    eth_btc = tickers[0]['askPrice']
    alt_eth = tickers[4]['askPrice']
    alt_btc = tickers[23]['askPrice']

    info = client.get_exchange_info()

    pricelist = [eth_btc, alt_eth, alt_btc]

    # 0.01 BTC -> ETH -> QTUM -> BTC
    fwd = Decimal(0.01) / Decimal(eth_btc) / Decimal(alt_eth) * Decimal(alt_btc)

    # 0.01 BTC -> QTUM -> ETH -> BTC
    bwd = Decimal(0.01) / Decimal(alt_btc) * Decimal(alt_eth) * Decimal(eth_btc)

    if fwd > 0.01:
        print("Forward: 0.01 BTC to " + str(fwd))
        # condition for trade
        if fwd > Decimal(0.01001):
            print("trade worthy forward")
            forward(pricelist)
            end = time.time()
            print(end - start)
            report(wallet)
    elif bwd > 0.01:
        print("Backward: 0.01 BTC to " + str(bwd))
        # condition for trade
        if bwd > Decimal(0.01001):
            print("trade worthy backward")
            backward(pricelist)
            end = time.time()
            print(end - start)
            report(wallet)
        else:
            print("trade not worth backward")
    else:
        end = time.time()
        print("No trade")


for i in range(10):
    main()
    time.sleep(5)

