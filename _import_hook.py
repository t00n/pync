import imp
import os
import types
import sys
from redbaron import RedBaron
from pync import *

class PyncImporter(object):
    def __init__(self):
        self.modules = []

    def register_modules(self, *args):
        self.modules.extend(args)

    def register_importer(self):
        sys.meta_path.insert(0, self)

    def find_module(self, name, path=None):
        if name in self.modules:
            return self
        return None

    def load_module(self, name):
        try:
            suffix = name.split('.')[-1]
            fd, pathname, (suffix, mode, type_) = imp.find_module(suffix)
        except ImportError:
            return None

        module = types.ModuleType(name) #create empty module object

        with fd:
            if type_ == imp.PY_SOURCE:
                filename = pathname
            elif type_ == imp.PY_COMPILED:
                filename = pathname[:-1]
            elif type_ == imp.PKG_DIRECTORY:
                filename = os.path.join(pathname, '__init__.py')
                module.__path__ = [pathname]
            else:
                return imp.load_module(name, fd, pathname, (suffix, mode, type_))

            if filename != pathname:
                try:
                    with open(filename, 'U') as real_file:
                        src = real_file.read()
                except IOError: #fallback
                    return imp.load_module(name, fd, pathname, (suffix, mode, type_))
            else:
                src = fd.read()

        module.__file__ = filename
        red = RedBaron(src)
        red.insert(0, 'import pync')
        for func in red.find_all('def'):
            func.decorators.append('@pync.curry')
        inlined = red.dumps()
        code = compile(inlined, filename, 'exec')
        sys.modules[name] = module
        exec(code,  module.__dict__)

        return module

importer = PyncImporter()


