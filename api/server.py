from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
CORS(app, resources = {r"/*": {"origins": "*"}})

# array of stocks
stocksArray = [
            {
                "name": "AAPL",
                "shares": 100,
            },
            {
                "name": "GOOG",
                "shares": 68,
            },
            {
                "name": "MSFT",
                "shares": 145,
            },
        ]
# array of options
optionsArray = [
            {
                "name": "option1",
                "shares": 123,
            },
            {
                "name": "option2",
                "shares": 45,
            },
            {
                "name": "option3",
                "shares": 6777,
            },
        ]

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
    name = request.json["name"]
    shares = request.json["shares"]
    stocksArray.append({"name": name, "shares": shares})
    return {"message": "Stock added successfully"}

#add a new option
@app.route("/options", methods=["POST"])
def add_option():
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


if __name__ == "__main__":
    app.run(debug=True)  # run our server
