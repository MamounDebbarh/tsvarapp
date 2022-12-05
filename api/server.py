from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import yfinance as yf

from services.portfolioManager import PortfolioManager
from services.models import Models

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
CORS(app, resources = {r"/*": {"origins": "*"}})

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

@app.route("/stocks", methods=["GET"])
def stocks():
    return {
        "stocks": stocksArray
    }

@app.route("/options", methods=["GET"])
def options():
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
    optionsArray.append({"name": name, "shares": shares})
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
    # Calculate the value at risk for the portfolio
    # using historical simulation
    portfolio = PortfolioManager(stocksArray, optionsArray)
    model = Models(portfolio)
    var = model.calculatePortfolioValueAtRiskWithHistoricalSimulationMethod(confidenceLevel)
    print("confidenceInterval: ", portfolio.calculateConfidenceInterval(confidenceLevel))
    print("var: ", var)
    return { "var": var}

# portfolio daily returns
@app.route("/portfolioReturns", methods=["GET"])
def portfolioReturns():
    portfolio = PortfolioManager(stocksArray, optionsArray)
    portfolioReturns = portfolio.calculatePortfolioReturns()
    portfolioCovarienceMatrix = portfolio.calculateVarianceCovarianceMatrix() # TODO: remove this
    portfolioExpectedReturns = portfolio.calculateExpectedPortfolioReturns() # TODO: remove this
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
    model = Models(portfolio)
    var = model.calculatePortfolioValueAtRiskWithMonteCarloSimulationMethod(confidenceLevel, 30, 100000)
    print("var: ", var)
    return { "var": var}





if __name__ == "__main__":
    app.run(debug=True)  # run our server

