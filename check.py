from ctypes import *

lib = CDLL('libbrot.so')

ccheck = lib.check

def check(maxit, reals, imags, size):
    ARRF = c_double * size
    ARRI = c_int * size
    out = ARRI()

    ccheck(maxit, ARRF(*reals), ARRF(*imags), size, out)

    return list(out)

# check.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double)