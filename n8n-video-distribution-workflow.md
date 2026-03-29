# N8N VIDEO DISTRIBUTION WORKFLOW
## Auto-upload videos to TikTok, Instagram, YouTube with unique content

**Version:** 1.0
**Date:** 2026-03-24
**Channels:** Health Hacks, MONEYSTACK

---

## 🏗️ ARCHITECTURE OVERVIEW

```
Dropbox Upload
    ↓
Detect Channel (folder path)
    ↓
Download Video → Extract Metadata
    ↓
Transcribe Audio (Whisper)
    ↓
Generate Content (AI - 3 platforms)
    ↓
Humanize Titles/Descriptions
    ↓
Upload to Platforms (parallel):
    → TikTok
    → Instagram
    → YouTube
    ↓
Save Metadata JSON
    ↓
Move Video to /uploaded/
    ↓
Telegram Notification
```

---

## 📂 DROPBOX FOLDER STRUCTURE

```
/Health-Hacks/
  queue/           ← Upload videos here
  uploaded/        ← Auto-moved after processing
    2026-03-24/
    2026-03-25/

/MONEYSTACK/
  queue/
  uploaded/
    2026-03-24/
```

**Naming:** Any filename works (no convention required)

---

## 🔌 N8N WORKFLOW NODES (18 total)

### **1. TRIGGER: Dropbox Poll**
**Node:** Dropbox Trigger
**Type:** Poll
**Interval:** Every 5 minutes
**Settings:**
```json
{
  "resource": "file",
  "event": "fileCreated",
  "path": "",
  "recursive": true,
  "includeMediaInfo": true,
  "simplify": true
}
```

**Filters:**
- File extension: `.mp4`, `.mov`, `.avi`
- Path contains: `/queue/`

**Output:**
```json
{
  "id": "id:abc123",
  "name": "video001.mp4",
  "path_display": "/Health-Hacks/queue/video001.mp4",
  "size": 12582912,
  "server_modified": "2026-03-24T22:00:00Z"
}
```

---

### **2. CODE: Extract Channel & Metadata**
**Node:** Code (JavaScript)
**Function:** Parse path, determine channel, generate video ID

```javascript
// Input: Dropbox file data
const file = $input.item.json;
const path = file.path_display;

// Extract channel from path
let channel = "UNKNOWN";
if (path.includes("/Health-Hacks/")) channel = "HEALTH_HACKS";
if (path.includes("/MONEYSTACK/")) channel = "MONEYSTACK";

// Generate unique video ID
const timestamp = new Date().toISOString().split('T')[0].replace(/-/g, '');
const randomId = Math.random().toString(36).substring(2, 6);
const videoId = `${channel.toLowerCase()}-${timestamp}-${randomId}`;

// Channel context
const channelContexts = {
  "HEALTH_HACKS": {
    "niche": "Pain relief, energy, sleep, stress, gut health, mental clarity",
    "audience": "Office workers, health-conscious adults 25-45",
    "tone": "Science-backed, practical, empathetic, no BS",
    "products": ["calmorarelief.com"],
    "youtubeHandle": "@HealthHacks",
    "tiktokHandle": "@healthhacks",
    "instagramHandle": "@healthhacks"
  },
  "MONEYSTACK": {
    "niche": "Money psychology, savings, financial mental health, anti-debt",
    "audience": "Young professionals, students 18-35",
    "tone": "Real talk, relatable, anti-hustle, honest",
    "products": [],
    "youtubeHandle": "@MONEYSTACK_YT",
    "tiktokHandle": "@moneystack",
    "instagramHandle": "@moneystack"
  }
};

return {
  json: {
    videoId: videoId,
    channel: channel,
    channelContext: channelContexts[channel],
    originalFilename: file.name,
    dropboxPath: file.path_display,
    fileSize: file.size,
    detectedAt: new Date().toISOString(),
    dropboxFileId: file.id
  }
};
```

**Output:**
```json
{
  "videoId": "health_hacks-20260324-a7f3",
  "channel": "HEALTH_HACKS",
  "channelContext": {...},
  "originalFilename": "video001.mp4",
  "dropboxPath": "/Health-Hacks/queue/video001.mp4"
}
```

---

### **3. DROPBOX: Download File**
**Node:** Dropbox - Download File
**Action:** Download
**Input:** `{{ $json.dropboxPath }}`
**Settings:**
```json
{
  "path": "={{ $json.dropboxPath }}",
  "options": {
    "binaryProperty": "videoData"
  }
}
```

**Output:** Binary data in `videoData` property

---

### **4. CODE: Get Video Duration**
**Node:** Code (Python)
**Function:** Extract video metadata (duration, resolution)

```python
import subprocess
import json

# Input video from binary data
video_path = "/tmp/video_temp.mp4"

# Save binary to file
binary_data = items[0].binary["videoData"]
with open(video_path, "wb") as f:
    f.write(binary_data.data)

# Get duration with ffprobe
result = subprocess.run([
    "ffprobe", "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    video_path
], capture_output=True, text=True)

duration = float(result.stdout.strip())

# Get resolution
result = subprocess.run([
    "ffprobe", "-v", "error",
    "-select_streams", "v:0",
    "-show_entries", "stream=width,height",
    "-of", "json",
    video_path
], capture_output=True, text=True)

metadata = json.loads(result.stdout)
width = metadata["streams"][0]["width"]
height = metadata["streams"][0]["height"]

return {
    "videoPath": video_path,
    "duration": round(duration, 1),
    "resolution": f"{width}x{height}",
    "aspectRatio": "vertical" if height > width else "horizontal"
}
```

**Output:**
```json
{
  "videoPath": "/tmp/video_temp.mp4",
  "duration": 45.2,
  "resolution": "1080x1920",
  "aspectRatio": "vertical"
}
```

---

### **5. HTTP: Transcribe with Whisper**
**Node:** HTTP Request
**Method:** POST
**URL:** `https://api.openai.com/v1/audio/transcriptions`
**Authentication:** Bearer Token
**Settings:**
```json
{
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "method": "POST",
  "url": "https://api.openai.com/v1/audio/transcriptions",
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "file",
        "value": "={{ $binary.videoData }}",
        "type": "file"
      },
      {
        "name": "model",
        "value": "whisper-1"
      },
      {
        "name": "language",
        "value": "en"
      }
    ]
  },
  "options": {
    "timeout": 60000
  }
}
```

**Headers:**
```
Authorization: Bearer sk-proj-YOUR_OPENAI_KEY
```

**Response:**
```json
{
  "text": "If you've been sitting at a desk all day and your lower back is killing you, this three minute stretch will change your life..."
}
```

---

### **6. CODE: Prepare AI Prompt**
**Node:** Code (JavaScript)
**Function:** Build prompt for content generation

```javascript
const channel = $node["Extract Channel"].json.channel;
const context = $node["Extract Channel"].json.channelContext;
const transcript = $node["Whisper"].json.text;
const duration = $node["Get Duration"].json.duration;

const prompt = `You're writing social media content for ${channel}.

**Channel context:**
- Niche: ${context.niche}
- Audience: ${context.audience}
- Tone: ${context.tone}

**Video transcript:**
"${transcript}"

**Duration:** ${duration} seconds

Generate 3 UNIQUE titles and descriptions for each platform. Each platform needs a DIFFERENT ANGLE (not just rewording).

## TikTok (Viral/Hook)
- Title: 8-12 words max, emotional hook, 1 emoji
- Caption: 1-2 sentences, relatable pain point, 4-6 hashtags
- Hook formula: "POV:", "If you...", "When you..."
- Goal: Stop scroll, high engagement

## Instagram Reels (Aspirational)
- Title: Brand-aligned, lifestyle angle
- Caption: Mini-story (2-3 sentences), emojis, 5-8 hashtags
- Style: Personal experience, transformation
- Goal: Save/share, community

## YouTube Shorts (Educational/SEO)
- Title: Keyword-rich, clear value, under 60 chars
- Description: What/why/how (3-4 sentences), timestamps if >30sec, CTA
- Tags: 5-8 search keywords
- Goal: Search ranking, watch time

**RULES:**
1. Each platform = DIFFERENT angle (POV vs story vs education)
2. Write like a real YouTuber/TikToker (casual, direct, human)
3. NO corporate speak: "innovative", "transformative", "serves as", "delve"
4. NO clickbait that misrepresents content
5. Match transcript tone and energy
6. ${context.products.length > 0 ? `Include link ONLY in YouTube: ${context.products[0]}` : 'No product links'}

Output ONLY valid JSON (no markdown):
{
  "tiktok": {"title": "...", "caption": "...", "hashtags": ["tag1", "tag2"]},
  "instagram": {"title": "...", "caption": "...", "hashtags": ["tag1", "tag2"]},
  "youtube": {"title": "...", "description": "...", "tags": ["tag1", "tag2"]}
}`;

return {
  json: {
    prompt: prompt,
    model: "claude-3-5-sonnet-20241022",
    maxTokens: 1500
  }
};
```

---

### **7. HTTP: Generate Content (Claude)**
**Node:** HTTP Request
**Method:** POST
**URL:** `https://api.anthropic.com/v1/messages`
**Settings:**
```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "authentication": "genericCredentialType",
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "model",
        "value": "={{ $json.model }}"
      },
      {
        "name": "max_tokens",
        "value": "={{ $json.maxTokens }}"
      },
      {
        "name": "messages",
        "value": "={{ [{\"role\": \"user\", \"content\": $json.prompt}] }}"
      }
    ]
  }
}
```

**Headers:**
```
x-api-key: YOUR_ANTHROPIC_KEY
anthropic-version: 2023-06-01
Content-Type: application/json
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"tiktok\": {...}, \"instagram\": {...}, \"youtube\": {...}}"
    }
  ]
}
```

---

### **8. CODE: Parse AI Response**
**Node:** Code (JavaScript)
**Function:** Extract JSON from AI response

```javascript
const aiResponse = $node["Claude"].json.content[0].text;

// Parse JSON (handle potential markdown wrappers)
let content;
try {
  content = JSON.parse(aiResponse);
} catch (e) {
  // Try removing markdown code blocks
  const cleaned = aiResponse.replace(/```json\n?/g, '').replace(/```\n?/g, '');
  content = JSON.parse(cleaned);
}

return {
  json: {
    rawContent: content,
    tiktokTitle: content.tiktok.title,
    tiktokCaption: content.tiktok.caption,
    tiktokHashtags: content.tiktok.hashtags,
    instagramTitle: content.instagram.title,
    instagramCaption: content.instagram.caption,
    instagramHashtags: content.instagram.hashtags,
    youtubeTitle: content.youtube.title,
    youtubeDescription: content.youtube.description,
    youtubeTags: content.youtube.tags
  }
};
```

---

### **9. CODE: Humanize TikTok Content**
**Node:** Code (Python)
**Function:** Run humanize-ai-text on TikTok title + caption

```python
import subprocess

title = items[0].json["tiktokTitle"]
caption = items[0].json["tiktokCaption"]

def humanize(text):
    result = subprocess.run(
        ["python3", "/root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py", "-q", "-a"],
        input=text.encode(),
        capture_output=True
    )
    return result.stdout.decode().strip()

humanized_title = humanize(title)
humanized_caption = humanize(caption)

return {
    "tiktokTitle": humanized_title,
    "tiktokCaption": humanized_caption
}
```

---

### **10. CODE: Humanize Instagram Content**
**Node:** Code (Python)
**Function:** Run humanize-ai-text on Instagram title + caption

```python
import subprocess

title = items[0].json["instagramTitle"]
caption = items[0].json["instagramCaption"]

def humanize(text):
    result = subprocess.run(
        ["python3", "/root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py", "-q", "-a"],
        input=text.encode(),
        capture_output=True
    )
    return result.stdout.decode().strip()

humanized_title = humanize(title)
humanized_caption = humanize(caption)

return {
    "instagramTitle": humanized_title,
    "instagramCaption": humanized_caption
}
```

---

### **11. CODE: Humanize YouTube Content**
**Node:** Code (Python)
**Function:** Run humanize-ai-text on YouTube title + description

```python
import subprocess

title = items[0].json["youtubeTitle"]
description = items[0].json["youtubeDescription"]

def humanize(text):
    result = subprocess.run(
        ["python3", "/root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py", "-q", "-a"],
        input=text.encode(),
        capture_output=True
    )
    return result.stdout.decode().strip()

humanized_title = humanize(title)
humanized_description = humanize(description)

return {
    "youtubeTitle": humanized_title,
    "youtubeDescription": humanized_description
}
```

---

### **12. HTTP: Upload to TikTok**
**Node:** HTTP Request
**Method:** POST
**URL:** TikTok Content Posting API
**Settings:**
```json
{
  "method": "POST",
  "url": "https://open.tiktokapis.com/v2/post/publish/video/init/",
  "authentication": "genericCredentialType",
  "sendBody": true,
  "bodyParameters": {
    "post_info": {
      "title": "={{ $json.tiktokTitle }}",
      "privacy_level": "PUBLIC_TO_EVERYONE",
      "disable_duet": false,
      "disable_comment": false,
      "disable_stitch": false,
      "video_cover_timestamp_ms": 1000
    },
    "source_info": {
      "source": "FILE_UPLOAD",
      "video_size": "={{ $node['Download Video'].json.fileSize }}",
      "chunk_size": 10000000,
      "total_chunk_count": 1
    }
  }
}
```

**Headers:**
```
Authorization: Bearer YOUR_TIKTOK_ACCESS_TOKEN
Content-Type: application/json
```

**Note:** TikTok requires 2-step upload:
1. Initialize upload → get upload_url
2. Upload video chunks to upload_url
3. Publish post

---

### **13. HTTP: Upload to Instagram**
**Node:** HTTP Request (2-step)
**Method:** POST
**URL:** Instagram Graph API

**Step 1: Create Media Container**
```json
{
  "method": "POST",
  "url": "https://graph.facebook.com/v18.0/{{ $env.INSTAGRAM_ACCOUNT_ID }}/media",
  "sendBody": true,
  "bodyParameters": {
    "media_type": "REELS",
    "video_url": "={{ $node['Upload to Temp Host'].json.publicUrl }}",
    "caption": "={{ $json.instagramCaption }}\n\n{{ $json.instagramHashtags.map(h => '#' + h).join(' ') }}"
  }
}
```

**Step 2: Publish Container**
```json
{
  "method": "POST",
  "url": "https://graph.facebook.com/v18.0/{{ $env.INSTAGRAM_ACCOUNT_ID }}/media_publish",
  "sendBody": true,
  "bodyParameters": {
    "creation_id": "={{ $node['Create Container'].json.id }}"
  }
}
```

**Headers:**
```
Authorization: Bearer YOUR_INSTAGRAM_ACCESS_TOKEN
```

**Note:** Instagram requires publicly accessible video URL (use temp S3/Cloudflare R2)

---

### **14. HTTP: Upload to YouTube**
**Node:** HTTP Request (resumable upload)
**Method:** POST
**URL:** YouTube Data API v3

**Step 1: Initialize Upload**
```json
{
  "method": "POST",
  "url": "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
  "sendBody": true,
  "bodyParameters": {
    "snippet": {
      "title": "={{ $json.youtubeTitle }}",
      "description": "={{ $json.youtubeDescription }}",
      "tags": "={{ $json.youtubeTags }}",
      "categoryId": "26"
    },
    "status": {
      "privacyStatus": "public",
      "selfDeclaredMadeForKids": false
    }
  }
}
```

**Step 2: Upload Video Bytes**
(Use resumable upload URL from Step 1 response)

**Headers:**
```
Authorization: Bearer YOUR_YOUTUBE_OAUTH_TOKEN
Content-Type: application/json
```

**Note:** YouTube Shorts require #Shorts in title or description + vertical aspect ratio

---

### **15. CODE: Build Metadata JSON**
**Node:** Code (JavaScript)
**Function:** Compile all upload results

```javascript
const videoId = $node["Extract Channel"].json.videoId;
const channel = $node["Extract Channel"].json.channel;
const transcript = $node["Whisper"].json.text;
const duration = $node["Get Duration"].json.duration;

const tiktokResult = $node["Upload TikTok"].json;
const instagramResult = $node["Upload Instagram"].json;
const youtubeResult = $node["Upload YouTube"].json;

const metadata = {
  video_id: videoId,
  channel: channel,
  original_filename: $node["Extract Channel"].json.originalFilename,
  dropbox_path: $node["Extract Channel"].json.dropboxPath,
  
  video_info: {
    duration: duration,
    resolution: $node["Get Duration"].json.resolution,
    file_size_mb: Math.round($node["Download Video"].json.fileSize / 1048576 * 10) / 10
  },
  
  transcription: transcript,
  
  platforms: {
    tiktok: {
      title: $node["Humanize TikTok"].json.tiktokTitle,
      caption: $node["Humanize TikTok"].json.tiktokCaption,
      hashtags: $node["Parse AI"].json.tiktokHashtags,
      url: tiktokResult.share_url || "pending",
      video_id: tiktokResult.video_id || null,
      uploaded_at: new Date().toISOString(),
      status: tiktokResult.status || "success"
    },
    instagram: {
      title: $node["Humanize Instagram"].json.instagramTitle,
      caption: $node["Humanize Instagram"].json.instagramCaption,
      hashtags: $node["Parse AI"].json.instagramHashtags,
      url: instagramResult.permalink || "pending",
      media_id: instagramResult.id || null,
      uploaded_at: new Date().toISOString(),
      status: instagramResult.id ? "success" : "pending"
    },
    youtube: {
      title: $node["Humanize YouTube"].json.youtubeTitle,
      description: $node["Humanize YouTube"].json.youtubeDescription,
      tags: $node["Parse AI"].json.youtubeTags,
      url: `https://youtube.com/shorts/${youtubeResult.id}`,
      video_id: youtubeResult.id,
      uploaded_at: new Date().toISOString(),
      status: "success"
    }
  },
  
  created: new Date().toISOString(),
  processed_at: new Date().toISOString()
};

return { json: metadata };
```

---

### **16. WRITE FILE: Save Metadata**
**Node:** Write Binary File
**Function:** Save metadata JSON to workspace

**Settings:**
```json
{
  "fileName": "={{ $node['Extract Channel'].json.videoId }}.json",
  "filePath": "/root/.openclaw/workspace/.state/videos/",
  "dataPropertyName": "data"
}
```

**Code to prepare data:**
```javascript
const metadata = $node["Build Metadata"].json;
return {
  json: {
    data: Buffer.from(JSON.stringify(metadata, null, 2))
  }
};
```

---

### **17. DROPBOX: Move to Uploaded**
**Node:** Dropbox - Move File
**Function:** Move from /queue/ to /uploaded/YYYY-MM-DD/

**Settings:**
```javascript
// Source
const sourcePath = $node["Extract Channel"].json.dropboxPath;

// Destination
const channel = $node["Extract Channel"].json.channel;
const date = new Date().toISOString().split('T')[0];
const videoId = $node["Extract Channel"].json.videoId;
const ext = sourcePath.split('.').pop();

const destPath = `/${channel}/uploaded/${date}/${videoId}.${ext}`;

return {
  from_path: sourcePath,
  to_path: destPath
};
```

---

### **18. HTTP: Send Telegram Notification**
**Node:** HTTP Request
**Method:** POST
**URL:** `https://api.telegram.org/bot{{ $env.TELEGRAM_BOT_TOKEN }}/sendMessage`

**Settings:**
```javascript
const metadata = $node["Build Metadata"].json;
const videoId = metadata.video_id;

const message = `🎬 **Video Distributed!**

📹 \`${videoId}\`

✅ **TikTok:** "${metadata.platforms.tiktok.title}"
   ${metadata.platforms.tiktok.url}

✅ **Instagram:** "${metadata.platforms.instagram.title}"
   ${metadata.platforms.instagram.url}

✅ **YouTube:** "${metadata.platforms.youtube.title}"
   ${metadata.platforms.youtube.url}

⏱ Duration: ${metadata.video_info.duration}s
📊 Channel: ${metadata.channel}

🔗 Metadata saved: \`.state/videos/${videoId}.json\``;

return {
  json: {
    chat_id: "8116230130",
    text: message,
    parse_mode: "Markdown"
  }
};
```

---

## 🔧 N8N WORKFLOW CONNECTIONS

```
[Dropbox Trigger]
    ↓
[Extract Channel]
    ↓
[Download File] ← (needs dropboxPath)
    ↓
[Get Duration] ← (needs binary videoData)
    ↓
[Whisper Transcribe] ← (needs binary videoData)
    ↓
[Prepare AI Prompt] ← (needs transcript, channel, duration)
    ↓
[Claude Generate] ← (needs prompt)
    ↓
[Parse AI Response]
    ↓
[Split into 3 parallel branches]
    ├─→ [Humanize TikTok] → [Upload TikTok]
    ├─→ [Humanize Instagram] → [Temp Host] → [Upload Instagram]
    └─→ [Humanize YouTube] → [Upload YouTube]
    ↓
[Wait for all 3] (Merge node)
    ↓
[Build Metadata]
    ↓
[Save Metadata File]
    ↓
[Move Dropbox File]
    ↓
[Telegram Notification]
```

---

## 🔑 REQUIRED CREDENTIALS

### **1. Dropbox**
**Type:** OAuth2
**Steps:**
1. Create app: https://www.dropbox.com/developers/apps
2. Get App key + App secret
3. OAuth redirect: `https://your-n8n.com/rest/oauth2-credential/callback`
4. Permissions: `files.content.read`, `files.content.write`, `files.metadata.read`

### **2. OpenAI (Whisper)**
**Type:** API Key
**URL:** https://platform.openai.com/api-keys
**Format:** `sk-proj-...`

### **3. Anthropic (Claude)**
**Type:** API Key
**URL:** https://console.anthropic.com/settings/keys
**Format:** `sk-ant-...`
**Or use OpenRouter:** `sk-or-v1-...`

### **4. TikTok**
**Type:** OAuth2
**Complexity:** Medium
**Steps:**
1. Register developer account: https://developers.tiktok.com/
2. Create app → Select "Content Posting API"
3. Get Client Key + Client Secret
4. Implement OAuth flow (user authorizes app)
5. Get access_token + refresh_token

**Scopes needed:**
- `video.upload`
- `video.publish`

**Note:** TikTok requires individual account authorization (each user must approve)

### **5. Instagram**
**Type:** OAuth2 (Facebook)
**Complexity:** High (most annoying API)
**Steps:**
1. Convert personal Instagram → Business account
2. Connect to Facebook Page
3. Create Facebook App: https://developers.facebook.com/apps/
4. Add Instagram Graph API product
5. Generate long-lived access token
6. Get Instagram Account ID

**Permissions needed:**
- `instagram_basic`
- `instagram_content_publish`
- `pages_read_engagement`

**Note:** Instagram requires video to be publicly accessible (can't upload directly)

**Workaround:** Upload to temp S3/Cloudflare R2 → give Instagram the URL → Instagram downloads it

### **6. YouTube**
**Type:** OAuth2 (Google)
**Complexity:** Medium
**Steps:**
1. Create Google Cloud Project: https://console.cloud.google.com/
2. Enable YouTube Data API v3
3. Create OAuth 2.0 Client ID (Web application)
4. Get refresh_token via OAuth flow
5. Exchange for access_token (expires every hour)

**Scopes needed:**
- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube`

### **7. Telegram (Notifications)**
**Type:** Bot Token
**Already have:** Bot token in credentials
**Format:** `bot{TOKEN}`

### **8. Temp File Host (for Instagram)**
**Need:** S3 bucket or Cloudflare R2
**Why:** Instagram can't accept direct file upload, needs public URL
**Alternatives:**
- AWS S3 (pay-as-you-go)
- Cloudflare R2 (10GB free/month)
- DigitalOcean Spaces ($5/mo)

---

## ⚙️ N8N ENVIRONMENT VARIABLES

Add to n8n settings:

```bash
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
TIKTOK_ACCESS_TOKEN=...
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_ACCOUNT_ID=...
YOUTUBE_REFRESH_TOKEN=...
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
TELEGRAM_BOT_TOKEN=...
S3_BUCKET=...
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
```

---

## 🚨 ERROR HANDLING

### **Add Error Triggers:**

**After each upload node:**
```javascript
// Check if upload failed
if ($node["Upload TikTok"].error || !$node["Upload TikTok"].json.video_id) {
  // Send error notification
  return {
    error: true,
    platform: "TikTok",
    message: $node["Upload TikTok"].error || "Upload failed"
  };
}
```

**Error Notification:**
```
❌ Upload Failed

Platform: TikTok
Video: health_hacks-20260324-a7f3
Error: Rate limit exceeded

Video saved for manual retry.
```

---

## 💾 METADATA STORAGE

**Files:** `/root/.openclaw/workspace/.state/videos/`

**Example:** `health_hacks-20260324-a7f3.json`

**Schema:**
```json
{
  "video_id": "health_hacks-20260324-a7f3",
  "channel": "HEALTH_HACKS",
  "original_filename": "back-pain-video.mp4",
  "dropbox_path": "/Health-Hacks/uploaded/2026-03-24/health_hacks-20260324-a7f3.mp4",
  
  "video_info": {
    "duration": 45.2,
    "resolution": "1080x1920",
    "file_size_mb": 12.3
  },
  
  "transcription": "If you've been sitting at a desk all day...",
  
  "platforms": {
    "tiktok": {
      "title": "POV: Your back pain disappears in 60 seconds",
      "caption": "For everyone who sits 8+ hours...",
      "hashtags": ["backpain", "relief", "wellness"],
      "url": "https://tiktok.com/@healthhacks/video/123456",
      "video_id": "123456",
      "uploaded_at": "2026-03-24T22:05:00Z",
      "status": "live"
    },
    "instagram": {
      "title": "The stretch that saved my back",
      "caption": "I used to take ibuprofen...",
      "hashtags": ["backpainrelief", "wellness"],
      "url": "https://instagram.com/p/abc123/",
      "media_id": "abc123",
      "uploaded_at": "2026-03-24T22:07:00Z",
      "status": "live"
    },
    "youtube": {
      "title": "Fix Lower Back Pain in 3 Minutes",
      "description": "Simple stretch for desk workers...",
      "tags": ["back pain", "stretching"],
      "url": "https://youtube.com/shorts/xyz789",
      "video_id": "xyz789",
      "uploaded_at": "2026-03-24T22:10:00Z",
      "status": "live"
    }
  },
  
  "created": "2026-03-24T22:00:00Z",
  "processed_at": "2026-03-24T22:10:23Z"
}
```

---

## 📊 PERFORMANCE TRACKING (Optional Phase 2)

**Add daily cron to fetch stats:**

```python
#!/usr/bin/env python3
"""Fetch video performance stats"""

import json
import requests
from pathlib import Path

VIDEOS_DIR = Path("/root/.openclaw/workspace/.state/videos")

def update_stats():
    for metadata_file in VIDEOS_DIR.glob("*.json"):
        with open(metadata_file) as f:
            metadata = json.load(f)
        
        # Fetch TikTok views
        if metadata["platforms"]["tiktok"]["video_id"]:
            # TikTok API call
            pass
        
        # Fetch Instagram views
        if metadata["platforms"]["instagram"]["media_id"]:
            # Instagram Graph API call
            pass
        
        # Fetch YouTube views
        if metadata["platforms"]["youtube"]["video_id"]:
            # YouTube Data API call
            pass
        
        # Update metadata file
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
```

**Cron:** `0 23 * * *` (daily at 11 PM)

---

## ⏱️ TIMING & PERFORMANCE

### **Workflow execution time:**
1. Trigger & download: 10 sec
2. Transcription (Whisper): 15 sec
3. AI generation (Claude): 8 sec
4. Humanize (3 parallel): 5 sec
5. Uploads (parallel): 30-45 sec
6. Metadata + notification: 5 sec

**Total: ~70-90 seconds per video**

### **Rate limits to consider:**
- **TikTok:** 50 posts/day per account
- **Instagram:** 25 Reels/day recommended (no hard limit)
- **YouTube:** 6 uploads/day for unverified accounts, unlimited after verification

### **Costs:**
- Whisper: $0.0045/video
- Claude: $0.003/video
- Humanize: $0 (local)
- **Total: $0.0075/video**

**Monthly (60 videos):** $0.45
**Monthly (180 videos):** $1.35

---

## 🚀 DEPLOYMENT OPTIONS

### **Option A: n8n Cloud**
**Pros:**
- ✅ Zero maintenance
- ✅ HTTPS automatic
- ✅ Fast setup (30 min)

**Cons:**
- ❌ 20K executions/month limit (free tier)
- ❌ Can't run local Python scripts easily

**Cost:**
- Free: 20K executions
- Starter ($20/mo): 100K executions

### **Option B: Self-Hosted n8n (Docker)**
**Pros:**
- ✅ Unlimited executions
- ✅ Can run local scripts (humanize-ai-text)
- ✅ Full control

**Cons:**
- ❌ Need server (VPS or this machine)
- ❌ Manual updates

**Install on clawdb:**
```bash
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -v /root/.openclaw/workspace:/workspace \
  n8nio/n8n
```

**Access:** http://localhost:5678 (or setup reverse proxy for HTTPS)

### **Option C: Hybrid (n8n Cloud + Webhook to Local)**
**Flow:**
- n8n Cloud: Handles Dropbox trigger, API calls
- Local script: Humanize + metadata (called via webhook)

**Pros:** Best of both worlds
**Cons:** Slightly more complex

---

## 📋 IMPLEMENTATION CHECKLIST

### **Phase 1: Core Workflow (No Uploads)**
- [ ] Install n8n (Cloud or Docker)
- [ ] Configure Dropbox trigger
- [ ] Add OpenAI credentials (Whisper)
- [ ] Add Anthropic/OpenRouter credentials (Claude)
- [ ] Test: Upload video → Get transcription + generated content
- [ ] Verify humanize script works in n8n

**Time:** 1-2 hours
**Outcome:** See generated titles/descriptions, no actual uploads

### **Phase 2: Platform APIs**
- [ ] Setup TikTok Developer App + OAuth
- [ ] Setup Instagram Business + Facebook API
- [ ] Setup YouTube API + OAuth
- [ ] Get all access tokens working
- [ ] Test manual API calls (outside n8n)

**Time:** 3-4 hours (Instagram is painful)
**Outcome:** Can manually post via API

### **Phase 3: Full Integration**
- [ ] Add upload nodes to n8n
- [ ] Add temp file hosting (for Instagram)
- [ ] Configure error handling
- [ ] Add metadata tracking
- [ ] Add Telegram notifications
- [ ] Test end-to-end with real video

**Time:** 2-3 hours
**Outcome:** Fully automated distribution

### **Phase 4: Monitoring (Optional)**
- [ ] Stats tracking script
- [ ] Daily performance report
- [ ] Alert on viral video (>10K views)

**Time:** 1 hour

**Total implementation: 8-10 hours**

---

## 🎯 QUICK START (Recommended Path)

### **Week 1: MVP without uploads**
1. Install n8n self-hosted on clawdb
2. Setup Dropbox trigger + Whisper + Claude
3. Generate content and review manually
4. Test humanize integration

**You:** Still upload manually, but system generates content

### **Week 2: Add TikTok**
1. Setup TikTok API (easiest of the 3)
2. Add upload node
3. Test with real video

**You:** Auto TikTok, manual Instagram + YouTube

### **Week 3: Add YouTube**
1. Setup YouTube API
2. Add upload node
3. Test

**You:** Auto TikTok + YouTube, manual Instagram

### **Week 4: Add Instagram**
1. Setup Instagram API (most annoying)
2. Setup temp hosting (S3/R2)
3. Complete workflow

**You:** Fully automated 🎉

---

## ❓ NEXT STEPS

**To start building:**

1. **Choose deployment:**
   - n8n Cloud (easy, limited)
   - Self-hosted on clawdb (unlimited)

2. **API priority:**
   - Start with TikTok only?
   - Or setup all 3 at once?

3. **Timeline:**
   - MVP this week?
   - Or design now, implement later?

---

**What do you want to do first?**

— n0body ◼️
