import sys

class Research:
    def __init__(self):
        f = open("data.csv", "r")

        self.file_string = f.read()
        f.close

    def file_reader(self):
        return(self.file_string)

if __name__ == '__main__':
    try:
        ex_class = Research()
        print(ex_class.file_reader())
    except Exception:
        pass
