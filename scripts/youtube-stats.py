#!/usr/bin/env python3
"""
Get real-time YouTube stats using yt-dlp
Works with /shorts endpoint (most channels post shorts now)
"""

import subprocess
import json
from datetime import datetime

CHANNELS = {
    "CALMORA": {
        "handle": "@calmorarelief",
        "url": "https://www.youtube.com/@calmorarelief/shorts"
    },
    "MONEYSTACK": {
        "handle": "@MONEYSTACK_YT",
        "url": "https://www.youtube.com/@MONEYSTACK_YT/shorts"
    },
    "ClawTV": {
        "handle": "@ClawTV_YT",
        "url": "https://www.youtube.com/@ClawTV_YT/shorts"
    }
}

def get_channel_stats(channel_name, config):
    """Fetch channel stats via yt-dlp"""
    
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--flat-playlist",
        "--playlist-end", "20",  # Last 20 videos
        config['url']
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return {"error": result.stderr[:100]}
        
        # Parse JSON lines
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    videos.append(json.loads(line))
                except:
                    pass
        
        if not videos:
            return {"error": "No videos found"}
        
        # Calculate stats
        total_views = sum(v.get('view_count', 0) for v in videos)
        
        # Sort by views
        top_video = max(videos, key=lambda v: v.get('view_count', 0))
        recent_video = videos[0]  # First = most recent
        
        return {
            "channel_name": channel_name,
            "handle": config['handle'],
            "total_videos": len(videos),
            "total_views": total_views,
            "avg_views": total_views // len(videos),
            "top_video": {
                "title": top_video['title'],
                "views": top_video.get('view_count', 0),
                "url": top_video['url']
            },
            "recent_video": {
                "title": recent_video['title'],
                "views": recent_video.get('view_count', 0),
                "url": recent_video['url']
            }
        }
        
    except Exception as e:
        return {"error": str(e)}

def main():
    print("\n" + "="*70)
    print("📊 YOUTUBE STATS — LIVE DATA".center(70))
    print("="*70 + "\n")
    
    all_stats = {}
    
    for channel_name, config in CHANNELS.items():
        print(f"🔍 Fetching {channel_name}... ", end="", flush=True)
        stats = get_channel_stats(channel_name, config)
        
        if "error" in stats:
            print(f"❌ {stats['error']}")
        else:
            all_stats[channel_name] = stats
            print(f"✅ {stats['total_views']:,} views")
    
    print("\n" + "="*70)
    print("📈 DETAILED BREAKDOWN".center(70))
    print("="*70 + "\n")
    
    # Sort by total views (highest first)
    for channel_name in sorted(all_stats, key=lambda x: all_stats[x]['total_views'], reverse=True):
        stats = all_stats[channel_name]
        
        print(f"🏆 {channel_name} ({stats['handle']})")
        print(f"   Total Views:  {stats['total_views']:,}")
        print(f"   Videos:       {stats['total_videos']}")
        print(f"   Avg/Video:    {stats['avg_views']:,}")
        print(f"\n   🔥 Top Video: {stats['top_video']['title'][:50]}...")
        print(f"      Views: {stats['top_video']['views']:,}")
        print(f"\n   📅 Recent:    {stats['recent_video']['title'][:50]}...")
        print(f"      Views: {stats['recent_video']['views']:,}")
        print()
    
    # Save to JSON
    output = {
        "timestamp": datetime.now().isoformat(),
        "channels": all_stats
    }
    
    import os
    os.makedirs("/root/.openclaw/workspace/.state", exist_ok=True)
    
    with open("/root/.openclaw/workspace/.state/youtube-stats.json", 'w') as f:
        json.dump(output, f, indent=2)
    
    print("="*70)
    print(f"💾 Saved to: .state/youtube-stats.json")
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
