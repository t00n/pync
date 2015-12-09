from functools import wraps, partial
from inspect import signature

class Function():
    def __init__(self, function):
        self.function = function
        self.args = []
        self.kwargs = {}

    def __call__(self, *args, **kwargs):
        self.args.extend(args)
        self.kwargs.update(kwargs)
        if len(self.args) + len(self.kwargs) >= len(signature(self.function).parameters):
            return self.function(*self.args, **self.kwargs)
        else:
            return self

def curry(func):
    def wrapper(*args, **kwargs):
        return Function(func)(*args, **kwargs)
    return wrapper

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
