import sys

from setuptools import setup


version = "0.1"

tests_require = [
    'mock==0.7.2',
]

if sys.version_info < (2, 7):
    tests_require.append('unittest2')


setup(
    name="libalbumart",
    version=version,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
)
