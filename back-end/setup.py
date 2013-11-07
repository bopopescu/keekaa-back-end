""" Setup File for DuJour Back-End """

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="dujour-backend",
    version="0.0.1",
    author="David Tsai",
    author_email="dbtsai@dbtsai.com",
    description=("This is the backend used for DuJour."),
    packages=[
        'website',
        'website.accounts',
        'website.actions',
        'website.api',
        'website.api.v1',
        'website.brands',
        'website.library',
        'website.media',
        'website.users',
    ],
    long_description=read('README.rst'),
)
