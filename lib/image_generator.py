#!/usr/bin/env python3
"""
Image Generation Helper Module
Uses inference.sh CLI (infsh) for AI image generation
"""

import subprocess
import json
import logging
import time
from pathlib import Path
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Generate images using inference.sh CLI"""
    
    # Model costs and best uses
    MODELS = {
        'p-image': {
            'app_id': 'pruna/p-image',
            'cost': 0.001,
            'best_for': 'Fast, reliable generation for all use cases'
        },
        'p-image-lora': {
            'app_id': 'pruna/p-image-lora',
            'cost': 0.001,
            'best_for': 'Custom LoRA styles'
        },
        'wan-image': {
            'app_id': 'alibaba/wan-2-7-image',
            'cost': 0.002,
            'best_for': 'High quality realistic images'
        }
    }
    
    @staticmethod
    def generate_image(
        prompt: str,
        model: str = 'p-image',
        output_path: Optional[Path] = None,
        retry: int = 1
    ) -> Optional[str]:
        """
        Generate image using infsh CLI
        
        Args:
            prompt: Text description of desired image
            model: Model name (flux-klein-4b, p-image, wan-2-7-image)
            output_path: Where to save image (optional, will download if provided)
            retry: Number of retries on failure
            
        Returns:
            Image URL or local path if saved
        """
        
        if model not in ImageGenerator.MODELS:
            logger.error(f"Unknown model: {model}")
            return None
        
        model_info = ImageGenerator.MODELS[model]
        app_id = model_info['app_id']
        
        logger.info(f"🎨 Generating image with {model}...")
        logger.info(f"   Prompt: {prompt[:100]}...")
        logger.info(f"   Cost: ${model_info['cost']}")
        
        # Build infsh command
        input_json = json.dumps({"prompt": prompt})
        
        cmd = [
            'infsh', 'app', 'run', app_id,
            '--input', input_json
        ]
        
        attempt = 0
        while attempt < retry:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=180,
                    check=True
                )
                
                # Parse output for image URL
                output = result.stdout
                
                # Look for image URL in output
                image_url = ImageGenerator._extract_image_url(output)
                
                if not image_url:
                    logger.error("❌ No image URL found in output")
                    logger.debug(f"Output: {output[:500]}")
                    return None
                
                logger.info(f"✅ Image generated: {image_url}")
                
                # Download if output_path specified
                if output_path:
                    downloaded = ImageGenerator._download_image(image_url, output_path)
                    if downloaded:
                        logger.info(f"💾 Saved to: {output_path}")
                        return str(output_path)
                    else:
                        logger.warning("⚠️  Download failed, returning URL")
                        return image_url
                
                return image_url
                
            except subprocess.TimeoutExpired:
                logger.warning(f"⏱️  Timeout on attempt {attempt + 1}/{retry}")
                attempt += 1
                if attempt < retry:
                    time.sleep(10)
                    
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Generation failed: {e.stderr[:200]}")
                attempt += 1
                if attempt < retry:
                    time.sleep(10)
                    
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
                attempt += 1
                if attempt < retry:
                    time.sleep(10)
        
        logger.error(f"❌ Failed after {retry} attempts")
        return None
    
    @staticmethod
    def _extract_image_url(output: str) -> Optional[str]:
        """Extract image URL from infsh output"""
        
        # Try to parse as JSON first
        try:
            # Look for JSON in output
            if '{' in output:
                json_start = output.find('{')
                json_str = output[json_start:]
                # Try to find complete JSON
                data = json.loads(json_str)
                
                # Common response formats (in order of priority)
                if 'image' in data:
                    return data['image']
                if 'image_url' in data:
                    return data['image_url']
                if 'url' in data:
                    return data['url']
                if 'output' in data:
                    if isinstance(data['output'], str):
                        return data['output']
                    if isinstance(data['output'], dict):
                        if 'image' in data['output']:
                            return data['output']['image']
                        if 'url' in data['output']:
                            return data['output']['url']
                if 'images' in data and len(data['images']) > 0:
                    return data['images'][0]
        except json.JSONDecodeError:
            pass
        
        # Fallback: regex for URLs
        import re
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+\.(jpg|jpeg|png|webp|gif)'
        matches = re.findall(url_pattern, output, re.IGNORECASE)
        
        if matches:
            # Return full URL (matches gives us tuple from groups)
            for match in re.finditer(url_pattern, output, re.IGNORECASE):
                return match.group(0)
        
        return None
    
    @staticmethod
    def _download_image(url: str, output_path: Path) -> bool:
        """Download image from URL to local path"""
        
        try:
            import requests
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return False

# Convenience functions
def generate_blog_image(title: str, style_hint: str = "professional", model: str = 'p-image') -> Optional[str]:
    """Generate featured image for blog post"""
    
    prompt = f"Professional blog featured image: {title}, clean modern aesthetic, {style_hint}, high quality, minimalist design"
    
    return ImageGenerator.generate_image(prompt, model=model)

def generate_dog_training_image(topic: str, model: str = 'p-image') -> Optional[str]:
    """Generate dog training image"""
    
    prompt = f"High quality professional photograph: {topic}, happy dog, bright outdoor setting, natural lighting, shallow depth of field, photorealistic"
    
    return ImageGenerator.generate_image(prompt, model=model)

if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    
    print("Testing image generation...")
    
    # Test 1: P-Image (blog style)
    url = generate_blog_image("AI Automation Tools", "tech workspace aesthetic")
    print(f"Blog image: {url}")
    
    # Test 2: FLUX Klein (dog training)
    url = generate_dog_training_image("dog learning sit command")
    print(f"Dog image: {url}")
