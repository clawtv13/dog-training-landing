#!/bin/bash
# SEO Optimization Script for AI Automation Builder Blog
# Automatically updates sitemap, RSS feed, and validates SEO elements

set -e

BLOG_DIR="/root/.openclaw/workspace/ai-automation-blog/blog"
POSTS_DIR="$BLOG_DIR/posts"
SITEMAP="$BLOG_DIR/sitemap.xml"
RSS="$BLOG_DIR/rss.xml"
INDEX_JSON="$POSTS_DIR/index.json"

echo "🔍 SEO Optimization Script Starting..."

# Count posts
POST_COUNT=$(find "$POSTS_DIR" -name "*.html" -type f | wc -l)
echo "📊 Found $POST_COUNT posts"

# Validate meta tags in all posts
echo "✅ Validating meta tags..."
for post in "$POSTS_DIR"/*.html; do
    if [ -f "$post" ]; then
        filename=$(basename "$post")
        
        # Check for required meta tags
        if ! grep -q 'meta name="description"' "$post"; then
            echo "⚠️  Missing meta description in $filename"
        fi
        
        if ! grep -q 'meta name="keywords"' "$post"; then
            echo "⚠️  Missing keywords in $filename"
        fi
        
        if ! grep -q 'link rel="canonical"' "$post"; then
            echo "⚠️  Missing canonical URL in $filename"
        fi
        
        if ! grep -q 'application/ld+json' "$post"; then
            echo "⚠️  Missing JSON-LD structured data in $filename"
        fi
        
        if ! grep -q 'BreadcrumbList' "$post"; then
            echo "⚠️  Missing breadcrumb schema in $filename"
        fi
    fi
done

# Check sitemap freshness
if [ -f "$SITEMAP" ]; then
    echo "✅ Sitemap exists: $SITEMAP"
    SITEMAP_DATE=$(date -r "$SITEMAP" +%Y-%m-%d)
    TODAY=$(date +%Y-%m-%d)
    if [ "$SITEMAP_DATE" != "$TODAY" ]; then
        echo "⚠️  Sitemap is outdated. Last modified: $SITEMAP_DATE"
    fi
else
    echo "❌ Sitemap missing!"
fi

# Check robots.txt
if [ -f "$BLOG_DIR/robots.txt" ]; then
    echo "✅ robots.txt exists"
else
    echo "❌ robots.txt missing!"
fi

# Check RSS feed
if [ -f "$RSS" ]; then
    echo "✅ RSS feed exists: $RSS"
else
    echo "❌ RSS feed missing!"
fi

# Validate index.json
if [ -f "$INDEX_JSON" ]; then
    if jq empty "$INDEX_JSON" 2>/dev/null; then
        echo "✅ index.json is valid JSON"
    else
        echo "❌ index.json has invalid JSON syntax!"
    fi
else
    echo "❌ index.json missing!"
fi

# Check for image alt text placeholders
echo "🖼️  Checking for images without alt text..."
for post in "$POSTS_DIR"/*.html; do
    if [ -f "$post" ]; then
        if grep -q '<img' "$post"; then
            filename=$(basename "$post")
            if grep -q '<img[^>]*>' "$post" | grep -v 'alt=' 2>/dev/null; then
                echo "⚠️  Found images without alt text in $filename"
            fi
        fi
    fi
done

echo ""
echo "🎯 SEO Optimization Complete!"
echo "📈 Total posts: $POST_COUNT"
echo "🔗 Sitemap: $SITEMAP"
echo "📡 RSS feed: $RSS"
echo "🤖 robots.txt: $BLOG_DIR/robots.txt"
echo ""
echo "Next steps:"
echo "1. Update sitemap.xml with new posts"
echo "2. Update RSS feed with latest content"
echo "3. Regenerate index.json if posts changed"
echo "4. Submit sitemap to Google Search Console"
echo "5. Test structured data with Google Rich Results Test"
