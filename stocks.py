import yahoo_fin.stock_info as info
import datetime

ticker = []
test = 'ZM'

date = datetime.date.today()
print(date)

file = open('guide/tickers.txt', 'r').readlines()
for line in file:
    line = line.replace('\n', '')
    ticker.append(line)

print(info.get_data(test, start_date="1/2/2018"))
print(info.get_balance_sheet(test))
print(info.get_analysts_info(test))
