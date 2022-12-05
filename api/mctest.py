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
            {
                "name": "AAPL",
                "shares": 1,
            },
            {
                "name": "GOOG",
                "shares": 2,
            },
            {
                "name": "MSFT",
                "shares": 3,
            },
        ]
# array of options
optionsArray = []

portfolio = PortfolioManager(stocksArray, optionsArray)
portfolioReturnsWithWeights = portfolio.getPortfolioReturnsWithWeights()
portfolioReturns = portfolio.getPortfolioReturns()

def mcSim(portfolio):
    # Monte Carlo Method
    mc_sims = 400 # number of simulations
    T = 100 #timeframe in days
    weights = portfolio.getPortfolioWeights()
    meanM = np.full(shape=(T, len(weights)), fill_value=portfolioReturns.mean())
    meanM = meanM.T
    portfolio_sims = np.full(shape=(T, mc_sims), fill_value=0.0)
    varianceCovarianceMatrix = portfolioReturns.cov()

    for m in range(0, mc_sims):
        # MC loops
        Z = np.random.normal(size=(T, len(weights)))
        L = np.linalg.cholesky(varianceCovarianceMatrix)
        dailyReturns = meanM + np.inner(L, Z)
        portfolio_sims[:,m] = np.cumprod(np.inner(weights, dailyReturns.T)+1)
    return portfolio_sims

def mcVaR(returns, alpha=5):
    """ Input: pandas series of returns
        Output: percentile on return distribution to a given confidence level alpha
    """
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)
    else:
        raise TypeError("Expected a pandas data series.")

def mcCVaR(returns, alpha=5):
    """ Input: pandas series of returns
        Output: CVaR or Expected Shortfall to a given confidence level alpha
    """
    if isinstance(returns, pd.Series):
        belowVaR = returns <= mcVaR(returns, alpha=alpha)
        return returns[belowVaR].mean()
    else:
        raise TypeError("Expected a pandas data series.")

portfolioSim = mcSim(portfolio=portfolio)
portResults = pd.Series(portfolioSim[-1,:])
VaR = mcVaR(portResults, alpha=5)
CVaR = mcCVaR(portResults, alpha=5)

print("Monte Carlo VaR: \n", VaR)
print("Monte Carlo CVaR: \n", CVaR)