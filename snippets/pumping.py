import itertools

def pump(fun):
    def wrap( *args, **kwargs ):
        corutine =  fun(*args,**kwargs)
        corutine.send(None)
        return corutine.send
    return wrap

@pump
def ac():
    total = 0
    while True:
        if total <= 0:
            total = 0
            val = yield False
            total += val
        else:
            val = yield True
            total += val



lista = iter([1,2,3,-2,1,-5,1,2,3,4,5])

a = itertools.groupby(lista,key = ac())

b = [list(val) for test,val in a if test]

print(b)
