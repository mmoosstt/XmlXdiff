from setuptools import find_packages, setup, Command


NAME = 'XmlXdiff'
DESCRIPTION = 'Compare xml files with svg output.'
URL = 'https://github.com/mmoosstt/XmlXdiff'
EMAIL = 'diponaut@gmx.de'
AUTHOR = 'mmoosstt'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = "0.1"

REQUIRED = [
    'PySide2',
    'lxml',
    'svgwriter'
]

EXTRAS = {}

long_description = """# XmlXdiff #
 - generating nice plots of differences between xml files
 - general comparison without grammatical information
 - playground for performance analysis
 - principle works
 
# Implementation #
 - creating an hashed tree representation of each element
 - each element is identified by it's xml path and a hash
 """

with open('README.md', 'r') as f:
    long_description = f.read()


from setuptools import setup


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=long_description,
      url=URL,
      author=AUTHOR,
      author_email=EMAIL,
      license='LGPL',
      package_dir={'': 'lib'},
      packages=['XmlXdiff', 'XmlXdiff.XReport'],
      install_requires=REQUIRED,
      zip_safe=True,
      )
