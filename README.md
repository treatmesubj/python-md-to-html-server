# Python Markdown-to-HTML Server

It's the standard Python [http.server module](https://docs.python.org/3/library/http.server.html), but the `SimpleHTTPRequestHandler` class is inherited by a new class with its `do_GET` method overridden to render a requested Markdown file to a temporary HTML file via [markdown-it-py](https://github.com/executablebooks/markdown-it-py), which is served instead.

It's a simple way to write up some Markdown with a terminal & a web browser.

<img src="./scrot.png" height="400"/>
