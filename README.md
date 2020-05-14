# Downloading Stock Price Data (Single Stock)
## Purpose
This repo is used to download historical stock price data from Yahoo Finance and export to a csv file.

## Usage
First of all, you can explore all arguments that you are able to input by running ```python SingleStockDownloader.py -h```

For example, if you want to download Apple historical stock price (daily prices) from 01/01/2019 to 31/12/2019, you can run:

```python SingleStockDownloader.py --stk AAPL --s 01/01/2019 --e 31/12/2020 --fq d```

Then you can find the result in a file named as 'AAPL.csv'

Please remember that:
  * Stock argument ('--stk') only accepts stock ticker symbol. It can be eith lowercase letters or capital letters.
  * Date arguments ('--s' and '--e') only accept dates in form of 'dd/mm/yyyy'
  * Frequency argument ('--fq') only accepts one of three values: 'd' (daily) or 'w' (weekly) or 'm' (monthly)
