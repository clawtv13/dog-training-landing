#!/usr/bin/env python3
"""
Performance Tracker - Calculate quality metrics for blog posts

Features:
- Readability scoring (Flesch-Kincaid, 0-100)
- SEO scoring (meta, keywords, structure, links, images)
- Topic clustering (TF-IDF + k-means)
- Updates analytics.db with scores

Run daily to score all unscored posts.
"""

import os
import re
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from collections import Counter

# NLP & ML libraries
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from bs4 import BeautifulSoup

# ============================================================================
# CONFIGURATION
# ============================================================================

WORKSPACE = Path(__file__).parent.parent
POSTS_DIR = WORKSPACE / "blog" / "posts"
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"
DB_PATH = DATA_DIR / "analytics.db"
LOG_FILE = LOGS_DIR / "performance-tracker.log"

# Create directories
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Topic cluster labels
CLUSTER_LABELS = {
    0: "AI Tools",
    1: "Ethics",
    2: "Technical",
    3: "Business",
    4: "Random"
}

# ============================================================================
# HTML PARSING
# ============================================================================

def extract_text_from_html(html_path):
    """Extract clean text from HTML post"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def extract_metadata(html_path):
    """Extract SEO metadata from HTML"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    metadata = {
        'meta_description': False,
        'h1_count': 0,
        'h2_count': 0,
        'internal_links': 0,
        'images_with_alt': 0,
        'total_images': 0,
        'word_count': 0
    }
    
    # Check meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content') and '{{EXCERPT}}' not in meta_desc.get('content'):
        metadata['meta_description'] = True
    
    # Count headers
    metadata['h1_count'] = len(soup.find_all('h1'))
    metadata['h2_count'] = len(soup.find_all('h2'))
    
    # Count internal links
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'workless.build' in href or href.startswith('/') or href.startswith('./'):
            metadata['internal_links'] += 1
    
    # Count images and alt tags
    images = soup.find_all('img')
    metadata['total_images'] = len(images)
    metadata['images_with_alt'] = sum(1 for img in images if img.get('alt'))
    
    # Word count from article content
    article = soup.find('article') or soup.find('main') or soup.find('body')
    if article:
        text = article.get_text()
        metadata['word_count'] = len(text.split())
    
    return metadata

# ============================================================================
# SCORING FUNCTIONS
# ============================================================================

def calculate_readability_score(text):
    """
    Calculate readability score (0-100, higher = easier to read)
    Uses Flesch Reading Ease
    """
    if not text or len(text.split()) < 100:
        return 0.0
    
    try:
        # Flesch Reading Ease (0-100, 100 = easiest)
        score = textstat.flesch_reading_ease(text)
        
        # Clamp to 0-100 range
        score = max(0, min(100, score))
        
        return round(score, 2)
    except Exception as e:
        logger.warning(f"Readability calculation error: {e}")
        return 0.0

def calculate_seo_score(metadata, text):
    """
    Calculate SEO score (0-100)
    Checks: meta description, keyword density, structure, links, images
    """
    score = 0
    max_score = 100
    
    # Meta description (20 points)
    if metadata['meta_description']:
        score += 20
    
    # Header structure (20 points)
    # Should have exactly 1 H1 and multiple H2s
    if metadata['h1_count'] == 1:
        score += 10
    if metadata['h2_count'] >= 3:
        score += 10
    
    # Internal links (20 points)
    # At least 2-3 internal links
    if metadata['internal_links'] >= 2:
        score += 20
    elif metadata['internal_links'] >= 1:
        score += 10
    
    # Image alt tags (20 points)
    if metadata['total_images'] > 0:
        alt_ratio = metadata['images_with_alt'] / metadata['total_images']
        score += int(20 * alt_ratio)
    else:
        score += 20  # No images is fine
    
    # Keyword density (20 points)
    # Check for 2-3% density of AI-related terms
    if text and metadata['word_count'] > 0:
        keywords = ['ai', 'automation', 'agent', 'llm', 'tool', 'build', 'productivity']
        text_lower = text.lower()
        
        keyword_count = sum(text_lower.count(kw) for kw in keywords)
        density = (keyword_count / metadata['word_count']) * 100
        
        # Optimal: 2-3% density
        if 2.0 <= density <= 3.0:
            score += 20
        elif 1.5 <= density <= 4.0:
            score += 15
        elif 1.0 <= density <= 5.0:
            score += 10
        elif density > 0:
            score += 5
    
    return min(score, max_score)

# ============================================================================
# TOPIC CLUSTERING
# ============================================================================

def cluster_topics(texts, n_clusters=5):
    """
    Cluster posts into topics using TF-IDF + k-means
    Returns cluster assignments for each text
    """
    if len(texts) < n_clusters:
        # Not enough data, return default clusters
        return [4] * len(texts)  # "Random"
    
    try:
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )
        
        X = vectorizer.fit_transform(texts)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X)
        
        # Get top terms per cluster for auto-labeling
        order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()
        
        cluster_keywords = {}
        for i in range(n_clusters):
            top_terms = [terms[ind] for ind in order_centroids[i, :5]]
            cluster_keywords[i] = top_terms
        
        # Smart label mapping based on keywords
        label_mapping = smart_label_clusters(cluster_keywords)
        
        # Map clusters to labels
        labeled_clusters = [label_mapping.get(c, 4) for c in clusters]
        
        return labeled_clusters
        
    except Exception as e:
        logger.warning(f"Clustering error: {e}")
        return [4] * len(texts)  # Default to "Random"

def smart_label_clusters(cluster_keywords):
    """
    Map clusters to semantic labels based on keywords
    """
    mapping = {}
    
    tool_keywords = {'tool', 'api', 'platform', 'software', 'service', 'app'}
    ethics_keywords = {'ethics', 'privacy', 'bias', 'safety', 'risk', 'responsible'}
    technical_keywords = {'code', 'technical', 'implementation', 'architecture', 'system', 'algorithm'}
    business_keywords = {'business', 'revenue', 'pricing', 'customer', 'market', 'growth', 'founder'}
    
    for cluster_id, keywords in cluster_keywords.items():
        keyword_set = set(keywords)
        
        # Score each category
        tool_score = len(keyword_set & tool_keywords)
        ethics_score = len(keyword_set & ethics_keywords)
        technical_score = len(keyword_set & technical_keywords)
        business_score = len(keyword_set & business_keywords)
        
        scores = {
            0: tool_score,      # AI Tools
            1: ethics_score,    # Ethics
            2: technical_score, # Technical
            3: business_score,  # Business
            4: 0                # Random (fallback)
        }
        
        # Assign to highest scoring category
        best_label = max(scores, key=scores.get)
        
        # If no clear winner, mark as Random
        if scores[best_label] == 0:
            best_label = 4
        
        mapping[cluster_id] = best_label
    
    return mapping

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def get_unscored_posts():
    """Get posts from analytics.db that have NULL scores"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, slug
        FROM posts
        WHERE readability_score IS NULL
           OR seo_score IS NULL
           OR quality_score IS NULL
           OR topic_cluster IS NULL
    """)
    
    unscored = cursor.fetchall()
    conn.close()
    
    return unscored

def update_post_scores(slug, readability, seo, quality, topic):
    """Update scores in analytics.db"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE posts
        SET readability_score = ?,
            seo_score = ?,
            quality_score = ?,
            topic_cluster = ?
        WHERE slug = ?
    """, (readability, seo, quality, topic, slug))
    
    conn.commit()
    conn.close()

def insert_post_if_missing(slug, published_date, word_count):
    """Insert post into analytics.db if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO posts (slug, published_date, word_count, prompt_version)
            VALUES (?, ?, ?, 'v1')
        """, (slug, published_date, word_count))
        
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Post already exists
    finally:
        conn.close()

def get_all_post_texts():
    """Get all post texts for clustering"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT slug FROM posts ORDER BY published_date")
    posts = cursor.fetchall()
    conn.close()
    
    texts = []
    slugs = []
    
    for (slug,) in posts:
        html_file = POSTS_DIR / f"{slug}.html"
        if html_file.exists():
            text = extract_text_from_html(html_file)
            texts.append(text)
            slugs.append(slug)
    
    return slugs, texts

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def process_all_posts():
    """Process all HTML posts in the posts directory"""
    
    logger.info("=" * 70)
    logger.info("🔍 PERFORMANCE TRACKER - Starting analysis")
    logger.info("=" * 70)
    
    # Get all HTML posts
    html_files = sorted(POSTS_DIR.glob("*.html"))
    html_files = [f for f in html_files if f.name != 'index.json']
    
    if not html_files:
        logger.warning("No HTML posts found!")
        return
    
    logger.info(f"Found {len(html_files)} posts")
    
    # First pass: Ensure all posts are in database
    logger.info("\n📝 Phase 1: Indexing posts...")
    for html_file in html_files:
        slug = html_file.stem
        
        # Extract date from filename (YYYY-MM-DD-...)
        try:
            date_parts = slug.split('-')[:3]
            published_date = '-'.join(date_parts)
        except:
            published_date = datetime.now().strftime('%Y-%m-%d')
        
        # Get word count
        text = extract_text_from_html(html_file)
        word_count = len(text.split())
        
        insert_post_if_missing(slug, published_date, word_count)
    
    # Get unscored posts
    unscored = get_unscored_posts()
    
    if not unscored:
        logger.info("\n✅ All posts already scored!")
        return
    
    logger.info(f"\n📊 Phase 2: Scoring {len(unscored)} unscored posts...")
    
    # Second pass: Calculate individual scores
    post_data = []
    
    for post_id, slug in unscored:
        html_file = POSTS_DIR / f"{slug}.html"
        
        if not html_file.exists():
            logger.warning(f"Post file not found: {slug}.html")
            continue
        
        logger.info(f"\nProcessing: {slug}")
        
        # Extract text and metadata
        text = extract_text_from_html(html_file)
        metadata = extract_metadata(html_file)
        
        # Calculate scores
        readability = calculate_readability_score(text)
        seo = calculate_seo_score(metadata, text)
        quality = round((readability + seo) / 2, 2)
        
        post_data.append({
            'slug': slug,
            'text': text,
            'readability': readability,
            'seo': seo,
            'quality': quality
        })
        
        logger.info(f"  Readability: {readability:.1f}/100")
        logger.info(f"  SEO: {seo}/100")
        logger.info(f"  Quality: {quality:.1f}/100")
    
    # Third pass: Topic clustering (on ALL posts for better clustering)
    logger.info("\n🏷️  Phase 3: Topic clustering...")
    
    all_slugs, all_texts = get_all_post_texts()
    
    if len(all_texts) >= 5:
        clusters = cluster_topics(all_texts, n_clusters=5)
        
        # Map slugs to clusters
        slug_to_cluster = dict(zip(all_slugs, clusters))
        
        # Assign clusters to new posts
        for data in post_data:
            cluster_id = slug_to_cluster.get(data['slug'], 4)
            data['topic'] = CLUSTER_LABELS[cluster_id]
    else:
        # Not enough posts for clustering
        for data in post_data:
            data['topic'] = "Random"
    
    # Fourth pass: Update database
    logger.info("\n💾 Phase 4: Updating database...")
    
    for data in post_data:
        update_post_scores(
            data['slug'],
            data['readability'],
            data['seo'],
            data['quality'],
            data['topic']
        )
        
        logger.info(f"Scored post {data['slug']}: "
                   f"readability={data['readability']:.1f}, "
                   f"seo={data['seo']}, "
                   f"cluster={data['topic']}")
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("✅ PERFORMANCE TRACKER - Complete!")
    logger.info("=" * 70)
    
    # Calculate averages
    avg_readability = sum(d['readability'] for d in post_data) / len(post_data)
    avg_seo = sum(d['seo'] for d in post_data) / len(post_data)
    avg_quality = sum(d['quality'] for d in post_data) / len(post_data)
    
    logger.info(f"\n📈 Summary:")
    logger.info(f"  Posts scored: {len(post_data)}")
    logger.info(f"  Avg Readability: {avg_readability:.1f}/100")
    logger.info(f"  Avg SEO: {avg_seo:.1f}/100")
    logger.info(f"  Avg Quality: {avg_quality:.1f}/100")
    
    # Topic distribution
    topics = [d['topic'] for d in post_data]
    topic_counts = Counter(topics)
    logger.info(f"\n🏷️  Topic Distribution:")
    for topic, count in topic_counts.most_common():
        logger.info(f"  {topic}: {count} posts")
    
    logger.info(f"\n📝 Log saved to: {LOG_FILE}")
    logger.info("")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run performance tracker"""
    try:
        process_all_posts()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
