# mias-loader
A tiny Python module for loading raw MIAS images into Numpy arrays.

## Installation

Best installed using ```pip```:

```
    pip install -e .
```

# Usage:

Use the ```load_image``` function to get raw MIAS image data as a Numpy array.

```python
    from mias_load import load_image
    img = load_image("mdb001lm")
    print img
```
