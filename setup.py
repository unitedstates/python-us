from us import __appname__, __version__
from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name=__appname__,
    version=__version__,
    author="Jeremy Carbaugh",
    author_email="jcarbaugh@sunlightfoundation.com",
    url='https://github.com/sunlightlabs/python-us',
    description='US state meta information and other fun stuff',
    long_description=long_description,
    license='BSD',
    packages=find_packages(),
    package_data={'us': ['*.pkl']},
    include_package_data=True,
    install_requires=['metaphone'],
    entry_points={
        'console_scripts': ['states = us.cli.states:main']},
    platforms=['any'],
)
