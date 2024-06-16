#!/usr/bin/python3
"""
This module contains a script to convert Markdown files to HTML, including parsing of bold and italic syntax.
"""

import sys
import os
import re
import hashlib

def process_custom_syntax(block):
    """
    Process custom Markdown syntax for bold text, converting to HTML with specific transformations.
    - [[text]]: Convert text to its MD5 hash
    - ((text)): Remove all instances of 'c' (case insensitive) from the text
    Args:
        block (str): The block of text to process.
    Returns:
        str: The processed block of text.
    """
    # MD5 hash conversion
    block = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), block)
    # Remove all 'c' and 'C' characters
    block = re.sub(r'\(\((.*?)\)\)', lambda match: match.group(1).replace('c', '').replace('C', ''), block)
    return block

# Define missing variables
bold_regex = r'\*\*(.*?)\*\*'
italic_regex = r'__(.*?)__'
heading_regex = r'^(#+)\s(.*)$'
unordered_list_item_regex = r'^\*\s(.*)$'
ordered_list_item_regex = r'^\d+\.\s(.*)$'
html_content = []
in_unordered_list = False
in_ordered_list = False

# Define the 'blocks' variable
blocks = []

# Inside the main loop where blocks are processed
for block in blocks:
    block = block.strip()
    # Apply custom syntax transformations
    block = process_custom_syntax(block)
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

html_filename = "output.html"

with open(html_filename, 'w') as html_file:
    html_file.writelines(html_content)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_filename = sys.argv[1]
    if not os.path.exists(md_filename):
        print(f"Missing {md_filename}", file=sys.stderr)
        sys.exit(1)

    html_filename = sys.argv[2]
    sys.exit(0)