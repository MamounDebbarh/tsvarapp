# value at risk calculator models
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
import yfinance as yf
from scipy.stats import norm
import scipy.stats as st




class Models:
    def __init__(self, portfolioManager):
        self.portfolioManager = portfolioManager

    def getPortfolioManager(self):
        return self.portfolioManager
    
    # calculate portfolio value at risk with historical simulation method
    def calculatePortfolioValueAtRiskWithHistoricalSimulationMethod(self, confidenceLevel):
        # Calculate the portfolio returns
        portfolioReturns = self.portfolioManager.getPortfolioReturns()
        # Calculate the portfolio mean with porfolio weights
        portfolioMean = np.dot(portfolioReturns.mean(), self.portfolioManager.getPortfolioWeights())
        print("portfolioMean: ", portfolioMean)
        # Calculate the porfolio standard deviation with portfolio weights
        portfolioStandardDeviation = np.sqrt(np.dot(self.portfolioManager.getPortfolioWeights().T, np.dot(portfolioReturns.cov(), self.portfolioManager.getPortfolioWeights())))
        # Calculate the portfolio value at risk with historical simulation method
        portfolioValueAtRiskWithHistoricalSimulationMethod = norm.ppf(confidenceLevel, portfolioMean, portfolioStandardDeviation)
        return portfolioValueAtRiskWithHistoricalSimulationMethod

    # calculate portfolio value at risk with historical simulation method over x days
    def calculatePortfolioValueAtRiskWithHistoricalSimulationMethodOverXDays(self, confidenceLevel, days):
        var = self.calculatePortfolioValueAtRiskWithHistoricalSimulationMethod(confidenceLevel)
        return var * np.sqrt(days)

    

    # TODO - Remove this method or understand what can be done with it
    def calculatePortfolioValueAtRiskWithHistoricalSimulationMethod2(self, confidenceLevel):
        # Calculate the portfolio returns
        portfolioReturns = self.portfolioManager.getPortfolioReturns()
        # Calculate the portfolio value at risk with historical simulation method of entire portfolio
        portfolioValueAtRiskWithHistoricalSimulationMethod = portfolioReturns.quantile(1 - confidenceLevel)
        return portfolioValueAtRiskWithHistoricalSimulationMethod


    def calculatePortfolioValueAtRiskWithParametricMethod(self, confidenceLevel):

        return 0


    # Geometric brownian motion simulation for stock price prediction with monte carlo method
    def geometricBrownianMotion(self, stockName, timePeriod, numberOfSimulations):
        # Get the stock prices
        ticker = yf.Ticker(stockName)
        stockPrices = ticker.history(period="max")["Close"]
        # Calculate the log returns
        logReturns = np.log(1 + stockPrices.pct_change())
        # Calculate the drift
        drift = logReturns.mean() - (0.5 * logReturns.var())
        # Calculate the standard deviation
        standardDeviation = logReturns.std()
        # Calculate the daily returns
        dailyReturns = np.exp(drift + standardDeviation * np.random.normal(0, 1, (timePeriod, numberOfSimulations)))
        # Calculate the stock prices
        stockPrices = stockPrices[-1] * dailyReturns
        return stockPrices
    
    # calculate portfolio value at risk with monte carlo simulation method
    def calculatePortfolioValueAtRiskWithMonteCarloSimulationMethod(self, confidenceLevel, timePeriod, numberOfSimulations):
        # Calculate the portfolio value at risk with monte carlo simulation method
        portfolioVaR = []
        for stock in self.portfolioManager.stocksArray:
            stockPrices = self.geometricBrownianMotion(stock["name"], timePeriod, numberOfSimulations)
            portfolioVaR.append(stockPrices[-1] * stock["shares"])
        # Calculate the portfolio value at risk with monte carlo simulation method
        portfolioVaR = pd.DataFrame(portfolioVaR).sum()
        portfolioVaR = portfolioVaR.quantile(confidenceLevel)
        return portfolioVaR
    
    # calculate conditional value at risk with monte carlo simulation method

    # calculate portfolio value at risk with garch method
    def calculatePortfolioValueAtRiskWithGarchMethod(self, confidenceLevel):
        return 0

    # calculate portfolio value at risk with cornish fisher method
    def calculatePortfolioValueAtRiskWithCornishFisherMethod(self, confidenceLevel):
        return 0

