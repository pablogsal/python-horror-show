import itertools


def perm(iterable):
    if len(iterable) == 1:
        yield iterable
    for index, elem in enumerate(iterable):
        for group in perm(iterable[:index] + iterable[index + 1:]):
            yield [elem] + group

a = [1, 2, 3]
# print(list(itertools.permutations(a)))
print(list(perm(a)))
