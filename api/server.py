from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
CORS(app, resources = {r"/*": {"origins": "*"}})

@app.route("/stocks", methods=["GET"])
def stocks():
    return {
        "stocks": [
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
    }


# create stock JSON object with name and price
@app.route("/stock/<string:name>")
def stock(name):
    return {"name": name, "price": 100}


if __name__ == "__main__":
    app.run(debug=True)  # run our server
