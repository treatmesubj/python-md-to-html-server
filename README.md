# Python Markdown-to-HTML Server

It's the standard Python [http.server module](https://docs.python.org/3/library/http.server.html) but via [markdown-it-py](https://github.com/executablebooks/markdown-it-py), requested Markdown files are rendered and served as HTML

The `http.server` module's `SimpleHTTPRequestHandler` class is inherited by a new class with its `do_GET` method overridden

It makes for a simple way to write up some Markdown with a terminal & a web browser

**TIP**: In most browsers, keyboard shortcut `Ctrl+Shift+R` will refresh the page and ignore cache

![](<./scrot.png>)
