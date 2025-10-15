#!/usr/bin/env python3
"""
Generate a preview HTML file from sample data for styling experimentation.
This allows you to test the digest layout locally before implementing the full RSS automation.
"""

import json
from datetime import datetime
from jinja2 import Template

def generate_preview():
    # Load sample data
    with open('sample_data.json', 'r') as f:
        posts = json.load(f)

    # Load template
    with open('template.html', 'r') as f:
        template_content = f.read()

    # Create Jinja2 template
    template = Template(template_content)

    # Prepare template variables
    current_date = datetime.now().strftime("%B %d, %Y")
    post_count = len(posts)

    # Render the template
    html_output = template.render(
        posts=posts,
        current_date=current_date,
        post_count=post_count
    )

    # Write to preview.html
    with open('preview.html', 'w') as f:
        f.write(html_output)

    print(f"✓ Generated preview.html with {post_count} sample posts")
    print("  Open preview.html in your browser to see the styled digest")

if __name__ == "__main__":
    generate_preview()
