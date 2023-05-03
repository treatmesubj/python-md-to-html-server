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
import socket  # For gethostbyaddr()
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

from bs4 import BeautifulSoup, element

from httpmdhtml import md_to_html


class md_to_html_SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(
        self, *args, MarkdownIt_obj=None, css_file=None, live_md_rr=False, **kwargs
    ):
        self.MarkdownIt_obj = MarkdownIt_obj
        self.css_file = css_file
        self.live_md_rr = live_md_rr
        super().__init__(*args, **kwargs)

    def do_GET(self, rm_temp_html=False):
        """Serve a GET request."""
        self.url_dc_path = urllib.parse.unquote(
            urllib.parse.urlsplit(self.path).path
        )  # url decode, strip query params for file check
        if (
            self.MarkdownIt_obj
            and self.url_dc_path.endswith(".md")
            and os.path.exists(os.path.join(self.directory, f".{self.url_dc_path}"))
        ):  # check for markdown file request
            in_file_path = os.path.join(self.directory, f".{self.url_dc_path}")
            out_file_path = os.path.join(
                self.directory, f".{os.path.splitext(self.url_dc_path)[0]}.html"
            )
            md_to_html.markdown_to_html(
                self.MarkdownIt_obj,
                in_file_path=in_file_path,
                out_file_path=out_file_path,
                css_file=self.css_file,
                live_md_rr=self.live_md_rr,
            )
            self.path = f"{os.path.splitext(self.path)[0]}.html"
            rm_temp_html = True
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
        if rm_temp_html:
            os.remove(out_file_path)  # remove temp html file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cgi", action="store_true", help="Run as CGI Server")
    parser.add_argument(
        "--bind",
        "-b",
        metavar="ADDRESS",
        help="Specify alternate bind address " "[default: all interfaces]",
    )
    parser.add_argument(
        "--directory",
        "-d",
        default=os.getcwd(),
        help="Specify alternative directory " "[default:current directory]",
    )
    parser.add_argument(
        "--css_file",
        default=None,
        help='css-file-path whose content will be written to the <style> element. Can be "none"; do not use any css',
    )
    parser.add_argument(
        "--live_md_rr",
        "-l",
        action="store",
        type=int,
        default=None,
        help="Continuous refresh rate of MD page, in ms. Respects cache",
    )
    parser.add_argument(
        "port",
        action="store",
        default=8000,
        type=int,
        nargs="?",
        help="Specify alternate port [default: 8000]",
    )
    args = parser.parse_args()
    if args.cgi:
        handler_class = CGIHTTPRequestHandler
    else:
        MarkdownIt_obj = (
            MarkdownIt("commonmark").enable("table").enable("strikethrough")
        )
        if args.css_file and all(
            (args.css_file != "none", not os.path.isfile(args.css_file))
        ):
            raise FileNotFoundError(
                f"looks like the given `css_file` argument's value - {args.css_file} - cannot be found"
            )
        handler_class = partial(
            md_to_html_SimpleHTTPRequestHandler,
            directory=args.directory,
            MarkdownIt_obj=MarkdownIt_obj,
            css_file=args.css_file,
            live_md_rr=args.live_md_rr,
        )

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    http_server_test(
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
    )
