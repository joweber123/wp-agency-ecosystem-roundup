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
    "Automattic",
    "Automattic Source Code"
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

    # Check if all posts already have insights
    posts_needing_analysis = [p for p in agency_posts if not p.get('agency_reason')]

    if not posts_needing_analysis:
        print(f"\n✅ All {len(agency_posts)} posts already have AI insights!")
        print(f"   No API call needed - skipping analysis to save credits.\n")
        return

    print(f"\n🤖 Analyzing {len(posts_needing_analysis)} new posts for agency relevance...")
    print(f"   {len(agency_posts) - len(posts_needing_analysis)} posts already have insights")
    print(f"   {len(all_posts) - len(agency_posts)} Industry Insights posts (not analyzed)\n")

    # Prepare only new posts for AI analysis
    posts_for_analysis = []
    for post in posts_needing_analysis:
        posts_for_analysis.append({
            'url': post['link'],
            'title': post['title'],
            'summary': post['summary'],
            'blog': post['blog_name']
        })

    # Create the prompt
    prompt = f"""You are an expert in WordPress agency operations and business development.

Analyze these {len(posts_for_analysis)} blog posts and provide insights for WordPress agencies.

For EACH post, you must respond with a ONE clear sentence (max 15 words) explaining why this post matters to agencies - whether it's for client services, business opportunities, competitive intelligence, technical awareness, or industry trends.

EVERY post must get an insight. Even if a post seems less directly applicable, frame it from an agency perspective (e.g., "Stay informed on platform changes that may affect client sites" or "Industry news to share with clients").

Respond with ONLY valid JSON in this exact format:
{{
  "analyses": [
    {{"url": "post_url", "reason": "One sentence why agencies should know this"}}
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
        insights_added = 0
        for post in all_posts:
            if post['link'] in analysis_lookup:
                analysis = analysis_lookup[post['link']]
                post['agency_relevant'] = True  # All get insights now
                post['agency_reason'] = analysis['reason']
                insights_added += 1
            else:
                # Industry Insights posts - not analyzed
                post['agency_relevant'] = False
                post['agency_reason'] = None

        # Save updated posts
        with open('fetched_posts.json', 'w') as f:
            json.dump(all_posts, f, indent=2)

        print(f"✅ Analysis complete!")
        print(f"   {insights_added} posts received AI insights")
        print(f"   {len(all_posts) - insights_added} Industry Insights posts (not analyzed)")
        print(f"\n💾 Updated fetched_posts.json with AI insights\n")

        # Show some examples
        print("📋 Sample insights:")
        count = 0
        for post in all_posts:
            if post.get('agency_reason') and count < 3:
                print(f"\n   • {post['title'][:60]}...")
                print(f"     {post['agency_reason']}")
                count += 1

    except Exception as e:
        print(f"❌ Error calling OpenAI API: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    analyze_posts()
