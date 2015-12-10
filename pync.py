from functools import wraps, partial
from inspect import signature, _empty
from copy import copy

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
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Function(func)(*args, **kwargs)
    return wrapper

class List(list):
    def __getitem__(self, key):
        if isinstance(key, tuple):
            lst = [self[i] for i in key]
            lst.append([x for i, x in enumerate(self) if i not in key])
            return tuple(lst)
        return super(List, self).__getitem__(key)

functions = {}

def patternmatching(func):
    key = func.__name__
    if key not in functions:
        functions[key] = []
    functions[key].append(copy(func))
    @wraps(func)
    def wrapper(*args, **kwargs):
        for function in functions[key]:
            sign = signature(function)
            ok, i = True, 0
            for k, val in sign.parameters.items():
                print(args[i], val.default)
                if val.default != _empty and val.default != args[i]:
                    ok = False
                i+=1
            if ok:
                return function(*args, **kwargs)
    return wrapper