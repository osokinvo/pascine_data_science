from ast import Pass


def to_dictionary():
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]

    dict_of_tuples = dict()
    for val, k in list_of_tuples:
        if k in dict_of_tuples.keys():
            dict_of_tuples[k].add(val)
        else:
            dict_of_tuples[k] = {val}

    for k, list_of_val in dict_of_tuples.items():
        for val in list_of_val:
            print("'{}' : '{}'".format(k, val))

if __name__ == '__main__':
    to_dictionary()