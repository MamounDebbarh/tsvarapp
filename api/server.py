from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import yfinance as yf

from services.portfolioManager import portfolioManager
from services.varCalculator import varCalculator

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
    portfolio = portfolioManager(stocksArray, optionsArray)
    var = portfolio.calculatePortfolioValueAtRiskWithConfidenceLevel(confidenceLevel)
    return { "var": var }

# portfolio daily returns
@app.route("/portfolioReturns", methods=["GET"])
def portfolioReturns():
    portfolio = portfolioManager(stocksArray, optionsArray)
    portfolioReturns = portfolio.calculatePortfolioReturns()
    return { "portfolioReturns": portfolioReturns.to_json() }

# get portfolio beta
@app.route("/portfolioBeta", methods=["GET"])
def portfolioBeta():
    portfolio = portfolioManager(stocksArray, optionsArray)
    portfolioBeta = portfolio.calculatePortfolioBeta()
    return { "portfolioBeta": portfolioBeta }

if __name__ == "__main__":
    app.run(debug=True)  # run our server

