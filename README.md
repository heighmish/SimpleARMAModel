# ARMA Model with Rolling Prediction Validation
The program uses the yfinance module to download financial data, pandas and numpy to manage dataframes, and the statsmodels library for ARMA modelling.

## Data Preprocessing

Log returns are calculated from adjusted close price. Logs are useful for price data as they scale large numbers down to be far more managable. Additionally scaling data very often makes machine learning models calculate faster and with greater accuracy. Log returns, are achived by differencing the data. Differencing the data is important in achieving stationarity which is crucial for time series analysis.

## ARMA Construction
ARMA models, autoregressive moving average models, at least the model described here, use no outside information to predict the price. The model uses only the past price information to try and predict future prices.

ARMA(1,1) is used as the default for this model currently, as computing the optimal orders according to AIC or BIC is very computationally expensive relative to performance gains over many companies. 

Statsmodels ARIMA is the library used the I stands for integrated. As the program uses log returned data we set the integration order to 0, (1,0,1) in the program.

## Cross-Validation

The cross-validation is strategy used here is very primitive and likely not very efficient. For 30% of the data set, for 3 years this is approximately 1 year, the program calculates a new arma model, calculates a 1 day ahead forecast and compares it to the actual value.

As this is financial data, for a positive predicted value we would 'buy' the share and for negative predicted value we would 'sell'. If the predicted value is the same sign (+ or -) as the actual value this is considered a correct choice as this would have made the investor money. If the signs are in the opposite directions this is incorrect and regardless of the magnitude of the actual change, the investment lost money. 

The program keeps track of 'value' which is a an indicator of the predictive success of the model. Value represents the the real change an investment would have made if the models predictions were followed. A positive value indicates the model made money and negative indicates money was lost.

The stock market can change quite dramatically from day to day prices can drop or rise substantially due to many other factors that this model does not account for. This means there can often be a positive 'value' yet the 'correct' predictions rate is less than 50%.

## How to Use
Add or remove any company ticker you desire to the companies list at the bottom, or just initialise a new class instance. 

The for loop range under ARMA_modelling, the range length can be changed for more validation instances. Currently set at 0.3 or 30%. Under the class constructor the share price history can be made shorter or longer. 

The ARMA order can also be altered, but as the program estimates potentially hundreds of models per company it is best to keep the order low, (0,0) is always interesting.

## Conclusions
The ARMA model can be very powerful but its utility especially arises when combined with other financial models that complement the ARMA's weaknesses, namely models that use outside information such as share volume or price to earnings ratio.

Neural networks are becoming more and more commonly used for share price prediction as are data scraping and sentiment analysis.

Combining models into an ensemble will often produce the best outcome.
