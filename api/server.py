from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

from services.portfolioManager import PortfolioManager
from services.models import historicalVaR, historicalCVaR, var_parametric, cvar_parametric, mcSim, mcVaR, mcCVaR, calculateVarstdmean, useBrownianMotionVar

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
CORS(app, resources = {r"/*": {"origins": "*"}})

# array of stocks
stocksArray = [
    {
        "name": "AMZN",
        "shares": 2,
    },
    {
        "name": "MSFT",
        "shares": 3,
    },
]
# array of options
optionsArray = [
    {
        "name": "AAPL",
        "shares": 1,
        "type": "call",
        "r": 0.1,
    },
    {
        "name": "GOOG",
        "shares": 2,
        "type": "put",
        "r": 0.1,
    },
]

@app.route("/stocks", methods=["GET"])
def stocks():
    portfolio = PortfolioManager(stocksArray, optionsArray)
    stockPrices = portfolio.calculatePortfolioValue()
    returnsWithWeights = portfolio.generatePorfolioReturnsWithWeights()
    return {
        "stocks": stocksArray,
    }

@app.route("/portfolio-information", methods=["GET"])
def portfolio_information():
    portfolio = PortfolioManager(stocksArray, optionsArray)
    returnsWithWeights = portfolio.generatePorfolioReturnsWithWeights()
    correlationMatrix = portfolio.getPortfolioCorrelationMatrix()
    choleskyDecomposition = portfolio.getCholeskyDecomposition()
    eigenDecomposition = portfolio.getEigenDecomposition()

    # convert choleskyDecomposition and eigenDecomposition to json
    # so that it can be sent to the frontend
    choleskyDecomposition = json.dumps({'nums': choleskyDecomposition.tolist()})
    eigenDecomposition = np.array(eigenDecomposition)
    eigenDecomposition = json.dumps({'nums': eigenDecomposition.tolist()})

    returnsWithWeights.reset_index(inplace=True)
    returnsWithWeights['Date'] = returnsWithWeights['Date'].dt.strftime('%Y-%m-%d')

    return {
        "returnsWithWeights": returnsWithWeights.to_json(),
        "correlationMatrix": correlationMatrix.to_json(),
        "choleskyDecomposition": choleskyDecomposition,
        "eigenDecomposition": eigenDecomposition,
    }


@app.route("/options", methods=["GET"])
def options():
    portfolio = PortfolioManager(stocksArray, optionsArray)
    portfolioOptionPrices = portfolio.getOptionPricesFromBlackScholes()
    optionsGreeks = portfolio.calculateAllGreeks()
    return {
        "options": optionsArray
    }

#add a new stock
@app.route("/stocks", methods=["POST"])
def add_stock():

    # Check if the stock symbol is recognisable by YFinance
    # If not, return an error message
    ticker = yf.Ticker(request.json["name"])
    if not ticker.info:
        return {"message": "Stock symbol not found"}

    name = request.json["name"]
    shares = request.json["shares"]
    
    stocksArray.append({"name": name, "shares": shares})
    return {"message": "Stock added successfully"}

#add a new option
@app.route("/options", methods=["POST"])
def add_option():
    # Check if the option symbol is recognisable by YFinance
    # If not, return an error message
    ticker = yf.Ticker(request.json["name"])
    if not ticker.info:
        return {"message": "Stock symbol not found"}
    
    name = request.json["name"]
    shares = request.json["shares"]
    r = request.json["r"]
    type = request.json["type"]
    optionsArray.append({"name": name, "shares": shares, "r": r, "type": type})
    return {"message": "Option added successfully"}

# delete a stock from the array
@app.route("/stocks/<string:name>", methods=["DELETE"])
def delete_stock(name):
    for stock in stocksArray:
        if stock["name"] == name:
            stocksArray.remove(stock)
            return {"message": "Stock deleted successfully"}
    return {"message": "Stock not found"}

# delete an option from the array
@app.route("/options/<string:name>", methods=[ "GET", "POST", "DELETE"])
def delete_option(name):
    for option in optionsArray:
        if option["name"] == name:
            optionsArray.remove(option)
            return {"message": "Option deleted successfully"}
    return {"message": "Option not found"}

# Value at risk calculator using historical simulation
@app.route("/var", methods=["POST"])
def var():
    confidenceLevel = request.json["confidenceLevel"]
    timeInDays = request.json["timeInDays"]
    # Calculate the value at risk for the portfolio
    # using historical simulation
    portfolio = PortfolioManager(stocksArray, optionsArray)
    portfolioReturnsWithWeights = portfolio.generatePorfolioReturnsWithWeights()

    # hvarMath = calculateVarstdmean(confidenceLevel, portfolio) * np.sqrt(timeInDays)
    hvar = historicalVaR(portfolioReturnsWithWeights)
    hvar = hvar * np.sqrt(timeInDays)
    hCVaR  = historicalCVaR(portfolioReturnsWithWeights)
    hCVaR = hCVaR * np.sqrt(timeInDays)
    pRet = portfolioReturnsWithWeights * timeInDays
    pRet = pRet.to_json()
    pStd = portfolio.calculatePortfolioStandardDeviation() * np.sqrt(timeInDays)

    normVaR = var_parametric(portfolioReturnsWithWeights, pStd) * np.sqrt(timeInDays)
    normCVaR = cvar_parametric(portfolioReturnsWithWeights, pStd) * np.sqrt(timeInDays)
    tVaR = var_parametric(portfolioReturnsWithWeights, pStd, distribution='t-distribution') * np.sqrt(timeInDays)
    tCVaR = cvar_parametric(portfolioReturnsWithWeights, pStd, distribution='t-distribution') * np.sqrt(timeInDays)

    portfolioSim = mcSim(portfolio=portfolio)
    print(portfolioSim)
    portResults = pd.Series(portfolioSim[-1,:])
    VaR = mcVaR(portResults, alpha=confidenceLevel) * np.sqrt(timeInDays)
    CVaR = mcCVaR(portResults, alpha=confidenceLevel) * np.sqrt(timeInDays)

    varBrownian = useBrownianMotionVar(portfolio, confidenceLevel, timeInDays, 400)

    # select Porfolio element in series
    hvar = 0 - hvar["Portfolio"]
    hCVaR = 0 - hCVaR["Portfolio"]

    # select last row of Portfolio column
    normVaR = normVaR.iloc[-1]["Portfolio"]
    normCVaR = normCVaR.iloc[-1]["Portfolio"]
    tVaR = tVaR.iloc[-1]["Portfolio"]
    tCVaR = tCVaR.iloc[-1]["Portfolio"]
    
    VaR = (1-VaR) / 10
    CVaR = (1-CVaR) / 10

    # sum of stock prices * shares
    total = 0
    for stock in stocksArray:
        total = total + stock["shares"] * stock["price"]
    
    diff = varBrownian - total
    varBrownian = diff / total



    portfolioPerformances = {
        "historicalVaR": hvar,
        "historicalCVaR": hCVaR,
        "normalDistributionVaR": normVaR,
        "normalDistributionCVaR": normCVaR,
        "tDistributionVaR": tVaR,
        "tDistributionCVaR": tCVaR,
        "monteCarloVaR": VaR,
        "monteCarloCVaR": CVaR,
        "brownianMotionMonteCarloVaR": varBrownian
    }

    # plot portFolioPerformances as a bar chart
    plt.bar(portfolioPerformances.keys(), portfolioPerformances.values())

    # compute the percentage difference between hvar, normVaR, tVaR, and VaR
    percentageDiff = { 
        "historical-normal": (hvar - normVaR) / hvar,
        "historical-t": (hvar - tVaR) / hvar,
        "historical-monteCarlo": (hvar - VaR) / hvar,
        "normal-t": (normVaR - tVaR) / normVaR,
        "normal-monteCarlo": (normVaR - VaR) / normVaR,
        "t-monteCarlo": (tVaR - VaR) / tVaR,
        "monteCarlo-historical": (VaR - hvar) / VaR,
        "monteCarlo-normal": (VaR - normVaR) / VaR,
    }
    # plot percentageDiff as a point chart
    plt.plot(percentageDiff.keys(), percentageDiff.values(), 'ro')

    return portfolioPerformances

# portfolio daily returns
@app.route("/portfolioReturns", methods=["GET"])
def portfolioReturns():
    portfolio = PortfolioManager(stocksArray, optionsArray)
    portfolioReturns = portfolio.calculatePortfolioReturns()
    # print("portfolioReturns: ", portfolioReturns)
    return { "portfolioReturns": portfolioReturns.to_json(orient="records") }

# get portfolio beta
@app.route("/portfolioBeta", methods=["GET"])
def portfolioBeta():
    portfolio = PortfolioManager(stocksArray, optionsArray)
    portfolioBeta = portfolio.calculatePortfolioBeta()
    return { "portfolioBeta": portfolioBeta }

# value at risk calculator using monte carlo simulation
@app.route("/monteCarloVar", methods=["POST"])
def monteCarloVar():
    confidenceLevel = request.json["confidenceLevel"]  
    portfolio = PortfolioManager(stocksArray, optionsArray)
    # model = Models()
    # var = model.calculatePortfolioValueAtRiskWithMonteCarloSimulationMethod(confidenceLevel, 30, 100000)
    print("var: ", var)
    return { "var": var}

# get portfolio option prices
@app.route("/portfolioOptionPrices", methods=["GET"])
def portfolioOptionPrices():
    portfolio = PortfolioManager(stocksArray, optionsArray)
    portfolioOptionPrices = portfolio.getOptionPricesFromBlackScholes()
    optionsGreeks = portfolio.calculateAllGreeks()
    return { "portfolioOptionPrices": portfolioOptionPrices }



if __name__ == "__main__":
    app.run(debug=True)  # run our server

