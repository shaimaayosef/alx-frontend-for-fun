#!/usr/bin/python3
"""
This module contains a script to convert Markdown files to HTML.
"""

import sys
import os

def markdown_to_html(md_filename, html_filename):
    """
    Converts a Markdown file to an HTML file.

    Args:
        md_filename (str): The name of the Markdown file.
        html_filename (str): The name of the output HTML file.
    """
    # This function is a placeholder for the actual conversion logic.
    pass

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

    # Placeholder for conversion logic
    html_filename = sys.argv[2]
    markdown_to_html(md_filename, html_filename)

    # Exit successfully
    sys.exit(0)