#!/usr/bin/python3
"""
This module contains a script to convert Markdown files to HTML, including parsing of bold and italic syntax.
"""

import sys
import os
import re
import hashlib

def markdown_to_html(md_filename, html_filename):
    with open(md_filename, 'r') as md_file:
        markdown_content = md_file.read()

    blocks = re.split(r'\n\n+', markdown_content)

    html_content = []
    in_unordered_list = False
    in_ordered_list = False

    # Updated regular expressions
    heading_regex = r'^(#{1,6})\s*(.*)'
    unordered_list_item_regex = r'^\-\s+(.*)'
    ordered_list_item_regex = r'^\*\s+(.*)'
    bold_regex = r'\*\*(.*?)\*\*'
    italic_regex = r'__(.*?)__'
    md5_syntax_regex = r'\[\[(.*?)\]\]'  # New regex for MD5 conversion
    remove_c_syntax_regex = r'\(\((.*?)\)\)'  # New regex for removing 'c's

    for block in blocks:
        # Check for MD5 conversion syntax
        if re.match(md5_syntax_regex, block):
            content = re.findall(md5_syntax_regex, block)[0]
            md5_hash = hashlib.md5(content.encode()).hexdigest()
            html_content.append(md5_hash)
            continue

        # Check for removing 'c's syntax
        if re.match(remove_c_syntax_regex, block):
            content = re.findall(remove_c_syntax_regex, block)[0]
            content_without_c = content.replace('c', '').replace('C', '')
            html_content.append(content_without_c)
            continue

        # Existing parsing logic...

    # Convert the list of HTML content blocks to a single string
    final_html_content = '\n'.join(html_content)
    with open(html_filename, 'w') as html_file:
        html_file.write(final_html_content)