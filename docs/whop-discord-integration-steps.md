# WHOP → DISCORD INTEGRATION — SETUP

**Goal:** Auto-assign @WhopVIP role when users subscribe

---

## 📝 INFORMACIÓN NECESARIA

### **Tu Discord Server:**
- **Server Name:** ClawTV
- **Server ID:** `1484937580339400784`
- **VIP Role ID:** `1485266360371253379`
- **Bot Token:** (ya configurado en Discord)

### **Tu Whop:**
- **URL:** https://whop.com/clawtv-community
- **Product:** $49/mo Community Pass (ya existe)

---

## 🔧 PASOS (En Whop Dashboard)

### **Step 1: Go to Integrations**

1. Login to Whop: whop.com
2. Go to your product dashboard
3. Click "Integrations" (left sidebar)
4. Find "Discord" integration
5. Click "Connect"

---

### **Step 2: Authorize Discord Bot**

1. Whop te pedirá permisos para tu servidor
2. Selecciona "ClawTV" server
3. Authorize permissions:
   - ✅ Manage Roles
   - ✅ View Channels
   - ✅ Send Messages
   - ✅ Create Invite Links

4. Click "Authorize"

---

### **Step 3: Configure Role Assignment**

**En Whop Discord Settings:**

1. **Discord Server:** ClawTV (auto-detected)
2. **Role to Assign:** WhopVIP
   - Role ID: `1485266360371253379`
   - O selecciona de dropdown

3. **Invite Settings:**
   - ✅ Auto-send Discord invite on purchase
   - ✅ DM user with welcome message
   - ✅ Remove role on cancellation

4. Save settings

---

### **Step 4: Test Integration**

**Test Flow:**

1. Create test account (or use different email)
2. Subscribe to product (use test card if available)
3. Check:
   - ✅ Received Discord invite via email/DM
   - ✅ Joined server automatically
   - ✅ Has @WhopVIP role
   - ✅ Can see VIP channels

4. Cancel subscription
5. Check:
   - ✅ Role removed
   - ✅ Can't see VIP channels anymore

---

## 🎨 WELCOME MESSAGE (Configure in Whop)

**When user subscribes, Whop DMs them:**

```
🎉 Welcome to ClawTV VIP!

You now have access to:
✅ My exact openclaw.json (save $19K/year)
✅ 20+ premium workflows
✅ Private mastermind community
✅ Monthly live calls
✅ Direct support (24h response)

📱 JOIN DISCORD:
[Discord Invite Link]

Once you join, you'll automatically get @WhopVIP role and access to all premium channels.

Questions? Reply to this DM or ask in #vip-chat

— n0body ◼️
```

---

## 📊 MONITORING

**Whop Dashboard shows:**
- Active subscribers
- Discord connection status
- Role assignment success rate
- Errors (if any)

**Check weekly:**
- Are roles being assigned?
- Any failed integrations?
- Need to re-authorize bot?

---

## 🚨 TROUBLESHOOTING

### **Problem: Roles not assigning**

**Check:**
1. Bot has "Manage Roles" permission
2. @WhopVIP role is BELOW bot role in hierarchy
3. Role ID is correct in Whop settings

**Fix:**
- Discord → Server Settings → Roles
- Drag bot role ABOVE @WhopVIP
- Re-save Whop integration

---

### **Problem: Users can't join server**

**Check:**
1. Server isn't at member limit
2. Invite links haven't expired
3. User isn't banned

**Fix:**
- Create new permanent invite
- Update in Whop settings

---

### **Problem: Role removed but user still has access**

**Check:**
1. User has multiple roles
2. Channel permissions conflict

**Fix:**
- Audit channel permissions
- Ensure ONLY @WhopVIP can see VIP channels

---

## ✅ CHECKLIST

**Before Launch:**
- [ ] Discord integration connected
- [ ] Role assignment configured
- [ ] Test purchase completed successfully
- [ ] Welcome message customized
- [ ] VIP channels verified (only @WhopVIP sees them)
- [ ] Cancellation flow tested

**After Launch:**
- [ ] Monitor first 10 subscribers
- [ ] Ensure smooth onboarding
- [ ] Reply to questions quickly
- [ ] Collect feedback

---

## 📝 FALLBACK (If Integration Fails)

**Manual process:**

1. User subscribes on Whop
2. You get notification email
3. Manually send Discord invite
4. Manually assign @WhopVIP role

**Time:** 2-3 min per user

**Use this if:**
- Integration bugs out
- Testing phase
- Want more control

---

**Next: Setup Whop integration, then launch!**

— n0body ◼️
