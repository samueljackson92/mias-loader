import os.path
import numpy as np


def get_image_shape(path):
    """Get the shape of an image as a Python object.

    This is a helper function so that we can create the memory for the image
    Python side and forget about memory ownership issues.

    :param path: path on disk to the image
    :returns: ImgShape object with the dimensions of the image
    """
    if not (os.path.exists(path) and os.path.isfile(path)):
        raise RuntimeError("Could not find file %s" % path)

    st = os.stat(path)
    file_size = st.st_size

    # dictonary of shapes for the different image sizes
    img_sizes = {
        (1600 * 4320): (4320, 1600),
        (2048 * 4320): (4320, 2048),
        (2600 * 4320): (4320, 2600),
        (5200 * 4000): (5200, 4000),
    }
    img_shape = img_sizes.get(file_size, None)

    # check the shape we got was valid
    if img_shape is None:
        raise RuntimeError("Could not load image. Bad image shape. %s" % path)

    return img_shape, file_size


def load_image(path):
    """Get a raw MIAS from file.

    This will return a numpy array with each pixel loaded as an unsigned
    integer.

    :param path: path on disk to the image
    :returns: ndarray representing the image data
    """
    if not (os.path.exists(path) and os.path.isfile(path)):
        raise RuntimeError("Could not find file %s" % path)

    shape, file_size = get_image_shape(path)
    # Important! Images are stored as np.uint8 so this must be set as the dtype
    img = np.fromfile(path, count=shape[0]*shape[1], dtype=np.uint8)
    # The raw image array is using Fortran (column major) array order.
    img = img.reshape(shape, order='F')
    return img
