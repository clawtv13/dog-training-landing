#!/usr/bin/env python3
"""
Transcribe video by extracting audio first, then using Whisper
Usage: python3 transcribe-video.py video.mp4
Output: video.txt (ready to upload to Google Drive)
"""

import sys
import os
import subprocess
from pathlib import Path
import tempfile

try:
    import openai
except ImportError:
    print("❌ OpenAI library not installed")
    print("Run: pip install openai")
    sys.exit(1)

# OpenAI API Key
OPENAI_API_KEY = "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"

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def extract_audio(video_path, output_audio):
    """Extract audio from video using ffmpeg"""
    print("🎵 Extracting audio with ffmpeg...")
    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vn',  # No video
        '-acodec', 'libmp3lame',
        '-b:a', '64k',  # Low bitrate for small file
        '-ac', '1',  # Mono
        '-ar', '16000',  # 16kHz sample rate
        '-y',  # Overwrite
        output_audio
    ]
    
    result = subprocess.run(cmd, 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.PIPE, 
                          text=True)
    
    if result.returncode != 0:
        print(f"❌ ffmpeg error: {result.stderr}")
        return False
    
    audio_size = os.path.getsize(output_audio) / (1024 * 1024)
    print(f"✅ Audio extracted: {audio_size:.1f} MB")
    return True

def transcribe_audio(audio_path):
    """Transcribe audio using OpenAI Whisper API"""
    print("🎙️  Transcribing with Whisper...")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    
    return transcript.strip()

def main(video_path):
    """Main workflow"""
    
    if not os.path.exists(video_path):
        print(f"❌ File not found: {video_path}")
        sys.exit(1)
    
    # Check ffmpeg
    if not check_ffmpeg():
        print("❌ ffmpeg not installed!")
        print("\nInstall:")
        print("  macOS: brew install ffmpeg")
        print("  Windows: https://ffmpeg.org/download.html")
        print("  Linux: sudo apt install ffmpeg")
        sys.exit(1)
    
    # Video info
    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"📹 Video: {os.path.basename(video_path)}")
    print(f"💾 Size: {file_size_mb:.1f} MB\n")
    
    # Extract audio to temp file
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_audio:
        temp_audio_path = tmp_audio.name
    
    try:
        # Step 1: Extract audio
        if not extract_audio(video_path, temp_audio_path):
            sys.exit(1)
        
        # Step 2: Transcribe audio
        transcript = transcribe_audio(temp_audio_path)
        
        # Step 3: Save transcript
        base_name = Path(video_path).stem
        output_dir = os.path.dirname(video_path) or '.'
        output_path = os.path.join(output_dir, f"{base_name}.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        print(f"\n✅ Transcript saved!")
        print(f"📄 File: {output_path}")
        print(f"📝 Length: {len(transcript)} characters")
        print(f"\n💡 Upload to Google Drive:")
        print(f"   - {os.path.basename(video_path)}")
        print(f"   - {os.path.basename(output_path)}")
        
    except openai.APIError as e:
        print(f"\n❌ OpenAI API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        # Cleanup temp audio
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 transcribe-video.py <video-file>")
        print("\nExample:")
        print("  python3 transcribe-video.py health-test.mp4")
        print("\nRequires:")
        print("  - ffmpeg (for audio extraction)")
        print("  - openai (pip install openai)")
        sys.exit(1)
    
    video_path = sys.argv[1]
    main(video_path)
