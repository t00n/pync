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