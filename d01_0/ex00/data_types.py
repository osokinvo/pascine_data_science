def  data_types():
    """
    [int, str, float, bool, list, dict, tuple, set]
    """
    a = 1
    b = "output"
    c = 1.0
    d = a != c
    e = list()
    f = dict()
    g = tuple()
    h = set()
    e.append(str(type(a))[8:-2])
    e.append(str(type(b))[8:-2])
    e.append(str(type(c))[8:-2])
    e.append(str(type(d))[8:-2])
    e.append(str(type(e))[8:-2])
    e.append(str(type(f))[8:-2])
    e.append(str(type(g))[8:-2])
    e.append(str(type(h))[8:-2])
    print(e)

if __name__ == '__main__':
    data_types()
