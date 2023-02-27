"""
just convert a markdown file to HTML and write it out to a file
"""
import os
import sys
import base64
from pathlib import Path
import argparse
import re
from markdown_it import MarkdownIt
# from markdown_it.presets import gfm_like
from bs4 import BeautifulSoup, element


def markdown_to_html(MarkdownIt_obj, in_file_path, out_file_path="tmp.html", encode_local_images=False):
    text = open(in_file_path, "r").read()
    tokens = MarkdownIt_obj.parse(text)
    html_text = MarkdownIt_obj.render(text)
    # pretty CSS
    soup = BeautifulSoup(html_text, 'html5lib') # adds <html>, <head>,  <body>
    soup.select_one('head').append(soup.new_tag("style"))
    soup.select_one("style").string="body { background-color: #272822; color: white; font-family: Courier; } a[href] { color: #66d9ef; } code { color: #ae81ff; background-color: #272b33; border-radius: 6px; }"
    if encode_local_images:
        img_elems = soup.select("img")
        url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        for img in img_elems:
            if not re.match(url_pattern, img.attrs['src']):
                img_path = os.path.join(os.path.dirname(in_file_path), img.attrs['src'])
                with open(img_path, "rb") as image_obj:
                    img_bytes = str(base64.b64encode(image_obj.read()), "utf-8")
                img.attrs['src'] = f"data:image/png;base64,{img_bytes}"
    Path(out_file_path).write_text(str(soup))


if __name__ == "__main__":
    # gfm_like.make(); MarkdownIt_obj = MarkdownIt("gfm-like")
    MarkdownIt_obj = MarkdownIt("commonmark").enable("table").enable("strikethrough")
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file_path', '-i',
                       help='in file path')
    parser.add_argument('--out_file_path', '-o',
                        help='out file path')
    parser.add_argument('--encode_local_images', '-e', action='store_true',
                        help='encode local images')
    args = parser.parse_args()

    markdown_to_html(
        MarkdownIt_obj=MarkdownIt_obj,
        in_file_path=args.in_file_path,
        out_file_path=args.out_file_path,
        encode_local_images=args.encode_local_images
    )
