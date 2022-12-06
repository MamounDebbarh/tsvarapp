import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
import yfinance as yf
from scipy.stats import norm, t
import scipy.stats as st


from services.portfolioManager import PortfolioManager

# array of stocks
stocksArray = [
            # {
            #     "name": "AAPL",
            #     "shares": 1,
            # },
            # {
            #     "name": "GOOG",
            #     "shares": 2,
            # },
            # {
            #     "name": "MSFT",
            #     "shares": 3,
            # },
        ]
# array of options
optionsArray = []

portfolio = PortfolioManager(stocksArray, optionsArray)
portfolioReturnsWithWeights = portfolio.getPortfolioReturnsWithWeights()
portfolioReturns = portfolio.getPortfolioReturns()

interestRate = 0.01
underline = 30
strike = 40
T = 240/365
sigma = 0.3

# black scholes
def blackScholes(interestRate, underline, strike, T, sigma, type="C"):
    # calculate black scholes option price
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "c":
            price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif type == "p":
            price = K*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - S*norm.cdf(-d1, 0, 1)
        return price
    except:
        print("Please confirm option type, either 'c' for Call or 'p' for Put!")