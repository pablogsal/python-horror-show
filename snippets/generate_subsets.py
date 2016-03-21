import itertools


def subsets(iterable):
    if len(iterable) < 1:
        yield iterable
        return
    last = iterable[-1]
    for sub in subsets(iterable[:-1]):
        yield sub
        yield sub + [last]

a = [1, 2, 3]
print(list(subsets(a)))
