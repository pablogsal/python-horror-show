import itertools


def nwise(iterable, n):
    iterables = itertools.tee(iterable, n)
    temp = list()
    for index, iterable in enumerate(iterables):
        temp.append(itertools.islice(iterable, index, None))
    return zip(*temp)


a = nwise([1, 2, 3, 4, 5], 3)
print(list(a))
