import timeit
import sys

from functools import reduce

from pyrsistent import l

def func_loop(num:list):
    result = 0
    for i in num:
        result += i**2
    return result

if __name__ == '__main__':
    if len(sys.argv) == 4:
        metod_name = sys.argv[1]
        iter_count = sys.argv[2].strip()
        num = sys.argv[3].strip()
        if metod_name in ['loop','reduce'] and iter_count.isnumeric() and num.isdecimal():
            iter_count = int(iter_count)
            num = int(num)
            r = range(1,num+1)
            if metod_name == 'loop':
                print(func_loop(r))
                print(timeit.timeit('func_loop(r)', number=iter_count, globals=globals()))
            else:
                print(reduce(lambda s, n: s+n**2,r))
                print(timeit.timeit('reduce(lambda s, n: s+n**2,r)', number=iter_count, globals=globals()))
        else:
            print("Wrong input!")
