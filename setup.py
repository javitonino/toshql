import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="toshql",
    version="0.0.1",
    author="Javier Torres",
    author_email="jtorres@carto.com",
    description=("PostgreSQL example commands for tosh"),
    license="BSD",
    keywords="shell asyncio postgresql",
    url="https://github.com/javitonino/toshql",
    packages=find_packages('.'),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "Topic :: System :: Shells",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires="""
        tosh>=0.0.1, <1
    """
)
