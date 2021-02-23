import yfinance as yf
import datetime

ticker = []

date = datetime.date.today()
print(date)

file = open('guide/tickers.txt', 'r').readlines()
for line in file:
    line = line.replace('\n', '')
    ticker.append(line)

netflix_df = yf.download(ticker[9], start='2021-02-10', end='2021-02-22', progress=False)
