from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="httpmdhtml",
    version="0.0.8",
    license="gpl-3.0",
    author="John Hupperts",
    author_email="jrock4503@hotmail.com",
    description="HTTP server that converts markdown to HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/treatmesubj/python-md-to-html-server",
    download_url="https://github.com/treatmesubj/python-md-to-html-server/archive/refs/tags/v0.0.8.tar.gz",
    packages=["httpmdhtml"],
    package_dir={"python-md-to-html-server": "httpmdhtml"},
    project_urls={
        "Source": "https://github.com/treatmesubj/python-md-to-html-server",
    },
    install_requires=[
        "markdown-it-py",
        "beautifulsoup4",
        "html5lib"
    ],
)
