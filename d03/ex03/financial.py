import requests
from bs4 import BeautifulSoup
import sys

if __name__ == '__main__':
    response = requests.get('https://finance.yahoo.com/quote/msft/financials?p=msft').text
    soup = BeautifulSoup (response, 'html.parser')
    if soup.title.string.find(sys.argv[1]) < 0:
        raise Exception
