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
    # {
    #     "name": "AAPL",
    #     "shares": 1,
    #     "type": "call",
    #     "price": 0,
    # },
    # {
    #     "name": "GOOG",
    #     "shares": 2,
    #     "type": "put",
    #     "price": 0,
    # },
    {
        "name": "TSLA",
        "shares": 3,
        "type": "call",
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

# print(getOptionInfoFromYahooFinance("AAPL", "call")[0].info())


# black scholes
def blackScholes(r, S, K, T, sigma, type="call"):
    # calculate black scholes option price
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if type == "call":
        price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
    elif type == "put":
        price = K*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - S*norm.cdf(-d1, 0, 1)
    return price
    

# get blackSckoles parameters from AAPL option using getOptionInfoFromYahooFinance
def getBlackScholesParametersFromAAPLOption():
    # get options info from yahoo finance for all options in the portfolio
        for option in optionsArray:
            # get option info from yahoo finance
            optionInfo, nextValidExpiryDate = getOptionInfoFromYahooFinance(option["name"], option["type"])
            # conver nextValidExpiryDate to datetime
            nextValidExpiryDate = dt.datetime.strptime(nextValidExpiryDate, "%Y-%m-%d")
            # get stock price
            S = optionInfo["lastPrice"][0]
            # get strike price
            K = optionInfo["strike"][0]
            # get days between now and nextValidExpiryDate
            T = (nextValidExpiryDate - dt.datetime.now()).days
            if T == 0:
                T = 1
            # get volatility
            sigma = optionInfo["impliedVolatility"][0]
            # get risk free rate
            r = 0.01
            # run black scholes to get option price
            print("S: ", S)
            print("K: ", K)
            print("T: ", T)
            print("sigma: ", sigma)
            print("r: ", r)
            option[ "S" ] = S
            option[ "K" ] = K
            option[ "T" ] = T
            option["sigma"] = sigma
            price = blackScholes(r, S, K, T, sigma, option["type"])
            # add parameters to option
            print("price: ", price)
            option["price"] = price
        return optionsArray
    

AAPLOptionPrice = getBlackScholesParametersFromAAPLOption()
print("AAPL option price: ", AAPLOptionPrice)

