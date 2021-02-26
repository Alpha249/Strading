# To-D0:
# 1. Sort company link list into separate lists - ✓
# 2. Export link list to individual csv files - ✓
# 3. Figure out way to remove column name in .csv - ✓
# 4. Filter links based on date - ✓

import time
from datetime import datetime, date

import pandas as pd
import requests
from bs4 import BeautifulSoup

start = time.perf_counter()

companies = []
dates = []
f_date = []
links = []
val = []

with open('guide/companies.txt', 'r') as f:
    f = f.readlines()
    for lines in f:
        lines = lines.replace('\n', '')
        companies.append(lines)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/88.0.4324.182 Safari/537.36"
}


def News(company):
    for i in company:
        # Initialize BeautifulSoup and requests
        URL = f"https://news.google.com/rss/search?q={i}&hl=en-US&gl=US&ceid=US:en"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'xml')

        # Link filtering
        link_ = soup.find_all("link")
        for v in link_:
            links.append(v.get_text())
        link = [x for x in links if "https://news.google.com/search?q=" not in x]

        # Date filtering
        Date_ = soup.find_all("pubDate")
        for n in Date_:
            dates.append(n.get_text())

        for t in dates:
            obj = datetime.strptime(t, '%a, %d %b %Y %H:%M:%S %Z')
            d = date(year=obj.year, month=obj.month, day=obj.day)
            f_date.append(d.strftime('%d-%b-%Y'))

        # Create dictionary
        dictionary = dict(zip(link, f_date))

        for key, value in dict(dictionary).items():
            vald = datetime.strptime(value, '%d-%b-%Y')
            today = date.today()

            if vald.month == today.month:
                if vald.day >= int(today.day) - 2:
                    pass
                else:
                    del dictionary[f'{key}']
            else:
                del dictionary[f'{key}']

            pass

        final_links = list(dictionary.keys())

        # Export data
        df = pd.DataFrame(final_links)
        df.to_csv(f'links/{i}.csv')

        # Reset lists so no overlap occurs
        del link[:]
        del links[:]
        del final_links[:]

        print(f"{i}'s news scraped successfully")

        # Pause to avoid IP blocking
        time.sleep(3)


def Filter(company):
    for k in company:
        file = f'links/{k}.csv'

        with open(file, 'r', encoding='utf-8') as u:
            u.seek(0)
            line = u.readlines()
            del line[:1]

        with open(file, 'w+') as j:
            for line_ in line:
                j.write(line_)


News(companies)
Filter(companies)

end = time.perf_counter()

print(f"Time take: {end - start}")
