# DISCORD SERVER SUBSCRIPTIONS — SETUP GUIDE

**Goal:** Enable paid memberships directly in Discord ($49/mo)

---

## 📋 REQUIREMENTS

1. Discord server must be:
   - Community server (enable in settings)
   - Owner/Admin account
   - Server must meet eligibility (varies by region)

2. Payment setup:
   - Stripe Connect account (Discord handles this)
   - Bank account for payouts

---

## 🛠️ STEP-BY-STEP SETUP

### **Step 1: Enable Community**

1. Server Settings → Enable Community
2. Accept rules (moderation channel, etc.)
3. Save changes

### **Step 2: Enable Monetization**

1. Server Settings → Monetization
2. Click "Get Started"
3. Connect Stripe account (Discord walks you through)
4. Verify business info

### **Step 3: Create Subscription Tier**

1. Monetization → Server Subscriptions
2. "Create a Tier"
3. Settings:
   - **Name:** VIP Access
   - **Price:** $49/month
   - **Description:** "Get my exact OpenClaw configs, premium workflows, monthly calls, and direct support."
   - **Perks:** 
     - Access to VIP channels
     - Priority support
     - Premium configs & templates
     - Monthly live calls

4. Assign role: @VIP (auto-assigned when user subscribes)

### **Step 4: Create VIP Channels**

1. Create new category: "💎 VIP ACCESS"
2. Set permissions:
   - @everyone: ❌ View Channel
   - @VIP: ✅ View Channel

3. Create channels inside category:
   - #vip-chat
   - #vip-configs
   - #vip-skills
   - #vip-templates
   - #vip-calls
   - #ask-n0body

### **Step 5: Upload Premium Content**

In each VIP channel, pin first message with resources:

**#vip-configs:**
```
💾 PREMIUM CONFIGS

Download here:
→ n0body-openclaw.json (my exact setup)
→ cost-optimizer.json (81% reduction)
→ youtube-automation.json
→ content-3channel.json

Updated: 2026-03-22
```

**#vip-skills:**
```
📦 PREMIUM SKILLS LIBRARY

1. YouTube Automation Skill
   - Auto-generate scripts
   - SEO optimization
   - Content calendar
   
2. Cost Monitoring Skill
   - Real-time alerts
   - Budget tracking

[Links to download each skill]
```

### **Step 6: Promotion in Free Channels**

**Pin in #general-chat:**
```
🔥 NEW: VIP ACCESS AVAILABLE

Get my exact OpenClaw setup:
✅ Configs that save $19K/year
✅ Premium automation workflows
✅ Monthly live calls
✅ Direct support (24h response)

$49/month — Cancel anytime

[Subscribe in Server Shop]
```

**Weekly posts in #announcements:**
- New VIP content added
- Member testimonials
- Value reminders

---

## 💳 PAYMENT FLOW (User Perspective)

1. User clicks "Server Shop" (top of channel list)
2. Sees VIP tier ($49/mo)
3. Clicks "Subscribe"
4. Enters payment info (Stripe)
5. Instant access — @VIP role assigned automatically
6. Can now see VIP channels

---

## 📊 ANALYTICS & MANAGEMENT

**Discord provides:**
- Subscriber count
- Monthly revenue
- Churn rate
- Growth trends

**Access:** Server Settings → Monetization → Analytics

---

## 💰 PAYOUTS

**Frequency:** Monthly (NET-30)

**Fee structure:**
- Discord: 10%
- Stripe: 2.9% + $0.30 per transaction

**Example:**
- User pays: $49
- Discord fee: $4.90
- Stripe fee: ~$1.50
- You receive: ~$42.60

**50 subscribers:**
- Gross: $2,450/mo
- Net to you: ~$2,130/mo

---

## 🔧 TROUBLESHOOTING

**"Monetization not available":**
- Server must be Community-enabled
- Must meet Discord's eligibility criteria (region, server age, etc.)
- Some regions not supported yet

**Alternative:**
- Use Stripe + manual invites (Option 2)
- Or use Whop (Option 3)

---

## ✅ POST-LAUNCH CHECKLIST

**Week 1:**
- [ ] Monitor first subscribers
- [ ] Welcome DM each new VIP
- [ ] Ensure auto-role working
- [ ] Upload initial premium content

**Ongoing:**
- [ ] Add new content weekly
- [ ] Host monthly calls
- [ ] Reply in #ask-n0body within 24h
- [ ] Post wins/testimonials in free channels

---

**Need help?** Drop in #questions (free channel)

— n0body ◼️
