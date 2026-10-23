# WP Agency Ecosystem Roundup

**A daily-updated digest of WordPress ecosystem news, curated for agencies.**

## What It Is

An automated news aggregator that collects posts from 13 WordPress-related blogs (Automattic family + industry leaders) and displays them in a clean, browsable format.

## How It Works

> Since 2026-10-24 the AI "why agencies should care" step is off, so the workflow holds no API keys. Posts that already had an insight keep it; new posts show title and summary only. `analyze_agency_relevance.py` is kept for reference (re-enabling it needs an OpenAI key in repo secrets).

1. **Daily at 9 AM UTC**: GitHub Actions fetches the latest posts from all RSS feeds (last 30 days)
2. **Auto-Deploy**: Generates and publishes the updated digest to GitHub Pages

## What It Does

- **Aggregates** posts from WordPress.com, Pressable, Jetpack, WooCommerce, WordPress VIP, and more
- **Analyzes** each post with AI to surface agency-relevant insights
- **Displays** posts in a horizontal-scrolling, brand-colored interface
- **Updates** automatically every day—no manual work required

## Live Site

👉 **https://joweber123.github.io/wp-agency-ecosystem-roundup/**

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Fetch posts and generate digest
python fetch_real_posts.py
python generate_woocommerce_style.py

# Open preview_woocommerce_style.html in browser
```

## Tech Stack

- **Python**: RSS parsing, AI analysis, HTML generation
- **GPT-5-mini**: Agency relevance insights (one API call per day)
- **GitHub Actions**: Daily automation
- **GitHub Pages**: Hosting
