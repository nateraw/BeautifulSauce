from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

LONG_DESC = open("README.md").read()

setup(
    name="BeautifulSauce",
    version='0.0.1',
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    description="Tools that make BeautifulSoup more beautiful.",
    long_description=LONG_DESC,
    license="MIT",
    url="https://github.com/nateraw/BeautifulSauce",
    install_requires=requirements,
    packages=find_packages(),
    test_suite="tests",
    include_package_data=True
)
