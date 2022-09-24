import timeit
import random
from collections import Counter

def my_func(rand_arr:list, max:int):
    res_dict = {i: 0 for i in range(max +1)}
    for n in rand_arr:
        res_dict[n] += 1
    return res_dict

def my_top(rand_dict:list):
    top_list = sorted(rand_dict, key=lambda item: (-item[1]))
    return top_list[0:10]

if __name__ == '__main__':
    rand_arr = [random.randint(0, 100) for _ in range(1000000)]
    iter_count = 1
    rand_dict = my_func(rand_arr, 100)
    print(f"my function: {timeit.timeit('my_func(rand_arr, 100)', number=iter_count, globals=globals())}")
    print(f"Counter: {timeit.timeit('Counter(rand_arr)', number=iter_count, globals=globals())}")
    print(f"my top: {timeit.timeit('my_top(rand_dict.items())', number=iter_count, globals=globals())}")
    rand_list = list(Counter(rand_arr))
    print(f"Counter's top: {timeit.timeit('list(Counter(rand_list))[0:10]', number=iter_count, globals=globals())}")