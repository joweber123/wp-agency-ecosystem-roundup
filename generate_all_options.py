#!/usr/bin/env python3
"""
Generate preview HTML files for all 6 layout options.
"""

import json
import ssl
from datetime import datetime
from jinja2 import Template

# Handle SSL certificate verification issues
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def generate_option_preview(option_number, template_file, output_file):
    """Generate a single option preview."""
    # Load feed configuration to get all blog names
    with open('feed_urls.json', 'r') as f:
        config = json.load(f)

    # Load fetched posts
    with open('fetched_posts.json', 'r') as f:
        posts = json.load(f)

    # Group posts by blog name, maintaining order from feed_urls.json
    posts_by_blog = {}
    for feed_config in config['feeds']:
        blog_name = feed_config['name']
        blog_posts = [p for p in posts if p['blog_name'] == blog_name]
        posts_by_blog[blog_name] = blog_posts

    # Load template
    with open(template_file, 'r') as f:
        template_content = f.read()

    template = Template(template_content)

    # Render
    html_output = template.render(
        posts_by_blog=posts_by_blog,
        current_date=datetime.now().strftime("%B %d, %Y"),
        post_count=len(posts)
    )

    # Write output
    with open(output_file, 'w') as f:
        f.write(html_output)

    print(f"✓ Generated {output_file}")

def main():
    print("=" * 60)
    print("Generating All Layout Options")
    print("=" * 60 + "\n")

    options = [
        (1, 'template_option1.html', 'preview_option1.html', 'Horizontal Scrolling Cards'),
        (2, 'template_option2.html', 'preview_option2.html', 'Collapsible Accordion'),
        (3, 'template_option3.html', 'preview_option3.html', 'Compact Table/List'),
        (4, 'template_option4.html', 'preview_option4.html', 'Masonry Grid'),
        (5, 'template_option5.html', 'preview_option5.html', 'Tabs'),
        (6, 'template_option6.html', 'preview_option6.html', 'Compact Multi-Column'),
    ]

    for num, template, output, name in options:
        print(f"Option {num}: {name}")
        generate_option_preview(num, template, output)
        print()

    print("=" * 60)
    print("All options generated!")
    print("=" * 60)
    print("\nOpen these files to compare layouts:")
    for num, _, output, name in options:
        print(f"  • {output} - {name}")

if __name__ == "__main__":
    main()
