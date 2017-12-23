import urllib3
import json
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import urlencode

if __name__ == '__main__':
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://8.lemicp.com/trade/jczq/hhtz?playid=9006&e=2')
    
    soup = BeautifulSoup(r.data)

    list_soup = soup.find('div', {'class': 'mod hist_20171019'})
    print(list_soup)
