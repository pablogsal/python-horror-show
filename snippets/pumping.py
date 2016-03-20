"""
Test to use coroutines with itertools module to extend usage.
"""

import itertools


def pump(fun):
    """
    Decorator to prime coroutines for use with itertools module
    """
    def wrap(*args, **kwargs):
        corutine = fun(*args, **kwargs)
        corutine.send(None)
        return corutine.send
    return wrap


@pump
def acum_filter():
    """
    Coroutine filter that gives True if the current sum is positive and False if the sum reaches
    zero or lower values. In the latter case, the current sum restarts to zero.
    """
    total = 0
    while True:
        if total <= 0:
            total = 0
            value = yield False
            total += value
        else:
            value = yield True
            total += value


test_values = iter([1, 2, 3, -2, 1, -5, 1, 2, 3, 4, 5])
filtered_values = itertools.groupby(test_values, key=acum_filter())
final_values = [list(val) for test, val in filtered_values if test]
print(final_values)
