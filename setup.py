"""BeautifulSoup's saucy sibling!

BeautifulSauce provides:

- ability to featurize HTML documents with custom functions
- integration of CSS attributes (with inheritance!) applied to each Tag
- options for indexing HTML with numerical index lists
- built in utility functions that cover common boilerplate snippets
"""

DOCLINES = (__doc__ or '').split("\n")

from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="BeautifulSauce",
    version='0.0.8',
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    license="MIT",
    url="https://github.com/nateraw/BeautifulSauce",
    install_requires=requirements,
    packages=find_packages(),
    test_suite="tests",
    include_package_data=True
)
