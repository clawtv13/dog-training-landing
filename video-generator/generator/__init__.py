"""Video Generator - Script to Video AI"""
from .llm import parse_script_to_scenes, parse_script_sync
from .stock import get_videos_for_scenes, get_videos_sync, search_video, clear_cache
from .tts import generate_speech, generate_speech_for_scenes, generate_speech_sync, list_voices
from .music import (
    search_music,
    search_music_by_mood,
    get_music_for_video,
    get_music_sync,
    apply_auto_ducking,
    mix_audio_simple,
    mix_with_music_sync,
    MOOD_QUERIES,
)
from .subtitles import (
    generate_subtitles_from_timings,
    generate_subtitles_simple,
    export_srt,
    export_ass,
    SubtitleSegment,
    # Animated subtitles (TikTok/CapCut style)
    group_words_into_lines,
    create_animated_subtitles,
    apply_animated_subtitles,
)
from .composer import compose_video, cleanup_temp_files
from .effects import (
    ken_burns,
    pan_effect,
    zoom_pulse,
    apply_effect,
    apply_random_effect,
    apply_preset,
    EFFECT_PRESETS
)
from .transitions import (
    fade_transition,
    slide_transition,
    zoom_transition,
    swipe_transition,
    apply_transition,
    apply_random_transition,
    concatenate_with_transitions,
    apply_preset_transition,
    TRANSITION_PRESETS
)
from .image_gen import (
    generate_image,
    generate_images_for_scenes,
    list_styles,
    list_models,
    STYLE_PRESETS,
    FLUX_MODELS,
)

__all__ = [
    # LLM
    "parse_script_to_scenes",
    "parse_script_sync",
    # Stock
    "get_videos_for_scenes", 
    "get_videos_sync",
    "search_video",
    "clear_cache",
    # Music
    "search_music",
    "search_music_by_mood",
    "get_music_for_video",
    "get_music_sync",
    "apply_auto_ducking",
    "mix_audio_simple",
    "mix_with_music_sync",
    "MOOD_QUERIES",
    # TTS
    "generate_speech",
    "generate_speech_for_scenes",
    "generate_speech_sync",
    "list_voices",
    # Subtitles
    "generate_subtitles_from_timings",
    "generate_subtitles_simple",
    "export_srt",
    "export_ass",
    "SubtitleSegment",
    # Animated Subtitles
    "group_words_into_lines",
    "create_animated_subtitles",
    "apply_animated_subtitles",
    # Composer
    "compose_video",
    "cleanup_temp_files",
    # Effects
    "ken_burns",
    "pan_effect",
    "zoom_pulse",
    "apply_effect",
    "apply_random_effect",
    "apply_preset",
    "EFFECT_PRESETS",
    # Transitions
    "fade_transition",
    "slide_transition",
    "zoom_transition",
    "swipe_transition",
    "apply_transition",
    "apply_random_transition",
    "concatenate_with_transitions",
    "apply_preset_transition",
    "TRANSITION_PRESETS",
    # AI Image Generation
    "generate_image",
    "generate_images_for_scenes",
    "list_styles",
    "list_models",
    "STYLE_PRESETS",
    "FLUX_MODELS",
]
