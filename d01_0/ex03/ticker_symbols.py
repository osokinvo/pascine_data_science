import sys

def ticker_symbols():
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
        ticker_symbol = sys.argv[1].upper()
        if ticker_symbol in COMPANIES.values():
            reverseMap = dict(map(reversed, COMPANIES.items()))
            company_name = reverseMap.get(ticker_symbol)
            print("{} {}".format(COMPANIES[company_name], STOCKS[ticker_symbol]))
        else:
            print('Unknown company')

if __name__ == '__main__':
    ticker_symbols()
