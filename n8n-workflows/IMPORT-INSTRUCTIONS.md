# n8n Email Capture - Import Instructions

**Time Required:** 5-10 minutes
**Cost:** $0

---

## 🔗 STEP 1: Open n8n

**New Tunnel URL:**
```
https://writing-majority-drink-brad.trycloudflare.com
```

*(This tunnel stays active as long as server is running)*

---

## 📥 STEP 2: Import Workflow

1. Click **"Workflows"** (left sidebar)
2. Click **"+"** → **"Import from File"**
3. Upload or paste content from:
   ```
   /root/.openclaw/workspace/n8n-workflows/cleverdogmethod-email-capture.json
   ```
4. Click **"Import"**

---

## 🔐 STEP 3: Setup Telegram Credentials

1. Click on **"Notify Telegram"** node (red, needs credentials)
2. Click **"Credential to connect with"** dropdown
3. Click **"+ Create New Credential"**
4. Enter:
   - **Access Token:** `8318289285:AAGFvnbGoLh0uXO9Rcz9N23iW25DEYh-BBU`
5. Click **"Save"**
6. Click **"Save"** on node

---

## 🌐 STEP 4: Get Webhook URL

1. Click on **"Webhook"** node (first node)
2. Click **"Listen for Test Event"**
3. **COPY the webhook URL** (looks like):
   ```
   https://writing-majority-drink-brad.trycloudflare.com/webhook/cleverdogmethod-email
   ```
4. **Save this URL** - you'll need it for website

---

## ✅ STEP 5: Activate Workflow

1. Click **"Save"** (top right)
2. Toggle **"Active"** switch (top right) to ON
3. Workflow is now LIVE and listening

---

## 🌐 STEP 6: Update Website

**Edit:** `/root/.openclaw/workspace/dog-training-landing-clean/free-resources.html`

**Find line ~179:**
```javascript
// Send to backend (implement later)
console.log('Email captured:', data);
```

**Replace with:**
```javascript
// Send to n8n webhook
try {
    const response = await fetch('https://writing-majority-drink-brad.trycloudflare.com/webhook/cleverdogmethod-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        console.error('Webhook failed:', response.status);
    }
} catch (err) {
    console.error('Webhook error:', err);
}
```

---

## 🧪 STEP 7: Test

1. Visit: https://cleverdogmethod.com/free-resources.html
2. Click any "Download Free PDF"
3. Enter test email: `test@example.com`
4. Submit

**Check:**
- ✅ You receive Telegram notification
- ✅ CSV file created: Check n8n container `/data/cleverdogmethod-emails.csv`
- ✅ Success message shown on website

---

## 📁 WHERE EMAILS ARE STORED

**File:** `/data/cleverdogmethod-emails.csv` (inside n8n container)

**To view:**
```bash
docker exec n8n cat /data/cleverdogmethod-emails.csv
```

**To export:**
```bash
docker exec n8n cat /data/cleverdogmethod-emails.csv > ~/cleverdogmethod-emails.csv
```

---

## 🔄 HOW IT WORKS

```
User submits email
    ↓
Webhook receives POST
    ↓
Format data node cleans input
    ↓
Save to CSV file (persistent in n8n volume)
    ↓
Telegram notification to you
    ↓
User sees success message + downloads PDF
```

---

## 📊 VIEW COLLECTED EMAILS

**From command line:**
```bash
docker exec n8n cat /data/cleverdogmethod-emails.csv | wc -l
```

**From n8n UI:**
1. Go to **"Executions"** tab
2. See all captured emails with full data

---

## ➕ OPTIONAL: Add Gmail Node (Later)

**To send PDFs via email:**

1. Add node between "Format Data" and "Telegram"
2. Node type: **Gmail**
3. Operation: **Send Email**
4. Configure:
   - To: `={{ $json.email }}`
   - Subject: `Your Free Dog Training Guide`
   - Message: Welcome email body
   - Attachments: Upload PDF or use HTTP Request node to fetch

**Requires:** Gmail OAuth credentials (easy setup in n8n)

---

## 🚨 IMPORTANT: Tunnel Persistence

**Current tunnel expires when:**
- Server restarts
- Cloudflared process dies

**Solutions:**

**Option A: Keep current tunnel alive**
```bash
# Add to crontab
@reboot nohup cloudflared tunnel --url http://localhost:5678 > /root/n8n-tunnel.log 2>&1 &
```

**Option B: Use Cloudflare Tunnel (permanent)**
- Free permanent subdomain
- Survives restarts
- 15 min setup

**Option C: Use ngrok (free tier)**
- 1 free tunnel
- Persistent URLs available

**For now:** Current tunnel works, revisit if it dies

---

## 📝 SUMMARY

**What you're importing:**
- ✅ Webhook endpoint for email capture
- ✅ CSV storage (persistent in n8n Docker volume)
- ✅ Telegram notifications
- ✅ Ready to activate

**Total time:** 10 minutes
**Total cost:** $0

---

**Ready to import? Open n8n and follow Step 2!**
