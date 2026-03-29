# VIDEO DISTRIBUTION SYSTEM — SETUP GUIDE

**Status:** ✅ n8n installed, workflow ready
**Your task:** Add API keys → Test → Enable auto-upload

---

## 🎯 WHAT'S ALREADY DONE

✅ **n8n installed** on clawdb (Docker)
✅ **Workflow JSON created** (ready to import)
✅ **Support scripts created:**
  - `transcribe.py` (Whisper)
  - `generate-content.py` (Claude)
  - `humanize.py` (cleanup AI text)

✅ **humanize-ai-text skill installed**

---

## 🔑 STEP 1: ACCESS N8N

### **Open n8n:**
```
http://localhost:5678
```

**First time:**
1. Create owner account (email + password)
2. Skip onboarding tour

---

## 📥 STEP 2: IMPORT WORKFLOW

1. **Click** "+" (top right) → **Import from file**
2. **Select:** `/root/.openclaw/workspace/n8n-workflows/video-distribution.json`
3. **Import** → Workflow appears

**You'll see 12 nodes:**
- Dropbox Trigger
- Extract Channel
- Download Video
- Get Video Metadata
- Transcribe Audio
- Generate Content
- Humanize TikTok/Instagram/YouTube (3 nodes)
- Merge Humanized
- Build Metadata
- Save Metadata
- Telegram Notification

---

## 🔌 STEP 3: ADD CREDENTIALS

### **3.1: Dropbox**

**In n8n:**
1. Click **"Dropbox Trigger"** node
2. Click **"Create New Credential"**
3. Select **"Dropbox OAuth2 API"**

**Setup:**
1. Go to: https://www.dropbox.com/developers/apps
2. Click **"Create app"**
3. Choose:
   - API: **Scoped access**
   - Access: **Full Dropbox**
   - Name: `n8n-video-distribution`
4. **Permissions tab** → Enable:
   - `files.content.read`
   - `files.content.write`
   - `files.metadata.read`
5. Copy **App key** and **App secret**
6. **OAuth2 Redirect URIs** → Add: `http://localhost:5678/rest/oauth2-credential/callback`

**Back in n8n:**
- Paste App Key
- Paste App Secret
- Click **"Connect my account"**
- Authorize Dropbox

✅ **Test:** Should show green checkmark

---

### **3.2: OpenAI (Whisper)**

**Get API key:**
1. Go to: https://platform.openai.com/api-keys
2. Create new key → Copy

**In workspace:**
```bash
echo "sk-proj-YOUR_KEY_HERE" > /root/.openclaw/workspace/.credentials/openai-key.txt
```

---

### **3.3: OpenRouter (Claude)**

**Already have key:**
```
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
```

**Save to file:**
```bash
echo "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" > /root/.openclaw/workspace/.credentials/openrouter-key.txt
```

---

### **3.4: Telegram (already configured)**

**Bot token:** Already working
**Chat ID:** 8116230130

**Add to n8n environment:**
1. n8n → Settings → Environments
2. Add variable:
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: `YOUR_BOT_TOKEN`

---

## 📂 STEP 4: CREATE DROPBOX FOLDERS

**In your Dropbox:**

1. Create folders:
```
/Health-Hacks/
  queue/
  uploaded/

/MONEYSTACK/
  queue/
  uploaded/
```

2. **Test:** Upload any `.mp4` file to `/Health-Hacks/queue/`

---

## ✅ STEP 5: TEST MVP (No Uploads)

### **Activate workflow:**
1. In n8n, click **"Activate"** toggle (top right)
2. Workflow turns green

### **Test:**
1. Upload test video to: `/Health-Hacks/queue/test.mp4`
2. Wait 5 minutes (Dropbox polls every 5 min)
3. Check n8n → Executions tab
4. Should see:
   - ✅ Transcription
   - ✅ Generated content (3 platforms)
   - ✅ Humanized text
   - ✅ Metadata saved
   - ✅ Telegram notification

**Check metadata:**
```bash
cat /root/.openclaw/workspace/.state/videos/*.json | jq '.'
```

**Should show:**
- Video ID
- Transcription
- TikTok/Instagram/YouTube titles/descriptions
- All humanized

---

## 🚀 STEP 6: ADD UPLOAD NODES (Phase 2)

**Once MVP works, add 3 upload nodes:**

### **6.1: TikTok Upload Node**

**Prerequisites:**
1. TikTok Developer Account: https://developers.tiktok.com/
2. Create App → Enable "Content Posting API"
3. Get access token via OAuth

**In n8n:**
1. Add **HTTP Request** node after "Humanize TikTok"
2. Method: POST
3. URL: `https://open.tiktokapis.com/v2/post/publish/video/init/`
4. Headers:
   - `Authorization: Bearer {{ $env.TIKTOK_ACCESS_TOKEN }}`
   - `Content-Type: application/json`
5. Body:
```json
{
  "post_info": {
    "title": "={{ $json.tiktokTitle }}",
    "description": "={{ $json.tiktokCaption }}\n\n{{ $json.tiktokHashtags.map(t => '#' + t).join(' ') }}",
    "privacy_level": "PUBLIC_TO_EVERYONE"
  },
  "source_info": {
    "source": "FILE_UPLOAD"
  }
}
```

---

### **6.2: Instagram Upload Node**

**Prerequisites:**
1. Convert Instagram to Business Account
2. Connect to Facebook Page
3. Facebook Developer App: https://developers.facebook.com/
4. Enable Instagram Graph API
5. Get long-lived access token

**Challenge:** Instagram requires publicly accessible video URL

**Solution:** Add temp S3/R2 upload node before Instagram

**In n8n:**
1. Add **S3/R2 Upload** node → Get public URL
2. Add **HTTP Request** node:
   - POST to `https://graph.facebook.com/v18.0/{{ $env.INSTAGRAM_ACCOUNT_ID }}/media`
   - Body: `media_type=REELS`, `video_url={public_url}`, `caption=...`
3. Add second **HTTP Request** to publish container

---

### **6.3: YouTube Upload Node**

**Prerequisites:**
1. Google Cloud Project: https://console.cloud.google.com/
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Get refresh token

**In n8n:**
1. Add **HTTP Request** node after "Humanize YouTube"
2. Method: POST
3. URL: `https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status`
4. Headers:
   - `Authorization: Bearer {{ $env.YOUTUBE_ACCESS_TOKEN }}`
5. Body:
```json
{
  "snippet": {
    "title": "={{ $json.youtubeTitle }}",
    "description": "={{ $json.youtubeDescription }}\\n\\n#Shorts",
    "tags": "={{ $json.youtubeTags }}",
    "categoryId": "26"
  },
  "status": {
    "privacyStatus": "public",
    "selfDeclaredMadeForKids": false
  }
}
```

---

## 📋 API KEYS CHECKLIST

Copy this and fill in as you get keys:

```bash
# Dropbox (OAuth - done in n8n UI)
☐ Dropbox connected via OAuth

# OpenAI Whisper
☐ sk-proj-...

# OpenRouter (Claude)
☐ sk-or-v1-... (already have)

# TikTok
☐ TikTok access token

# Instagram  
☐ Instagram access token
☐ Instagram account ID
☐ S3/R2 bucket for temp hosting

# YouTube
☐ YouTube OAuth refresh token
☐ YouTube client ID
☐ YouTube client secret

# Telegram
☐ Bot token (already have)
```

---

## 🧪 TESTING PROTOCOL

### **Phase 1: MVP (Content Generation Only)**
1. Upload video to Dropbox/Health-Hacks/queue/
2. Wait 5 min
3. Check Telegram notification
4. Verify metadata JSON has titles/descriptions
5. **Manual:** Copy content and post to platforms yourself

**Goal:** Verify transcription + generation + humanization works

### **Phase 2: Add One Platform (TikTok)**
1. Setup TikTok API
2. Add upload node
3. Test with 1 video
4. Verify video goes live on TikTok

### **Phase 3: Add Remaining Platforms**
1. YouTube next (easier than Instagram)
2. Instagram last (requires S3)

---

## 🚨 TROUBLESHOOTING

### **n8n not accessible:**
```bash
docker ps | grep n8n
docker logs n8n
```

### **Workflow fails:**
1. Check n8n → Executions → Click failed execution
2. See which node failed
3. Check error message

### **Transcription fails:**
```bash
# Test script manually
python3 /root/.openclaw/workspace/scripts/video-distribution/transcribe.py /path/to/video.mp4
```

### **Humanize fails:**
```bash
# Test manually
echo "This innovative solution serves as..." | python3 /root/.openclaw/workspace/skills/humanize-ai-text/scripts/transform.py
```

---

## 📊 MONITORING

### **Check workflow executions:**
- n8n → Executions tab
- Filter by status (success/error)
- See logs for each execution

### **Check metadata files:**
```bash
ls -la /root/.openclaw/workspace/.state/videos/
cat /root/.openclaw/workspace/.state/videos/health_hacks-*.json | jq '.content'
```

### **Check Dropbox:**
- Videos should move from `/queue/` to `/uploaded/YYYY-MM-DD/`

---

## 🎯 CURRENT STATUS

**✅ DONE:**
- n8n installed and running
- Workflow JSON created (MVP version)
- Support scripts ready
- Metadata structure defined
- Telegram notifications configured

**⏳ TODO (Your part):**
1. Access n8n: http://localhost:5678
2. Import workflow JSON
3. Connect Dropbox OAuth
4. Add OpenAI API key
5. Test with 1 video

**⏳ TODO (Phase 2 - Later):**
1. Setup TikTok/Instagram/YouTube APIs
2. Add upload nodes
3. Enable full automation

---

## 💾 FILES CREATED

**Scripts:**
- `/root/.openclaw/workspace/scripts/video-distribution/transcribe.py`
- `/root/.openclaw/workspace/scripts/video-distribution/generate-content.py`
- `/root/.openclaw/workspace/scripts/video-distribution/humanize.py`

**Workflows:**
- `/root/.openclaw/workspace/n8n-workflows/video-distribution.json`

**Documentation:**
- `/root/.openclaw/workspace/n8n-video-distribution-workflow.md` (full design doc)
- `/root/.openclaw/workspace/VIDEO-DISTRIBUTION-SETUP.md` (this file)

**Metadata storage:**
- `/root/.openclaw/workspace/.state/videos/` (will be created on first run)

---

## ❓ NEXT STEP

**Open n8n and import the workflow:**

```
http://localhost:5678
```

1. Create account (first time)
2. Import `/root/.openclaw/workspace/n8n-workflows/video-distribution.json`
3. Connect Dropbox
4. Test with video

**Cuando esté importado, avísame y te ayudo con el resto.**

— n0body ◼️
