import os.path
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


def get_image_shape(path):
    """Get the shape of an image as a Python object.

    This is a helper function so that we can create the memory for the image
    Python side and forget about memory ownership issues.

    :param path: path on disk to the image
    :returns: ImgShape object with the dimensions of the image
    """

    if not (os.path.exists(path) and os.path.isfile(path)):
        raise RuntimeError("Could not find file %s" % path)

    img_shape = _get_file_size(path)
    shape = (img_shape.height, img_shape.width)

    # check the shape we got was valid
    if len(shape) < 2 or (shape[0] == 0 and shape[1] == 0):
        raise RuntimeError("Could not load image. Bad image shape. %s" % path)

    return shape


def load_image(path):
    """Get a raw MIAS from file.

    This will return a numpy array with each pixel loaded as an unsigned
    integer.

    :param path: path on disk to the image
    :returns: ndarray representing the image data
    """
    if not (os.path.exists(path) and os.path.isfile(path)):
        raise RuntimeError("Could not find file %s" % path)

    # get the shape of the image
    shape = get_image_shape(path)
    size = shape[0]*shape[1]

    # create somewhere to put the data
    img = np.empty(shape, dtype=np.uint32)
    img_buff = c_uint_p(img.ctypes.data_as(c_uint_p))

    _load_raw_image(path, byref(img_buff), size)

    # convert the image data to a numpy array and reshape as image
    img = np.ctypeslib.as_array(img_buff, (size,))
    img = img.reshape(shape, order='F')
    return img


if __name__ == "__main__":
    import skimage.io as io
    img = load_image("./mdb001lm")
    io.imshow(img)
    io.show()
