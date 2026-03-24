"""Transition effects between video clips"""
import random
from typing import Literal, Callable

# Fix Pillow 10+ compatibility
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips


# Type definitions
TransitionName = Literal["fade", "slide", "zoom", "swipe", "none"]
SlideDirection = Literal["left", "right", "up", "down"]


def fade_transition(
    clip1: VideoFileClip,
    clip2: VideoFileClip,
    duration: float = 0.5
) -> VideoFileClip:
    """
    Create crossfade/dissolve transition between two clips.
    
    Args:
        clip1: First clip (will fade out)
        clip2: Second clip (will fade in)
        duration: Transition duration in seconds
    
    Returns:
        Combined clip with fade transition
    """
    # Ensure transition isn't longer than either clip
    duration = min(duration, clip1.duration / 2, clip2.duration / 2)
    
    # Apply fade effects
    clip1_faded = clip1.fx(fadeout, duration)
    clip2_faded = clip2.fx(fadein, duration)
    
    # Set clip2 to start before clip1 ends (overlap)
    clip2_timed = clip2_faded.set_start(clip1.duration - duration)
    
    # Composite with crossfade
    final = CompositeVideoClip(
        [clip1_faded, clip2_timed],
        size=clip1.size
    )
    
    # Set final duration
    total_duration = clip1.duration + clip2.duration - duration
    final = final.set_duration(total_duration)
    
    return final


def slide_transition(
    clip1: VideoFileClip,
    clip2: VideoFileClip,
    duration: float = 0.4,
    direction: SlideDirection = "left"
) -> VideoFileClip:
    """
    Create slide transition - clip2 slides in from a direction.
    
    Args:
        clip1: First clip
        clip2: Second clip (slides in)
        duration: Transition duration in seconds
        direction: Direction clip2 enters from
    
    Returns:
        Combined clip with slide transition
    """
    duration = min(duration, clip1.duration / 2, clip2.duration / 2)
    w, h = clip1.size
    
    # Create position functions based on direction
    if direction == "left":
        # Clip2 enters from the left
        def clip2_pos(t):
            if t < clip1.duration - duration:
                return (-w, 0)  # Off screen left
            else:
                progress = (t - (clip1.duration - duration)) / duration
                x = -w + (w * progress)
                return (x, 0)
        
        def clip1_pos(t):
            if t < clip1.duration - duration:
                return (0, 0)
            else:
                progress = (t - (clip1.duration - duration)) / duration
                x = w * progress
                return (x, 0)
    
    elif direction == "right":
        def clip2_pos(t):
            if t < clip1.duration - duration:
                return (w, 0)  # Off screen right
            else:
                progress = (t - (clip1.duration - duration)) / duration
                x = w - (w * progress)
                return (x, 0)
        
        def clip1_pos(t):
            if t < clip1.duration - duration:
                return (0, 0)
            else:
                progress = (t - (clip1.duration - duration)) / duration
                x = -w * progress
                return (x, 0)
    
    elif direction == "up":
        def clip2_pos(t):
            if t < clip1.duration - duration:
                return (0, h)  # Off screen bottom
            else:
                progress = (t - (clip1.duration - duration)) / duration
                y = h - (h * progress)
                return (0, y)
        
        def clip1_pos(t):
            if t < clip1.duration - duration:
                return (0, 0)
            else:
                progress = (t - (clip1.duration - duration)) / duration
                y = -h * progress
                return (0, y)
    
    else:  # down
        def clip2_pos(t):
            if t < clip1.duration - duration:
                return (0, -h)  # Off screen top
            else:
                progress = (t - (clip1.duration - duration)) / duration
                y = -h + (h * progress)
                return (0, y)
        
        def clip1_pos(t):
            if t < clip1.duration - duration:
                return (0, 0)
            else:
                progress = (t - (clip1.duration - duration)) / duration
                y = h * progress
                return (0, y)
    
    # Set positions
    clip1_moving = clip1.set_position(clip1_pos)
    clip2_timed = clip2.set_start(0).set_position(clip2_pos)
    
    # Composite
    total_duration = clip1.duration + clip2.duration - duration
    final = CompositeVideoClip(
        [clip1_moving, clip2_timed],
        size=(w, h)
    )
    final = final.set_duration(total_duration)
    
    return final


def zoom_transition(
    clip1: VideoFileClip,
    clip2: VideoFileClip,
    duration: float = 0.4,
    zoom_out_scale: float = 0.5,
    zoom_in_scale: float = 2.0
) -> VideoFileClip:
    """
    Create zoom transition - clip1 zooms out, clip2 zooms in.
    
    Args:
        clip1: First clip (zooms out)
        clip2: Second clip (zooms in)
        duration: Transition duration in seconds
        zoom_out_scale: Final scale for clip1 (0.5 = 50%)
        zoom_in_scale: Initial scale for clip2 (2.0 = 200%)
    
    Returns:
        Combined clip with zoom transition
    """
    import numpy as np
    from PIL import Image
    
    duration = min(duration, clip1.duration / 2, clip2.duration / 2)
    w, h = clip1.size
    transition_start = clip1.duration - duration
    
    def process_clip1(get_frame, t):
        """Zoom out clip1 during transition"""
        frame = get_frame(t)
        
        if t < transition_start:
            return frame
        
        progress = (t - transition_start) / duration
        # Ease out
        progress = 1 - (1 - progress) ** 2
        
        scale = 1.0 - (1.0 - zoom_out_scale) * progress
        alpha = 1.0 - progress  # Fade out as it zooms
        
        img = Image.fromarray(frame)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        if new_w > 0 and new_h > 0:
            resized = img.resize((new_w, new_h), Image.LANCZOS)
            
            # Center on canvas
            result = Image.new('RGB', (w, h), (0, 0, 0))
            x = (w - new_w) // 2
            y = (h - new_h) // 2
            result.paste(resized, (x, y))
            
            # Apply alpha
            result_array = np.array(result).astype(float) * alpha
            return result_array.astype(np.uint8)
        
        return np.zeros((h, w, 3), dtype=np.uint8)
    
    def process_clip2(get_frame, t):
        """Zoom in clip2 during transition"""
        # Adjust time for clip2
        clip2_t = t - transition_start
        if clip2_t < 0:
            return np.zeros((h, w, 3), dtype=np.uint8)
        
        frame = get_frame(min(clip2_t, clip2.duration - 0.001))
        
        if clip2_t > duration:
            return frame
        
        progress = clip2_t / duration
        # Ease out
        progress = progress ** 0.5
        
        scale = zoom_in_scale - (zoom_in_scale - 1.0) * progress
        alpha = progress  # Fade in as it zooms
        
        img = Image.fromarray(frame)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        if new_w > 0 and new_h > 0:
            resized = img.resize((new_w, new_h), Image.LANCZOS)
            
            # Center crop
            x = (new_w - w) // 2
            y = (new_h - h) // 2
            cropped = resized.crop((x, y, x + w, y + h))
            
            # Apply alpha
            result_array = np.array(cropped).astype(float) * alpha
            return result_array.astype(np.uint8)
        
        return frame
    
    clip1_zoomed = clip1.fl(lambda gf, t: process_clip1(gf, t))
    clip2_zoomed = clip2.fl(lambda gf, t: process_clip2(gf, t))
    clip2_timed = clip2_zoomed.set_start(transition_start)
    
    total_duration = clip1.duration + clip2.duration - duration
    
    final = CompositeVideoClip(
        [clip1_zoomed, clip2_timed],
        size=(w, h)
    )
    final = final.set_duration(total_duration)
    
    return final


def swipe_transition(
    clip1: VideoFileClip,
    clip2: VideoFileClip,
    duration: float = 0.35,
    direction: SlideDirection = "left"
) -> VideoFileClip:
    """
    Create swipe/wipe transition - a line sweeps across revealing clip2.
    
    Args:
        clip1: First clip
        clip2: Second clip (revealed)
        duration: Transition duration in seconds
        direction: Swipe direction
    
    Returns:
        Combined clip with swipe transition
    """
    import numpy as np
    
    duration = min(duration, clip1.duration / 2, clip2.duration / 2)
    w, h = clip1.size
    transition_start = clip1.duration - duration
    
    def make_swipe_frame(t):
        """Combine frames with swipe reveal"""
        if t < transition_start:
            return clip1.get_frame(t)
        
        if t >= clip1.duration:
            clip2_t = t - transition_start
            return clip2.get_frame(min(clip2_t, clip2.duration - 0.001))
        
        progress = (t - transition_start) / duration
        # Ease in-out
        progress = progress * progress * (3 - 2 * progress)
        
        frame1 = clip1.get_frame(t)
        clip2_t = t - transition_start
        frame2 = clip2.get_frame(min(clip2_t, clip2.duration - 0.001))
        
        result = frame1.copy()
        
        if direction == "left":
            # Reveal from right to left
            reveal_x = int(w * (1 - progress))
            if reveal_x < w:
                result[:, reveal_x:] = frame2[:, reveal_x:]
        
        elif direction == "right":
            # Reveal from left to right
            reveal_x = int(w * progress)
            if reveal_x > 0:
                result[:, :reveal_x] = frame2[:, :reveal_x]
        
        elif direction == "up":
            # Reveal from bottom to top
            reveal_y = int(h * (1 - progress))
            if reveal_y < h:
                result[reveal_y:, :] = frame2[reveal_y:, :]
        
        else:  # down
            # Reveal from top to bottom
            reveal_y = int(h * progress)
            if reveal_y > 0:
                result[:reveal_y, :] = frame2[:reveal_y, :]
        
        return result
    
    total_duration = clip1.duration + clip2.duration - duration
    
    # Create video from frames
    from moviepy.editor import VideoClip
    final = VideoClip(make_swipe_frame, duration=total_duration)
    final = final.set_fps(clip1.fps if hasattr(clip1, 'fps') and clip1.fps else 30)
    
    return final


def apply_transition(
    clip1: VideoFileClip,
    clip2: VideoFileClip,
    transition: TransitionName = "fade",
    duration: float = 0.5,
    **kwargs
) -> VideoFileClip:
    """
    Apply a specific transition between two clips.
    
    Args:
        clip1: First clip
        clip2: Second clip
        transition: Transition type
        duration: Transition duration
        **kwargs: Additional transition parameters
    
    Returns:
        Combined clip with transition
    """
    transitions_map: dict[str, Callable] = {
        "fade": fade_transition,
        "slide": slide_transition,
        "zoom": zoom_transition,
        "swipe": swipe_transition,
        "none": lambda c1, c2, **kw: concatenate_videoclips([c1, c2])
    }
    
    transition_fn = transitions_map.get(transition, fade_transition)
    return transition_fn(clip1, clip2, duration=duration, **kwargs)


def apply_random_transition(
    clip1: VideoFileClip,
    clip2: VideoFileClip,
    duration: float = 0.4,
    exclude: list[TransitionName] = None
) -> VideoFileClip:
    """
    Apply a random transition between two clips.
    
    Args:
        clip1: First clip
        clip2: Second clip
        duration: Transition duration
        exclude: List of transitions to exclude
    
    Returns:
        Combined clip with random transition
    """
    exclude = exclude or []
    
    # Available transitions with their parameter options
    transitions_config = [
        ("fade", {}),
        ("slide", {"direction": "left"}),
        ("slide", {"direction": "right"}),
        ("slide", {"direction": "up"}),
        ("swipe", {"direction": "left"}),
        ("swipe", {"direction": "right"}),
        ("zoom", {}),
    ]
    
    available = [(name, params) for name, params in transitions_config if name not in exclude]
    
    if not available:
        return concatenate_videoclips([clip1, clip2])
    
    trans_name, params = random.choice(available)
    return apply_transition(clip1, clip2, trans_name, duration=duration, **params)


def concatenate_with_transitions(
    clips: list[VideoFileClip],
    transition: TransitionName = "fade",
    duration: float = 0.4,
    random_transitions: bool = False
) -> VideoFileClip:
    """
    Concatenate multiple clips with transitions between them.
    
    Args:
        clips: List of video clips
        transition: Transition type (ignored if random_transitions=True)
        duration: Transition duration
        random_transitions: Use random transitions between each clip
    
    Returns:
        Single clip with all transitions applied
    """
    if not clips:
        raise ValueError("No clips provided")
    
    if len(clips) == 1:
        return clips[0]
    
    result = clips[0]
    
    for i, clip in enumerate(clips[1:], 1):
        if random_transitions:
            result = apply_random_transition(result, clip, duration=duration)
        else:
            result = apply_transition(result, clip, transition=transition, duration=duration)
    
    return result


# Transition presets for common use cases
TRANSITION_PRESETS = {
    "quick_fade": {
        "transition": "fade",
        "params": {"duration": 0.3}
    },
    "smooth_fade": {
        "transition": "fade",
        "params": {"duration": 0.6}
    },
    "slide_left": {
        "transition": "slide",
        "params": {"duration": 0.4, "direction": "left"}
    },
    "slide_right": {
        "transition": "slide",
        "params": {"duration": 0.4, "direction": "right"}
    },
    "dramatic_zoom": {
        "transition": "zoom",
        "params": {"duration": 0.5, "zoom_out_scale": 0.3, "zoom_in_scale": 2.5}
    },
    "subtle_zoom": {
        "transition": "zoom",
        "params": {"duration": 0.4, "zoom_out_scale": 0.7, "zoom_in_scale": 1.5}
    },
    "quick_swipe": {
        "transition": "swipe",
        "params": {"duration": 0.25, "direction": "left"}
    }
}


def apply_preset_transition(
    clip1: VideoFileClip,
    clip2: VideoFileClip,
    preset_name: str
) -> VideoFileClip:
    """
    Apply a preset transition configuration.
    
    Args:
        clip1: First clip
        clip2: Second clip
        preset_name: Name of preset from TRANSITION_PRESETS
    
    Returns:
        Combined clip with preset transition applied
    """
    preset = TRANSITION_PRESETS.get(preset_name)
    if not preset:
        return apply_transition(clip1, clip2, "fade")
    
    return apply_transition(
        clip1, clip2,
        preset["transition"],
        **preset["params"]
    )
