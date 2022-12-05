import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
import yfinance as yf
from scipy.stats import norm


PERIOD = "5y"

class PortfolioManager:
    def __init__(self, stocksArray, optionsArray):
        self.stocksArray = stocksArray
        self.optionsArray = optionsArray
        self.portfolioValue = self.calculatePortfolioValue()
        self.portfolioWeights = self.calculatePortfolioWeights()
        self.portfolioReturns = self.calculatePortfolioReturns()
        self.portfolioReturnsWithWeights = self.generatePorfolioReturnsWithWeights()
        self.portfolioStandardDeviation = self.calculatePortfolioStandardDeviation()

    def getStocksArray(self):
        return self.stocksArray
    
    def getOptionsArray(self):
        return self.optionsArray
    
    def getPortfolioValue(self):
        return self.portfolioValue

    def getPortfolioWeights(self):
        return self.portfolioWeights

    def getPortfolioReturns(self):
        return self.portfolioReturns

    def getPortfolioStandardDeviation(self):
        return self.portfolioStandardDeviation

    def getPortfolioReturnsWithWeights(self):
        return self.portfolioReturnsWithWeights

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
            stockPrices = yf.download(tickers=stockNames, start=start, end=end)["Close"]
        # Get the option prices
        if len(optionNames) > 0:
            optionPrices = yf.download(tickers=optionNames, start=start, end=end)["Close"]
        # Merge the stock and option prices
        if len(stockNames) > 0 and len(optionNames) > 0:
            portfolioData = pd.merge(stockPrices, optionPrices, on="Date")
        elif len(stockNames) > 0:
            portfolioData = stockPrices
        elif len(optionNames) > 0:
            portfolioData = optionPrices
        portfolioData = portfolioData.dropna()
        return portfolioData

    # calculate portfolio value from portfolio data
    def calculatePortfolioValue(self):
        # Download portfolio data
        portfolioData = self.downloadPortfolioData()
        # Calculate the portfolio value
        portfolioValue = 0
        for stock in self.stocksArray:
            portfolioValue += stock["shares"] * portfolioData[stock["name"]]
        for option in self.optionsArray:
            portfolioValue += option["shares"] * portfolioData[option["name"]]
        return portfolioValue

    # calculate portfolio daily returns
    def calculatePortfolioReturns(self):
        # Download portfolio data
        portfolioData = self.downloadPortfolioData()
        # Calculate the portfolio returns
        portfolioReturns = portfolioData.pct_change()
        portfolioReturns = portfolioReturns.dropna()
        return portfolioReturns

    def generatePorfolioReturnsWithWeights(self):
        # Calculate the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Calculate the portfolio weights
        portfolioWeights = self.calculatePortfolioWeights()
        # create porfolio weights column
        portfolioReturns["Portfolio"] = portfolioReturns.dot(portfolioWeights)
        portfolioReturns = portfolioReturns.dropna()
        return portfolioReturns

    # get portfolio correlation matrix
    def getPortfolioCorrelationMatrix(self):
        # Calculate the portfolio returns
        portfolioReturns = self.getPortfolioReturns()
        # Calculate the portfolio correlation matrix
        portfolioCorrelationMatrix = portfolioReturns.corr()
        return portfolioCorrelationMatrix

    # Cholesky decomposition of the variance covariance matrix
    def getCholeskyDecomposition(self):
        # Calculate the variance covariance matrix
        portfolioReturns = self.calculatePortfolioReturns()
        varianceCovarianceMatrix = portfolioReturns.cov()         # Calculate the Cholesky decomposition
        choleskyDecomposition = np.linalg.cholesky(varianceCovarianceMatrix)
        return choleskyDecomposition
    
    # eigen decomposition of the variance covariance matrix
    def getEigenDecomposition(self):
        # Calculate the variance covariance matrix
        portfolioReturns = self.calculatePortfolioReturns()
        varianceCovarianceMatrix = portfolioReturns.cov()        # Calculate the eigen decomposition
        eigenValues, eigenVectors = np.linalg.eig(varianceCovarianceMatrix)
        return eigenValues, eigenVectors
    
    # calculate portfolio weights
    def calculatePortfolioWeights(self):
        # download portfolio data
        portfolioData = self.downloadPortfolioData()
        uptodatedStockPrices = []
        uptodatedOptionPrices = []
        updatedPortfolioValue = 0
        # get uptodate stock prices
        for stock in self.stocksArray:
            uptodatedStockPrices.append(portfolioData[stock["name"]][-1])
        # get uptodate option prices
        for option in self.optionsArray:
            uptodatedOptionPrices.append(portfolioData[option["name"]][-1])
        # get updated portfolio value
        for stock in uptodatedStockPrices:
            updatedPortfolioValue += stock
        for option in uptodatedOptionPrices:
            updatedPortfolioValue += option
        # calculate portfolio weights
        portfolioWeights = []
        for stock in uptodatedStockPrices:
            portfolioWeights.append(stock / updatedPortfolioValue)
        for option in uptodatedOptionPrices:
            portfolioWeights.append(option / updatedPortfolioValue)
        return np.array(portfolioWeights)

    # calculate portfolio standard deviation
    def calculatePortfolioStandardDeviation(self):
        # Calculate the variance covariance matrix
        portfolioReturns = self.calculatePortfolioReturns()
        varianceCovarianceMatrix = portfolioReturns.cov()
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
        portfolioReturns = self.calculatePortfolioReturns()
        varianceCovarianceMatrix = portfolioReturns.cov()
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

    # Calculate confidence interval
    def calculateConfidenceInterval(self, confidenceLevel):
        # Calculate the portfolio returns
        portfolioReturns = self.getPortfolioReturns()
        # Calculate the portfolio mean with porfolio weights
        portfolioMean = np.dot(portfolioReturns.mean(), self.getPortfolioWeights())
        # Calculate the porfolio standard deviation with portfolio weights
        portfolioStandardDeviation = np.sqrt(np.dot(self.getPortfolioWeights().T, np.dot(portfolioReturns.cov(), self.getPortfolioWeights())))
        # Calculate the confidence interval
        confidenceInterval = norm.interval(confidenceLevel, portfolioMean, portfolioStandardDeviation)
        return confidenceInterval
    
# Path: api\services\stockManager.py