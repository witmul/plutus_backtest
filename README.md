# Project_name
## Project description

This package was created for the purpose of local tests of financial strategies. The package contains various indicators and tools 
allowing users obtaining exact results of their strategies over a certain period of time. The users are also able to pick 
endless amount of trading instruments and set criteria such as long or short positioning. Beside that optional stop loss and take profit
signals are available not only as general limit level for entire portfolio but can be also applied for each instrument individually.
Another optional tool available is weights factor distribution which is oriented to assign weights according to the provided values. 
In addition, the package allows to create several backtests and combine them all together into one to see the full picture of the investment 
strategy.

## Installation: 
* Dependency: pandas, numpy, plotly, yfinance
* Install from pypi:
```
pip install project_name 
```
* Verified in Python:
```python
from backt.backt import backtest
```
## Examples: 
A short and fast way to run a single backtest would be:

```python
from backt.backt import backtest
bt = backtest(asset = ["AAPL", "BTC-USD","GC=F"], o_day = ["2021-08-01", "2021-07-15", "2021-08-20"],
              c_day = ["2021-09-01", "2021-09-01","2021-09-15"])
bt.execution()
```

As a result you will see a statistical table as well as graphical representation of the portfolio which shows accumulated return.

![1](https://user-images.githubusercontent.com/83161286/146902663-33525a28-d62e-45b1-9561-cbf0ce1b559a.png)

In order to access dataframe with daily changes, use:
```
bt.final_portfolio.head()
```
The result will appear as following:

![2](https://user-images.githubusercontent.com/83161286/146903435-f88144f7-adbb-447d-92ce-a9f5f35723b7.png)


Additional "plotting" fuction  will enable users to observe additional graphs such as drawdown and monthly income plots:
```
bt.plotting()
```

![3 1](https://user-images.githubusercontent.com/83161286/146904414-5fd9d562-ff74-4401-9cdf-9d281a64664d.png)
![3 2](https://user-images.githubusercontent.com/83161286/146904423-7ad8b9f9-e2e2-47b0-b9ee-786b92ab6a35.png)



More complex approach would be assigning weights factor/stop loss/ take profit indicators:

```
bt = backtest(asset = ["AAPL", "BTC-USD","GC=F"], o_day = ["2021-08-01", "2021-07-15", "2021-08-20"],
              c_day = ["2021-09-01", "2021-09-01","2021-09-15"], weights_factor = [10, -5, 35], 
              stop_loss = [0.8, 0.9, 0.95], take_profit = [1.1, 1.2, 1.05])
bt.execution()
```

In this case all parameters are used. The weights will not distributed equally. "AAPL"  will have 20% of the total portoflio BTC-USD - 10% and 
"GC=F" will have 70%. The negative sign in the weights factor will mean short selling, therefore first "AAPL" and "GC=F" instruments are in long position and 
"BTC-USD" is in the short. Stop loss and take profit shall be interpreted as "AAPL" has 20% of stop loss and 10% of take profit, "BTC-USD" has 10% of stop loss and 20% of take profit, "GC=F" 5% of stop loss and 5% of take profit. As result accumulative graph will look as:

![4](https://user-images.githubusercontent.com/83161286/146915546-113db7ce-99d8-4c92-90d5-f0f556499b57.png)

In case of users have a need to test one instrument but sevral times with different timelines, the library will interpretate it as
```
bt = backtest(asset = ["AMZN", "AMZN","AMZN"], o_day = ["2021-08-01", "2021-09-01", "2021-10-01"],
              c_day = ["2021-08-15", "2021-09-15","2021-10-15"])
bt.execution()
bt.final_portfolio.head(15)
```
![5](https://user-images.githubusercontent.com/83161286/146916428-a9bd2839-26cf-4044-b792-bedcebf1365c.png)

Each time when one asset is repeating the library will assign additional number to it to track required periods. 
It's worth to mention that due to data limitation the code will use only close price for the analysis of the securities. Only the first trading day has relationship open/close, since it's assumed that the tradingstarts with open price and finishes with close one.


Ultimately in addition if the users would like to perform several backtest and combine them into one to see the full picture then there is few functions related to that, namely
```
bt1 = backtest(asset = ["AAPL", "BTC-USD","GC=F"], o_day = ["2021-08-01", "2021-07-15", "2021-08-20"],
              c_day = ["2021-09-01", "2021-09-01","2021-09-15"])
bt2 = backtest(asset = ["AMZN", "EURUSD=X"], o_day = ["2021-06-01", "2021-06-15"],
              c_day = ["2021-06-30", "2021-07-05"])

p1 = bt1.execution()
p2 = bt2.execution()
q1 = bt1.final_portfolio
q2 = bt2.final_portfolio

dic ={}
dic[0] = q1
dic[1]= q2

combined_frame =backtest.puzzle_assembly(dic)
```
First of all each backtest shall be executed in order to obtain final portfolio of each one. Then they shall be assigned to an empty dictionary. Thereafter 
function "puzzle_assembly" takes the data from diffirent backtest and unite it into one dataframe.

![6](https://user-images.githubusercontent.com/83161286/146918856-ede46b8a-830c-42ad-9e63-b80063d80460.png)

In order to visualize data functions "puzzle_execution" or "puzzle_plotting" shall be called. Which work exactly in the same way as it was explained previously.
```
backtest.puzzle_execution(combined_frame)
```
![7](https://user-images.githubusercontent.com/83161286/146919316-c2176568-ccc1-459d-be08-d8155073baea.png)




