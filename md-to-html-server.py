import copy
import datetime
import email.utils
import html
import http.client
import io
import mimetypes
import os
import posixpath
import select
import shutil
import socket # For gethostbyaddr()
import socketserver
import sys
import time
import urllib.parse
import contextlib
import argparse
from functools import partial
from pathlib import Path

from http.server import test as http_server_test  # not in http.server.__all__
from http import HTTPStatus
from http.server import *

from markdown_it import MarkdownIt
# from markdown_it.presets import gfm_like

from bs4 import BeautifulSoup, element


def markdown_to_html(MarkdownIt_obj, file_path):
    text = open(file_path, "r").read()
    tokens = MarkdownIt_obj.parse(text)
    html_text = MarkdownIt_obj.render(text)
    # pretty CSS
    soup = BeautifulSoup(html_text, 'html5lib') # adds <html> & <body>
    soup.select_one('head').append(soup.new_tag("style"))
    soup.select_one("style").string="body { background-color: #272822; color: white; } a[href] { color: #66d9ef; }"
    Path("./tmp.html").write_text(str(soup))


class md_to_html_SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, MarkdownIt_obj=None, **kwargs):
        self.MarkdownIt_obj = MarkdownIt_obj
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Serve a GET request."""
        if self.path.endswith(".md") and os.path.exists(f".{self.path}"):  # check for markdown file request
            markdown_to_html(self.MarkdownIt_obj, f".{self.path}")  # render temp html file
            self.path = "/tmp.html"
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
        try:
            os.remove("./tmp.html")  # remove temp html file
        except FileNotFoundError:
            pass


if __name__ == "__main__":

    # gfm_like.make(); MarkdownIt_obj = MarkdownIt("gfm-like")
    MarkdownIt_obj = MarkdownIt("commonmark").enable("table").enable("strikethrough")

    parser = argparse.ArgumentParser()
    parser.add_argument('--cgi', action='store_true',
                       help='Run as CGI Server')
    parser.add_argument('--bind', '-b', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                        '[default:current directory]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    args = parser.parse_args()
    if args.cgi:
        handler_class = CGIHTTPRequestHandler
    else:
        handler_class = partial(md_to_html_SimpleHTTPRequestHandler,
                                directory=args.directory,
                                MarkdownIt_obj=MarkdownIt_obj)

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    http_server_test(
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
    )
