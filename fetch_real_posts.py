#!/usr/bin/env python3
"""
Fetch real RSS posts from Automattic family blogs.
This lets you preview the digest with actual current content.
"""

import json
import feedparser
import ssl
from datetime import datetime, timedelta
from jinja2 import Template
from bs4 import BeautifulSoup

# Handle SSL certificate verification issues
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def extract_image_url(entry):
    """
    Extract image URL from RSS entry.
    Priority: media_content -> media_thumbnail -> first img in content/summary
    """
    # Priority 1: media_content
    if hasattr(entry, 'media_content') and entry.media_content:
        return entry.media_content[0].get('url')

    # Priority 2: media_thumbnail
    if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
        return entry.media_thumbnail[0].get('url')

    # Priority 3: Parse HTML content for first image
    html_content = ''
    if hasattr(entry, 'content') and entry.content:
        html_content = entry.content[0].value
    elif hasattr(entry, 'summary'):
        html_content = entry.summary

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img.get('src')

    # Fallback: placeholder
    return "https://placehold.co/800x400/cccccc/666666?text=No+Image"

def clean_summary(entry):
    """Extract clean text from entry summary/description."""
    html_content = ''
    if hasattr(entry, 'summary'):
        html_content = entry.summary
    elif hasattr(entry, 'description'):
        html_content = entry.description

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        # Limit to ~200 characters
        if len(text) > 200:
            text = text[:200].rsplit(' ', 1)[0] + '...'
        return text

    return "No summary available."

def fetch_posts(days_back=30):
    """Fetch posts from all feeds published within the last N days."""
    # Load feed URLs
    with open('feed_urls.json', 'r') as f:
        config = json.load(f)

    cutoff_date = datetime.now() - timedelta(days=days_back)
    all_posts = []

    print(f"Fetching posts from the last {days_back} days (~1 month)...\n")

    for feed_config in config['feeds']:
        blog_name = feed_config['name']
        feed_url = feed_config['url']

        print(f"Fetching: {blog_name}")
        print(f"  URL: {feed_url}")

        try:
            feed = feedparser.parse(feed_url)

            if feed.bozo and not feed.entries:
                print(f"  ⚠ Warning: Failed to parse feed")
                continue

            new_posts = 0
            for entry in feed.entries:
                # Parse publish date
                pub_date = None
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed'):
                    pub_date = datetime(*entry.updated_parsed[:6])

                # Filter by date
                if pub_date and pub_date >= cutoff_date:
                    post = {
                        'title': entry.get('title', 'No Title'),
                        'link': entry.get('link', '#'),
                        'pubDate': pub_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        'blog_name': blog_name,
                        'image_url': extract_image_url(entry),
                        'summary': clean_summary(entry),
                        '_sort_date': pub_date  # For sorting
                    }
                    all_posts.append(post)
                    new_posts += 1

            print(f"  ✓ Found {new_posts} new posts\n")

        except Exception as e:
            print(f"  ✗ Error: {str(e)}\n")
            continue

    # Sort by date (newest first)
    all_posts.sort(key=lambda x: x['_sort_date'], reverse=True)

    # Remove the sort helper field
    for post in all_posts:
        del post['_sort_date']

    return all_posts

def generate_html(posts):
    """Generate HTML from posts using the template."""
    # Load feed configuration to get all blog names
    with open('feed_urls.json', 'r') as f:
        config = json.load(f)

    # Group posts by blog name, maintaining order from feed_urls.json
    posts_by_blog = {}
    for feed_config in config['feeds']:
        blog_name = feed_config['name']
        blog_posts = [p for p in posts if p['blog_name'] == blog_name]
        posts_by_blog[blog_name] = blog_posts

    # Load template
    with open('template.html', 'r') as f:
        template_content = f.read()

    template = Template(template_content)

    # Render
    html_output = template.render(
        posts_by_blog=posts_by_blog,
        current_date=datetime.now().strftime("%B %d, %Y"),
        post_count=len(posts)
    )

    # Write to preview.html
    with open('preview.html', 'w') as f:
        f.write(html_output)

def main():
    print("=" * 60)
    print("Automattic RSS Digest - Real Feed Fetcher")
    print("=" * 60 + "\n")

    # Fetch posts
    posts = fetch_posts(days_back=30)

    print("=" * 60)
    print(f"Total: {len(posts)} posts found from the last 30 days")
    print("=" * 60 + "\n")

    if posts:
        # Generate HTML
        generate_html(posts)
        print("✓ Generated preview.html with real blog posts")
        print("  Open preview.html in your browser to see the digest\n")

        # Also save as JSON for inspection
        with open('fetched_posts.json', 'w') as f:
            json.dump(posts, f, indent=2)
        print("✓ Saved post data to fetched_posts.json")
    else:
        print("⚠ No posts found. The blogs might not have published recently.")
        print("  You can adjust the days_back parameter to look further back.")

if __name__ == "__main__":
    main()
