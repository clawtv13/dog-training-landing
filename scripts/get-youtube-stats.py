#!/usr/bin/env python3
"""
Get YouTube channel stats without API
Uses yt-dlp to extract channel info
"""

import subprocess
import json
import sys

CHANNELS = {
    "CALMORA": "https://www.youtube.com/@calmorarelief",
    "MONEYSTACK": "https://www.youtube.com/@MONEYSTACK_YT",
    "ClawTV": "https://www.youtube.com/@ClawTV_YT"
}

def get_channel_stats(channel_name, channel_url):
    """Extract stats using yt-dlp"""
    
    try:
        # yt-dlp can extract channel info
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--flat-playlist",
            "--playlist-end", "20",  # Get last 20 videos
            channel_url + "/videos"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"❌ {channel_name}: Error - {result.stderr[:200]}")
            return None
        
        # Parse output (each line is a JSON object for one video)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    videos.append(json.loads(line))
                except:
                    pass
        
        if not videos:
            print(f"⚠️ {channel_name}: No videos found")
            return None
        
        # Calculate stats
        total_views = sum(v.get('view_count', 0) for v in videos if v.get('view_count'))
        video_count = len(videos)
        
        # Get channel info from first video
        first_video = videos[0]
        
        stats = {
            "channel_name": channel_name,
            "url": channel_url,
            "videos": video_count,
            "total_views": total_views,
            "avg_views": total_views // video_count if video_count > 0 else 0,
            "latest_video": {
                "title": first_video.get('title', 'Unknown'),
                "views": first_video.get('view_count', 0),
                "url": f"https://youtube.com/watch?v={first_video.get('id', '')}"
            }
        }
        
        return stats
        
    except subprocess.TimeoutExpired:
        print(f"⏱️ {channel_name}: Timeout")
        return None
    except Exception as e:
        print(f"❌ {channel_name}: {e}")
        return None

def main():
    print("📊 FETCHING YOUTUBE STATS")
    print("=" * 60)
    print()
    
    all_stats = {}
    
    for channel_name, channel_url in CHANNELS.items():
        print(f"🔍 Checking {channel_name}...")
        stats = get_channel_stats(channel_name, channel_url)
        
        if stats:
            all_stats[channel_name] = stats
            print(f"✅ {channel_name}: {stats['total_views']:,} views | {stats['videos']} videos")
        
        print()
    
    # Print summary
    print("=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    print()
    
    for channel_name, stats in sorted(all_stats.items(), key=lambda x: x[1]['total_views'], reverse=True):
        print(f"🏆 {channel_name}")
        print(f"   Views: {stats['total_views']:,}")
        print(f"   Videos: {stats['videos']}")
        print(f"   Avg: {stats['avg_views']:,} views/video")
        print(f"   Latest: {stats['latest_video']['title'][:50]}... ({stats['latest_video']['views']:,} views)")
        print()
    
    # Save to JSON
    output_file = "/root/.openclaw/workspace/.state/youtube-stats.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(all_stats, f, indent=2)
    
    print(f"💾 Saved to: {output_file}")

if __name__ == '__main__':
    main()
