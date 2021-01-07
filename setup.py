import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandas-etl-pipeline",
    version="0.1.0",
    author="Rob Dalton",
    description="Package for creating ETL pipelines with Pandas DataFrames.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rob-dalton/pandas-etl-pipeline",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
