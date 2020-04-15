from bs4 import BeautifulSoup
import requests

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import style

import pandas as pd
import pandas_datareader.data as web  
import csv



urls = ['https://finance.yahoo.com/cryptocurrencies', 'https://finance.yahoo.com/trending-tickers', 'https://finance.yahoo.com/most-active'
		, 'https://finance.yahoo.com/gainers', 'https://finance.yahoo.com/losers', 'https://finance.yahoo.com/etfs'
		, 'https://finance.yahoo.com/commodities', 'https://finance.yahoo.com/world-indices', 'https://finance.yahoo.com/currencies'
		, 'https://finance.yahoo.com/mutualfunds', 'https://finance.yahoo.com/options/highest-open-interest'
		, 'https://finance.yahoo.com/options/highest-implied-volatility', 'https://finance.yahoo.com/bonds']
#https://finance.yahoo.com/calendar
#https://finance.yahoo.com/currency-converter

headers = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "Connection":"keep-alive",
        "Host":"www.nasdaq.com",
        "Referer":"http://www.nasdaq.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
        }


def downloadHist(ticker='AMZN', startY=2015, startM=1, startD=1, endY=2020, endM=1, endD=1):
	style.use('ggplot')

	start = dt.datetime(startY, startM, startD)
	end = dt.datetime(endY, endM, endD)

	df = web.DataReader(ticker, 'yahoo', start, end)
	df.to_csv(f'{ticker}History.csv')
	

#scrapes yfinance ranking tables
def getTopData(url='https://finance.yahoo.com/most-active'):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'lxml')
	#initializes var body as the body of the table that will be scraped
	body = soup.table.tbody
	
	numRows = 0
	with open('topData.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['#','Link', 'Ticker', 'Name', 'Price', 'Market Time', 'Change', '%Change', 'Volume', 'Avg Vol(3m)', 'Market Cap', 'Intraday High/Low', '52 Week Range'])
		for row in body.find_all('tr'):

			numRows+=1

			#initalizing variables to be scraped
			link = row.a.get('href')
			ticker = row.a.text
			name = row.td.next_sibling.text
			price = row.td.next_sibling.next_sibling.text
			marketTime = row.td.next_sibling.next_sibling.next_sibling.text
			change = row.td.next_sibling.next_sibling.next_sibling.next_sibling.span.text
			percentChange = row.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.span.text
			volume = row.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
			avgVolMon = row.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
			marketCap = row.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
			intraDay = row.canvas.get('data-reactid')
			weekrange = row.canvas.next.get('data-reactid')

			writer.writerow([numRows, link, ticker, name, price, marketTime, change, percentChange, volume, avgVolMon, marketCap, intraDay, weekrange])


def getIndivData(quote):
	url = 'https://finance.yahoo.com/quote/CCL?p=CCL'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'lxml')



def lastStockPrice(ticker):#Scrapes correct area but there is some block in place that doesn't let me scrape the price
	url = f'https://www.nasdaq.com/market-activity/stocks/{ticker}/latest-real-time-trades'
	r = requests.get(url,headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')

	body = soup.table.tbody

	time = body.tr.th
	price = body.tr.td

	return price




'''
Functions to Produce:

-write individual data to csv

-function that returns last price on nasdaq
'''

if __name__ == "__main__":
	#getTopData(urls[2])
	#lastStockPrice('TSLA')
	#getIndivData('TSLA')
	downloadHist(startY=1997, endM=4, endD=14)
	dp = pd.read_csv('AMZNHistory.csv', parse_dates=True, index_col=0)
	dp['Close'].plot()
	plt.yscale('log')
	plt.show()

