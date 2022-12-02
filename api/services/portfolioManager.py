import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
import yfinance as yf

class portfolioManager:
    def __init__(self, stocksArray, optionsArray):
        self.stocksArray = stocksArray
        self.optionsArray = optionsArray
        self.portfolioValue = self.calculatePortfolioValue()

    def getStocksArray(self):
        return self.stocksArray
    
    def getOptionsArray(self):
        return self.optionsArray
    
    def getPortfolioValue(self):
        return self.portfolioValue

    def calculatePortfolioValue(self):
        # Calculate the portfolio value
        portfolioValue = 0
        for stock in self.stocksArray:
            ticker = yf.Ticker(stock["name"])
            portfolioValue += ticker.history(period="max")["Close"][-1] * stock["shares"]
        for option in self.optionsArray:
            ticker = yf.Ticker(option["name"])
            portfolioValue += ticker.history(period="max")["Close"][-1] * option["shares"]
        return portfolioValue

    # calculate portfolio daily returns
    def calculatePortfolioReturns(self):
        # Get the stock prices
        stockPrices = []
        for stock in self.stocksArray:
            ticker = yf.Ticker(stock["name"])
            stockPrices.append(ticker.history(period="max")["Close"])
        # Get the option prices
        optionPrices = []
        for option in self.optionsArray:
            ticker = yf.Ticker(option["name"])
            optionPrices.append(ticker.history(period="max")["Close"])
        # Calculate the portfolio returns
        portfolioReturns = []
        for i in range(len(stockPrices)):
            portfolioReturns.append(stockPrices[i] * self.stocksArray[i]["shares"])
        for i in range(len(optionPrices)):
            portfolioReturns.append(optionPrices[i] * self.optionsArray[i]["shares"])
        portfolioReturns = pd.DataFrame(portfolioReturns).sum()
        portfolioReturns = portfolioReturns.pct_change()
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
    
    # calculate portfolio value at risk
    def calculatePortfolioValueAtRisk(self):
        # Calculate the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Calculate the portfolio value at risk
        portfolioValueAtRisk = portfolioReturns.quantile(0.05)
        return portfolioValueAtRisk
    
    # calculate portfolio value at risk with confidence level
    def calculatePortfolioValueAtRiskWithConfidenceLevel(self, confidenceLevel):
        # Calculate the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Calculate the portfolio value at risk with confidence level
        portfolioValueAtRiskWithConfidenceLevel = portfolioReturns.quantile(confidenceLevel)
        return portfolioValueAtRiskWithConfidenceLevel
    
    # calculate portfolio conditional value at risk
    def calculatePortfolioConditionalValueAtRisk(self):
        # Calculate the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Calculate the portfolio conditional value at risk
        portfolioConditionalValueAtRisk = portfolioReturns.quantile(0.05)
        return portfolioConditionalValueAtRisk


# Path: api\services\stockManager.py