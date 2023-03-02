from setuptools import setup
setup(
    name="httpmdhtml",
    version="0.0.3",
    license="gpl-3.0",
    author="John Hupperts",
    author_email="jrock4503@hotmail.com",
    url="https://github.com/treatmesubj/python-md-to-html-server",
    download_url="https://github.com/treatmesubj/python-md-to-html-server/archive/refs/tags/v0.0.3.tar.gz",
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
