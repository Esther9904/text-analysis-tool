import yfinance as yf
from datetime import datetime, date
import requests

def extractBasicInfo(data):
    keysToExtract = [ 'longName', 'website', 'sector', 'fullTimeEmployees', 'marketCap' , 'totalRevenue' , 'trailingEps']
    basicInfo = {}
    for key in keysToExtract :
        if key in data:
            basicInfo[key] = data[key]
        else:
           basicInfo[key] = '' 
    return basicInfo

def getPriceHistory(company):
    historyDf = company.history(period='12mo')
    prices = historyDf['Open'].tolist()
    dates = historyDf.index.strftime('%Y-%m-%d').tolist()
    return {
        'price': prices,
        'date': dates
    }

def getEarningsDates(company):
    earningsDatesDf = company.earnings_dates
    allDates = earningsDatesDf.index.strftime('%Y-%m-%d').tolist()
    dateObjects = [datetime.strptime(date, '%Y-%m-%d') for date in allDates]
    currentDate= datetime.today()
    futureDates = [date.strftime('%Y-%m-%d') for date in dateObjects if date > currentDate]
    return futureDates

def getCompanyNews(company):
    newsList = company.news
    allNewsArticles = []
    for newsDict in newsList:
        newsDictToAdd = {
            'title': newsDict['content']['title'],
            'url': newsDict['content']['canonicalUrl']['url']      
        }
        allNewsArticles.append(newsDictToAdd)
    return allNewsArticles

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
}
def extractCompanyNewsArticles(newsArticles):
    url = newsArticles[0]['url']
    page = requests.get(url, headers=headers)
    print(page.text)
    

def getCompanyStockInfo(tickerSymbol):
    # Get data from yahoo Finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on company
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningDates = getEarningsDates(company)
    newsArticles = getCompanyNews(company)
    extractCompanyNewsArticles(newsArticles)
    

getCompanyStockInfo('MSFT')