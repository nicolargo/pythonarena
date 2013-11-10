#!/usr/bin/env python

# import os
# import sys
# import glob

from setuptools import setup

data_files = [
    ('share/doc/skeleton', ['AUTHORS', 'README.md'])
]

setup(
    name='skeleton',
    version='0.1',
    description="...",
    long_description=open('README.md').read(),
    author='Nicolas Hennion',
    author_email='nicolas@nicolargo.com',
    url='https://github.com/nicolargo/witsub',
    #download_url='https://s3.amazonaws.com/skeleton/skeleton-1.2.tar.gz',
    license="LGPL",
    keywords="..",
    packages=['skeleton'],
    include_package_data=True,
    data_files=data_files,
    # test_suite="witsub.test",
    entry_points={"console_scripts": ["skeleton=skeleton.skeleton:main"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2',
    ]
)
