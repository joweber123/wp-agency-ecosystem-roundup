#!/usr/bin/env python3
"""
Analyze blog posts for relevance to WordPress agencies using OpenAI.
Adds agency_relevant (bool) and agency_reason (str) fields to posts.
"""

import json
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Automattic/WordPress blogs (exclude Industry Insights)
AUTOMATTIC_BLOGS = [
    "Automattic for Agencies",
    "Pressable",
    "WordPress.com",
    "Jetpack",
    "WooCommerce Developer",
    "WooCommerce",
    "WordPress VIP",
    "WordPress.org News",
    "Automattic"
]

def analyze_posts():
    """Analyze posts for agency relevance using OpenAI."""

    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("   Create a .env file with: OPENAI_API_KEY=your_key_here")
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Load posts
    try:
        with open('fetched_posts.json', 'r') as f:
            all_posts = json.load(f)
    except FileNotFoundError:
        print("❌ Error: fetched_posts.json not found")
        print("   Run fetch_real_posts.py first")
        sys.exit(1)

    # Filter to only Automattic/WordPress posts
    agency_posts = [p for p in all_posts if p['blog_name'] in AUTOMATTIC_BLOGS]

    print(f"\n🤖 Analyzing {len(agency_posts)} Automattic/WordPress posts for agency relevance...")
    print(f"   (Skipping {len(all_posts) - len(agency_posts)} Industry Insights posts)\n")

    # Prepare posts for AI analysis
    posts_for_analysis = []
    for post in agency_posts:
        posts_for_analysis.append({
            'url': post['link'],
            'title': post['title'],
            'summary': post['summary'],
            'blog': post['blog_name']
        })

    # Create the prompt
    prompt = f"""You are an expert in WordPress agency operations and business development.

Analyze these {len(posts_for_analysis)} blog posts and determine which ones would be valuable for WordPress agencies to know about.

For EACH post, you must respond with:
1. is_relevant: true if the post would help agencies serve clients better, win new business, improve operations, or stay competitive. false if it's too technical for most agencies, purely informational, or not actionable.
2. reason: If relevant, provide ONE clear sentence (max 15 words) explaining the specific value for agencies. If not relevant, set to null.

Focus on: client services, business opportunities, competitive advantages, workflow improvements, upselling potential.

Respond with ONLY valid JSON in this exact format:
{{
  "analyses": [
    {{"url": "post_url", "is_relevant": true, "reason": "One sentence why agencies care"}},
    {{"url": "post_url", "is_relevant": false, "reason": null}}
  ]
}}

Posts to analyze:
{json.dumps(posts_for_analysis, indent=2)}"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-5-mini-2025-08-07",  # Latest GPT-5 mini model
            messages=[
                {"role": "system", "content": "You are a WordPress agency business consultant. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            # Note: GPT-5-mini only supports default temperature (1)
            response_format={"type": "json_object"}
        )

        # Parse response
        ai_response = json.loads(response.choices[0].message.content)
        analyses = ai_response.get('analyses', [])

        # Create lookup dict
        analysis_lookup = {a['url']: a for a in analyses}

        # Update posts with AI analysis
        relevant_count = 0
        for post in all_posts:
            if post['link'] in analysis_lookup:
                analysis = analysis_lookup[post['link']]
                post['agency_relevant'] = analysis['is_relevant']
                post['agency_reason'] = analysis['reason']
                if analysis['is_relevant']:
                    relevant_count += 1
            else:
                # Industry Insights posts - not analyzed
                post['agency_relevant'] = False
                post['agency_reason'] = None

        # Save updated posts
        with open('fetched_posts.json', 'w') as f:
            json.dump(all_posts, f, indent=2)

        print(f"✅ Analysis complete!")
        print(f"   {relevant_count} posts marked as agency-relevant")
        print(f"   {len(agency_posts) - relevant_count} posts not relevant for agencies")
        print(f"\n💾 Updated fetched_posts.json with AI insights\n")

        # Show some examples
        print("📋 Sample agency-relevant posts:")
        count = 0
        for post in all_posts:
            if post.get('agency_relevant') and count < 3:
                print(f"\n   ⭐ {post['title'][:60]}...")
                print(f"      Why: {post['agency_reason']}")
                count += 1

    except Exception as e:
        print(f"❌ Error calling OpenAI API: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    analyze_posts()
