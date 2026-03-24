"""
Video Generator - Script to Video AI (Full Featured)
Clone of CapCut's "Create with AI" functionality

Features:
- Script → Scenes parsing with LLM
- Stock video from Pexels + Pixabay
- TTS with Edge TTS (free, unlimited)
- Animated subtitles (karaoke, bounce, highlight)
- Ken Burns / Pan effects
- Transitions (fade, slide, zoom, swipe)
- Background music with auto-ducking

Usage:
    python main.py "Your script text here"
    python main.py --script-file script.txt
    python main.py "Script" --voice en-US-JennyNeural --music calm
"""

import asyncio
import argparse
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from config import VOICES, VIDEO_SETTINGS, OUTPUT_DIR
from generator import (
    parse_script_to_scenes,
    get_videos_for_scenes,
    generate_speech_for_scenes,
    generate_subtitles_from_timings,
    cleanup_temp_files,
    list_voices
)
from generator.composer import compose_video

console = Console()


async def generate_video(
    script: str,
    voice: str = "en-US-GuyNeural",
    aspect_ratio: str = "9:16",
    subtitle_style: str = "karaoke",
    animated_subtitles: bool = True,
    add_effects: bool = True,
    add_transitions: bool = True,
    transition_type: str = "fade",
    add_music: bool = False,
    music_mood: str = "calm",
    logo_path: Path = None,
    output_name: str = "output"
) -> Path:
    """
    Generate a complete video from a script.
    
    Args:
        script: The narration text
        voice: Edge TTS voice ID
        aspect_ratio: "9:16" (vertical), "16:9" (horizontal), "1:1" (square)
        subtitle_style: "karaoke", "bounce", "highlight_box", "wave", or static styles
        animated_subtitles: Use word-by-word animated subtitles
        add_effects: Apply Ken Burns/pan effects
        add_transitions: Add transitions between clips
        transition_type: "fade", "slide", "zoom", "swipe", "random"
        add_music: Add background music
        music_mood: Mood for music ("calm", "energetic", "dramatic", etc.)
        logo_path: Path to logo for watermark
        output_name: Name for the output file
    
    Returns:
        Path to the generated video
    """
    
    orientation = "portrait" if aspect_ratio == "9:16" else "landscape"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Step 1: Parse script into scenes
        task = progress.add_task("🎬 Analyzing script with AI...", total=None)
        scenes = await parse_script_to_scenes(script)
        console.print(f"   [dim]📝 Generated {len(scenes)} scenes[/dim]")
        progress.remove_task(task)
        
        # Step 2: Generate voiceover
        task = progress.add_task("🎙️ Generating voiceover...", total=None)
        audio_path, word_timings = await generate_speech_for_scenes(scenes, voice)
        console.print(f"   [dim]🔊 Audio: {audio_path.name}[/dim]")
        progress.remove_task(task)
        
        # Step 3: Fetch video clips
        task = progress.add_task("🎥 Fetching video clips...", total=None)
        video_clips = await get_videos_for_scenes(scenes, orientation)
        console.print(f"   [dim]📹 Downloaded {len(video_clips)} clips[/dim]")
        progress.remove_task(task)
        
        # Step 4: Generate static subtitles as fallback
        task = progress.add_task("📝 Processing subtitles...", total=None)
        static_subtitles = generate_subtitles_from_timings(word_timings)
        console.print(f"   [dim]💬 Created {len(static_subtitles)} segments[/dim]")
        progress.remove_task(task)
        
        # Step 5: Compose final video
        features = []
        if add_effects:
            features.append("effects")
        if add_transitions:
            features.append("transitions")
        if add_music:
            features.append(f"music ({music_mood})")
        if animated_subtitles:
            features.append(f"animated subs ({subtitle_style})")
        
        feature_str = ", ".join(features) if features else "basic"
        task = progress.add_task(f"🎞️ Composing video ({feature_str})...", total=None)
        
        output_path = compose_video(
            video_clips=video_clips,
            audio_path=audio_path,
            subtitles=static_subtitles,
            word_timings=word_timings,
            scenes=scenes,
            output_name=output_name,
            aspect_ratio=aspect_ratio,
            animated_subtitles=animated_subtitles,
            subtitle_animation=subtitle_style,
            add_effects=add_effects,
            add_transitions=add_transitions,
            transition_type=transition_type,
            add_music=add_music,
            music_mood=music_mood,
            logo_path=logo_path,
        )
        progress.remove_task(task)
        
        # Cleanup
        cleanup_temp_files()
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="🎬 Generate videos from scripts using AI (CapCut clone)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "My dog used to bark all night..."
  python main.py --script-file myscript.txt --voice en-US-JennyNeural
  python main.py "Script" --music calm --effects --transitions
  python main.py "Script" --subtitle-style bounce --no-effects

Subtitle Styles (animated):
  karaoke       Word changes color when spoken (default)
  bounce        Word scales up when spoken
  highlight_box Word gets background highlight
  wave          Words appear one by one

Music Moods:
  calm, energetic, dramatic, happy, sad, mysterious, romantic, neutral
        """
    )
    
    # Basic options
    parser.add_argument("script", nargs="?", help="The script/narration text")
    parser.add_argument("--script-file", "-f", type=Path, help="Read script from file")
    parser.add_argument("--output", "-o", default="output", help="Output filename (without extension)")
    parser.add_argument("--voice", "-v", default="en-US-GuyNeural", help="TTS voice to use")
    parser.add_argument("--format", "-r", default="9:16", choices=["9:16", "16:9", "1:1"], 
                        help="Video aspect ratio")
    
    # Subtitle options
    parser.add_argument("--subtitle-style", "-s", default="karaoke", 
                        choices=["karaoke", "bounce", "highlight_box", "wave", "bold", "minimal"],
                        help="Subtitle animation style")
    parser.add_argument("--no-animated-subs", action="store_true", help="Use static subtitles instead")
    
    # Effect options
    parser.add_argument("--effects", action="store_true", default=True, help="Add Ken Burns/pan effects")
    parser.add_argument("--no-effects", action="store_true", help="Disable effects")
    
    # Transition options
    parser.add_argument("--transitions", action="store_true", default=True, help="Add transitions")
    parser.add_argument("--no-transitions", action="store_true", help="Disable transitions")
    parser.add_argument("--transition-type", "-t", default="fade",
                        choices=["fade", "slide", "zoom", "swipe", "random"],
                        help="Type of transition between clips")
    
    # Music options
    parser.add_argument("--music", "-m", nargs="?", const="calm", default=None,
                        help="Add background music with mood (calm, energetic, dramatic, etc.)")
    
    # Logo option
    parser.add_argument("--logo", type=Path, help="Path to logo for watermark")
    
    # Info commands
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    
    args = parser.parse_args()
    
    # Handle info commands
    if args.list_voices:
        console.print("\n[bold]Available Voices:[/bold]\n")
        for voice in list_voices():
            console.print(f"  • {voice}")
        return
    
    # Get script text
    if args.script_file:
        if not args.script_file.exists():
            console.print(f"[red]Error: File not found: {args.script_file}[/red]")
            return
        script = args.script_file.read_text()
    elif args.script:
        script = args.script
    else:
        console.print("[red]Error: Please provide a script or --script-file[/red]")
        parser.print_help()
        return
    
    # Process boolean flags
    add_effects = not args.no_effects
    add_transitions = not args.no_transitions
    animated_subtitles = not args.no_animated_subs
    add_music = args.music is not None
    music_mood = args.music if args.music else "calm"
    
    # Display settings
    console.print()
    console.print(Panel.fit(
        "[bold green]🎬 Video Generator[/bold green]\n"
        "[dim]CapCut-style AI video creation[/dim]",
        border_style="green"
    ))
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Voice", args.voice)
    table.add_row("Format", args.format)
    table.add_row("Subtitles", f"{args.subtitle_style} ({'animated' if animated_subtitles else 'static'})")
    table.add_row("Effects", "✓" if add_effects else "✗")
    table.add_row("Transitions", f"✓ ({args.transition_type})" if add_transitions else "✗")
    table.add_row("Music", f"✓ ({music_mood})" if add_music else "✗")
    table.add_row("Script", f"{script[:40]}{'...' if len(script) > 40 else ''}")
    console.print(table)
    console.print()
    
    # Generate video
    output_path = asyncio.run(generate_video(
        script=script,
        voice=args.voice,
        aspect_ratio=args.format,
        subtitle_style=args.subtitle_style,
        animated_subtitles=animated_subtitles,
        add_effects=add_effects,
        add_transitions=add_transitions,
        transition_type=args.transition_type,
        add_music=add_music,
        music_mood=music_mood,
        logo_path=args.logo,
        output_name=args.output
    ))
    
    console.print()
    console.print(Panel.fit(
        f"[bold green]✅ Video generated successfully![/bold green]\n\n"
        f"📁 [white]{output_path}[/white]",
        border_style="green"
    ))


if __name__ == "__main__":
    main()
