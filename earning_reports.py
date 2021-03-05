from datetime import datetime, date
import yahoo_fin

read_dates = []
call_dates = []
ticker = []

file = open('guide/tickers.txt', 'r').readlines()
for line in file:
    line = line.replace('\n', '')
    ticker.append(line)


def CheckDate(tickers):
    for i in tickers:
        with open(f'earning_dates/{i}.txt', 'r', encoding='utf-8') as f:
            dates = f.readlines()

            for element in dates:
                read_dates.append(element.strip())

            today = datetime.now()

            for element in read_dates:
                date_obj = datetime.strptime(element, "%d-%m-%Y")
                call_dates.append(date_obj)

            for k in call_dates:
                if today.date() == k.date():
                    with open(f'earning_dates/today.txt', 'a') as j:
                        j.write(f'{i}: {k.strftime("%d-%m-%Y")}\n')
                    del call_dates[:]
                    break
                else:
                    print(f"{i}'s earning call not today.")
                    del call_dates[:]


CheckDate(ticker)
