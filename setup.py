from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pychess_engine",
    version="1.0.0",
    author="Vanshu Galhotra",
    author_email="galhotravanshu@gmail.com",
    description="A chess engine module for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanshugalhotra/pychess_engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Board Games",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[],  # Add dependencies here if needed
    entry_points={
        "console_scripts": [
            "pychess_engine=pychess_engine.cli:main",  # Adjust CLI entry point if necessary
        ],
    },
)
