# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup


def get_version(fname='mccabe.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.rst',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='jones-complexity',
    version=get_version(),
    description="Jones Complexity checker, plugin for flake8",
    long_description=get_long_description(),
    keywords='flake8 mccabe',
    author='Tarek Ziade',
    author_email='tarek@ziade.org',
    url='https://github.com/pycqa/mccabe',
    license='Expat license',
    py_modules=['mccabe'],
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'flake8.extension': [
            'C90 = jones_complexity:JonesComplexityChecker',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
