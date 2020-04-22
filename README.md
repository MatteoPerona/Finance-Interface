# Finance Interface
 A library for filtering, storing, and manipulating stock/crypto data
 
 # Usage:
 
 import StockData as sd
 
  # For Yahoo Finance Filtered Ranking Tables:
 
  sd.getTopData(url)
  - the url entered must be a yfinance ranking table 
  - ex: 'https://finance.yahoo.com/most-active' (this url is also the default value)
  - create your own yfinance filters and enter the url to get data as csv
 
 
  # For Realtime Stock Data:
 
  sd.lastStockPrice(ticker)
  - enter a ticker (string)
  - returns last price
 
  sd.currentChange(ticker)
   - enter a ticker (string)
   - returns change
  
  sd.priceCollector(ticker)
  - enter a ticker (string)
  - get second by second price of given ticker written to csv
 
 
  # Yahoo Finance Analytics:
 
  sd.getHistory(ticker, startY=2015, startM=1, startD=1)
  - enter a ticker (string), start year (int), start month(int), and start dat(int)
  - produces a csv file with daily stock info from start y, m, d to present y, m, d
 
  sd.getSummary(ticker)
  - enter a ticker
  - produces a csv with yfinance summary
 
  sd.getAnalysis(ticker)
  - enter a ticker
  - produces a csv with yfinance analysis
 
  sd.getStats(ticker)
  - enter a ticker
  - produces a csv with yfinance stats
 
  sd.getFinancials(ticker)
  - enter a ticker
  - produces a csv with yfinance financials
 
 
 
