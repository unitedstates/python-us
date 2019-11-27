from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='us',
    version='2.0.0',
    author="Jeremy Carbaugh",
    author_email="jeremy@isl.co",
    url='https://github.com/unitedstates/python-us',
    description='US state meta information and other fun stuff',
    long_description=long_description,
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
         'jellyfish==0.7.2'
    ],
    entry_points={
        'console_scripts': ['states = us.cli.states:main']},
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
