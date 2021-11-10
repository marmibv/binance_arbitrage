"""
author: Aiden Lewington
project: Binance Arbitrage Trading Bot
aim: using triangular arbitrage, automate trades that are guaranteed to return a specified profit or more.
"""

from binance.client import Client
from decimal import *
import time

api_key = ""
api_secret = ""

# initialise a client
client = Client(api_key, api_secret, {"timeout": 600})

getcontext().prec = 8

lot_sizes = {
    "ETHBTC": 0.00100000,
    "XRPETH": 1.00000000,
    "XRPBTC": 1.00000000
}


# trade forward
# BTC -> ETH -> XRP -> BTC
def forward(pricelist):
    eth_btc = pricelist[0]
    xrp_eth = pricelist[1]
    xrp_btc = pricelist[2]

    # buy eth with 0.01 btc
    eth_amount = Decimal(0.01) / Decimal(eth_btc)
    print("0.01 BTC to ETH ->" + str(eth_amount) + " ETH")
    eth_amount = eth_amount - (eth_amount % lot_sizes["ETHBTC"])
    print("trimmed to " + str(eth_amount))
    q1 = "{:0.0{}f}".format(eth_amount, 5)
    order_one = client.order_market_buy(symbol='ETHBTC', quantity=q1)

    # buy xrp with eth
    xrp_amount = eth_amount * Decimal(xrp_eth)
    print(str(eth_amount) + " ETH to XRP -> " + str(xrp_amount) + " XRP")
    xrp_amount = xrp_amount - (xrp_amount % lot_sizes["XRPBTC"])
    print("trimmed to " + str(xrp_amount))
    q2 = "{:0.0{}f}".format(xrp_amount, 5)
    order_two = client.order_market_buy(symbol='XRPETH', quantity=q2)
    print("trade two complete")

    # sell xrp amount for btc
    q3 = "{:0.0{}f}".format(xrp_amount, 5)
    order_three = client.order_market_sell(symbol='XRPBTC', quantity=q3)
    btc_amount = xrp_amount * Decimal(xrp_btc)
    print(str(xrp_amount) + " XRP to BTC ->" + str(btc_amount) + " BTC")
    print("========================================")
    print("0.01 BTC to " + str(btc_amount))
    print("========================================")


# trade backward
# BTC -> XRP -> ETH -> BTC
def backward(pricelist):
    eth_btc = pricelist[0]
    xrp_eth = pricelist[1]
    xrp_btc = pricelist[2]

    # buy xrp with 0.01 btc
    xrp_amount = Decimal(0.01) / Decimal(xrp_btc)
    print("0.01 BTC to XRP -> " + str(xrp_amount) + " XRP")
    xrp_amount = xrp_amount - (xrp_amount % Decimal(lot_sizes["XRPBTC"]))
    print("trimmed to " + str(xrp_amount))
    q1 = "{:0.0{}f}".format(xrp_amount, 5)
    order_one = client.order_market_buy(symbol='XRPBTC', quantity=q1)

    # sell xrp amount for eth
    eth_amount = xrp_amount * Decimal(xrp_eth)
    print(str(xrp_amount) + " XRP to ETH -> " + str(eth_amount) + " ETH")
    eth_amount = eth_amount - (eth_amount % Decimal(lot_sizes["ETHBTC"]))
    print("trimmed to " + str(eth_amount))
    q2 = "{:0.0{}f}".format(eth_amount, 5)
    order_two = client.order_market_sell(symbol='XRPETH', quantity=q1)
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

    start = time.time()

    tickers = client.get_ticker()
    eth_btc = tickers[0]['askPrice']
    xrp_eth = tickers[91]['askPrice']
    xrp_btc = tickers[90]['askPrice']

    pricelist = [eth_btc, xrp_eth, xrp_btc]

    # 0.01 BTC -> ETH -> XRP -> BTC
    fwd = Decimal(0.01) / Decimal(eth_btc) / Decimal(xrp_eth) * Decimal(xrp_btc)

    # 0.01 BTC -> XRP -> ETH -> BTC
    bwd = Decimal(0.01) / Decimal(xrp_btc) * Decimal(xrp_eth) * Decimal(eth_btc)

    if fwd > 0.01:
        print("Forward: 0.01 BTC to " + str(fwd))
        # condition for trade
        if fwd / Decimal(0.01) > Decimal(1.0002):
            print("trade worthy forward")
            forward(pricelist)
            end = time.time()
            print(end - start)
            report(wallet)
    elif bwd > 0.01:
        print("Backward: 0.01 BTC to " + str(bwd))
        # condition for trade
        if bwd / Decimal(0.01) > Decimal(1.0002):
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


for i in range(50):
    main()


