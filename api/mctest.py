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
optionsArray = [
    {
        "name": "AAPL",
        "type": "call",
    },
    {
        "name": "GOOG",
        "type": "put",
    },
]

# get option informaton from yahoo finance
def getOptionInfoFromYahooFinance(name, type):
    # get option info from yahoo finance
    optionInfo = yf.Ticker(name)
    # get next valid expiry date
    nextValidExpiryDate = optionInfo.options[0]
    # get option info
    optionInfo = optionInfo.option_chain(nextValidExpiryDate)
    # get call options
    callOptions = optionInfo.calls
    # get put options
    putOptions = optionInfo.puts
    # get option info
    if type == "call":
        optionInfo = callOptions
    elif type == "put":
        optionInfo = putOptions
    # return option info
    return optionInfo, nextValidExpiryDate

print(getOptionInfoFromYahooFinance("AAPL", "call")[0].info())


# black scholes
def blackScholes(r, S, K, T, sigma, type="C"):
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

# get blackSckoles parameters from AAPL option using getOptionInfoFromYahooFinance
def getBlackScholesParametersFromAAPLOption():
    # get option info from yahoo finance
    optionInfo, nextValidExpiryDate = getOptionInfoFromYahooFinance("AAPL", "call")
    # conver nextValidExpiryDate to datetime
    nextValidExpiryDate = dt.datetime.strptime(nextValidExpiryDate, "%Y-%m-%d")
    # get risk free rate
    r = optionInfo["openInterest"]
    # get stock price
    S = optionInfo["lastPrice"][0]
    # get strike price
    K = optionInfo["strike"][0]
    # get time to maturity
    T = (nextValidExpiryDate - dt.datetime.now()).days/365
    # get volatility
    sigma = optionInfo["impliedVolatility"][0]
    # return parameters
    return r, S, K, T, sigma
    

r, S, K, T, sigma = getBlackScholesParametersFromAAPLOption()
AAPLOptionPrice = blackScholes(r, S, K, T, sigma, type="c")
print("risk free rate: ", r)
print("stock price: ", S)
print("strike price: ", K)
print("time to maturity: ", T)
print("volatility: ", sigma)
print("AAPL option price: ", AAPLOptionPrice)

