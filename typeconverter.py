#!/usr/bin/python3
import ctypes


class TypeConverter(ctypes.Union):
    class NiceFieldRepr:
        def __repr__(self):
            return " ".join(["%s: %#x" % (k, getattr(self, k)) for k, v in self._fields_])

    class U32(ctypes.Structure, NiceFieldRepr):
        _fields_ = [("l", ctypes.c_uint32),
                    ("h", ctypes.c_uint32)]

    class S32(ctypes.Structure, NiceFieldRepr):
        _fields_ = [("l", ctypes.c_int32),
                    ("h", ctypes.c_int32)]

    class U16(ctypes.Structure, NiceFieldRepr):
        _fields_ = [("ll", ctypes.c_uint16),
                    ("lh", ctypes.c_uint16),
                    ("hl", ctypes.c_uint16),
                    ("hh", ctypes.c_uint16)]

    class S16(ctypes.Structure, NiceFieldRepr):
        _fields_ = [("ll", ctypes.c_uint16),
                    ("lh", ctypes.c_uint16),
                    ("hl", ctypes.c_uint16),
                    ("hh", ctypes.c_uint16)]

    class F32(ctypes.Structure):
        _fields_ = [("l", ctypes.c_float),
                    ("h", ctypes.c_float)]

        def __repr__(self):
            return " ".join(["%s: %s" % (k, getattr(self, k)) for k, v in self._fields_])

    _fields_ = [("u16", U16),
                ("s16", S16),
                ("u32", U32),
                ("s32", S32),
                ("u64", ctypes.c_uint64),
                ("s64", ctypes.c_int64),
                ("f32", F32),
                ("f64", ctypes.c_double)]

    def __repr__(self):
        return "\n".join(["%s: %s" % (k, hex(getattr(self, k))
                          if not any([issubclass(v, ctypes.Structure),
                                      isinstance(getattr(self, k),
                                                 (float, ctypes.Structure))])
                          else str(getattr(self, k)))
                          for k, v in self._fields_])


if __name__ == "__main__":
    tc = TypeConverter()
    print(tc)
