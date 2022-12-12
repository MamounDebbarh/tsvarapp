# value at risk calculator models
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
import yfinance as yf
from scipy.stats import norm, t
import scipy.stats as st

from services.portfolioManager import PortfolioManager

# Var calculator testing method. Not used in the app
def calculateVarstdmean(confidenceLevel, portfolioManager):
    # Calculate the portfolio returns
    portfolioReturns = portfolioManager.calculatePortfolioReturns()
    # Calculate the portfolio mean with porfolio weights
    portfolioMean = np.dot(portfolioReturns.mean(), portfolioManager.calculatePortfolioWeights())
    # Calculate the porfolio standard deviation with portfolio weights
    portfolioStandardDeviation = np.sqrt(np.dot(portfolioManager.calculatePortfolioWeights().T, np.dot(portfolioReturns.cov(), portfolioManager.calculatePortfolioWeights())))
    # Calculate the portfolio value at risk with historical simulation method
    portfolioValueAtRiskWithHistoricalSimulationMethod = norm.ppf(confidenceLevel, portfolioMean, portfolioStandardDeviation)
    return portfolioValueAtRiskWithHistoricalSimulationMethod

def historicalVaR(portfolioReturnsWithWeights, alpha=5):
    if isinstance(portfolioReturnsWithWeights, pd.Series):
        return np.percentile(portfolioReturnsWithWeights, alpha)
    elif isinstance(portfolioReturnsWithWeights, pd.DataFrame):
        return portfolioReturnsWithWeights.aggregate(historicalVaR, alpha=alpha)
    else:
        raise TypeError("Expected returns to be dataframe or series: ", type(portfolioReturnsWithWeights))

def historicalCVaR(portfolioReturnsWithWeights, alpha=5):
    if isinstance(portfolioReturnsWithWeights, pd.Series):
        belowVaR = portfolioReturnsWithWeights <= historicalVaR(portfolioReturnsWithWeights, alpha=alpha)
        return portfolioReturnsWithWeights[belowVaR].mean()
    elif isinstance(portfolioReturnsWithWeights, pd.DataFrame):
        return portfolioReturnsWithWeights.aggregate(historicalCVaR, alpha=alpha)
    else:
        raise TypeError("Expected returns to be dataframe or series")
        
def var_parametric(portofolioReturns, portfolioStd, distribution='normal', alpha=5, dof=6):
    if distribution == 'normal':
        VaR = norm.ppf(1-alpha/100)*portfolioStd - portofolioReturns
    elif distribution == 't-distribution':
        nu = dof
        VaR = np.sqrt((nu-2)/nu) * t.ppf(1-alpha/100, nu) * portfolioStd - portofolioReturns
    else:
        raise TypeError("Expected distribution type 'normal'/'t-distribution'")
    return VaR

def cvar_parametric(portofolioReturns, portfolioStd, distribution='normal', alpha=5, dof=6):
    if distribution == 'normal':
        CVaR = (alpha/100)**-1 * norm.pdf(norm.ppf(alpha/100))*portfolioStd - portofolioReturns
    elif distribution == 't-distribution':
        nu = dof
        xanu = t.ppf(alpha/100, nu)
        CVaR = -1/(alpha/100) * (1-nu)**(-1) * (nu-2+xanu**2) * t.pdf(xanu, nu) * portfolioStd - portofolioReturns
    else:
        raise TypeError("Expected distribution type 'normal'/'t-distribution'")
    return CVaR

def mcSim(portfolio):
    # Monte Carlo Method
    portfolioReturns = portfolio.calculatePortfolioReturns()
    mc_sims = 400 # number of simulations
    T = 100 #timeframe in days
    weights = portfolio.calculatePortfolioWeights()
    meanM = np.full(shape=(T, len(weights)), fill_value=portfolio.calculatePortfolioReturns().mean())
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
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)
    else:
        raise TypeError("Expected a pandas data series.")

def mcCVaR(returns, alpha=5):
    if isinstance(returns, pd.Series):
        belowVaR = returns <= mcVaR(returns, alpha=alpha)
        return returns[belowVaR].mean()
    else:
        raise TypeError("Expected a pandas data series.")


# Geometric brownian motion simulation for stock price prediction with monte carlo method
def geometricBrownianMotion(stockName, timePeriod, numberOfSimulations):
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
def useBrownianMotionVar(portfolio ,confidenceLevel, timePeriod, numberOfSimulations):
    # Calculate the portfolio value at risk with monte carlo simulation method
    portfolioVaR = []
    for stock in portfolio.stocksArray:
        stockPrices = geometricBrownianMotion(stock["name"], timePeriod, numberOfSimulations)
        portfolioVaR.append(stockPrices[-1] * stock["shares"])
    # Calculate the portfolio value at risk with monte carlo simulation method
    portfolioVaR = pd.DataFrame(portfolioVaR).sum()
    portfolioVaR = portfolioVaR.quantile(confidenceLevel)
    return portfolioVaR


