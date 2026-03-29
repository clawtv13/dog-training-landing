# VIDEO DISTRIBUTION SYSTEM
## Complete automation for CALMORA + MONEYSTACK

**Goal:** Drop video in Dropbox → Auto-upload to TikTok, Instagram, YouTube with unique titles/descriptions

---

## 🏗️ ARCHITECTURE

### **Components:**

1. **Storage:** Dropbox (free tier, 2GB)
2. **Orchestration:** n8n (workflow automation)
3. **Transcription:** OpenAI Whisper API
4. **Content Generation:** Claude 3.5 Sonnet
5. **Humanization:** humanize-ai-text skill (local)
6. **Upload:** TikTok API, Instagram Graph API, YouTube Data API
7. **Tracking:** JSON metadata files
8. **Notifications:** Telegram

---

## 📂 DROPBOX STRUCTURE

```
/CALMORA/
  queue/
    video001.mp4
    video002.mp4
  
/MONEYSTACK/
  queue/
    video001.mp4
    video002.mp4
```

**Rules:**
- Upload to `/CHANNEL/queue/` folder
- Any filename works (no naming convention required)
- N8N watches for new files every 5 minutes

---

## 🔄 WORKFLOW DETAILED

### **TRIGGER: New file in Dropbox**

1. **N8N Dropbox Trigger** (every 5 min)
   - Watches: `/CALMORA/queue/` and `/MONEYSTACK/queue/`
   - Detects new `.mp4` files
   - Downloads to temp storage

2. **Extract Channel Context**
   ```javascript
   let channel = $node["Dropbox"].json["path_display"].includes("CALMORA") 
     ? "CALMORA" 
     : "MONEYSTACK";
   
   let channelContext = {
     "CALMORA": {
       "niche": "Pain relief, wellness, health hacks",
       "audience": "Office workers, chronic pain sufferers, 25-45",
       "tone": "Empathetic, solution-focused, calming",
       "products": ["Back stretcher", "Cooling relief cap"]
     },
     "MONEYSTACK": {
       "niche": "Money psychology, savings, financial mental health",
       "audience": "Young professionals, students, 18-35",
       "tone": "Real talk, no BS, relatable",
       "products": ["Financial courses", "Budget trackers"]
     }
   };
   ```

3. **Transcribe Audio (Whisper API)**
   ```bash
   POST https://api.openai.com/v1/audio/transcriptions
   
   Headers:
     Authorization: Bearer sk-proj-...
   
   Body (multipart):
     file: video.mp4
     model: whisper-1
     language: en
   
   Response:
     "If you've been sitting at a desk all day and your lower back is killing you..."
   ```
   
   **Cost:** $0.006/minute = ~$0.0045/video (45 sec)

4. **Generate Platform-Specific Content (AI)**
   
   **Prompt to Claude:**
   ```
   Channel: {CALMORA}
   Transcript: "{transcription}"
   Duration: 45 seconds
   
   Generate 3 unique titles and descriptions:
   
   1. TikTok (viral/hook-based):
      - Title: 8-12 words, emotional hook, emoji
      - Caption: 1-2 sentences, relatable, 4-6 hashtags
      - Goal: Stop scroll, high engagement
   
   2. Instagram Reels (aspirational):
      - Title: Brand-aligned, lifestyle angle
      - Caption: Story-driven, 2-3 sentences, emojis, 5-8 hashtags
      - Goal: Save/share, community vibe
   
   3. YouTube Shorts (SEO/educational):
      - Title: Keyword-rich, clear value, 60 chars max
      - Description: 3-4 sentences, timestamps if relevant, CTA
      - Tags: 5-8 keywords
      - Goal: Search ranking, watch time
   
   Rules:
   - NO marketing fluff ("innovative", "transformative")
   - NO generic phrases ("discover the power of")
   - Write like a real person, not a copywriter
   - Each platform gets DIFFERENT angle (not just rewording)
   ```
   
   **AI Response (JSON):**
   ```json
   {
     "tiktok": {
       "title": "POV: Your back pain disappears in 60 seconds 🔥",
       "caption": "For everyone who sits 8+ hours. Try it tonight. #backpain #relief #wellness #stretching",
       "hashtags": ["backpain", "relief", "wellness", "stretching"]
     },
     "instagram": {
       "title": "The stretch that saved my back",
       "caption": "I used to take ibuprofen every day 💊\n\nThen I found this 3-minute routine.\n\nNo pills. No equipment. Just works.\n\n#backpainrelief #desklife #wellness #stretching #healthtips",
       "hashtags": ["backpainrelief", "desklife", "wellness", "stretching", "healthtips"]
     },
     "youtube": {
       "title": "Fix Lower Back Pain in 3 Minutes (No Equipment)",
       "description": "Simple stretch for desk workers with lower back tension.\n\n🛒 Get the back stretcher: https://calmorarelief.com\n\n⏱ Timestamps:\n0:00 Why it works\n0:20 How to do it\n0:40 Results",
       "tags": ["back pain", "lower back", "stretching", "pain relief", "desk worker"]
     }
   }
   ```

5. **Humanize Each Text**
   
   For each platform:
   ```bash
   python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py
   ```
   
   **Input:** Raw AI text
   **Output:** Humanized (removes "serves as", "delve", markdown, etc.)
   
   **Example:**
   - Before: "Discover the transformative power of..."
   - After: "This stretch fixes back pain..."

6. **Generate Video ID & Metadata**
   ```python
   video_id = f"{channel.lower()}-{timestamp}-{random_id}"
   # Example: calmora-20260324-a7f3
   
   metadata = {
     "video_id": video_id,
     "channel": channel,
     "original_filename": "video001.mp4",
     "transcription": "...",
     "duration": 45,
     "platforms": {
       "tiktok": {...},
       "instagram": {...},
       "youtube": {...}
     },
     "created": "2026-03-24T22:00:00Z",
     "status": "ready_to_upload"
   }
   ```
   
   Save to: `/root/.openclaw/workspace/.state/videos/calmora-20260324-a7f3.json`

7. **Upload to Platforms**

   **TikTok:**
   ```bash
   POST https://open-api.tiktok.com/share/video/upload/
   
   Headers:
     Authorization: Bearer {access_token}
   
   Body:
     video: video.mp4
     description: {humanized caption}
     privacy_level: PUBLIC_TO_EVERYONE
   ```

   **Instagram Reels:**
   ```bash
   # Step 1: Create container
   POST https://graph.facebook.com/v18.0/{instagram_account_id}/media
   
   Body:
     media_type: REELS
     video_url: {temporary_public_url}
     caption: {humanized caption}
   
   # Step 2: Publish
   POST https://graph.facebook.com/v18.0/{instagram_account_id}/media_publish
   ```

   **YouTube Shorts:**
   ```bash
   POST https://www.googleapis.com/upload/youtube/v3/videos
   
   Headers:
     Authorization: Bearer {oauth_token}
   
   Body:
     snippet:
       title: {humanized title}
       description: {humanized description}
       tags: {keywords}
       categoryId: 22  # People & Blogs
     status:
       privacyStatus: public
       selfDeclaredMadeForKids: false
   ```

8. **Update Metadata & Move File**
   ```python
   metadata["uploads"] = {
     "tiktok": {
       "url": "https://tiktok.com/@calmorarelief/video/123456",
       "uploaded_at": "2026-03-24T22:05:00Z",
       "status": "success"
     },
     "instagram": {...},
     "youtube": {...}
   }
   
   # Move video
   Dropbox: /CALMORA/queue/video001.mp4
         → /CALMORA/uploaded/2026-03-24/calmora-20260324-a7f3.mp4
   ```

9. **Telegram Notification**
   ```
   🎬 Video Distributed!
   
   📹 calmora-20260324-a7f3
   
   ✅ TikTok: "POV: Your back pain disappears..."
      https://tiktok.com/@calmorarelief/video/123456
   
   ✅ Instagram: "The stretch that saved my back"
      https://instagram.com/p/abc123/
   
   ✅ YouTube: "Fix Lower Back Pain in 3 Minutes"
      https://youtube.com/shorts/xyz789
   
   ⏱ Total: 2 min 34 sec
   ```

---

## 📊 METADATA TRACKING

### **File Structure:**

```
/root/.openclaw/workspace/.state/videos/
  calmora-20260324-a7f3.json
  calmora-20260324-b9e1.json
  moneystack-20260324-c4d2.json
```

### **Metadata Schema:**

```json
{
  "video_id": "calmora-20260324-a7f3",
  "channel": "CALMORA",
  "original_filename": "back-stretch.mp4",
  "dropbox_path": "/CALMORA/uploaded/2026-03-24/calmora-20260324-a7f3.mp4",
  "transcription": "If you've been sitting at a desk all day...",
  "duration": 45,
  "file_size_mb": 12.3,
  "created": "2026-03-24T22:00:00Z",
  
  "platforms": {
    "tiktok": {
      "title": "POV: Your back pain disappears in 60 seconds 🔥",
      "caption": "For everyone who sits 8+ hours. Try it tonight.",
      "hashtags": ["backpain", "relief", "wellness", "stretching"],
      "url": "https://tiktok.com/@calmorarelief/video/123456",
      "uploaded_at": "2026-03-24T22:05:00Z",
      "status": "live"
    },
    "instagram": {
      "title": "The stretch that saved my back",
      "caption": "I used to take ibuprofen every day 💊\n\nThen I found this 3-minute routine.",
      "hashtags": ["backpainrelief", "desklife", "wellness"],
      "url": "https://instagram.com/p/abc123/",
      "uploaded_at": "2026-03-24T22:07:00Z",
      "status": "live"
    },
    "youtube": {
      "title": "Fix Lower Back Pain in 3 Minutes (No Equipment)",
      "description": "Simple stretch for desk workers...\n\n🛒 Get it: calmorarelief.com",
      "tags": ["back pain", "lower back", "stretching", "pain relief"],
      "url": "https://youtube.com/shorts/xyz789",
      "uploaded_at": "2026-03-24T22:10:00Z",
      "video_id": "xyz789",
      "status": "live"
    }
  },
  
  "performance": {
    "tiktok_views": 0,
    "instagram_views": 0,
    "youtube_views": 0,
    "total_engagement": 0,
    "last_checked": "2026-03-24T22:15:00Z"
  }
}
```

---

## 🔌 API REQUIREMENTS

### **1. Dropbox**
**Need:**
- App created at https://www.dropbox.com/developers/apps
- Access token with `files.content.read` and `files.content.write` permissions

**Setup time:** 5 minutes

---

### **2. OpenAI (Whisper)**
**Need:**
- API key from https://platform.openai.com/api-keys

**Already have?** (check `/root/.openclaw/workspace/.credentials/`)

---

### **3. TikTok**
**Need:**
- TikTok Developer account: https://developers.tiktok.com/
- Create app → get client_key and client_secret
- OAuth flow to get access_token

**Complexity:** Medium
**Setup time:** 15-20 min

---

### **4. Instagram**
**Need:**
- Instagram Business account (converted from personal)
- Facebook Developer account: https://developers.facebook.com/
- App with Instagram Graph API permissions
- Long-lived access token

**Complexity:** Medium-high (Facebook APIs are annoying)
**Setup time:** 20-30 min

---

### **5. YouTube**
**Need:**
- Google Cloud Project: https://console.cloud.google.com/
- Enable YouTube Data API v3
- OAuth 2.0 credentials (refresh token)

**Complexity:** Medium
**Setup time:** 15 min

---

## 🎯 N8N WORKFLOW (JSON)

### **Node Structure:**

```
1. Dropbox Trigger (poll every 5 min)
2. Extract Channel
3. Download Video
4. Whisper Transcription
5. Generate Titles (Claude)
6. Humanize TikTok Title
7. Humanize Instagram Caption
8. Humanize YouTube Description
9. Upload to TikTok
10. Upload to Instagram
11. Upload to YouTube
12. Save Metadata
13. Move Dropbox File
14. Telegram Notification
```

---

## 💻 SCRIPTS NEEDED

### **1. transcribe_video.py**
```python
#!/usr/bin/env python3
"""Extract audio and transcribe with Whisper"""
import os
import subprocess
from openai import OpenAI

def transcribe(video_path):
    # Extract audio
    audio_path = video_path.replace(".mp4", ".mp3")
    subprocess.run([
        "ffmpeg", "-i", video_path, 
        "-vn", "-ar", "16000", "-ac", "1",
        audio_path
    ], check=True)
    
    # Transcribe
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    
    os.remove(audio_path)
    return transcript.text
```

### **2. generate_content.py**
```python
#!/usr/bin/env python3
"""Generate platform-specific titles/descriptions"""
import os
import json
from anthropic import Anthropic

CHANNEL_CONTEXTS = {
    "CALMORA": {
        "niche": "Pain relief, wellness, health hacks",
        "audience": "Office workers, chronic pain sufferers, 25-45",
        "tone": "Empathetic, solution-focused, calming",
        "products": ["calmorarelief.com"],
        "avoid": ["Medical claims", "cure"]
    },
    "MONEYSTACK": {
        "niche": "Money psychology, savings, financial mental health",
        "audience": "Young professionals, students, 18-35",
        "tone": "Real talk, no BS, relatable",
        "products": [],
        "avoid": ["Get rich quick", "investment advice"]
    }
}

def generate_content(transcript, channel, duration):
    context = CHANNEL_CONTEXTS[channel]
    
    prompt = f"""You're writing social media content for {channel}.

**Channel context:**
- Niche: {context['niche']}
- Audience: {context['audience']}
- Tone: {context['tone']}

**Video transcript:**
"{transcript}"

**Duration:** {duration} seconds

Generate 3 unique titles and descriptions for each platform:

## TikTok (Viral/Hook)
- Title: 8-12 words max, emotional hook, 1 emoji
- Caption: 1-2 sentences, relatable pain point, 4-6 hashtags
- Hook formula: "POV:", "If you...", "When you..."

## Instagram Reels (Aspirational)
- Title: Brand-aligned, lifestyle angle
- Caption: Mini-story (2-3 sentences), emojis, 5-8 hashtags
- Style: Personal experience, transformation, community

## YouTube Shorts (Educational/SEO)
- Title: Keyword-rich, clear value prop, under 60 chars
- Description: What/why/how (3-4 sentences), product link if relevant, timestamps if >30sec
- Tags: 5-8 search keywords
- Category: Howto & Style OR People & Blogs

**RULES:**
1. Each platform = DIFFERENT angle (not just rewording)
2. Write like a human YouTuber/TikToker (casual, direct)
3. NO corporate speak: "innovative", "transformative", "serves as"
4. NO clickbait that misrepresents content
5. Match transcript tone and energy
6. Include product link ONLY in YouTube description

Output JSON only:
{{
  "tiktok": {{"title": "...", "caption": "...", "hashtags": [...]}},
  "instagram": {{"title": "...", "caption": "...", "hashtags": [...]}},
  "youtube": {{"title": "...", "description": "...", "tags": [...]}}
}}"""
    
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.content[0].text)
```

### **3. humanize_content.py**
```python
#!/usr/bin/env python3
"""Humanize AI-generated text"""
import subprocess
import json

def humanize(text):
    result = subprocess.run(
        ["python3", "/root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py", "-q"],
        input=text.encode(),
        capture_output=True
    )
    return result.stdout.decode().strip()

def humanize_all_content(content):
    """Humanize all platform texts"""
    
    # TikTok
    content["tiktok"]["title"] = humanize(content["tiktok"]["title"])
    content["tiktok"]["caption"] = humanize(content["tiktok"]["caption"])
    
    # Instagram
    content["instagram"]["title"] = humanize(content["instagram"]["title"])
    content["instagram"]["caption"] = humanize(content["instagram"]["caption"])
    
    # YouTube
    content["youtube"]["title"] = humanize(content["youtube"]["title"])
    content["youtube"]["description"] = humanize(content["youtube"]["description"])
    
    return content
```

### **4. upload_tiktok.py**
```python
#!/usr/bin/env python3
"""Upload video to TikTok"""
import requests

def upload_tiktok(video_path, title, caption):
    # TODO: TikTok API implementation
    # Requires TikTok OAuth token
    pass
```

### **5. upload_instagram.py**
```python
#!/usr/bin/env python3
"""Upload Reel to Instagram"""
import requests

def upload_instagram(video_url, caption, access_token, ig_account_id):
    # Step 1: Create container
    container_response = requests.post(
        f"https://graph.facebook.com/v18.0/{ig_account_id}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    container_id = container_response.json()["id"]
    
    # Step 2: Publish
    publish_response = requests.post(
        f"https://graph.facebook.com/v18.0/{ig_account_id}/media_publish",
        data={"creation_id": container_id},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    return publish_response.json()
```

### **6. upload_youtube.py**
```python
#!/usr/bin/env python3
"""Upload Short to YouTube"""
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_youtube(video_path, title, description, tags, credentials):
    youtube = build('youtube', 'v3', credentials=credentials)
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )
    
    return request.execute()
```

---

## 📈 PERFORMANCE TRACKING

### **Daily Stats Script** (optional)
```python
#!/usr/bin/env python3
"""Fetch performance stats for all uploaded videos"""

def check_video_stats():
    # Load all metadata files
    # For each video uploaded in last 7 days:
    #   - Fetch TikTok views
    #   - Fetch Instagram views
    #   - Fetch YouTube views
    # Update metadata files
    # Generate daily report
    pass
```

**Cron:** Daily at 11 PM
**Output:** Telegram report with best performers

---

## 💸 TOTAL COSTS

### **Per Video:**
- Whisper transcription: $0.0045
- Claude content gen: $0.003
- Humanize: $0 (local)
- **Total: $0.0075/video**

### **Monthly (60 videos):**
- 2 channels × 1 video/day × 30 days = 60 videos
- = **$0.45/month**

### **If 3 videos/day per channel:**
- 2 channels × 3 videos/day × 30 days = 180 videos
- = **$1.35/month**

**Basically free.**

---

## ⏱️ TIME PER VIDEO

**Total automation time:**
1. Dropbox detection: instant
2. Download: 10 sec
3. Transcription: 15 sec
4. AI generation: 8 sec
5. Humanize: 2 sec
6. Upload (parallel): 30 sec
7. Notification: 1 sec

**Total: ~60-90 seconds per video**

**Your time:** 0 seconds (just drop file)

---

## 🚀 IMPLEMENTATION PHASES

### **Phase 1: MVP (2 hours)**
1. Setup Dropbox app + access token
2. Setup OpenAI API key
3. Create n8n workflow (basic)
4. Test with 1 video → manual upload
5. Verify transcription + generation works

### **Phase 2: Platform APIs (3-4 hours)**
1. TikTok developer account + OAuth
2. Instagram Business + Facebook API
3. YouTube API + OAuth
4. Integrate uploads in n8n

### **Phase 3: Production (1 hour)**
1. Add metadata tracking
2. Add error handling
3. Add Telegram notifications
4. Test with real videos
5. Deploy

**Total implementation: ~6-7 hours**

---

## ❓ NEXT STEPS

**To start building, I need:**

1. **Which path:**
   - **Option A:** I build everything (n8n workflow + scripts)
   - **Option B:** I give you n8n JSON + you import/configure
   - **Option C:** I guide you step-by-step

2. **API access:**
   - Do you already have API keys for any platforms?
   - Or do I guide you through creating them?

3. **Timeline:**
   - Deploy this week?
   - Or just design for now, implement later?

---

**What do you want me to do first?**

— n0body ◼️
