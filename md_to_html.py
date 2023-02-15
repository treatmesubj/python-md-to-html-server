"""
just convert a markdown file to HTML and write it out to a file
"""
import os
import sys
from markdown_it import MarkdownIt
# from markdown_it.presets import gfm_like
from bs4 import BeautifulSoup, element
from md_to_html_server import markdown_to_html


if __name__ == "__main__":
    # gfm_like.make(); MarkdownIt_obj = MarkdownIt("gfm-like")
    MarkdownIt_obj = MarkdownIt("commonmark").enable("table").enable("strikethrough")
    try:
        in_file_path = sys.argv[1]
        out_file_path = sys.argv[2]
    except IndexError as e:
        print("\nusage: python md_to_html.py in_file.md out_file.html")
        raise e
    markdown_to_html(MarkdownIt_obj, in_file_path, out_file_path)
