import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import yfinance as yf

from services.portfolioManager import portfolioManager

class backtester:
# Class to backtest methods in models.py and portfolioManager.py using historical data from yahoo finance
    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate

    
    
    


