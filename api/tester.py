from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import time as time
import glob as glob

from services.portfolioManager import PortfolioManager
from services.models import historicalVaR, historicalCVaR, var_parametric, cvar_parametric, mcSim, mcVaR, mcCVaR, calculateVarstdmean, useBrownianMotionVar


# # array of stocks
# stocksArray = [
#     {
#         "name": "AMZN",
#         "shares": 2,
#     },
#     {
#         "name": "MSFT",
#         "shares": 3,
#     },
# ]
# # array of options
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




def var(stocksArray, optionsArray, i):
    portfolio = PortfolioManager(stocksArray, optionsArray)
    stockPrices = portfolio.calculatePortfolioValue()
    confidenceLevel = 0.95
    timeInDays = 1
    # Calculate the value at risk for the portfolio
    # using historical simulation
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
        "HVaR": hvar,
        "HCVaR": hCVaR,
        "NormVaR": normVaR,
        "NormCVaR": normCVaR,
        "TVaR": tVaR,
        "TCVaR": tCVaR,
        "MCVaR": VaR,
        "MCCVaR": CVaR,
        "BMGVaR": varBrownian
    }

    # plot portFolioPerformances as a bar chart
    plt.bar(portfolioPerformances.keys(), portfolioPerformances.values())
    # title of the chart
    title = "Portfolio Performances for Scenario" + str(i)
    plt.title(title)
    plt.show()


    # compute the percentage difference between hvar, normVaR, tVaR, and MCVaR
    percentageDiff = { 
        "H-N": (hvar - normVaR) / hvar,
        "H-T": (hvar - tVaR) / hvar,
        "H-MC": (hvar - VaR) / hvar,
        "N-T": (normVaR - tVaR) / normVaR,
        "N-MC": (normVaR - VaR) / normVaR,
        "T-MC": (tVaR - VaR) / tVaR,
    }

    # save the percentage difference to a json file
    fileName = "percentageDiff" + str(i) + ".json"
    with open(fileName, 'w') as fp:
        json.dump(percentageDiff, fp)
    

    # plot percentageDiff as a point chart
    plt.plot(percentageDiff.keys(), percentageDiff.values(), 'ro')
    plt.show()

    return portfolioPerformances

# Method to merge all percentageDiff json files into one
def mergeJson():
    # create a list of all percentageDiff json files
    files = glob.glob("percentageDiff*.json")
    # create an empty list to store all data
    data = []
    # iterate through each file
    for file in files:
        # open the file
        with open(file) as f:
            # load the data from the file
            data.append(json.load(f))
    # write all data to a new file
    with open('merged.json', 'w') as f:
        json.dump(data, f)

# Tester Method
def tester():
    # get all stocksArrays from scenarios.json and run var() on each
    i = 0
    with open('scenarios.JSON') as f:
        data = json.load(f)
        for i in range(len(data)):
            # concantenate i to stocksArray
            index = "stocksArray" + str(i)
            stocksArray = data[index]
            var(stocksArray, optionsArray, i)
            i = i + 1
            # Empty cache
            # wait for 5 seconds before running the next scenario
            time.sleep(2)

# Method to go through merged.json and plot the combined data into a point chart
def plotMerged():
    # open merged.json
    with open('merged.json') as f:
        data = json.load(f)
        # create empty lists to store the data
        hvarNorm = []
        hvarT = []
        hvarMC = []
        normVarT = []
        normVarMC = []
        tVarMC = []

        # iterate through each scenario
        for scenario in data:
            # iterate through each percentage difference
            for key, value in scenario.items():
                # add the value to the correct list
                if key == "H-N":
                    hvarNorm.append(value)
                elif key == "H-T":
                    hvarT.append(value)
                elif key == "H-MC":
                    hvarMC.append(value)
                elif key == "N-T":
                    normVarT.append(value)
                elif key == "N-MC":
                    normVarMC.append(value)
                elif key == "T-MC":
                    tVarMC.append(value)
        
        # plot the data as a point chart with labes and title
        plt.plot(hvarNorm, 'ro', label="H-N")
        plt.plot(hvarT, 'bo', label="H-T")
        plt.plot(hvarMC, 'go', label="H-MC")
        plt.plot(normVarT, 'yo', label="N-T")
        plt.plot(normVarMC, 'co', label="N-MC")
        plt.plot(tVarMC, 'mo', label="T-MC")
        plt.legend()
        plt.title("Percentage Difference between VaR Methods")
        plt.show()




if __name__ == "__main__":
    plotMerged()

