#!/usr/bin/env python

# import os

from setuptools import setup

# import glob


data_files = [("share/doc/skeleton", ["AUTHORS", "README.md"])]


def get_data_files():
    data_files = [("share/doc/skeleton", ["AUTHORS", "NEWS", "README.md"])]

    # if hasattr(sys, 'real_prefix') or 'bsd' in sys.platform:
    #     conf_path = os.path.join(sys.prefix, 'etc', 'glances')
    # elif not hasattr(sys, 'real_prefix') and 'linux' in sys.platform:
    #     conf_path = os.path.join('/etc', 'glances')
    # elif 'darwin' in sys.platform:
    #     conf_path = os.path.join('/usr/local', 'etc', 'glances')
    # elif 'win32' in sys.platform:
    #     conf_path = os.path.join(os.environ.get('APPDATA'), 'glances')
    # data_files.append((conf_path, ['conf/glances.conf']))

    # for mo in glob.glob('i18n/*/LC_MESSAGES/*.mo'):
    #     data_files.append((os.path.dirname(mo).replace('i18n/', 'share/locale/'), [mo]))

    return data_files


def get_requires():
    requires = []

    return requires


setup(
    name="skeleton",
    version="0.1",
    description="...",
    long_description=open("README.md").read(),
    author="Nicolas Hennion",
    author_email="nicolas@nicolargo.com",
    url="https://github.com/nicolargo/skeleton",
    # download_url='https://s3.amazonaws.com/skeleton/skeleton-0.1.tar.gz',
    license="MIT",
    keywords="...",
    install_requires=get_requires(),
    extras_require={},
    packages=["skeleton"],
    include_package_data=True,
    data_files=get_data_files(),
    # test_suite="skeleton.test",
    entry_points={"console_scripts": ["skeleton=skeleton.skeleton:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 2",
    ],
)
