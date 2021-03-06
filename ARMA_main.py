import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import arch
import yfinance as yf
import statsmodels.api as sm
import warnings
import time
warnings.simplefilter('ignore', category=UserWarning)
warnings.simplefilter('ignore', category=FutureWarning)
warnings.simplefilter('ignore', category=RuntimeWarning)

class Share:
    def __init__(self, ticker):
        self.companyTicker = ticker
        self.ticker = yf.Ticker(ticker)
        self.share_data = self.ticker.history(period="3y")
        self.close_price = 100*np.log(self.share_data["Close"]).diff()
        self.close_price = self.close_price.dropna()
        self.close_price_len = len(self.close_price)
        self.ARMA_modelling()
        
    def ARMA_modelling(self): 
        value = 0
        correct = 0
        incorrect = 0
        #error = 0
        optimalOrder = self.ComputeOptimalArmaOrder()
        self.predictionArr, self.ActualArr = [],[]
        beginValidationTime = time.time()
        for i in range(int((self.close_price_len-(self.close_price_len*0.3))), self.close_price_len-1):
            exog = self.close_price[0:i]
            actual = self.close_price[i+1]
            model = sm.tsa.arima.ARIMA(exog, order=optimalOrder).fit()
            forecast = model.forecast(steps=1)
            #error += (actual-forecast)
            self.predictionArr.append(forecast.values)
            self.ActualArr.append(actual)
            if forecast.values[0] > 0:
                value = value + (actual*1)
                if actual > 0:
                    correct += 1
                else:
                    incorrect += 1
            else: 
                value = value +(actual*-1)
                if actual < 0:
                    correct += 1
                else:
                    incorrect += 1
        finishValidationTime = time.time()
        print(f'share Name: {self.companyTicker}, value: {value}, correct: {correct}, incorrect: {incorrect}, order: {optimalOrder}')
        print(f'Validation process took: {round(finishValidationTime-beginValidationTime)} seconds')
        self.finalValue = value
        self.totalCorrect = correct
        self.totalIncorrect = incorrect
    
    def ComputeOptimalArmaOrder(self):
        startTime = time.time()
        optimalOrder = sm.tsa.stattools.arma_order_select_ic(self.close_price, max_ar=4, max_ma=2, ic="bic").bic_min_order
        tempOrd = list(optimalOrder)
        tempOrd.insert(1,0)
        optimalOrder = tuple(tempOrd)
        finishTime = time.time()
        print(f'Calculating the optimal order took: {round(finishTime-startTime)} seconds')
        return optimalOrder
    
    def printGraph(self):
        plt.plot(self.predictionArr)
        plt.plot(self.ActualArr)
        plt.show()
    

Tesla = Share("TSLA") 
Apple = Share("AAPL")        
#MajorCompanies = ["MSFT", "AMZN", "FB", "GOOGL", "JNJ", "NVDA", "DIS", "PYPL", "INTC", "AAPL"] 
#for company in MajorCompanies:
    #temp = Share(company)      
    #temp.printGraph()                                                       