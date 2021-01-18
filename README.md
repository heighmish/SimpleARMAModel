# ARMA Model with Rolling Prediction Validation
The program uses the yfinance module to download financial data, pandas and numpy to manage dataframes, and the statsmodels library for ARMA modelling. ARCH is imported for future plans to include volatility modelling.

## Data Preprocessing

Log returns are calculated from adjusted close price. Logs are useful for price data as they scale large numbers down to be far more managable. Additionally scaling data very often makes machine learning models calculate faster and with greater accuracy. Log returns, are achived by differencing the data. Differencing the data is important in achieving stationarity which is crucial for time series analysis.

## ARMA Construction
ARMA models, autoregressive moving average models, at least the model described here, use no outside information to predict the price. The model uses only the past price information to try and predict future prices.

Use statsmodels ARMA order select and the Bayesian Information criteria to calculate the optimal ARMA order between 4 auto regressive processes and 2 moving average processes. Calculating this value is reasonably computationally expensive ~3 seconds for 3 years of data points. 

Statsmodels ARIMA is the model used for this program. The I stands for integrated. As the program uses log returned data we set the integration order to 0. Where the ARMA order is specified as (p,d,q) where p is AR components, d is integrated components and q is moving average processes, all models are of the form (p,0,q).

## Cross-Validation

The cross-validation is strategy used here is very primitive and likely not very efficient. For 30% of the data set, for 3 years this is approximately 1 year, the program calculates a new arma model, calculates a 1 day ahead forecast and compares it to the actual value.

As this is financial data, for a positive predicted value we would 'buy' the share and for negative predicted value we would 'sell'. If the predicted value is the same sign (+ or -) as the actual value this is considered a correct choice as this would have made the investor money. If the signs are in the opposite directions this is incorrect and regardless of the magnitude of the actual change, the investment lost money. 

The program keeps track of 'value' which is a an indicator of the predictive success of the model. Value represents the the real change an investment would have made if the models predictions were followed. A positive value indicates the model made money and negative indicates money was lost.

The stock market can change quite dramatically from day to day prices can drop or rise substantially due to many other factors that this model does not account for. This means there can often be a positive 'value' yet the 'correct' predictions rate is less than 50%.

## How to Use
Add or remove any company ticker you desire to the companies list at the bottom, or just initialise a new class instance. 

The for loop range under ARMA_modelling, the range length can be changed for more validation instances. Currently set at 0.3 or 30%. Under the class constructor the share price history can be made shorter or longer. 

A strong argument can be made that the ARMA order should be fixed to (0,0,0) or (1,0,1) for fast computing speed if 10s or hundreds of companies want to be analysed as both calculating the optimal order takes additional time, and every additional AR and MA order increases runtime by a significant margin.

## Conclusions
The ARMA model can be very powerful but its utility especially arises when combined with other financial models that complement the ARMA's weaknesses, namely models that use outside information such as share volume or price to earnings ratio.

Neural networks are becoming more and more commonly used for share price prediction as are data scraping and sentiment analysis.

Combining models into an ensemble will often produce the best outcome.
