from datetime import datetime
import yahoo_fin

read_dates = []
call_dates = []
ticker = []

file = open('guide/tickers.txt', 'r').readlines()
for line in file:
    line = line.replace('\n', '')
    ticker.append(line)


def CheckDate(tickers):
    with open('earning_dates/today.txt', 'w') as clear:
        clear.truncate(0)

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
                    return True

        del read_dates[:]
        del call_dates[:]


def EarningAnalysis(tickers):
    pass


CheckDate(ticker)
