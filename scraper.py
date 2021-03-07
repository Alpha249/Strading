# To-Do:
# 1. Sort company link list into separate lists - ✓
# 2. Export link list to individual csv files - ✓
# 3. Figure out way to remove column name in .csv - ✓
# 4. Filter links based on date - ✓
# 5. Change links data to title - ✓
# 6. Filter news sources from title data in .csv - ✓

import time
from datetime import datetime, date
import random
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

start = time.perf_counter()

companies = []
dates = []
f_date = []
titles = []
user_agents = []

regex = r'(\s-\s.*)'

with open('guide/useragents.txt', 'r') as ua:
    ua = ua.readlines()
    for p in ua:
        p = p.replace('\n', '')
        user_agents.append(p)

with open('guide/companies.txt', 'r') as f:
    f = f.readlines()
    for lines in f:
        lines = lines.replace('\n', '')
        companies.append(lines)


headers = {
    "User-Agent": random.choice(user_agents),
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive"

}


def News(company):
    for i in company:
        # Initialize BeautifulSoup and requests
        URL = f"https://news.google.com/rss/search?q={i}&hl=en-US&gl=US&ceid=US:en"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'xml')

        # Title filtering
        title_ = soup.find_all("title")
        for v in title_:
            titles.append(v.get_text())

        # Date filtering
        Date_ = soup.find_all("pubDate")
        for n in Date_:
            dates.append(n.get_text())

        for t in dates:
            obj = datetime.strptime(t, '%a, %d %b %Y %H:%M:%S %Z')
            d = date(year=obj.year, month=obj.month, day=obj.day)
            f_date.append(d.strftime('%d-%b-%Y'))

        # Create dictionary
        dictionary = dict(zip(titles, f_date))

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

        final_titles = list(dictionary.keys())

        # Export data
        df = pd.DataFrame(final_titles)
        df.to_csv(f'titles/{i}.csv', encoding='utf-8')

        # Reset lists so no overlap occurs
        del titles[:]
        del final_titles[:]

        print(f"{i}'s news scraped successfully.")

        # Pause to avoid IP blocking
        time.sleep(3)


def Filter(company):
    for k in company:
        file = f'titles/{k}.csv'

        with open(file, 'r', encoding='utf-8') as u:
            u.seek(0)
            u = u.readlines()
            # Delete first line
            del u[:1]

        # Sub all the new sources for whitespaces
        matches = [re.sub(regex, '', line) for line in u]

        # Write to same file with cleaned titles
        with open(file, 'w+', encoding='utf-8') as j:
            for line_ in matches:
                j.write(line_)


News(companies)
Filter(companies)

end = time.perf_counter()

print(f"Time taken: {end - start}")
