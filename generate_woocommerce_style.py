#!/usr/bin/env python3
"""
Generate WooCommerce-style preview with horizontal scrolling sections.
"""

import json
import ssl
from datetime import datetime
from jinja2 import Template

# Handle SSL certificate verification issues
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def main():
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
    with open('template_woocommerce_style.html', 'r') as f:
        template_content = f.read()

    template = Template(template_content)

    # Render
    html_output = template.render(
        posts_by_blog=posts_by_blog,
        current_date=datetime.now().strftime("%B %d, %Y"),
        post_count=len(posts)
    )

    # Write to preview
    with open('preview_woocommerce_style.html', 'w') as f:
        f.write(html_output)

    print("✓ Generated preview_woocommerce_style.html")
    print("  Open preview_woocommerce_style.html in your browser to see the WooCommerce-style layout")

if __name__ == "__main__":
    main()
