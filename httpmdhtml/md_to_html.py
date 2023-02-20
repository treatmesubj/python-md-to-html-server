"""
just convert a markdown file to HTML and write it out to a file
"""
import os
import sys
from markdown_it import MarkdownIt
# from markdown_it.presets import gfm_like
from bs4 import BeautifulSoup, element


def markdown_to_html(MarkdownIt_obj, in_file_path, out_file_path="tmp.html"):
    text = open(in_file_path, "r").read()
    tokens = MarkdownIt_obj.parse(text)
    html_text = MarkdownIt_obj.render(text)
    # pretty CSS
    soup = BeautifulSoup(html_text, 'html5lib') # adds <html>, <head>,  <body>
    soup.select_one('head').append(soup.new_tag("style"))
    soup.select_one("style").string="body { background-color: #272822; color: white; font-family: Courier; } a[href] { color: #66d9ef; } code { color: #ae81ff; background-color: #272b33; border-radius: 6px; }"
    Path(out_file_path).write_text(str(soup))


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
