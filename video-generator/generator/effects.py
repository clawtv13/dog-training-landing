"""Visual effects module for video clips"""
import random
from typing import Literal, Callable

# Fix Pillow 10+ compatibility
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from moviepy.editor import VideoFileClip, CompositeVideoClip


# Type definitions
Direction = Literal["left", "right", "up", "down"]
EffectName = Literal["ken_burns", "pan", "zoom_pulse", "none"]


def ken_burns(
    clip: VideoFileClip,
    zoom_start: float = 1.0,
    zoom_end: float = 1.15,
    direction: Literal["in", "out"] = "in"
) -> VideoFileClip:
    """
    Apply Ken Burns zoom effect - gradual zoom during clip duration.
    
    Args:
        clip: Input video clip
        zoom_start: Initial zoom level (1.0 = 100%)
        zoom_end: Final zoom level (1.15 = 115%)
        direction: "in" (zoom_start → zoom_end) or "out" (zoom_end → zoom_start)
    
    Returns:
        Clip with Ken Burns effect applied
    """
    if direction == "out":
        zoom_start, zoom_end = zoom_end, zoom_start
    
    w, h = clip.size
    duration = clip.duration
    
    def make_frame(get_frame, t):
        """Generate frame at time t with interpolated zoom"""
        progress = t / duration if duration > 0 else 0
        current_zoom = zoom_start + (zoom_end - zoom_start) * progress
        
        frame = get_frame(t)
        
        # Calculate crop region for zoom effect
        new_w = int(w / current_zoom)
        new_h = int(h / current_zoom)
        
        # Center the crop
        x1 = (w - new_w) // 2
        y1 = (h - new_h) // 2
        x2 = x1 + new_w
        y2 = y1 + new_h
        
        # Ensure bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        # Crop and resize back to original dimensions
        cropped = frame[y1:y2, x1:x2]
        
        # Use simple resize with numpy/PIL
        from PIL import Image
        import numpy as np
        img = Image.fromarray(cropped)
        img = img.resize((w, h), Image.LANCZOS)
        return np.array(img)
    
    return clip.fl(lambda gf, t: make_frame(gf, t))


def pan_effect(
    clip: VideoFileClip,
    direction: Direction = "left",
    pan_amount: float = 0.15
) -> VideoFileClip:
    """
    Apply pan effect - smooth camera movement across the frame.
    
    Args:
        clip: Input video clip
        direction: Pan direction ("left", "right", "up", "down")
        pan_amount: How much to pan (0.15 = 15% of frame)
    
    Returns:
        Clip with pan effect applied
    """
    w, h = clip.size
    duration = clip.duration
    
    # Calculate how many pixels to pan
    if direction in ("left", "right"):
        pan_pixels = int(w * pan_amount)
    else:
        pan_pixels = int(h * pan_amount)
    
    def make_frame(get_frame, t):
        """Generate frame at time t with pan offset"""
        progress = t / duration if duration > 0 else 0
        frame = get_frame(t)
        
        from PIL import Image
        import numpy as np
        
        # Convert to PIL for cropping
        img = Image.fromarray(frame)
        
        # Calculate offset based on direction
        offset = int(pan_pixels * progress)
        
        if direction == "left":
            # Pan left = camera moves right, content moves left
            x1 = offset
            y1 = 0
        elif direction == "right":
            # Pan right = camera moves left, content moves right
            x1 = pan_pixels - offset
            y1 = 0
        elif direction == "up":
            # Pan up = content moves up
            x1 = 0
            y1 = offset
        else:  # down
            # Pan down = content moves down
            x1 = 0
            y1 = pan_pixels - offset
        
        # Crop and resize to maintain dimensions
        if direction in ("left", "right"):
            crop_w = w - pan_pixels
            crop_h = h
        else:
            crop_w = w
            crop_h = h - pan_pixels
        
        x2 = x1 + crop_w
        y2 = y1 + crop_h
        
        cropped = img.crop((x1, y1, x2, y2))
        resized = cropped.resize((w, h), Image.LANCZOS)
        
        return np.array(resized)
    
    return clip.fl(lambda gf, t: make_frame(gf, t))


def zoom_pulse(
    clip: VideoFileClip,
    zoom_amount: float = 1.1,
    pulses: int = 2,
    ease: bool = True
) -> VideoFileClip:
    """
    Apply zoom pulse effect - rhythmic zoom in/out.
    
    Args:
        clip: Input video clip
        zoom_amount: Maximum zoom level (1.1 = 110%)
        pulses: Number of zoom cycles during clip
        ease: Apply easing for smoother animation
    
    Returns:
        Clip with zoom pulse effect applied
    """
    import math
    
    w, h = clip.size
    duration = clip.duration
    
    def make_frame(get_frame, t):
        """Generate frame at time t with pulsing zoom"""
        frame = get_frame(t)
        
        # Calculate pulse progress (0 to 2π for each pulse)
        pulse_progress = (t / duration) * pulses * 2 * math.pi if duration > 0 else 0
        
        # Sine wave for smooth zoom (0 to 1 to 0)
        if ease:
            # Eased sine wave
            zoom_factor = 1 + (zoom_amount - 1) * (0.5 * (1 - math.cos(pulse_progress)))
        else:
            zoom_factor = 1 + (zoom_amount - 1) * abs(math.sin(pulse_progress))
        
        from PIL import Image
        import numpy as np
        
        # Calculate crop for zoom
        new_w = int(w / zoom_factor)
        new_h = int(h / zoom_factor)
        
        x1 = (w - new_w) // 2
        y1 = (h - new_h) // 2
        x2 = x1 + new_w
        y2 = y1 + new_h
        
        # Ensure bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        img = Image.fromarray(frame)
        cropped = img.crop((x1, y1, x2, y2))
        resized = cropped.resize((w, h), Image.LANCZOS)
        
        return np.array(resized)
    
    return clip.fl(lambda gf, t: make_frame(gf, t))


def apply_effect(
    clip: VideoFileClip,
    effect: EffectName = "none",
    **kwargs
) -> VideoFileClip:
    """
    Apply a specific effect to a clip.
    
    Args:
        clip: Input video clip
        effect: Effect name ("ken_burns", "pan", "zoom_pulse", "none")
        **kwargs: Effect-specific parameters
    
    Returns:
        Clip with effect applied
    """
    effects_map: dict[str, Callable] = {
        "ken_burns": ken_burns,
        "pan": pan_effect,
        "zoom_pulse": zoom_pulse,
        "none": lambda c, **kw: c
    }
    
    effect_fn = effects_map.get(effect, lambda c, **kw: c)
    return effect_fn(clip, **kwargs)


def apply_random_effect(
    clip: VideoFileClip,
    exclude: list[EffectName] = None
) -> VideoFileClip:
    """
    Apply a random effect to a clip.
    
    Args:
        clip: Input video clip
        exclude: List of effects to exclude from random selection
    
    Returns:
        Clip with random effect applied
    """
    exclude = exclude or []
    
    # Available effects with default parameters
    effects_config = [
        ("ken_burns", {"zoom_start": 1.0, "zoom_end": 1.15, "direction": "in"}),
        ("ken_burns", {"zoom_start": 1.15, "zoom_end": 1.0, "direction": "out"}),
        ("pan", {"direction": "left", "pan_amount": 0.12}),
        ("pan", {"direction": "right", "pan_amount": 0.12}),
        ("pan", {"direction": "up", "pan_amount": 0.08}),
        ("pan", {"direction": "down", "pan_amount": 0.08}),
        ("zoom_pulse", {"zoom_amount": 1.08, "pulses": 2}),
        ("none", {}),
    ]
    
    # Filter out excluded effects
    available = [(name, params) for name, params in effects_config if name not in exclude]
    
    if not available:
        return clip
    
    effect_name, params = random.choice(available)
    return apply_effect(clip, effect_name, **params)


# Presets for common use cases
EFFECT_PRESETS = {
    "subtle_ken_burns": {
        "effect": "ken_burns",
        "params": {"zoom_start": 1.0, "zoom_end": 1.1, "direction": "in"}
    },
    "dramatic_ken_burns": {
        "effect": "ken_burns", 
        "params": {"zoom_start": 1.0, "zoom_end": 1.25, "direction": "in"}
    },
    "slow_pan_left": {
        "effect": "pan",
        "params": {"direction": "left", "pan_amount": 0.1}
    },
    "slow_pan_right": {
        "effect": "pan",
        "params": {"direction": "right", "pan_amount": 0.1}
    },
    "gentle_pulse": {
        "effect": "zoom_pulse",
        "params": {"zoom_amount": 1.05, "pulses": 1}
    },
    "energetic_pulse": {
        "effect": "zoom_pulse",
        "params": {"zoom_amount": 1.15, "pulses": 3}
    }
}


def apply_preset(clip: VideoFileClip, preset_name: str) -> VideoFileClip:
    """
    Apply a preset effect configuration.
    
    Args:
        clip: Input video clip
        preset_name: Name of preset from EFFECT_PRESETS
    
    Returns:
        Clip with preset effect applied
    """
    preset = EFFECT_PRESETS.get(preset_name)
    if not preset:
        return clip
    
    return apply_effect(clip, preset["effect"], **preset["params"])
