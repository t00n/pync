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

class MatchObject:
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, key):
        if isinstance(key, tuple):
            if isinstance(self.obj, list):
                lst = [self.obj[i] for i in key]
                lst.append([x for i, x in enumerate(self.obj) if i not in key])
                return tuple(lst)
        return obj.__getitem__[key]

def listmatching(func):
    def wrapper(*args, **kwargs):
        newargs = map(MatchObject, args)
        newkwargs = {key: MatchObject(val) for key, val in kwargs.items()}
        return func(*newargs, **newkwargs)
    return wrapper
