class Must_read:
    def __init__(self):
        f = open("data.csv", "r")

        self.file_string = f.read()
        f.close

    def print_file(self):
        print(self.file_string)

if __name__ == '__main__':
    try:
        ex_class = Must_read()
        ex_class.print_file()
    except Exception:
        pass
