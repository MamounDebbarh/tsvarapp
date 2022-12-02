# Value at risk calculator class
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
import yfinance as yf

from .portfolioManager import portfolioManager

from scipy.special import ndtri
from scipy.stats import norm
from scipy.stats import t
from scipy.stats import skew
from scipy.stats import kurtosis
from scipy.stats import skewtest
from scipy.stats import kurtosistest
from scipy.stats import jarque_bera
from scipy.stats import normaltest
from scipy.stats import shapiro
from scipy.stats import anderson

class varCalculator:
    def __init__(self, stocksArray, optionsArray, confidenceLevel):
        self.stocksArray = stocksArray
        self.optionsArray = optionsArray
        self.confidenceLevel = confidenceLevel
        self.var = self.calculateVar()
        self.cvar = self.calculateCvar()

    def getStockPrices(self):   
        # Get the stock prices
        stockPrices = []
        for stock in self.stocksArray:
            ticker = yf.Ticker(stock["name"])
            stockPrices.append(ticker.history(period="max")["Close"])
        return stockPrices
    
    def getOptionPrices(self):
        # Get the option prices
        optionPrices = []
        for option in self.optionsArray:
            ticker = yf.Ticker(option["name"])
            optionPrices.append(ticker.history(period="max")["Close"])
        return optionPrices

    def getVar(self):
        return self.var
    
    def getCvar(self):
        return self.cvar
    
    def getConfidenceLevel(self):
        return self.confidenceLevel
    
    def calculateCvar(self):
        # Calculate the conditional value at risk for the portfolio
        # using historical simulation
        # Get the stock prices
        stockPrices = self.getStockPrices()
        # Get the option prices
        optionPrices = self.getOptionPrices()
        # Calculate the portfolio value
        portfolioValue = self.calculatePortfolioValue(stockPrices, optionPrices)
        # Calculate the conditional value at risk
        cvar = []
        for i in range(len(portfolioValue)):
            cvar.append(portfolioValue[i][portfolioValue[i] <= self.var[i]].mean())
        return cvar
    
    def calculateVar(self):
        # Calculate the value at risk for the portfolio
        # using historical simulation
        # Get the stock prices
        stockPrices = self.getStockPrices()
        # Get the option prices
        optionPrices = self.getOptionPrices()
        # Calculate the portfolio value
        portfolioValue = self.calculatePortfolioValue(stockPrices, optionPrices)
        # Calculate the value at risk
        var = []
        for i in range(len(portfolioValue)):
            var.append(np.percentile(portfolioValue[i], 100 - self.confidenceLevel))
        return var
    
