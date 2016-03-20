import itertools

def pump(fun):
    c = fun()
    next(c)
    def wrap( x ):
        val =  c.send(x)
        next(c)
        return val
    return wrap

@pump
def ac():
    total = 0
    while True:
        val = (yield)
        total += val
        if total <= 0:
            yield False
            total = 0
        else:
            yield True



lista = iter([1,2,3,-2,1,-5,1,2,3,4,5])

a = itertools.groupby(lista,key = ac)

b = [list(val) for test,val in a if test]

print(b)