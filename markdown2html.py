#!/usr/bin/python3
"""
This module contains a script to convert Markdown files to HTML, including parsing of bold and italic syntax.
"""

import sys
import os
import re

def markdown_to_html(md_filename, html_filename):
    """
    Converts a Markdown file to an HTML file, including parsing of heading, unordered, ordered list syntax, paragraphs, bold, and italic text.

    Args:
        md_filename (str): The name of the Markdown file.
        html_filename (str): The name of the output HTML file.
    """
    with open(md_filename, 'r') as md_file:
        markdown_content = md_file.read()

    # Split content by two or more newlines to identify paragraphs and other blocks
    blocks = re.split(r'\n\n+', markdown_content)

    html_content = []
    in_unordered_list = False  # Track whether we are currently processing an unordered list
    in_ordered_list = False  # Track whether we are currently processing an ordered list

    # Regular expression to match Markdown headings
    heading_regex = r'^(#{1,6})\s*(.*)'
    # Regular expression to match Markdown unordered list items
    unordered_list_item_regex = r'^\-\s+(.*)'
    # Regular expression to match Markdown ordered list items
    ordered_list_item_regex = r'^\*\s+(.*)'
    # Regular expressions for bold and italic syntax
    bold_regex = r'\*\*(.*?)\*\*'
    italic_regex = r'__(.*?)__'

    for block in blocks:
        block = block.strip()
        # Apply bold and italic transformations
        block = re.sub(bold_regex, r'<b>\1</b>', block)
        block = re.sub(italic_regex, r'<em>\1</em>', block)

        if re.match(heading_regex, block):
            level = len(re.match(heading_regex, block).group(1))
            content = re.match(heading_regex, block).group(2)
            html_content.append(f'<h{level}>{content}</h{level}>\n')
        elif re.match(unordered_list_item_regex, block):
            if not in_unordered_list:
                html_content.append('<ul>\n')
                in_unordered_list = True
            for item in block.split('\n'):
                content = re.match(unordered_list_item_regex, item).group(1)
                html_content.append(f'    <li>{content}</li>\n')
            html_content.append('</ul>\n')
            in_unordered_list = False
        elif re.match(ordered_list_item_regex, block):
            if not in_ordered_list:
                html_content.append('<ol>\n')
                in_ordered_list = True
            for item in block.split('\n'):
                content = re.match(ordered_list_item_regex, item).group(1)
                html_content.append(f'    <li>{content}</li>\n')
            html_content.append('</ol>\n')
            in_ordered_list = False
        else:  # Treat as a paragraph
            # Replace single newlines within a paragraph with <br />
            paragraph = block.replace('\n', '<br />\n')
            html_content.append(f'<p>\n    {paragraph}\n</p>\n')

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