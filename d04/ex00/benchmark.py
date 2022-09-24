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

if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
    iter_count = 9_000_000
    loop_time = timeit.timeit('list_loop(emails,"@gmail.com")', number=iter_count, globals=globals())
    compr_time = timeit.timeit('list_compr(emails,"@gmail.com")', number=iter_count, globals=globals())
    if loop_time < compr_time:
        print("it is better to use a loop")
        print(f"{loop_time} vs {compr_time}")
    else:
        print("it is better to use a list comprehension")
        print(f"{compr_time} vs {loop_time}")
