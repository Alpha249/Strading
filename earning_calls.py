import pandas as pd
from datetime import datetime, date
from yahoo_earnings_calendar import YahooEarningsCalendar
import dateutil.parser
import time

start = time.perf_counter()

ticker = []
dates = []

file = open('guide/tickers.txt', 'r').readlines()
for line in file:
    line = line.replace('\n', '')
    ticker.append(line)


def Calendar(Ticker):
    for i in Ticker:
        # Setting the dates
        start_date = datetime.now().date()
        end_date = date(datetime.now().year, 12, 31)

        # Downloading the earnings calendar
        yec = YahooEarningsCalendar()
        earnings_list = yec.get_earnings_of(i)
        earnings_df = pd.DataFrame(earnings_list)

        # Extracting the date from the string and filtering for the period of interest
        earnings_df['report_date'] = earnings_df['startdatetime'].apply(lambda x: dateutil.parser.isoparse(x).date())
        earnings_df = earnings_df.loc[earnings_df['report_date'].between(start_date, end_date)] \
            .sort_values('report_date')

        # Creating initial date list
        earning_dates = earnings_df['report_date'].to_list()

        # Converting datetime objects to strings
        for j in earning_dates:
            d = date(year=j.year, month=j.month, day=j.day)
            dates.append(d.strftime("%d-%m-%Y"))

        # Export Dates
        with open(f'earning_dates/{i}.txt', 'w') as f:
            for k in dates:
                f.write(f"{k}\n")

        print(f"{i}'s earning report dates exported.")

        # Reset lists so no overlap occurs
        del dates[:]


Calendar(ticker)

end = time.perf_counter()

print(f"Time taken: {end - start}")
