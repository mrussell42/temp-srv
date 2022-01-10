import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="temp_srv-mrussell",
    version="0.0.1",
    author="Matt Russell",
    author_email="mrussell@cantab.net",
    description="A web based temperature logging server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrussell42/temp-srv",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    )
