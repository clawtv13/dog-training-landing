#!/usr/bin/env python3
"""
Check recent YouTube uploads for all channels
"""
import subprocess
import json
from datetime import datetime

CHANNELS = {
    "CALMORA": "@calmorarelief",
    "MONEYSTACK": "@MONEYSTACK_YT",
    "ClawTV": "@ClawTV_YT"
}

def get_recent_videos(handle):
    """Get recent videos from channel using yt-dlp"""
    cmd = [
        'yt-dlp',
        '--flat-playlist',
        '--playlist-end', '5',
        '--print', '%(id)s|||%(title)s|||%(view_count)s|||%(upload_date)s',
        f'https://www.youtube.com/{handle}/videos'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            videos = []
            for line in result.stdout.strip().split('\n'):
                if '|||' in line:
                    parts = line.split('|||')
                    if len(parts) >= 4:
                        video_id, title, views, date = parts[0], parts[1], parts[2], parts[3]
                        videos.append({
                            'id': video_id,
                            'title': title,
                            'views': int(views) if views and views != 'NA' else 0,
                            'date': date,
                            'url': f'https://youtube.com/watch?v={video_id}'
                        })
            return videos
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

def main():
    print("="*60)
    print("         CHECKING RECENT YOUTUBE UPLOADS")
    print("="*60)
    
    all_stats = {}
    
    for channel_name, handle in CHANNELS.items():
        print(f"\n📺 {channel_name} ({handle})")
        print("-" * 60)
        
        videos = get_recent_videos(handle)
        
        if videos:
            all_stats[channel_name] = videos
            
            print(f"   ✅ Found {len(videos)} recent videos:\n")
            
            for i, video in enumerate(videos, 1):
                # Check if uploaded today (March 24, 2026)
                is_today = video['date'] == '20260324'
                marker = "🆕" if is_today else "  "
                
                print(f"   {marker} {i}. {video['title'][:50]}...")
                print(f"      📊 {video['views']:,} views")
                print(f"      📅 {video['date']}")
                print(f"      🔗 {video['url']}")
                print()
        else:
            print(f"   ❌ Could not fetch videos")
            all_stats[channel_name] = []
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY - TODAY'S UPLOADS (2026-03-24)")
    print("="*60)
    
    today_total = 0
    for channel_name, videos in all_stats.items():
        today_videos = [v for v in videos if v.get('date') == '20260324']
        if today_videos:
            print(f"\n{channel_name}: {len(today_videos)} new video(s)")
            for video in today_videos:
                print(f"  • {video['title'][:40]}... - {video['views']:,} views")
                today_total += video['views']
        else:
            print(f"\n{channel_name}: No uploads today")
    
    print(f"\n📈 Total views on today's videos: {today_total:,}")
    
    # Save
    with open('/root/.openclaw/workspace/.state/youtube-recent-check.json', 'w') as f:
        json.dump({
            'checked_at': datetime.now().isoformat(),
            'channels': all_stats
        }, f, indent=2)
    
    print(f"\n💾 Saved to: .state/youtube-recent-check.json")

if __name__ == "__main__":
    main()
