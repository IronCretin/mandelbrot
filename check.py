import ctypes

lib = ctypes.CDLL('libbrot.so')

check = lib.check

check.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double)