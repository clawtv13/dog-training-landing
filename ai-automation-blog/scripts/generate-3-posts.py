#!/usr/bin/env python3
"""
Generate 3 perfect blog posts with SEO scoring
Modified version of master-content-agent.py to generate 3 posts in one run
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from scripts.master_content_agent import (
    get_unpublished_content,
    conduct_seo_research,
    generate_with_quality_check,
    create_blog_post,
    deploy_to_github,
    send_notification,
    logger,
    is_duplicate,
    WORKSPACE
)

def main():
    """Generate 3 posts"""
    logger.info("="*70)
    logger.info("🚀 GENERATING 3 PERFECT POSTS FOR WORKLESS.BUILD")
    logger.info("="*70)
    
    # Get unpublished content
    items = get_unpublished_content()
    
    if len(items) < 3:
        logger.error(f"❌ Need at least 3 items, found {len(items)}")
        return
    
    # Take top 3
    selected = items[:3]
    
    results = []
    
    for i, item in enumerate(selected, 1):
        logger.info(f"\n{'='*70}")
        logger.info(f"POST {i}/3: {item['title'][:60]}...")
        logger.info(f"{'='*70}\n")
        
        try:
            # Check duplicate
            if is_duplicate(item['title'], item['summary']):
                logger.warning(f"⚠️  Skipping duplicate: {item['title']}")
                continue
            
            # SEO Research
            seo_research = conduct_seo_research(item)
            
            # Generate with quality check
            generated = generate_with_quality_check(item, seo_research)
            
            # Publish
            post_slug = create_blog_post(generated, item)
            
            # Store result
            results.append({
                'title': generated.title,
                'slug': post_slug,
                'quality_score': generated.quality_score.total,
                'word_count': generated.word_count,
                'primary_keyword': generated.seo_research.primary_keyword,
                'secondary_keywords': generated.seo_research.secondary_keywords,
                'read_time': generated.read_time
            })
            
            logger.info(f"✅ Post {i}/3 complete: {post_slug}")
            
        except Exception as e:
            logger.error(f"❌ Post {i}/3 failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    # Deploy all at once
    if results:
        logger.info(f"\n{'='*70}")
        logger.info("📦 DEPLOYING ALL POSTS TO GITHUB...")
        logger.info(f"{'='*70}\n")
        
        deployed = deploy_to_github()
        
        if deployed:
            logger.info("\n✅ ALL POSTS DEPLOYED SUCCESSFULLY!\n")
        else:
            logger.warning("\n⚠️  Deployment had issues\n")
    
    # Final report
    logger.info("\n" + "="*70)
    logger.info("📊 GENERATION SUMMARY")
    logger.info("="*70)
    
    for i, result in enumerate(results, 1):
        logger.info(f"\n🔹 Post {i}: {result['title']}")
        logger.info(f"   Quality Score: {result['quality_score']}/100")
        logger.info(f"   Word Count: {result['word_count']}")
        logger.info(f"   Read Time: {result['read_time']} min")
        logger.info(f"   Primary Keyword: {result['primary_keyword']}")
        logger.info(f"   Secondary Keywords: {', '.join(result['secondary_keywords'][:3])}")
        logger.info(f"   File: {result['slug']}.html")
    
    logger.info(f"\n{'='*70}")
    logger.info(f"✅ MISSION COMPLETE: {len(results)}/3 posts generated")
    logger.info("="*70)
    
    return results

if __name__ == "__main__":
    results = main()
