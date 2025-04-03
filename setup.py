from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pychess_engine",
    version="1.1.0",
    author="Vanshu Galhotra",
    author_email="galhotravanshu@gmail.com",
    description="A lightweight chess engine written in Python. It can evaluate chess positions, calculate best moves, and integrate with various interfaces. It is designed to be simple and extensible, offering the flexibility to implement your own chess logic or use it as part of a larger project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanshugalhotra/pychess-engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Board Games",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pychess_engine=pychess_engine.cli:main", 
        ],
    },
)
