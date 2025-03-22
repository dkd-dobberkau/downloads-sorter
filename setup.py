#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
import codecs
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="downloads-sorter",
    version=find_version("downloads_sorter", "__init__.py"),
    description="A tool to organize your downloads folder",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Downloads Sorter Team",
    author_email="info@example.com",
    url="https://github.com/yourusername/downloads-sorter",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'downloads-sorter=downloads_sorter.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Desktop Environment :: File Managers',
        'Topic :: Utilities',
    ],
    keywords='downloads, file organization, utility',
    python_requires='>=3.6',
    install_requires=[],
)
