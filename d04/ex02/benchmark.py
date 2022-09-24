import timeit
import sys

def list_compr(emails:list, comp:str):
    result = [email for email in emails if email.find(comp) >= 0]
    return result

def list_loop(emails:list, comp:str):
    result = list()
    for i in range(0, len(emails)):
        if emails[i].find(comp) >= 0:
            result.append(emails)
    return result

def func_for_map(email:str, comp:str):
    if email.find(comp) >= 0:
        return email

def list_filter(emails:list, comp:str):
    return list(filter(lambda email: email.find(comp) >= 0, emails))

def list_map(emails:list, comp:str):
    return list(map(func_for_map, emails, comp))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        metod_name = sys.argv[1]
        iter_count = sys.argv[2].strip()
        if metod_name in ['loop', 'list_comprehension', 'map', 'filter'] and iter_count.isnumeric():
            emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
            iter_count = int(iter_count)
            if metod_name == 'loop':
                print(timeit.timeit('list_loop(emails,"@gmail.com")', number=iter_count, globals=globals()))
            elif metod_name == 'list_comprehension':
                print(timeit.timeit('list_compr(emails,"@gmail.com")', number=iter_count, globals=globals()))
            elif metod_name == 'map':
                print(timeit.timeit('list_map(emails, "@gmail.com")', number=iter_count, globals=globals()))
            else:
                print(timeit.timeit('list_filter(emails, "@gmail.com")', number=iter_count, globals=globals()))
        else:
            print("Wrong input!")