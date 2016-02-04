from ctypes import *
import numpy as np

libmias = cdll.LoadLibrary("mias_load.so")

c_uint_p = POINTER(c_uint)


class ImgShape(Structure):
    _fields_ = [('width', c_uint),
                ('height', c_uint)]


_get_file_size = libmias.get_file_size
_get_file_size.argtypes = [POINTER(c_char)]
_get_file_size.restype = ImgShape

_load_raw_image = libmias.load_image
_load_raw_image.argtypes = [POINTER(c_char), POINTER(POINTER(c_uint)), c_uint]


def load_image(path):
    img_shape = _get_file_size(path)
    shape = (img_shape.width, img_shape.height)
    size = img_shape.height*img_shape.width

    img = np.empty(shape, dtype=np.uint32)
    img_buff = c_uint_p(img.ctypes.data_as(c_uint_p))

    _load_raw_image(path, byref(img_buff), size)

    img = np.ctypeslib.as_array(img_buff, img.shape)
    img = img.reshape(shape, order='F')

    return img


if __name__ == "__main__":
    img = load_image("./mdb001lm")
    print img
