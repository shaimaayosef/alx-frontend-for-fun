#!/usr/bin/python3
"""
This module contains a script to convert Markdown files to HTML.
"""

import sys
import os
import re

def markdown_to_html(md_filename, html_filename):
    """
    Converts a Markdown file to an HTML file, including parsing of heading, unordered, and ordered list syntax.

    Args:
        md_filename (str): The name of the Markdown file.
        html_filename (str): The name of the output HTML file.
    """
    with open(md_filename, 'r') as md_file:
        markdown_content = md_file.readlines()

    html_content = []
    in_unordered_list = False  # Track whether we are currently processing an unordered list
    in_ordered_list = False  # Track whether we are currently processing an ordered list

    # Regular expression to match Markdown headings
    heading_regex = r'^(#{1,6})\s*(.*)'
    # Regular expression to match Markdown unordered list items
    unordered_list_item_regex = r'^\-\s+(.*)'
    # Regular expression to match Markdown ordered list items
    ordered_list_item_regex = r'^\*\s+(.*)'

    for line in markdown_content:
        heading_match = re.match(heading_regex, line)
        unordered_list_item_match = re.match(unordered_list_item_regex, line)
        ordered_list_item_match = re.match(ordered_list_item_regex, line)

        if heading_match:
            if in_unordered_list:  # Close the unordered list before starting a new heading
                html_content.append('</ul>\n')
                in_unordered_list = False
            if in_ordered_list:  # Close the ordered list before starting a new heading
                html_content.append('</ol>\n')
                in_ordered_list = False
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            html_content.append(f'<h{level}>{content}</h{level}>\n')
        elif unordered_list_item_match:
            if in_ordered_list:  # Close the ordered list if starting an unordered list
                html_content.append('</ol>\n')
                in_ordered_list = False
            if not in_unordered_list:  # Start a new unordered list if not already in one
                html_content.append('<ul>\n')
                in_unordered_list = True
            content = unordered_list_item_match.group(1)
            html_content.append(f'    <li>{content}</li>\n')
        elif ordered_list_item_match:
            if in_unordered_list:  # Close the unordered list if starting an ordered list
                html_content.append('</ul>\n')
                in_unordered_list = False
            if not in_ordered_list:  # Start a new ordered list if not already in one
                html_content.append('<ol>\n')
                in_ordered_list = True
            content = ordered_list_item_match.group(1)
            html_content.append(f'    <li>{content}</li>\n')
        else:
            if in_unordered_list:  # Close the unordered list if the current line is not a list item
                html_content.append('</ul>\n')
                in_unordered_list = False
            if in_ordered_list:  # Close the ordered list if the current line is not a list item
                html_content.append('</ol>\n')
                in_ordered_list = False
            # For lines that do not match the heading or list syntax, just add them as is for now.

    if in_unordered_list:  # Ensure the unordered list is closed if the file ends while still in a list
        html_content.append('</ul>\n')
    if in_ordered_list:  # Ensure the ordered list is closed if the file ends while still in a list
        html_content.append('</ol>\n')

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