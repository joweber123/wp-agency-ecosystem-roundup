#!/usr/bin/env python3
"""Debug RSS feed fetching."""

import feedparser

# Test one feed
url = "https://wordpress.com/blog/feed/"
print(f"Testing: {url}\n")

feed = feedparser.parse(url)

print(f"Bozo: {feed.bozo}")
if feed.bozo:
    print(f"Bozo Exception: {feed.bozo_exception}")

print(f"Number of entries: {len(feed.entries)}")
print(f"Feed version: {feed.version if hasattr(feed, 'version') else 'Unknown'}")

if feed.entries:
    print(f"\nFirst entry:")
    entry = feed.entries[0]
    print(f"  Title: {entry.get('title', 'N/A')}")
    print(f"  Link: {entry.get('link', 'N/A')}")
    print(f"  Published: {entry.get('published', 'N/A')}")
    print(f"\nAll entry keys:")
    print(f"  {list(entry.keys())}")
