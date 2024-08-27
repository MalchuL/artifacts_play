import itertools


def test_product():
    print(list(itertools.product(["A", "B", "C"], ["D", "E"], ["F", "G", "M"])))