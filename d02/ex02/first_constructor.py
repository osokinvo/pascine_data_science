import sys

class Research:
    def __init__(self, path):
        f = open(path, "r")
        self.file_string = f.read()
        line_list = self.file_string.split('\n')
        if len(line_list) < 2:
            raise Exception("Cannot read this file")

        first_line = True
        for line in line_list:
            field_list = line.split(",")
            if first_line:
                if len(field_list) != 2 or len(field_list[0]) == 0 or len(field_list[1]) == 0:
                    raise Exception("Cannot read this file")
                first_line = False
            else:
                if len(field_list) != 2 or field_list[0] == field_list[1] or\
                    (field_list[0] != "0" and field_list[0] != "1") or\
                    (field_list[1] != "0" and field_list[1] != "1"):
                    raise Exception("Cannot read this file")
        f.close

    def file_reader(self):
        return(self.file_string)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            ex_class = Research(sys.argv[1])
            print(ex_class.file_reader())
        except Exception:
            sys.exit("Error")
    else:
        sys.exit("Invalid argument!")
