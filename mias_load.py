from ctypes import *
import numpy as np

c_uint_p = POINTER(c_uint)
libmias = cdll.LoadLibrary("mias_load.so")

_get_file_size = libmias.get_file_size
_get_file_size.argtypes = [POINTER(c_char)]
_get_file_size.restype = c_uint

_load_raw_image = libmias.load_image
_load_raw_image.argtypes = [POINTER(c_char), POINTER(POINTER(c_uint)), c_uint]


def load_image(path):
    size = _get_file_size(path)
    img = np.empty(size, dtype=np.uint32)
    img_buff = c_uint_p(img.ctypes.data_as(c_uint_p))

    _load_raw_image(path, byref(img_buff), size)

    img = np.ctypeslib.as_array(img_buff, img.shape)
    img = img.reshape((4320, 2048), order='F')

    return img


if __name__ == "__main__":
    img = load_image("./mdb001lm")
