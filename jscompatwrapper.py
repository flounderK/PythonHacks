import json


class JSCompatWrapper:

    def __init__(self, d, *args, **kwargs):
        if not isinstance(d, dict):
            raise Exception("d must be a dict")

        self._dict = d

    def __getattr__(self, name):
        attr = getattr(self._dict, name) if bool(hasattr(self._dict, name)) else \
                                            self._dict.get(name, AttributeError)
        if attr is AttributeError:
            raise AttributeError
        return JSCompatWrapper(attr) if isinstance(attr, dict) else attr

    def __getitem__(self, name):
        return self._dict.__getitem__(name)

    def __setitem__(self, name, value):
        return self._dict.__setitem__(name, value)

    def __dir__(self):
        return dir(self._dict)

    def __repr__(self):
        return repr(self._dict)



ipython = False
import inspect
for frame in inspect.stack():
    if 'IPython' in frame[1]:
        ipython = True


if ipython:
    import IPython
    formatter = IPython.get_ipython().display_formatter.formatters['text/plain']
    formatter.for_type(JSCompatWrapper, formatter.type_printers[dict])


