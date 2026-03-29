#!/bin/bash
# prepare-for-whisper.sh
# Extrae audio antes de subir a Google Drive

if [ $# -eq 0 ]; then
  echo "Usage: $0 <video-file>"
  echo "Example: $0 health-test.mp4"
  exit 1
fi

INPUT="$1"
BASENAME="${INPUT%.*}"
OUTPUT="${BASENAME}-audio.mp3"

echo "🎵 Extracting audio from: $INPUT"

ffmpeg -i "$INPUT" \
  -vn \
  -acodec libmp3lame \
  -ac 1 \
  -ar 16000 \
  -b:a 64k \
  "$OUTPUT" \
  -y 2>&1 | grep -E "(Duration|size=)"

if [ -f "$OUTPUT" ]; then
  ORIGINAL_SIZE=$(du -h "$INPUT" | cut -f1)
  AUDIO_SIZE=$(du -h "$OUTPUT" | cut -f1)
  
  echo ""
  echo "✅ Audio extracted!"
  echo "   Original: $ORIGINAL_SIZE"
  echo "   Audio: $AUDIO_SIZE"
  echo "   File: $OUTPUT"
  echo ""
  echo "📤 Upload this file to Google Drive:"
  echo "   $OUTPUT"
else
  echo "❌ Failed to extract audio"
  exit 1
fi
