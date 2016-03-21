
from collections import Iterable


def flatten(iterable):

    for item in iterable:
        if isinstance(item, Iterable):
            for elem in flatten(item):
                yield elem
        else:
            yield item

a = [[1, 2], 3, [[1, 2], [3], [[4, 4]], [[[4]]], 4]]

print(list(flatten(a)))
