import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import yfinance as yf

from .portfolioManager import portfolioManager

class backtester:

# Likelihood ratio framework of Christoffersen 

    def __init__(self, portfolioManager, confidenceLevel, timeHorizon, riskFreeRate):
        self.portfolioManager = portfolioManager
        self.confidenceLevel = confidenceLevel
        self.timeHorizon = timeHorizon
        self.riskFreeRate = riskFreeRate

    def getPortfolioManager(self):
        return self.portfolioManager
    
    def getConfidenceLevel(self):
        return self.confidenceLevel
    
    def getTimeHorizon(self):
        return self.timeHorizon
    
    def getRiskFreeRate(self):
        return self.riskFreeRate
    
    def calculatePortfolioValue(self):
        return self.portfolioManager.getPortfolioValue()
    
    def calculatePortfolioReturns(self):
        return self.portfolioManager.calculatePortfolioReturns()
    
    def calculatePortfolioStandardDeviation(self):
        return self.portfolioManager.calculatePortfolioStandardDeviation()
    
    def calculatePortfolioExpectedReturn(self):
        return self.portfolioManager.calculatePortfolioExpectedReturn()
    
    def calculatePortfolioSharpeRatio(self):
        return self.portfolioManager.calculatePortfolioSharpeRatio()
    
    def calculatePortfolioVaR(self):
        return self.portfolioManager.calculatePortfolioVaR()
    
    def calculatePortfolioCVaR(self):
        return self.portfolioManager.calculatePortfolioCVaR()

    # value at risk (var) T-test 
    def calculatePortfolioVaRTTest(self):
        # Get the portfolio value
        portfolioValue = self.calculatePortfolioValue()
        # Get the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Get the portfolio standard deviation
        portfolioStandardDeviation = self.calculatePortfolioStandardDeviation()
        # Get the portfolio expected return
        portfolioExpectedReturn = self.calculatePortfolioExpectedReturn()
        # Get the portfolio sharpe ratio
        portfolioSharpeRatio = self.calculatePortfolioSharpeRatio()
        # Get the portfolio VaR
        portfolioVaR = self.calculatePortfolioVaR()
        # Get the portfolio CVaR
        portfolioCVaR = self.calculatePortfolioCVaR()
        # Calculate the portfolio VaR T-test
        portfolioVaRTTest = (portfolioValue - portfolioVaR) / (portfolioStandardDeviation * np.sqrt(self.timeHorizon))
        return portfolioVaRTTest

    # conditional value at risk (cvar) T-test
    def calculatePortfolioCVaRTTest(self):
        # Get the portfolio value
        portfolioValue = self.calculatePortfolioValue()
        # Get the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Get the portfolio standard deviation
        portfolioStandardDeviation = self.calculatePortfolioStandardDeviation()
        # Get the portfolio expected return
        portfolioExpectedReturn = self.calculatePortfolioExpectedReturn()
        # Get the portfolio sharpe ratio
        portfolioSharpeRatio = self.calculatePortfolioSharpeRatio()
        # Get the portfolio VaR
        portfolioVaR = self.calculatePortfolioVaR()
        # Get the portfolio CVaR
        portfolioCVaR = self.calculatePortfolioCVaR()
        # Calculate the portfolio CVaR T-test
        portfolioCVaRTTest = (portfolioValue - portfolioCVaR) / (portfolioStandardDeviation * np.sqrt(self.timeHorizon))
        return portfolioCVaRTTest
    
    # Kupiec Test
    def calculatePortfolioKupiecTest(self):
        # Get the portfolio value
        portfolioValue = self.calculatePortfolioValue()
        # Get the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Get the portfolio standard deviation
        portfolioStandardDeviation = self.calculatePortfolioStandardDeviation()
        # Get the portfolio expected return
        portfolioExpectedReturn = self.calculatePortfolioExpectedReturn()
        # Get the portfolio sharpe ratio
        portfolioSharpeRatio = self.calculatePortfolioSharpeRatio()
        # Get the portfolio VaR
        portfolioVaR = self.calculatePortfolioVaR()
        # Get the portfolio CVaR
        portfolioCVaR = self.calculatePortfolioCVaR()
        # Calculate the portfolio Kupiec test
        portfolioKupiecTest = portfolioValue / portfolioVaR
        return portfolioKupiecTest
    