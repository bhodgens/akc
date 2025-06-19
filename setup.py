from setuptools import setup, find_packages

setup(
    name="akc",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "authentik-client",
        "typer",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "akc = akc.main:app",
        ],
    },
)

