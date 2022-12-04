# value at risk calculator models

class Models:
    def __init__(self, portfolioManager, confidenceLevel):
        self.portfolioManager = portfolioManager
        self.confidenceLevel = confidenceLevel

    def getPortfolioManager(self):
        return self.portfolioManager
    
    def getConfidenceLevel(self):
        return self.confidenceLevel
    
    
    # calculate portfolio value at risk with historical simulation method
    def calculatePortfolioValueAtRiskWithHistoricalSimulationMethod(self, confidenceLevel):
        # Calculate the portfolio returns
        portfolioReturns = self.calculatePortfolioReturns()
        # Calculate the portfolio value at risk with historical simulation method
        portfolioValueAtRiskWithHistoricalSimulationMethod = portfolioReturns.quantile(confidenceLevel)
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
        portfolioValueAtRiskWithMonteCarloSimulationMethod = []
        for stock in self.stocksArray:
            stockPrices = self.geometricBrownianMotion(stock["name"], timePeriod, numberOfSimulations)
            portfolioValueAtRiskWithMonteCarloSimulationMethod.append(stockPrices[-1] * stock["shares"])
        portfolioValueAtRiskWithMonteCarloSimulationMethod = pd.DataFrame(portfolioValueAtRiskWithMonteCarloSimulationMethod).sum()
        portfolioValueAtRiskWithMonteCarloSimulationMethod = portfolioValueAtRiskWithMonteCarloSimulationMethod.quantile(confidenceLevel)
        return portfolioValueAtRiskWithMonteCarloSimulationMethod
    
    # calculate conditional value at risk with monte carlo simulation method
    
        
    

    # calculate portfolio value at risk with garch method
    def calculatePortfolioValueAtRiskWithGarchMethod(self, confidenceLevel):
        return 0

    # calculate portfolio value at risk with cornish fisher method
    def calculatePortfolioValueAtRiskWithCornishFisherMethod(self, confidenceLevel):
        return 0

