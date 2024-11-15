from setuptools import setup, find_packages

setup(
    name="pychess",
    version="1.0.0",
    author="Vanshu Galhotra",
    author_email="galhotravanshu@gmail.com",
    description="A chess engine module for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vanshugalhotra/pychess",

    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pychess=pychess.cli:main",
        ],
    },
)
