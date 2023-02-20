# Python Markdown-to-HTML Server

It's the standard Python [http.server module](https://docs.python.org/3/library/http.server.html) but via [markdown-it-py](https://github.com/executablebooks/markdown-it-py), requested Markdown files are rendered and served as HTML

The `http.server` module's `SimpleHTTPRequestHandler` class is inherited by a new class with its `do_GET` method overridden. [beautifulsoup](https://pypi.org/project/beautifulsoup4/) and [html5lib](https://pypi.org/project/html5lib/) add `<html>`, `<head>`, & `<body>` elements and I insert a `<style>` element with some personally preferred CSS styling.

It makes for a simple way to write up some Markdown with a terminal & a web browser

**TIP**: In most browsers, keyboard shortcut `Ctrl+Shift+R` will refresh the page and ignore cache

## Installation
```
pip install "git+https://github.com/treatmesubj/python-md-to-html-server"
```

## Usage Example
```
python -m httpmdhtml.server -d . -b 127.0.0.1
```
#### Just Convert Markdown & Write an HTML File
```
python -m httpmdhtml.md_to_html in_file out_file
```

![](<./scrot.png>)
