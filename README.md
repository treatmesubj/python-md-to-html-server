# Python Markdown-to-HTML Server

It's an extension of the standard Python [http.server module](https://docs.python.org/3/library/http.server.html), but instead of serving a Markdown file, it renders it to a temporary HTML file via [markdown-it-py](https://github.com/executablebooks/markdown-it-py) and serves the HTML file instead.

It's less than 100 lines.

Along with a web browser, it makes for simple Markdown editing.