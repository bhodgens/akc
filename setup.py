from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="akc",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A client for Authentik.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/akc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "authentik-client",
        "typer",
        "rich",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "akc = akc.main:app",
        ],
    },
)
