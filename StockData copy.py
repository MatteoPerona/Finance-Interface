from bs4 import BeautifulSoup
import requests

from selenium import webdriver

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

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


#scrapes yfinance ranking tables
def getTopData(url='https://finance.yahoo.com/most-active'):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'lxml')
	#initializes var body as the body of the table that will be scraped
	body = soup.table.tbody
	
	numRows = 0
	with open('topData.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['#','Link', 'Ticker', 'Name', 'Price', 'Market Time', '%Change', 'Change', 'Volume', 'Avg Vol(3m)', 'Market Cap', 'Intraday High/Low', '52 Week Range'])
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



'''functions that work with current quotes'''
def lastStockPrice(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'    
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    price = soup.find('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
    return price.text

def currentChange(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'    
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    price = soup.find('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
    change = price.next_sibling
    return change.text

def priceCollector(ticker):
    now = dt.datetime.now()
    hour = now.hour
    minutes = now.minute
    price = lastStockPrice(ticker)
    with open(f'prices{ticker}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Datetime', 'Price'])
        while hour>=6 and minutes>=30 and hour<=9 and minutes>=30:
            sleep(1)
            now = dt.datetime.now()
            hour = now.hour
            minutes = now.minute
            writer.writerow([now, price])



'''Functions that get individual data and write to csv'''
def getHistory(ticker='AMD', startY=2015, startM=1, startD=1):
    start = dt.datetime(startY, startM, startD)
    end = dt.date.today()
    df = web.DataReader(ticker, 'yahoo', start, end)
    df.to_csv(f'{ticker}History.csv')


def getSummary(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    with open('summary.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ticker, 'Data'])
        
        pattern = soup.find('span', class_='Fw(b) D(b)--mobp C($positiveColor)').text
        writer.writerow(['Pattern', pattern])
        
        prevClose = soup.tr.find('span', class_='Trsdu(0.3s)').text
        writer.writerow(['Previous Close', prevClose])
        
        Open = soup.tr.next_sibling.find('span', class_='Trsdu(0.3s)').text
        writer.writerow(['Open', Open])
        
        bid = soup.tr.next_sibling.next_sibling.find('span', class_='Trsdu(0.3s)').text
        writer.writerow(['Bid', bid])
        
        ask = soup.tr.next_sibling.next_sibling.next_sibling.find('span', class_='Trsdu(0.3s)').text
        writer.writerow(['Ask', ask])
        
        dayRange = soup.find(attrs={'data-test':'DAYS_RANGE-value'}).text
        writer.writerow(["Day's Range", dayRange])
        
        wRange = soup.find(attrs={'data-test':'FIFTY_TWO_WK_RANGE-value'}).text
        writer.writerow(['52 Week Range', wRange])
        
        vol = soup.find(attrs={'data-test':'TD_VOLUME-value'}).text
        writer.writerow(['Volume', vol])
        
        avgVol = soup.find(attrs={'data-test':'AVERAGE_VOLUME_3MONTH-value'}).text
        writer.writerow(['Avg. Volume', avgVol])
        
        mCap= soup.find(attrs={'data-test':'MARKET_CAP-value'}).text
        writer.writerow(['Market Cap', mCap])
        
        beta = soup.find(attrs={'data-test':'BETA_5Y-value'}).text
        writer.writerow(['Beta', beta])
        
        pe = soup.find(attrs={'data-test':'PE_RATIO-value'}).text
        writer.writerow(['PE Ratio', pe])
        
        eps = soup.find(attrs={'data-test':'EPS_RATIO-value'}).text
        writer.writerow(['EPS', eps])
        
        ed = soup.find(attrs={'data-test':'EARNINGS_DATE-value'}).text
        writer.writerow(['Earnings Date', ed])
        
        fwdDiv = soup.find(attrs={'data-test':'DIVIDEND_AND_YIELD-value'}).text
        writer.writerow(['Forward Dividend & Yield', fwdDiv])
        
        exDiv = soup.find(attrs={'data-test':'EX_DIVIDEND_DATE-value'}).text
        writer.writerow(['Ex-Dividend Date', exDiv])
        
        yTEst = soup.find(attrs={'data-test':'ONE_YEAR_TARGET_PRICE-value'}).text
        writer.writerow(['1y Target Est', yTEst])


def getAnalysis(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}'
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    
    with open('analysis.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        tables = soup.find_all('table')
        for table in tables:
            head = table.thead
            body = table.tbody
            headRows = head.find_all('tr')
            bodyRows = body.find_all('tr')
            for tr in headRows:
                th = tr.find_all('th')
                writer.writerow([i.text for i in th])
            for tr in bodyRows:
                td = tr.find_all('td')
                writer.writerow([i.text for i in td])


def getStats(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    
    with open('stats.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        headRow = soup.table.thead.tr
        th = headRow.find_all('th')
        writer.writerow([i.text for i in th])
        
        tables = soup.find_all('table')
        for table in tables:
            body = table.tbody
            bodyRows = body.find_all('tr')
            for tr in bodyRows:
                td = tr.find_all('td')
                writer.writerow([i.text for i in td])


def getFinancials(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    
    with open('financials.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        table = soup.find('div', class_='M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)')
        head = table.find('div', class_='D(tbhg)')
        body = table.find('div', class_='D(tbrg)')

        span = head.find_all('span')
        writer.writerow([i.text for i in span])
        
        headDiv = body.find_all('div', class_='D(tbr) fi-row Bgc($hoverBgColor):h')
        for elem in headDiv:
            writer.writerow([span.text for span in elem])



if __name__ == "__main__":
	
	#getTopData(urls[2])

	print(lastStockPrice('gm'))
	#print(currentChange('TSLA'))

	'''getSummary('AMZN')
				getAnalysis('AMZN')
				getStats('AMZN')'''
	#getHistory()
	#df = pd.read_csv('AMDHistory.csv')


	

