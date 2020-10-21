def creat(a):
    def creat_1(b):
        return a * b
    return creat_1

x = creat(10)

x(5)