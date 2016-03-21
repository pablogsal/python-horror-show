import itertools


def pump(fun):
    def wrap(*args, **kwargs):
        l = fun(*args, **kwargs)
        l.send(None)
        return l.send
    return wrap


@pump
def cont():
    prev = None
    current = None
    count = itertools.count()
    id = next(count)
    while True:
        if prev is None or prev + 1 == current:
            prev = current
            current = yield id
        else:
            prev = current
            id = next(count)
            current = yield id


a = [1, 2, 3, 7, 11, 12, 13, 14, 8, 34, 35, 36]
gr = itertools.groupby(a, cont())
print([(a, list(b)) for a, b in gr])
