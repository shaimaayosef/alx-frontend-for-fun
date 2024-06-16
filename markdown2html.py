#!/usr/bin/python3
"""
This module contains a script to convert Markdown files to HTML.
"""

import sys
import os
import re

def markdown_to_html(md_filename, html_filename):
    """
    Converts a Markdown file to an HTML file, including parsing of heading syntax.

    Args:
        md_filename (str): The name of the Markdown file.
        html_filename (str): The name of the output HTML file.
    """
    with open(md_filename, 'r') as md_file:
        markdown_content = md_file.readlines()

    html_content = []

    # Regular expression to match Markdown headings
    heading_regex = r'^(#{1,6})\s*(.*)'

    for line in markdown_content:
        heading_match = re.match(heading_regex, line)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            html_content.append(f'<h{level}>{content}</h{level}>\n')
        else:
            # For lines that do not match the heading syntax, just add them as is for now.
            html_content.append(line)

    with open(html_filename, 'w') as html_file:
        html_file.writelines(html_content)

if __name__ == "__main__":
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    # Check if the Markdown file exists
    md_filename = sys.argv[1]
    if not os.path.exists(md_filename):
        print(f"Missing {md_filename}", file=sys.stderr)
        sys.exit(1)

    # Call the conversion function
    html_filename = sys.argv[2]
    markdown_to_html(md_filename, html_filename)

    # Exit successfully
    sys.exit(0)