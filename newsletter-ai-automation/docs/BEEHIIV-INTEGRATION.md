# Beehiiv Integration Guide

## Overview

Beehiiv offers powerful automation features but requires a hybrid approach: UI-based email creation + API-based enrollment and tracking.

---

## 🔑 API Setup

### 1. Get API Key

```bash
# Go to Beehiiv Dashboard → Settings → Integrations → API
# Copy your API key
export BEEHIIV_API_KEY="your_api_key_here"
```

### 2. Test Connection

```python
import requests

headers = {
    "Authorization": f"Bearer {BEEHIIV_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://api.beehiiv.com/v2/publications",
    headers=headers
)

print(response.json())
```

---

## 🏗️ Architecture: Hybrid Approach

### Why Hybrid?

Beehiiv's API has limitations:
- ❌ Cannot send emails directly via API
- ❌ Cannot create automation sequences via API
- ✅ Can enroll subscribers in existing automations
- ✅ Can manage subscriber data and custom fields

### Solution: UI + API

```
┌─────────────────────────────────────────┐
│         BEEHIIV UI                      │
│  (Create email sequences & templates)   │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         BEEHIIV API                     │
│  (Enroll subscribers, track data)       │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      LOCAL DATABASE (SQLite)            │
│  (Track engagement, triggers, metrics)  │
└─────────────────────────────────────────┘
```

---

## 📧 Setting Up Automations in Beehiiv UI

### Step 1: Create Automation Sequences

1. Go to **Automations** tab in Beehiiv
2. Click **Create Automation**
3. Choose **"Add by API"** as trigger
4. Build email sequence with delays

### Example: Welcome Sequence

```
Automation Name: "welcome-sequence"
Trigger: Add by API

Email 1 → Delay 0 days → "Welcome + Starter Kit"
Email 2 → Delay 2 days → "Quick Win Tutorial"
Email 3 → Delay 5 days → "Case Study"
Email 4 → Delay 7 days → "First Offer"
Email 5 → Delay 10 days → "Urgency"
```

### Step 2: Get Automation ID

After creating, click on automation → URL will show automation ID:
```
https://app.beehiiv.com/publications/[pub_id]/automations/[automation_id]
```

Save this `automation_id` for API calls.

---

## 🔗 API Endpoints

### Enroll Subscriber in Automation

```python
import requests

def enroll_in_automation(email, automation_id):
    url = f"https://api.beehiiv.com/v2/automations/{automation_id}/journey"
    
    headers = {
        "Authorization": f"Bearer {BEEHIIV_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": email
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Usage
result = enroll_in_automation("user@example.com", "auto_abc123")
print(result)
```

### Update Subscriber Custom Fields

```python
def update_subscriber(email, custom_fields):
    url = f"https://api.beehiiv.com/v2/subscriptions"
    
    headers = {
        "Authorization": f"Bearer {BEEHIIV_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": email,
        "custom_fields": custom_fields
    }
    
    response = requests.put(url, headers=headers, json=payload)
    return response.json()

# Usage
update_subscriber("user@example.com", {
    "engagement_score": 15,
    "segment": "active",
    "ltv": 97.00
})
```

### Get Subscriber Data

```python
def get_subscriber(email):
    url = f"https://api.beehiiv.com/v2/subscriptions"
    
    headers = {
        "Authorization": f"Bearer {BEEHIIV_API_KEY}"
    }
    
    params = {
        "email": email
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

---

## 🪝 Webhook Setup

Beehiiv can send webhooks for subscriber events:
- New subscription
- Email opened
- Email clicked
- Unsubscribe

### 1. Create Webhook Endpoint

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhooks/beehiiv', methods=['POST'])
def beehiiv_webhook():
    data = request.json
    
    event_type = data.get('event')
    email = data.get('email')
    
    if event_type == 'email.opened':
        # Track open
        tracker.record_open(
            email=email,
            sequence_name=data.get('automation_name'),
            step=data.get('email_index')
        )
    
    elif event_type == 'email.clicked':
        # Track click
        tracker.record_click(
            email=email,
            sequence_name=data.get('automation_name'),
            step=data.get('email_index'),
            url=data.get('url')
        )
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

### 2. Register Webhook in Beehiiv

Go to **Settings → Integrations → Webhooks**:
- URL: `https://yourdomain.com/webhooks/beehiiv`
- Events: Email Opened, Email Clicked
- Save

### 3. Secure Webhook (Optional)

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    computed = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(computed, signature)

# In webhook handler:
signature = request.headers.get('X-Beehiiv-Signature')
if not verify_webhook(request.data, signature, WEBHOOK_SECRET):
    return jsonify({"error": "Invalid signature"}), 401
```

---

## 🔄 Sync Strategy

### Daily Sync: Pull Data from Beehiiv

```python
import requests
from datetime import datetime

def sync_subscribers():
    """Pull all subscriber data from Beehiiv and update local DB"""
    
    url = "https://api.beehiiv.com/v2/subscriptions"
    headers = {"Authorization": f"Bearer {BEEHIIV_API_KEY}"}
    
    page = 1
    synced = 0
    
    while True:
        response = requests.get(
            url,
            headers=headers,
            params={"page": page, "limit": 100}
        )
        
        data = response.json()
        subscribers = data.get('data', [])
        
        if not subscribers:
            break
        
        # Update local database
        for sub in subscribers:
            update_local_subscriber(
                email=sub['email'],
                subscription_id=sub['id'],
                subscribed_at=sub['created_at'],
                custom_fields=sub.get('custom_fields', {})
            )
            synced += 1
        
        page += 1
    
    return synced

def update_local_subscriber(email, subscription_id, subscribed_at, custom_fields):
    conn = sqlite3.connect('email_sequences.db')
    c = conn.cursor()
    
    c.execute('''INSERT OR REPLACE INTO subscribers 
                 (email, subscription_id, subscribed_at, segment, engagement_score, ltv)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (email, 
               subscription_id, 
               subscribed_at,
               custom_fields.get('segment', 'cold'),
               custom_fields.get('engagement_score', 0),
               custom_fields.get('ltv', 0)))
    
    conn.commit()
    conn.close()

# Run daily via cron
# crontab: 0 2 * * * /usr/bin/python3 /path/to/sync_subscribers.py
```

### Real-Time: Push Enrollment

```python
def enroll_subscriber_flow(email, first_name=None):
    """
    Complete flow: Add to local DB → Enroll in Beehiiv automation
    """
    
    # 1. Add to local database
    conn = sqlite3.connect('email_sequences.db')
    c = conn.cursor()
    
    c.execute('''INSERT OR IGNORE INTO subscribers 
                 (email, first_name, subscribed_at)
                 VALUES (?, ?, ?)''',
              (email, first_name, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    # 2. Enroll in welcome sequence via Beehiiv API
    automation_id = "auto_welcome123"  # Your automation ID
    
    response = requests.post(
        f"https://api.beehiiv.com/v2/automations/{automation_id}/journey",
        headers={
            "Authorization": f"Bearer {BEEHIIV_API_KEY}",
            "Content-Type": "application/json"
        },
        json={"email": email}
    )
    
    # 3. Track enrollment locally
    c = conn.cursor()
    c.execute('''INSERT INTO sequence_enrollment 
                 (email, sequence_name, enrolled_at, variant)
                 VALUES (?, ?, ?, ?)''',
              (email, 'welcome', datetime.now().isoformat(), 'A'))
    
    conn.commit()
    conn.close()
    
    return response.json()
```

---

## 📊 Custom Fields Setup

### Required Custom Fields in Beehiiv

Go to **Settings → Custom Fields** and create:

| Field Name        | Type   | Description                    |
|-------------------|--------|--------------------------------|
| `engagement_score`| Number | Weighted activity score        |
| `segment`         | Text   | active/warm/cold/customer      |
| `ltv`             | Number | Lifetime value (revenue)       |
| `last_opened`     | Date   | Last email open timestamp      |
| `last_clicked`    | Date   | Last link click timestamp      |

### Update Custom Fields via API

```python
def update_engagement(email, score_change, segment=None):
    """Update engagement score and segment"""
    
    # Get current subscriber
    sub = get_subscriber(email)
    current_score = sub.get('custom_fields', {}).get('engagement_score', 0)
    
    new_score = current_score + score_change
    
    payload = {
        "email": email,
        "custom_fields": {
            "engagement_score": new_score
        }
    }
    
    if segment:
        payload["custom_fields"]["segment"] = segment
    
    requests.put(
        "https://api.beehiiv.com/v2/subscriptions",
        headers={
            "Authorization": f"Bearer {BEEHIIV_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )
```

---

## 🤖 Automation Workflow

### Complete Integration Example

```python
class BeehiivIntegration:
    def __init__(self, api_key, automation_ids):
        self.api_key = api_key
        self.base_url = "https://api.beehiiv.com/v2"
        self.automation_ids = automation_ids  # Dict: {name: id}
    
    def subscribe_and_enroll(self, email, first_name=None):
        """New subscriber: Add to Beehiiv + enroll in welcome"""
        
        # 1. Create/update subscriber
        self._upsert_subscriber(email, first_name)
        
        # 2. Enroll in welcome automation
        self._enroll_in_automation(email, 'welcome')
        
        # 3. Track locally
        self._track_enrollment(email, 'welcome')
    
    def handle_click(self, email, url):
        """Handle click event: Update engagement + trigger sequences"""
        
        # 1. Update engagement score
        self._increment_engagement(email, 3)
        
        # 2. Track locally
        tracker.record_click(email, 'welcome', 1, url)
        
        # 3. Check for triggers
        if 'pricing' in url:
            self._enroll_in_automation(email, 'abandoned-cart')
        elif 'download' in url:
            self._enroll_in_automation(email, 'upsell')
    
    def handle_conversion(self, email, product, amount):
        """Handle purchase: Update LTV + customer status"""
        
        # 1. Update custom fields
        self._update_custom_fields(email, {
            "ltv": amount,
            "segment": "customer"
        })
        
        # 2. Update engagement
        self._increment_engagement(email, 20)
        
        # 3. Track locally
        tracker.record_conversion(email, product, amount)
    
    def _upsert_subscriber(self, email, first_name):
        response = requests.post(
            f"{self.base_url}/subscriptions",
            headers=self._headers(),
            json={
                "email": email,
                "first_name": first_name,
                "custom_fields": {
                    "engagement_score": 0,
                    "segment": "cold",
                    "ltv": 0
                }
            }
        )
        return response.json()
    
    def _enroll_in_automation(self, email, sequence_name):
        automation_id = self.automation_ids.get(sequence_name)
        if not automation_id:
            return None
        
        response = requests.post(
            f"{self.base_url}/automations/{automation_id}/journey",
            headers=self._headers(),
            json={"email": email}
        )
        return response.json()
    
    def _update_custom_fields(self, email, fields):
        response = requests.put(
            f"{self.base_url}/subscriptions",
            headers=self._headers(),
            json={"email": email, "custom_fields": fields}
        )
        return response.json()
    
    def _increment_engagement(self, email, points):
        sub = self._get_subscriber(email)
        current = sub.get('custom_fields', {}).get('engagement_score', 0)
        
        self._update_custom_fields(email, {
            "engagement_score": current + points
        })
    
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

# Usage
integration = BeehiivIntegration(
    api_key=os.getenv("BEEHIIV_API_KEY"),
    automation_ids={
        "welcome": "auto_abc123",
        "upsell": "auto_def456",
        "abandoned-cart": "auto_ghi789"
    }
)

# New subscriber
integration.subscribe_and_enroll("user@example.com", "John")

# Click event (via webhook)
integration.handle_click("user@example.com", "https://site.com/pricing")

# Conversion
integration.handle_conversion("user@example.com", "Masterclass", 97.00)
```

---

## 🧪 Testing

### 1. Test Subscriber Creation

```bash
curl -X POST https://api.beehiiv.com/v2/subscriptions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "custom_fields": {
      "engagement_score": 0,
      "segment": "cold"
    }
  }'
```

### 2. Test Automation Enrollment

```bash
curl -X POST https://api.beehiiv.com/v2/automations/AUTO_ID/journey \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com"
  }'
```

### 3. Test Webhook

```bash
# Send mock webhook to your endpoint
curl -X POST http://localhost:5000/webhooks/beehiiv \
  -H "Content-Type: application/json" \
  -d '{
    "event": "email.opened",
    "email": "test@example.com",
    "automation_name": "welcome",
    "email_index": 0
  }'
```

---

## 🚨 Troubleshooting

### Issue: "Automation not found"
**Solution:** Verify automation ID in Beehiiv dashboard URL

### Issue: "Subscription already exists"
**Solution:** Use `PUT` instead of `POST` to update existing subscribers

### Issue: "Webhook not receiving events"
**Solution:** Check webhook URL is publicly accessible (use ngrok for local testing)

### Issue: "Custom fields not saving"
**Solution:** Ensure fields are created in Beehiiv UI first

---

## 📋 Deployment Checklist

- [ ] Get Beehiiv API key
- [ ] Create custom fields in Beehiiv UI
- [ ] Build automation sequences in Beehiiv UI
- [ ] Note down automation IDs
- [ ] Set up webhook endpoint (if using real-time tracking)
- [ ] Configure environment variables (API key)
- [ ] Test API connection
- [ ] Test subscriber creation
- [ ] Test automation enrollment
- [ ] Deploy webhook handler (if applicable)
- [ ] Set up daily sync cron job

---

*Beehiiv API Documentation: https://developers.beehiiv.com*
