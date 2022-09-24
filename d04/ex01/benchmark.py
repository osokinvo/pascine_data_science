import timeit

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

def func_for_filter(elem):
    if elem is None:
        return False
    return elem

def list_map(emails:list, comp:str):
    return list(filter(func_for_filter, (list(map(func_for_map, emails, comp)))))


if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
    iter_count = 9_000_000
    loop_time = timeit.timeit('list_loop(emails,"@gmail.com")', number=iter_count, globals=globals())
    compr_time = timeit.timeit('list_compr(emails,"@gmail.com")', number=iter_count, globals=globals())
    map_time = timeit.timeit('list_map(emails, "@gmail.com")', number=iter_count, globals=globals())
    sort_time = sorted([loop_time, compr_time, map_time])
    if loop_time == sort_time[0]:
        print("it is better to use a loop")
    elif compr_time == sort_time[0]:
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a map")
    print(f"{sort_time[0]} vs {sort_time[1]} vs {sort_time[2]}")