#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 27 2020 22:57
SingleStockDownloader.py
@author: Linh Ngo
"""


import requests
import json
import pandas as pd
import datetime
import argparse
import datetime as dt


def convert_time(time_string):
    # convert date string in form of dd/mm/yyyy to timestamp
    time_string = int(dt.datetime.strptime(time_string, '%d/%m/%Y').timestamp())
    return time_string


def create_url(stock, start_, end_, freq):
    if freq == 'm':
        freq = 'mo'
    elif freq == 'w':
        freq = 'wk'
    elif freq == 'd':
        freq = 'd'
    else:
        print('Please enter valid input d/m/w')
    url_base = 'https://finance.yahoo.com/quote/%s/history?period1=%d&period2=%d&interval=1%s&filter=history&frequency=1%s'
    url = url_base % (stock, start_, end_, freq, freq)
    return url


def query_yahoo(url):
    # Get html response from yahoo
    req = requests.get(url)
    # Extract data from data source:
    start_ = req.text.find('[', req.text.find('"HistoricalPriceStore":'))
    end_ = req.text.find(']', start_) + 1
    data = req.text[start_:end_]
    # Convert data to a list of dictionaries:
    stock_data = json.loads(data)
    # Loop through the list to remove unique dictionaries. This method changes the list within the loop.
    for item in stock_data:
        if 'type' in item:
            stock_data.remove(item)
    return stock_data


def convert_to_df(stock_data):
    stock_df = pd.DataFrame(stock_data)
    # Convert timestamp to date dd/mm/yyyy
    tmstmplist = stock_df['date'].tolist()
    datelist = []
    for item in tmstmplist:
        tdate = str(dt.datetime.fromtimestamp(item).date())
        datelist.append(tdate)
    stock_df['date'] = datelist
    stock_df = stock_df[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
    return stock_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--stk", help="Input stock ticker symbol")
    parser.add_argument("--s", help="Input start date dd/mm/yyyy")
    parser.add_argument("--e", help="Input end date dd/mm/yyyy")
    parser.add_argument("--fq", help="Input frequency d/m/w")
    args = parser.parse_args()
    stock = args.stk
    start_ = args.s
    end_ = args.e
    freq = args.fq
    print('Stock ticker symbol: ', stock)
    print('Start date: ', start_)
    print('End date: ', end_)
    print('Frequency: ', freq)

    start_date = convert_time(start_)
    end_date = convert_time(end_)
    url = create_url(stock, start_date, end_date, freq)
    res = query_yahoo(url)
    stock_data = convert_to_df(res)
    stock_data.to_csv(stock + '.csv', index=False)
