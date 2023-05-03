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
from bs4 import BeautifulSoup, element


def markdown_to_html(
    MarkdownIt_obj,
    in_file_path,
    out_file_path="tmp.html",
    encode_local_images=False,
    css_file=None,
    live_md_rr=None,
):
    text = open(in_file_path, "r").read()
    tokens = MarkdownIt_obj.parse(text)
    html_text = MarkdownIt_obj.render(text)
    # pretty CSS
    soup = BeautifulSoup(html_text, "html5lib")  # adds <html>, <head>,  <body>
    soup.select_one("head").append(soup.new_tag("meta"))
    soup.select_one("meta").attrs["charset"] = "UTF-8"
    # if lots of images, caching is preferable more often than not
    # soup.select_one('meta').attrs['http-equiv'] = "Cache-control"
    # soup.select_one('meta').attrs['content'] = "no-cache"
    soup.select_one("head").append(soup.new_tag("style"))
    if css_file:
        if css_file == "none":
            css = ""
        else:
            with open(css_file, "r") as f:
                css = f.read()
    else:
        css = """body { background-color: #272822; color: white; font-family: Courier; }
        a[href] { color: #66d9ef; }
        code { color: #ae81ff; background-color: #272b33; border-radius: 6px; }
        table, th, td { border: 1px solid; border-collapse: collapse; padding-left: 4px; padding-right: 4px; }"""
    soup.select_one("style").string = css
    if live_md_rr:
        script = (
            f"setTimeout(function(){{ document.location.reload(); }}, {live_md_rr});"
        )
        soup.select_one("head").append(soup.new_tag("script"))
        soup.select_one("script").string = script
    if encode_local_images:
        img_elems = soup.select("img")
        url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        for img in img_elems:
            if not re.match(url_pattern, img.attrs["src"]):
                img_path = os.path.join(os.path.dirname(in_file_path), img.attrs["src"])
                with open(img_path, "rb") as image_obj:
                    img_bytes = str(base64.b64encode(image_obj.read()), "utf-8")
                img.attrs["src"] = f"data:image/png;base64,{img_bytes}"
    Path(out_file_path).write_text(str(soup))


if __name__ == "__main__":
    MarkdownIt_obj = MarkdownIt("commonmark").enable("table").enable("strikethrough")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--in_file_path",
        "-i",
        required=True,
        help="in-file-path; your existing markdown file",
    )
    parser.add_argument(
        "--out_file_path",
        "-o",
        default="tmp.html",
        help="out-file-path; your HTML file to be created",
    )
    parser.add_argument(
        "--encode_local_images",
        "-e",
        action="store_true",
        help="in HTML, embed base64-encoded data of local images linked to in your markdown; removes dependency on presence of the external local images",
    )
    parser.add_argument(
        "--css_file",
        default=None,
        help='css-file-path whose content will be written to the <style> element. Can be "none"; do not use any css',
    )
    args = parser.parse_args()

    markdown_to_html(
        MarkdownIt_obj=MarkdownIt_obj,
        in_file_path=args.in_file_path,
        out_file_path=args.out_file_path,
        encode_local_images=args.encode_local_images,
        css_file=args.css_file,
    )
