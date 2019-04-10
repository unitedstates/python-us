from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='us',
    version='1.0.0',
    author="Jeremy Carbaugh",
    author_email="jeremy@isl.co",
    url='https://github.com/unitedstates/python-us',
    description='US state meta information and other fun stuff',
    long_description=long_description,
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'jellyfish==0.6.1'
    ],
    extras_require={
        # Run `pip install -e .[testing]` to also install
        # packages needed for the unit tests
        'testing': [
            'pytest>=3.10,<3.11',
            'pytz',
            'requests>=2.21,<2.22',
            # Make sure that this version is the same as is
            # used in the CircleCI Docker container
            'tox>=3.3,<3.4'
        ]
    },
    entry_points={
        'console_scripts': ['states = us.cli.states:main']},
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
