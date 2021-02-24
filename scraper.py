# To-D0:
# 1. Sort company link list into separate lists
# 2. Export link list to individual csv files

import time

import requests
from bs4 import BeautifulSoup

companies = []
links = []

file = open('guide/companies.txt', 'r').readlines()
for line in file:
    line = line.replace('\n', '')
    companies.append(line)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/88.0.4324.182 Safari/537.36"
}


def news(list_):
    for i in list_:
        URL = f"https://news.google.com/rss/search?q={i}&hl=en-US&gl=US&ceid=US:en"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'xml')
        link_ = soup.find_all("link")
        for x in link_:
            links.append(x.get_text())
        time.sleep(3)


news(companies)
print(links)
