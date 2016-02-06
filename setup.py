try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
    'py_modules': ['mias_load'],
    'name': 'mias_loader'
}

setup(**config)
