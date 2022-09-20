import sys

def stock_prices():
    if len(sys.argv) == 2:
        COMPANIES = {
            'Apple': 'AAPL',
            'Microsoft': 'MSFT',
            'Netflix': 'NFLX',
            'Tesla': 'TSLA',
            'Nokia': 'NOK'
        }

        STOCKS = {
            'AAPL': 287.73,
            'MSFT': 173.79,
            'NFLX': 416.90,
            'TSLA': 724.88,
            'NOK': 3.37
        }
        company_name = sys.argv[1].capitalize()
        if company_name in COMPANIES.keys():
            print(STOCKS[COMPANIES[company_name]])
        else:
            print('Unknown company')


if __name__ == '__main__':
    stock_prices()
