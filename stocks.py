import yfinance as yf
import datetime

ticker = []

date = datetime.date.today()
print(date)

file = open('guide/tickers.txt', 'r').readlines()
for line in file:
    line = line.replace('\n', '')
    ticker.append(line)
