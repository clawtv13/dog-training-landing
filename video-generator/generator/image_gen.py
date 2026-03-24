"""AI Image Generation module using Replicate (Flux models)"""
import os
import asyncio
import httpx
from pathlib import Path
from typing import Literal
import replicate

from config import TEMP_DIR

# Flux model options
FLUX_MODELS = {
    "schnell": "black-forest-labs/flux-schnell",      # Fast & cheap (~$0.003)
    "pro": "black-forest-labs/flux-1.1-pro",          # High quality (~$0.04)
    "pro2": "black-forest-labs/flux-2-pro",           # Best quality (~$0.05)
}

# Visual style presets (appended to prompts)
STYLE_PRESETS = {
    "realistic_film": "cinematic film still, realistic photography, 35mm film grain, shallow depth of field, dramatic lighting, high detail",
    "anime": "anime style, studio ghibli inspired, vibrant colors, detailed illustration, clean lines",
    "3d_render": "3D rendered, Pixar style, smooth textures, volumetric lighting, high quality render",
    "digital_art": "digital art, trending on artstation, highly detailed, vibrant colors, professional illustration",
    "photorealistic": "photorealistic, ultra HD, 8K, professional photography, sharp focus, detailed",
    "cinematic": "cinematic scene, movie still, anamorphic lens, dramatic atmosphere, professional color grading",
    "vintage": "vintage photograph, retro style, warm colors, film grain, nostalgic mood",
    "minimalist": "minimalist style, clean composition, simple shapes, modern aesthetic",
}

# Aspect ratio to dimensions
ASPECT_RATIOS = {
    "9:16": (768, 1344),   # Vertical (TikTok/Reels)
    "16:9": (1344, 768),   # Horizontal (YouTube)
    "1:1": (1024, 1024),   # Square (Instagram)
}


async def generate_image(
    prompt: str,
    style: str = "realistic_film",
    model: Literal["schnell", "pro", "pro2"] = "schnell",
    aspect_ratio: str = "9:16",
    output_path: Path = None,
) -> Path:
    """
    Generate a single image using Flux.
    
    Args:
        prompt: Scene description
        style: Visual style preset
        model: Flux model variant
        aspect_ratio: "9:16", "16:9", or "1:1"
        output_path: Where to save (auto-generated if None)
    
    Returns:
        Path to generated image
    """
    
    # Build full prompt with style
    style_suffix = STYLE_PRESETS.get(style, STYLE_PRESETS["realistic_film"])
    full_prompt = f"{prompt}, {style_suffix}"
    
    # Get dimensions
    width, height = ASPECT_RATIOS.get(aspect_ratio, ASPECT_RATIOS["9:16"])
    
    # Get model ID
    model_id = FLUX_MODELS.get(model, FLUX_MODELS["schnell"])
    
    # Run Flux
    output = await asyncio.to_thread(
        replicate.run,
        model_id,
        input={
            "prompt": full_prompt,
            "width": width,
            "height": height,
            "num_outputs": 1,
            "output_format": "png",
        }
    )
    
    # Get image URL from output
    if isinstance(output, list) and len(output) > 0:
        image_url = str(output[0])
    else:
        image_url = str(output)
    
    # Download image
    if output_path is None:
        output_path = TEMP_DIR / f"flux_{hash(prompt) % 10000:04d}.png"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
        response.raise_for_status()
        output_path.write_bytes(response.content)
    
    return output_path


async def generate_images_for_scenes(
    scenes: list[dict],
    style: str = "realistic_film",
    model: str = "schnell",
    aspect_ratio: str = "9:16",
) -> list[Path]:
    """
    Generate images for all scenes.
    
    Args:
        scenes: List of scene dicts with "visual_prompt" or "description"
        style: Visual style preset
        model: Flux model variant
        aspect_ratio: Video aspect ratio
    
    Returns:
        List of paths to generated images
    """
    
    tasks = []
    for i, scene in enumerate(scenes):
        # Get prompt from scene
        prompt = scene.get("visual_prompt") or scene.get("description") or scene.get("text", "")
        
        output_path = TEMP_DIR / f"scene_{i:03d}.png"
        
        task = generate_image(
            prompt=prompt,
            style=style,
            model=model,
            aspect_ratio=aspect_ratio,
            output_path=output_path
        )
        tasks.append(task)
    
    # Run all generations (could parallelize but Replicate has rate limits)
    results = []
    for task in tasks:
        try:
            result = await task
            results.append(result)
        except Exception as e:
            print(f"Warning: Image generation failed: {e}")
            results.append(None)
    
    return [r for r in results if r is not None]


def list_styles() -> list[str]:
    """Return available style presets"""
    return list(STYLE_PRESETS.keys())


def list_models() -> dict[str, str]:
    """Return available models with descriptions"""
    return {
        "schnell": "Flux Schnell - Fast & cheap (~$0.003/img)",
        "pro": "Flux 1.1 Pro - High quality (~$0.04/img)", 
        "pro2": "Flux 2 Pro - Best quality (~$0.05/img)",
    }
