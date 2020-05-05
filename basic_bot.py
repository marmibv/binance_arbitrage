
from binance.client import Client
from decimal import *

api_key = "18YtfZfxwuBEN1V4fupoJakkuWvy1cwlNCPaWNKopjxkJkAoDeZdUNtfPk1cBdeY"
api_secret = "IWckkJsFQCGONzFzz9CWJaapgpM2BSOiGxKWLqpHoIk1lJ8G2OlPWBwEio4eDihI"

# initialise a client
client = Client(api_key, api_secret, {"timeout": 600})

lot_sizes = {
    "ETHBTC" : 0.00100000,
    "XRPETH" : 1.00000000,
    "XRPBTC" : 1.00000000
}

getcontext().prec = 8

def main():

    balance = client.get_asset_balance(asset='BTC')

    # get our three price indices
    tickers = client.get_ticker()
    eth_btc = tickers[0]['askPrice']
    xrp_eth = tickers[91]['askPrice']
    xrp_btc = tickers[90]['askPrice']

    # 0.01 BTC -> XRP -> ETH -> BTC
    backward = 0.01 / float(xrp_btc) * float(xrp_eth) * float(eth_btc)

    print("backwards trade: " + str(backward))

    # buy xrp with 0.02 btc
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

main()
