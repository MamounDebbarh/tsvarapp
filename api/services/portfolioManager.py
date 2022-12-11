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

    def getStocksArray(self):
        return self.stocksArray
    
    def getOptionsArray(self):
        return self.optionsArray

    # get download portfolio data
    def downloadPortfolioData(self):
        start = dt.datetime(2015, 1, 1)
        end = dt.datetime.now()
        # get names in stocksArray
        stockNames = []
        for stock in self.stocksArray:
            stockNames.append(stock["name"])
        # Get the stock prices
        if len(stockNames) > 0:
            stockPrices = yf.download(tickers=stockNames, start=start, end=end)["Close"]
            portfolioData = stockPrices
        else:
            return "no stocks in portfolio"
        portfolioData = portfolioData.dropna()
        # name column after stock name if only one stock in portfolio
        print(portfolioData)
        if len(self.stocksArray) == 1:
            portfolioData = portfolioData.rename(columns={stockNames[0]: "Portfolio"})
        return portfolioData

    # calculate portfolio value from portfolio data
    def calculatePortfolioValue(self):
        # Download portfolio data
        portfolioData = self.downloadPortfolioData()
        # Calculate the portfolio value
        portfolioValue = 0
        # name column after stock name if only one stock in portfolio
        for stock in self.stocksArray:
            portfolioValue += stock["shares"] * portfolioData[stock["name"]]
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
        if len(self.stocksArray) == 1:
            portfolioReturns["Portfolio"] = 1
            return portfolioReturns
        else:
            portfolioReturns["Portfolio"] = portfolioReturns.dot(portfolioWeights)
        portfolioReturns = portfolioReturns.dropna()
        return portfolioReturns

    # get portfolio correlation matrix
    def getPortfolioCorrelationMatrix(self):
        # Calculate the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
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
        updatedPortfolioValue = 0
        # get uptodate stock prices
        for stock in self.stocksArray:
            uptodatedStockPrices.append(portfolioData[stock["name"]][-1])
        # get updated portfolio value
        for stock in uptodatedStockPrices:
            updatedPortfolioValue += stock
        # calculate portfolio weights
        portfolioWeights = []
        for stock in uptodatedStockPrices:
            portfolioWeights.append(stock / updatedPortfolioValue)
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
        portfolioReturns = self.calculatePortfolioReturns()
        # Calculate the portfolio mean with porfolio weights
        portfolioMean = np.dot(portfolioReturns.mean(), self.calculatePortfolioWeights())
        # Calculate the porfolio standard deviation with portfolio weights
        portfolioStandardDeviation = np.sqrt(np.dot(self.calculatePortfolioWeights().T, np.dot(portfolioReturns.cov(), self.calculatePortfolioWeights())))
        # Calculate the confidence interval
        confidenceInterval = norm.interval(confidenceLevel, portfolioMean, portfolioStandardDeviation)
        return confidenceInterval

    # get option informaton from yahoo finance
    def getOptionInfoFromYahooFinance(self, name, type):
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

    # black scholes
    def blackScholes(self, r, S, K, T, sigma, type="call"):
        # calculate black scholes option price
        d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        if type == "call":
            price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif type == "put":
            price = K*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - S*norm.cdf(-d1, 0, 1)
        return price

    # get blackSckoles parameters from options using getOptionInfoFromYahooFinance
    def getOptionPricesFromBlackScholes(self):
        # get options info from yahoo finance for all options in the portfolio
        for option in self.optionsArray:
            # get option info from yahoo finance
            optionInfo, nextValidExpiryDate = self.getOptionInfoFromYahooFinance(option["name"], option["type"])
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
            price = self.blackScholes(r, S, K, T, sigma, option["type"])
            # add parameters to option
            option[ "S" ] = S
            option[ "K" ] = K
            option[ "T" ] = T
            option["sigma"] = sigma
            option["price"] = price
        return self.optionsArray

    # calculate delta of options
    # Delta measures the rate of change of the theoretical option value with respect to changes in the underlying asset
    def calculateDelta(self):
        if self.optionsArray[0]["price"] == None:
            optionsArray = self.getOptionPricesFromBlackScholes()
        else:
            optionsArray = self.optionsArray
        # calculate delta
        for option in optionsArray:
            # get stock price
            S = option["S"]
            # get strike price
            K = option["K"]
            # get days between now and nextValidExpiryDate
            T = option["T"]
            # get volatility
            sigma = option["sigma"]
            # get risk free rate
            r = 0.01
            # calculate delta
            d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
            if option["type"] == "call":
                delta = norm.cdf(d1, 0, 1)
            elif option["type"] == "put":
                delta = norm.cdf(d1, 0, 1) - 1
            # add delta to option
            option["delta"] = delta
        return optionsArray

    # calculate gamma of options
    # Gamma measures the rate of change of the delta with respect to changes in the underlying asset
    def calculateGamma(self):
        if self.optionsArray[0]["delta"] == None:
            optionsArray = self.calculateDelta()
        else:
            optionsArray = self.optionsArray
        # calculate gamma
        for option in optionsArray:
            # get stock price
            S = option["S"]
            # get strike price
            K = option["K"]
            # get days between now and nextValidExpiryDate
            T = option["T"]
            # get volatility
            sigma = option["sigma"]
            # get risk free rate
            r = 0.01
            # calculate gamma
            d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
            gamma = norm.pdf(d1, 0, 1) / (S * sigma * np.sqrt(T))
            # add gamma to option
            option["gamma"] = gamma
        return optionsArray
    
    # calculate vega of options
    # Vega measures the rate of change of the theoretical option value with respect to changes in the volatility of the underlying asset
    def calculateVega(self):
        if self.optionsArray[0]["gamma"] == None:
            optionsArray = self.calculateGamma()
        else:
            optionsArray = self.optionsArray
        # calculate vega
        for option in optionsArray:
            # get stock price
            S = option["S"]
            # get strike price
            K = option["K"]
            # get days between now and nextValidExpiryDate
            T = option["T"]
            # get volatility
            sigma = option["sigma"]
            # get risk free rate
            r = 0.01
            # calculate vega
            d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
            vega = S * norm.pdf(d1, 0, 1) * np.sqrt(T)
            # add vega to option
            option["vega"] = vega
        return optionsArray
    
    # calculate theta of options
    # Theta measures the rate of change of the theoretical option value with respect to changes in the time to maturity
    def calculateTheta(self):
        if self.optionsArray[0]["vega"] == None:
            optionsArray = self.calculateVega()
        else:
            optionsArray = self.optionsArray
        # calculate theta
        for option in optionsArray:
            # get stock price
            S = option["S"]
            # get strike price
            K = option["K"]
            # get days between now and nextValidExpiryDate
            T = option["T"]
            # get volatility
            sigma = option["sigma"]
            # get risk free rate
            r = 0.01
            # calculate theta
            d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
            d2 = d1 - sigma*np.sqrt(T)
            if option["type"] == "call":
                theta = -S*norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
            elif option["type"] == "put":
                theta = -S*norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2, 0, 1)
            # add theta to option
            option["theta"] = theta
        return optionsArray
    
    # calculate rho of options
    # Rho measures the rate of change of the theoretical option value with respect to changes in the risk-free interest rate
    def calculateRho(self):
        if self.optionsArray[0]["theta"] == None:
            optionsArray = self.calculateTheta()
        else:
            optionsArray = self.optionsArray
        # calculate rho
        for option in optionsArray:
            # get stock price
            S = option["S"]
            # get strike price
            K = option["K"]
            # get days between now and nextValidExpiryDate
            T = option["T"]
            # get volatility
            sigma = option["sigma"]
            # get risk free rate
            r = 0.01
            # calculate rho
            d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
            d2 = d1 - sigma*np.sqrt(T)
            if option["type"] == "call":
                rho = K*T*np.exp(-r*T)*norm.cdf(d2, 0, 1)
            elif option["type"] == "put":
                rho = -K*T*np.exp(-r*T)*norm.cdf(-d2, 0, 1)
            # add rho to option
            option["rho"] = rho
        return optionsArray

    # calculate all greeks of options
    def calculateAllGreeks(self):
        
        optionsArray = self.optionsArray
        # calculate delta
        self.calculateDelta()
        # calculate gamma
        self.calculateGamma()
        # calculate vega
        self.calculateVega()
        # calculate theta
        self.calculateTheta()
        # calculate rho
        self.calculateRho()

        return optionsArray

    
# Path: api\services\stockManager.py