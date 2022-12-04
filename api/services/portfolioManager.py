import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
import yfinance as yf

PERIOD = "5y"

class portfolioManager:
    def __init__(self, stocksArray, optionsArray):
        self.stocksArray = stocksArray
        self.optionsArray = optionsArray

    def getStocksArray(self):
        return self.stocksArray
    
    def getOptionsArray(self):
        return self.optionsArray
    
    def getPortfolioValue(self):
        return self.portfolioValue

    # get download portfolio data
    def downloadPortfolioData(self):
        start = dt.datetime(2015, 1, 1)
        end = dt.datetime.now()
        # get names in stocksArray
        stockNames = []
        for stock in self.stocksArray:
            stockNames.append(stock["name"])
        # get names in optionsArray
        optionNames = []
        for option in self.optionsArray:
            optionNames.append(option["name"])

        # Get the stock prices
        if len(stockNames) > 0:
            stockPrices = yf.download(tickers=stockNames, start=start, end=end)["Adj Close"]
        # Get the option prices
        if len(optionNames) > 0:
            optionPrices = yf.download(tickers=optionNames, start=start, end=end)["Adj Close"]
        # Merge the stock and option prices
        if len(stockNames) > 0 and len(optionNames) > 0:
            portfolioData = pd.merge(stockPrices, optionPrices, on="Date")
        elif len(stockNames) > 0:
            portfolioData = stockPrices
        elif len(optionNames) > 0:
            portfolioData = optionPrices
        
        print(portfolioData)
        return portfolioData

    # calculate portfolio value from portfolio data
    def calculatePortfolioValue(self):
        # Download portfolio data
        portfolioData = self.downloadPortfolioData()
        # Calculate the portfolio value
        portfolioValue = 0
        for stock in self.stocksArray:
            portfolioValue += stock["shares"] * portfolioData[stock["ticker"]]["Close"][-1]
        for option in self.optionsArray:
            portfolioValue += option["shares"] * portfolioData[option["ticker"]]["Close"][-1]
        return portfolioValue

    # calculate portfolio daily returns
    def calculatePortfolioReturns(self):
        # Download portfolio data
        portfolioData = self.downloadPortfolioData()
        # Calculate the portfolio returns
        portfolioReturns = portfolioData.pct_change()
        return portfolioReturns

    # varience covariance matrix from portfolio returns
    def calculateVarianceCovarianceMatrix(self):
        # Calculate the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Calculate the variance covariance matrix
        varianceCovarianceMatrix = portfolioReturns.cov()
        return varianceCovarianceMatrix
    
    # calculate expected portfolio returns
    def calculateExpectedPortfolioReturns(self):
        # Calculate the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Calculate the expected portfolio returns
        expectedPortfolioReturns = portfolioReturns.mean()
        return expectedPortfolioReturns

    # calculate portfolio weights
    def calculatePortfolioWeights(self):
        # Calculate the portfolio value
        portfolioValue = self.calculatePortfolioValue()
        # Calculate the portfolio weights
        portfolioWeights = []
        for stock in self.stocksArray:
            portfolioWeights.append(stock["shares"] / portfolioValue)
        for option in self.optionsArray:
            portfolioWeights.append(option["shares"] / portfolioValue)
        return portfolioWeights
    
    # calculate portfolio standard deviation
    def calculatePortfolioStandardDeviation(self):
        # Calculate the variance covariance matrix
        varianceCovarianceMatrix = self.calculateVarianceCovarianceMatrix()
        # Calculate the portfolio weights
        portfolioWeights = self.calculatePortfolioWeights()
        # Calculate the portfolio standard deviation
        portfolioStandardDeviation = np.sqrt(np.dot(portfolioWeights.T, np.dot(varianceCovarianceMatrix, portfolioWeights)))
        return portfolioStandardDeviation
    
    # calculate portfolio sharpe ratio
    def calculatePortfolioSharpeRatio(self):
        # Calculate the expected portfolio returns
        expectedPortfolioReturns = self.calculateExpectedPortfolioReturns()
        # Calculate the portfolio standard deviation
        portfolioStandardDeviation = self.calculatePortfolioStandardDeviation()
        # Calculate the portfolio sharpe ratio
        portfolioSharpeRatio = expectedPortfolioReturns / portfolioStandardDeviation
        return portfolioSharpeRatio
    
    # calculate portfolio beta
    def calculatePortfolioBeta(self):
        # Calculate the variance covariance matrix
        varianceCovarianceMatrix = self.calculateVarianceCovarianceMatrix()
        # Calculate the portfolio weights
        portfolioWeights = self.calculatePortfolioWeights()
        # Calculate the portfolio beta
        portfolioBeta = np.dot(portfolioWeights.T, varianceCovarianceMatrix)
        return portfolioBeta
    
    # calculate portfolio alpha
    def calculatePortfolioAlpha(self):
        # Calculate the expected portfolio returns
        expectedPortfolioReturns = self.calculateExpectedPortfolioReturns()
        # Calculate the portfolio beta
        portfolioBeta = self.calculatePortfolioBeta()
        # Calculate the portfolio alpha
        portfolioAlpha = expectedPortfolioReturns - 0.02 * portfolioBeta
        return portfolioAlpha

# Path: api\services\stockManager.py