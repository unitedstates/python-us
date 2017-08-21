from us import __appname__, __version__
from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name=__appname__,
    version=__version__,
    author="Jeremy Carbaugh",
    author_email="jeremy@isl.co",
    url='https://github.com/unitedstates/python-us',
    description='US state meta information and other fun stuff',
    long_description=long_description,
    license='BSD',
    packages=find_packages(),
    package_data={'us': ['*.pkl']},
    include_package_data=True,
    install_requires=['jellyfish==0.5.6'],
    entry_points={
        'console_scripts': ['states = us.cli.states:main']},
    platforms=['any'],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
