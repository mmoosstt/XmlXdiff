from setuptools import find_packages, setup, Command


NAME = 'diffx'
DESCRIPTION = 'Compare xml files with svg output.'
URL = 'https://github.com/mmoosstt/XmlXdiff'
EMAIL = 'diponaut@gmx.de'
AUTHOR = 'mmoosstt'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = "1.1.1"

REQUIRED = [
    'PySide2',
    'lxml',
    'svgwrite',
    'dicttoxml',
]

EXTRAS = {}

with open('README.md', 'r') as f:
    long_description = f.read()


from setuptools import setup


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url=URL,
      author=AUTHOR,
      author_email=EMAIL,
      license='LGPL',
      package_dir={'': 'lib'},
      packages=['diffx', 'diffx.svg'],
      install_requires=REQUIRED,
      zip_safe=True,
      )
