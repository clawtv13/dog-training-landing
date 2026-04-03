#!/usr/bin/env python3
"""
Test script for image generation integration
Tests both blog generators without deploying
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

def test_blog_auto_post():
    """Test AI Automation Blog image generation"""
    logger.info("=" * 60)
    logger.info("TEST 1: AI Automation Blog (blog-auto-post-v2.py)")
    logger.info("=" * 60)
    
    try:
        from image_generator import generate_blog_image
        
        test_title = "AI Automation Tools for Solopreneurs"
        logger.info(f"Generating image for: {test_title}")
        
        url = generate_blog_image(
            test_title,
            style_hint="tech workspace, modern design, AI tools",
            model='p-image'
        )
        
        if url:
            logger.info(f"✅ Image generated: {url}")
            logger.info(f"✅ Test 1 PASSED")
            return True
        else:
            logger.error("❌ Test 1 FAILED: No URL returned")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test 1 FAILED with exception: {e}")
        return False

def test_cleverdog():
    """Test CleverDogMethod image generation"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: CleverDogMethod (cleverdogmethod-autonomous.py)")
    logger.info("=" * 60)
    
    try:
        from image_generator import generate_dog_training_image
        
        test_keyword = "dog training basics"
        logger.info(f"Generating image for: {test_keyword}")
        
        url = generate_dog_training_image(
            test_keyword,
            model='p-image'
        )
        
        if url:
            logger.info(f"✅ Image generated: {url}")
            logger.info(f"✅ Test 2 PASSED")
            return True
        else:
            logger.error("❌ Test 2 FAILED: No URL returned")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test 2 FAILED with exception: {e}")
        return False

def test_error_handling():
    """Test graceful error handling"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: Error Handling (invalid model)")
    logger.info("=" * 60)
    
    try:
        from image_generator import ImageGenerator
        
        logger.info("Attempting generation with invalid model...")
        
        url = ImageGenerator.generate_image(
            "test image",
            model='invalid-model-xyz',
            retry=1
        )
        
        if url is None:
            logger.info("✅ Gracefully returned None for invalid model")
            logger.info("✅ Test 3 PASSED")
            return True
        else:
            logger.error("❌ Test 3 FAILED: Should have returned None")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test 3 FAILED: Should handle error gracefully, got: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 TESTING IMAGE GENERATION INTEGRATION")
    logger.info("=" * 60)
    
    results = []
    
    # Test 1: Blog Auto Post
    results.append(("AI Automation Blog", test_blog_auto_post()))
    
    # Test 2: CleverDog
    results.append(("CleverDogMethod", test_cleverdog()))
    
    # Test 3: Error handling
    results.append(("Error Handling", test_error_handling()))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {name}")
    
    logger.info("=" * 60)
    logger.info(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("✅ ALL TESTS PASSED")
        return 0
    else:
        logger.error(f"❌ {total - passed} TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
