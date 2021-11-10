# binance_arbitrage trading bot
 This is a trading bot being made to take advantage of arbitrage opportunity in cryptocurrency markets, specifically on the exchange Binance.
 This has been made using the python-binance API wrapper available at https://python-binance.readthedocs.io/

This bot successfully trades on the binance exchange. APIs keys need to be changed - mine have since been deleted.  
</br>
**qtum.py** is the main bot trading through the coins ETH/BTC/QTUM. The thought being that qtum was a relatively small volume coin at the time of making this bot, therefore providing decent opportunity for arbitrage.  </br>
Things to consider in the future;  
* highly liquid markets will take advantage of arbritrage before you can (via HFT, better connection, C++ algos etc.) 
* the more illiquid a market is, the higher arbitrage there will be. The challenge here is finding a 3-way grouping of coins. To target these it should just be regular arbitrage between two currencies.
 
 Author  - aidenlew 2019
