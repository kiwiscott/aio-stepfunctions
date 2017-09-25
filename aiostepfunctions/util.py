import importlib
from uuid import uuid4


def unique_key(namespace):
    return namespace + str(uuid4()).replace('-', '')


def _mod_name(full_name):
    return '.'.join(full_name.split('.')[:-1])


def _func_name(full_name):
    return full_name.split('.')[-1:][0]


def load_func(full_name):
    mod_name = _mod_name(full_name)
    func_name = _func_name(full_name)

    mod = importlib.import_module(mod_name)
    return getattr(mod, func_name)
