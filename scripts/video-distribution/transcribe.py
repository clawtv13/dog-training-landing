#!/usr/bin/env python3
"""
Extract audio from video and transcribe with Whisper
Usage: python transcribe.py <video_path>
"""
import sys
import os
import subprocess
import tempfile
from openai import OpenAI

def transcribe_video(video_path):
    """Transcribe video audio using Whisper"""
    
    # Extract audio to temp file
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
        audio_path = temp_audio.name
    
    try:
        # Extract audio with ffmpeg
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vn", "-ar", "16000", "-ac", "1", "-ab", "64k",
            "-f", "mp3", audio_path, "-y"
        ], check=True, capture_output=True, stderr=subprocess.DEVNULL)
        
        # Transcribe with Whisper
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Try reading from credentials
            cred_file = "/root/.openclaw/workspace/.credentials/openai-key.txt"
            if os.path.exists(cred_file):
                with open(cred_file) as f:
                    api_key = f.read().strip()
        
        client = OpenAI(api_key=api_key)
        
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        
        return transcript.text
    
    finally:
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <video_path>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    if not os.path.exists(video_path):
        print(f"Error: File not found: {video_path}")
        sys.exit(1)
    
    try:
        transcript = transcribe_video(video_path)
        print(transcript)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
