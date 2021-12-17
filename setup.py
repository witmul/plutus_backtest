from setuptools import setup , find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='backt',
    version='0.0.8',
    author="Example Author",
    author_email="author@example.com",
    packages= find_packages(),
    url="https://github.com/witmul/backt/tree/main",
    install_requires=[
        'pandas',
        'yfinance',
        'plotly',
        'numpy'
    ],
    python_requires=">=3.9",
)