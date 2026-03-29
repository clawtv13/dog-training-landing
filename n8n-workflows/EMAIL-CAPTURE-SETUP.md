# n8n Email Capture Workflow - Step by Step

**Time:** 30 minutes
**Cost:** $0

---

## STEP 1: Access n8n

```
http://localhost:5678
```

Or via Cloudflare tunnel:
```
https://acm-indicate-attractions-prisoners.trycloudflare.com
```

---

## STEP 2: Create New Workflow

1. Click "+" (New Workflow)
2. Name: "CleverDog Email Capture"
3. Save

---

## STEP 3: Add Webhook Node

1. Click "Add first step"
2. Search: "Webhook"
3. Select "Webhook"
4. Configure:
   - **HTTP Method:** POST
   - **Path:** `email-capture`
   - **Respond:** Immediately
5. Click "Execute Node" to get webhook URL
6. **COPY THIS URL** - you'll need it for the website

**Example URL:**
```
https://acm-indicate-attractions-prisoners.trycloudflare.com/webhook/email-capture
```

---

## STEP 4: Add Google Sheets Node

1. Click "+" after Webhook
2. Search: "Google Sheets"
3. Select "Google Sheets"
4. Configure:
   - **Operation:** Append Row
   - **Credential:** Click "Create New" → Follow Google OAuth
   - **Document:** Create new sheet called "CleverDogMethod Emails"
   - **Sheet:** Sheet1
   - **Columns:**
     - Column A: `email` → `{{ $json.email }}`
     - Column B: `resource` → `{{ $json.resource }}`
     - Column C: `page` → `{{ $json.page }}`
     - Column D: `source` → `{{ $json.source }}`
     - Column E: `timestamp` → `{{ $now.format('YYYY-MM-DD HH:mm:ss') }}`

---

## STEP 5: Add Gmail Node

1. Click "+" after Google Sheets
2. Search: "Gmail"
3. Select "Gmail"
4. Configure:
   - **Operation:** Send Email
   - **Credential:** Click "Create New" → Follow Google OAuth
   - **To:** `{{ $json.email }}`
   - **Subject:** `Your Free Dog Training Guide Is Here! 🐕`
   - **Message (HTML):**

```html
<p>Hi there!</p>

<p>Thanks for downloading <strong>{{ $json.resource }}</strong>!</p>

<p>Your guide is attached to this email.</p>

<p><strong>Want complete dog training?</strong><br>
→ <a href="https://cleverdogmethod.com">Get The Full Program</a></p>

<p>Happy training!<br>
The Clever Dog Method Team</p>

<hr>
<p style="font-size: 12px; color: #999;">
You received this because you requested a free guide from cleverdogmethod.com
</p>
```

   - **Attachments:** (Skip for now - need to setup file access)

---

## STEP 6: Add Telegram Node

1. Click "+" after Gmail
2. Search: "Telegram"
3. Select "Telegram"
4. Configure:
   - **Operation:** Send Message
   - **Credential:** 
     - Bot Token: `8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU`
   - **Chat ID:** `8116230130`
   - **Message:**

```
🎉 New email signup!

📧 {{ $json.email }}
📁 Resource: {{ $json.resource }}
📍 From: {{ $json.page }}
🕒 {{ $now.format('YYYY-MM-DD HH:mm') }}

View all: [Google Sheets link]
```

---

## STEP 7: Activate Workflow

1. Click "Save" (top right)
2. Toggle "Active" (top right)
3. Workflow is now LIVE

---

## STEP 8: Update Website JavaScript

**Edit:** `/root/.openclaw/workspace/dog-training-landing-clean/js/email-handler.js`

**Find line ~40:**
```javascript
const response = await fetch('/api/subscribe', {
```

**Replace with:**
```javascript
const response = await fetch('https://acm-indicate-attractions-prisoners.trycloudflare.com/webhook/email-capture', {
```

*(Use YOUR actual webhook URL from Step 3)*

---

## STEP 9: Test

1. Visit: https://cleverdogmethod.com/free-resources.html
2. Click "Download Free PDF" on any resource
3. Enter test email
4. Submit

**Check:**
- ✅ Google Sheets: New row added
- ✅ Email received in inbox
- ✅ Telegram notification arrived

---

## OPTIONAL: Add PDF Attachments

**In Gmail node:**

1. Before Gmail node, add "Read Binary Files" node
2. Configure:
   - File Path: `/root/.openclaw/workspace/dog-training-landing-clean/resources/{{ $json.resource }}.pdf`
3. Connect to Gmail
4. Gmail node → Attachments: `{{ $binary.data }}`

**Requires:** n8n container needs access to workspace folder (volume mount)

---

## GOOGLE SHEETS SETUP

**Create spreadsheet:**
1. Go to: https://sheets.google.com
2. Create new: "CleverDogMethod Emails"
3. Headers (Row 1):
   - A1: Email
   - B1: Resource
   - C1: Page
   - D1: Source
   - E1: Timestamp

**Share with yourself** for easy access

---

## LIMITS - FREE TIER

**Gmail:**
- 500 emails/day
- 2,000 recipients/day

**Google Sheets:**
- 10M cells = ~50,000 emails with 5 columns
- Real limit: ~1M rows

**n8n:**
- Unlimited (self-hosted)

**Telegram:**
- Unlimited notifications

---

## ALTERNATIVE: Super Simple (No Email)

**If you just want to collect emails (no automatic PDF):**

**User flow:**
1. Submit email → Webhook → Google Sheets
2. PDF downloads directly (no email)
3. You export emails weekly to Mailchimp

**Removes Gmail node** - even simpler, still 100% gratis

---

## 🎯 MI RECOMENDACIÓN:

**Fase 1 (hoy - 10 min):**
- Webhook → Google Sheets → Telegram
- PDF download directo (sin email)

**Fase 2 (mañana):**
- Add Gmail node
- Send PDF por email

**Fase 3 (cuando >500 subs):**
- Migrate to Mailchimp/ConvertKit
- Email sequences

---

**TODO 100% GRATIS hasta llegar a 500 subscribers**

¿Empiezo con Fase 1 (webhook + sheets + telegram)?

— n0body ◼️