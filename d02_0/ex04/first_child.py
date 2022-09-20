import sys
from random import randint

class Research:
    def __init__(self, path):
        f = open(path, "r")
        self.file_string = f.read()
        self.line_list = self.file_string.split('\n')
        if len(self.line_list) < 2:
            raise Exception("Cannot read this file")
        f.close

    def file_reader(self, has_header=True):
        self.coin_list = list()
        for line in self.line_list:
            field_list = line.split(",")
            if has_header:
                if len(field_list) != 2 or len(field_list[0]) == 0 or len(field_list[1]) == 0:
                    raise Exception("Cannot read this file")
                has_header = False
            else:
                tmp_list = list()
                
                if len(field_list) != 2 or field_list[0] == field_list[1] or\
                    (field_list[0] != "0" and field_list[0] != "1") or\
                    (field_list[1] != "0" and field_list[1] != "1"):
                    raise Exception("Cannot read this file")
                tmp_list.append(int(field_list[0]))
                tmp_list.append(int(field_list[1]))
                self.coin_list.append(tmp_list)
        return(self.coin_list)

    class Calculations:
        def __init__(self, coin_list:list):
            self.coin_list = coin_list

        def counts(self):
            sum0 = 0
            sum1 = 0
            for i0, i1 in self.coin_list:
                sum0 += i0
                sum1 += i1
            return (sum0, sum1)

        def fractions(self, count):
            count0, count1 = count
            amount = count0 + count1
            return (count0 * 100 / amount, count1 * 100 / amount)

    class Analytics(Calculations):
        def predict_random(self, number_of_predictions):
            result = list()
            for i in range(number_of_predictions):
                num0 = randint(0,1)
                if num0 > 0:
                    num1 = 0
                else:
                    num1 = 1
                result.append([num0, num1])
            return result
        
        def predict_last(self):
            return self.coin_list[-1]

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            print("file_reader():")
            ex_class = Research(sys.argv[1])
            coin_list = ex_class.file_reader()
            print(coin_list)
            ex_calculations = ex_class.Calculations(coin_list)
            coin_count = ex_calculations.counts()
            print("counts:")
            print(f"{coin_count[0]} {coin_count[1]}")
            print("fractions():")
            coin_fractions = ex_calculations.fractions(coin_count)
            print(f"{coin_fractions[0]} {coin_fractions[1]}")
            print("predict_random():")
            ex_analytics = ex_class.Analytics(coin_list)
            print(ex_analytics.predict_random(3))
            print("predict_last():")
            print(ex_analytics.predict_last())

        except Exception:
            sys.exit("Error")
    else:
        sys.exit("Invalid argument!")
