# AUTO-UPLOAD SYSTEM — SETUP GUIDE

_Created: 2026-03-21_

---

## 🎯 Objetivo

Sistema que permite:
```
Tú: "Sube este video a CALMORA"
[Envías video.mp4 por Telegram]

Yo: Auto-subo a YouTube + TikTok + Instagram
     con copy optimizado
```

---

## 📋 PREREQUISITOS (TU PARTE):

### 1. YouTube API Access

**Steps:**
1. Go to: https://console.cloud.google.com/
2. Create new project: "Content Upload Bot"
3. Enable: **YouTube Data API v3**
4. Create **OAuth 2.0 credentials**:
   - Application type: Desktop app
   - Name: "CALMORA Uploader"
5. Download JSON (client_secret.json)
6. Share credentials with me

**Scopes needed:**
- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube`

---

### 2. TikTok Developer Access

**Option A: Official API (Mejor)**

**Steps:**
1. Go to: https://developers.tiktok.com/
2. Create account
3. Create app
4. Request: **Content Posting API** access
   - Approval takes 1-3 days
5. Get: Client Key + Client Secret

**Requirements:**
- Business account (upgrade from personal)
- Explanation of use case

---

**Option B: Browser Automation (Más Rápido)**

Use Playwright to simulate browser:
- No API approval needed
- Works immediately
- Slightly less reliable

---

### 3. Instagram Access

**Option A: Meta Graph API (Oficial)**

**Steps:**
1. Create Facebook Page
2. Connect IG Business account to Page
3. Meta for Developers → Create app
4. Request permissions: `instagram_content_publish`
5. Get access token

**Requirements:**
- Instagram Business account
- Facebook Page
- App review (puede tardar)

---

**Option B: Playwright (Recomendado para start)**

Browser automation:
- No approval needed
- Works instantly
- Requires login session

---

## 🔧 IMPLEMENTATION OPTIONS:

### **TIER 1: Full API (Best Long-term)**

**Pros:**
- Official, stable
- No browser needed
- Scalable
- Reliable

**Cons:**
- Setup complejo
- Approval delays
- Rate limits

**Timeline:** 1-2 weeks setup

---

### **TIER 2: Hybrid (Recommended)**

**YouTube:** API (fácil de aprobar)  
**TikTok:** Playwright (mientras esperas API)  
**Instagram:** Playwright

**Pros:**
- Works in 2-3 días
- Migrate to APIs later

**Cons:**
- Playwright requiere maintenance

**Timeline:** 2-3 días functional

---

### **TIER 3: Buffer/Hootsuite Wrapper**

**Use existing service:**
- Buffer API
- Hootsuite API
- Later.com API

**Pros:**
- One integration = all platforms
- They handle auth
- Scheduling built-in

**Cons:**
- Monthly cost ($20-50)
- Less control

**Timeline:** 1 día setup

---

## 📊 MI RECOMENDACIÓN:

### **START: Tier 3 (Buffer)**

**Week 1:**
- [ ] Buffer account ($10/mo trial)
- [ ] Connect YouTube/TikTok/IG
- [ ] Test upload via Buffer API
- [ ] Working prototype

### **Week 2-3:**
- [ ] Integrate con Telegram
- [ ] Command: /upload [channel] [video]
- [ ] Auto-generate copy
- [ ] Production ready

### **Month 2:**
- [ ] Migrate YouTube a API nativa
- [ ] Request TikTok API access
- [ ] Keep Buffer como backup

---

## 💻 CÓDIGO BASE (Ya Creado):

**Script:** `/root/.openclaw/workspace/scripts/auto-upload-system.py`

**Status:**
- ✅ Structure completa
- ✅ Copy generation
- ⏳ API integrations (pending credentials)
- ⏳ Telegram handler

---

## 🎯 PRÓXIMOS PASOS:

**OPCIÓN A: Buffer (Rápido)**
1. Crea cuenta Buffer
2. Conecta canales
3. Dame API key
4. Functional en 1 día

**OPCIÓN B: APIs Nativas (Better)**
1. Setup Google Cloud
2. Request TikTok developer
3. 1-2 semanas setup
4. Mejor long-term

**OPCIÓN C: Hybrid Start**
1. Buffer para testing
2. APIs después
3. Best of both

---

**¿Cuál prefieres?** — n0body ◼️