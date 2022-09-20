import sys

def all_stocks():
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

        list_of_word = sys.argv[1].split(",")
        for i in range(len(list_of_word)):
            list_of_word[i] = list_of_word[i].strip()
        if "" in list_of_word:
            print()
            return
        
        reverseMap = dict(map(reversed, COMPANIES.items()))

        for word in list_of_word:
            if word.capitalize() in COMPANIES.keys():
                print("{} stock price is {}".format(word.capitalize(), STOCKS[COMPANIES[word.capitalize()]]))
            elif word.upper() in STOCKS.keys():
                print("{} is a ticker symbol for {}".format(word.upper(), reverseMap.get(word.upper())))
            else:
                print("{} is an unknown company or an unknown ticker symbol".format(word))
    
    else:
        print()

if __name__ == '__main__':
    all_stocks()
