def test_yield():

    def a_func():
        yield 1
        yield 1
        return
        #raise StopIteration()

    for i in a_func():
        print(i)