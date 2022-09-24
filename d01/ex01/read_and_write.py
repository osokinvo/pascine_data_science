
def read_and_write():
    f = open('ds.csv', 'r')
    result = ""
    c = ','
    for s in f:
        l = s.split('"')
        while ",false," in l:
            l[l.index(',false,')] = "\tfalse\t"
        while ",true," in l:
            l[l.index(',true,')] = "\ttrue\t"
        while c in l:
            l[l.index(',')] = "\t"
        for i, field in enumerate(l):
            if field.find("\t") < 0 and len(field) > 0 and field.isprintable:
                l[i] = '"' + field + '"'
        result += "".join(l)

    f = open('ds.tsv', 'w')
    f.write(result)
    f.close

if __name__ == '__main__':
    read_and_write()
        