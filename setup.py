try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.core import Extension

# define the extension module
loader_tools = Extension('mias_load',
                         sources=['mias_load.c'],
                         extra_compile_args=['-std=c99'])

config = {
    'description': 'A tiny Python/C library for loading MIAS images from file.',
    'author': 'Samuel Jackson',
    'url': 'http://github.com/samueljackson92/mias-loader',
    'download_url': 'http://github.com/samueljackson92/mias-loader',
    'author_email': 'samueljackson@outlook.com',
    'version': '0.1.0',
    'install_requires': [
        'numpy'
    ],
    'ext_modules': [loader_tools],
    'py_modules': ['mias_load'],
    'name': 'mias_loader'
}

setup(**config)
