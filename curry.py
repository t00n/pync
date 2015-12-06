from functools import wraps, partial
from inspect import signature

def curry(func):
    def f(*args, **kwargs):
        newfunc = partial(func, *args, **kwargs)
        if len(signature(newfunc).parameters) == 0:
            return newfunc()
        else:
            return newfunc
    return f

@curry
def testfunc(x, y):
    return (x+1, y-1)

if __name__ == '__main__':
    assert testfunc(1, 1) == (2,0)
    a = testfunc(1)
    assert a(1) == (2,0)