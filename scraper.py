# To-D0:
# 1. Sort company link list into separate lists - ✓
# 2. Export link list to individual csv files - ✓
# 3. Figure out way to remove column name in .csv - ✓

import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

start = time.perf_counter()

companies = []
links = []

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
        URL = f"https://news.google.com/rss/search?q={i}&hl=en-US&gl=US&ceid=US:en"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'xml')
        link_ = soup.find_all("link")

        for v in link_:
            links.append(v.get_text())

        link = [x for x in links if "https://news.google.com/search?q=" not in x]

        df = pd.DataFrame(link)
        df.to_csv(f'links/{i}.csv')

        del link[:]
        del links[:]

        print(f"{i}'s news scraped successfully")

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
