#!/usr/bin/python
from opcode import opmap
from types import CodeType
import sys


def return_locals_patch(func):
    """removes the return statement from the provided function and
    makes the function return locals() instead"""
    func_co = func.__code__
    if not isinstance(func_co, CodeType):
        raise Exception("Unable to get code")
    kwargs = {k: getattr(func_co, k) for k in dir(func_co) if k.startswith('co_')}
    # patch in locals if it doesn't already exist
    if 'locals' not in kwargs['co_names']:
        kwargs['co_names'] += ('locals',)

    locals_ind = kwargs['co_names'].index('locals')
    LOAD_GLOBAL = opmap['LOAD_GLOBAL']
    CALL_FUNCTION = opmap['CALL_FUNCTION']
    RETURN_VALUE = opmap['RETURN_VALUE']

    new_code = bytes([LOAD_GLOBAL, locals_ind,
                      CALL_FUNCTION, 0,
                      RETURN_VALUE, 0])

    # remove old return statement
    kwargs['co_code'] = kwargs['co_code'][:-2] + new_code
    # patch function
    func.__code__ = func_co.replace(**kwargs)


def set_locals_as_globals(local_dict):
    """Takes in a dictionary (which is the result of `locals()` and sets all of the
    variables in that dictionary to the context of the main file"""
    try:
        this_module = sys.modules[__name__]
        for k, v in local_dict.items():
            if k == '__return__':
                continue
            setattr(this_module, k, v)
    except AttributeError:
        pass
    return local_dict


def main():
    variable = 'hello'


if __name__ == '__main__':
    print('Original call to main')
    print(main())
    print('patching main')
    return_locals_patch(main)
    set_locals_as_globals(main())
    print("Printing varaible that should only be in main's scope")
    print(variable)

