x = [i for i in range(10)]
for i in x:
    print(i)


class A:
    def __init__(self):
        self.x = [i for i in range(10)]

    def print(self):
        for i in self.x:
            print(i)


class B:
    def __init__(self):
        pass

    def print(self):
        x = [i for i in range(10)]
        for i in x:
            print(i)
