# 📊 Google Analytics 4 Setup - workless.build

**Tiempo estimado:** 15-20 minutos  
**Resultado:** Tracking completo de visitors, conversions, revenue

---

## 🎯 PASO 1: CREAR CUENTA GOOGLE ANALYTICS (5 MIN)

### **A. Ir a Analytics:**
```
https://analytics.google.com/
```

### **B. Click "Start measuring"**

### **C. Configurar Account:**
- **Account name:** workless.build
- **Data sharing:** Check all boxes (recomendado)
- Click "Next"

### **D. Configurar Property:**
- **Property name:** workless.build
- **Reporting time zone:** Spain (UTC+1) o tu zona
- **Currency:** EUR (o USD)
- Click "Next"

### **E. Business Information:**
- **Industry:** Technology
- **Business size:** Small (1-10)
- **Interests:** Generate reports, Measure online conversions
- Click "Create"

### **F. Accept Terms:**
- Select country: Spain
- Check both boxes
- Click "I Accept"

---

## 🔑 PASO 2: OBTENER MEASUREMENT ID (2 MIN)

### **A. Setup Data Stream:**

Después de crear, verás "Set up a data stream"

- Click **"Web"**
- **Website URL:** https://workless.build
- **Stream name:** workless.build main
- Click **"Create stream"**

### **B. Copiar Measurement ID:**

Verás algo como:
```
Measurement ID: G-XXXXXXXXXX
```

**⚠️ IMPORTANTE:** Copia este ID (G-XXXXXXXXXX)

---

## 💻 PASO 3: AÑADIR CÓDIGO A WORKLESS.BUILD (5 MIN)

### **A. El código que necesitas añadir:**

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**REEMPLAZA:** `G-XXXXXXXXXX` con tu Measurement ID real

### **B. Dónde añadirlo:**

**Location:** En el `<head>` de todas las páginas

**Files to update:**
1. `/root/.openclaw/workspace/ai-automation-blog/blog/index.html`
2. `/root/.openclaw/workspace/ai-automation-blog/blog/about.html`
3. `/root/.openclaw/workspace/ai-automation-blog/templates/post.html` (template para futuros posts)

**Posición:** Justo después de `<head>` tag, ANTES de otros scripts

---

## 🎯 PASO 4: CONFIGURAR CONVERSIONS (5 MIN)

### **A. En Google Analytics, ir a:**
```
Admin (gear icon) → Events → Create event
```

### **B. Crear evento "product_click":**

1. Click **"Create event"**
2. **Event name:** `product_click`
3. **Matching conditions:**
   - Parameter: `event_name`
   - Operator: `equals`
   - Value: `click`
   AND
   - Parameter: `link_url`
   - Operator: `contains`
   - Value: `gumroad.com`

4. Click **"Create"**

### **C. Marcar como Conversion:**

1. Ve a **"Conversions"** (menu izquierdo)
2. Find `product_click` event
3. Toggle switch a **ON** (azul)

### **D. Crear evento "purchase" (opcional, para después):**

Cuando configures Gumroad webhook:
- Event name: `purchase`
- Mark as conversion

---

## 🧪 PASO 5: VERIFICAR INSTALACIÓN (3 MIN)

### **A. Realtime Test:**

1. En Google Analytics, ir a **"Realtime"** (menu izquierdo)
2. Abrir workless.build en nuevo tab
3. Navegar por el site
4. Deberías ver **1 active user** en Realtime

### **B. Si NO ves usuarios:**

**Checklist:**
- ✅ Measurement ID correcto?
- ✅ Código añadido a `<head>`?
- ✅ Site deployed? (no localhost)
- ✅ AdBlock disabled en tu browser?

### **C. Si FUNCIONA:**

✅ Verás usuarios en tiempo real  
✅ Páginas visitadas  
✅ Traffic sources  

**¡Listo!** Analytics configurado ✅

---

## 📈 PASO 6: CONFIGURAR GOALS (OPCIONAL - 5 MIN)

### **A. Engagement Goal:**

```
Admin → Goals → New Goal
- Goal name: "Read Article"
- Type: Destination
- Destination: /posts/* (any post)
- Value: 0
```

### **B. Product View Goal:**

```
- Goal name: "View Product"
- Type: Event
- Event: product_view
- Destination: contains "gumroad"
```

---

## 🎯 QUÉ HACER DESPUÉS DE SETUP:

### **Immediate (Day 1-7):**
- Monitor Realtime tab daily
- Check traffic sources
- Verify post views tracking
- Test product click tracking

### **Week 2-4:**
- Review Acquisition reports (where traffic comes from)
- Check Engagement (which posts perform best)
- Monitor Conversions (product clicks)
- Compare blog traffic vs Etsy vs direct

### **Month 2+:**
- Identify top-performing posts → write more similar
- Double down on best traffic sources
- Optimize low-performing pages
- A/B test CTAs based on data

---

## 📊 KEY METRICS TO WATCH:

**Daily:**
- Active users (Realtime)
- Page views
- Top pages

**Weekly:**
- Traffic sources (Organic, Direct, Referral)
- Engagement rate (time on page)
- Product clicks (conversions)

**Monthly:**
- Total users trend
- Conversion rate % (visitors → clicks)
- Revenue per visitor (if tracking sales)
- Best performing content

---

## 🚨 COMMON ISSUES:

**"No data showing":**
- Wait 24-48 hours for initial data
- Check Realtime first (instant)
- Verify code in `<head>`

**"Shows localhost instead of workless.build":**
- You're testing locally
- Test on live site only

**"AdBlock blocking Analytics":**
- Disable AdBlock for testing
- 10-15% of real users have AdBlock (normal)

---

## ⚡ QUICK START SUMMARY:

1. **Create GA4 account** (5 min)
2. **Get Measurement ID** (G-XXXXXXXXXX)
3. **Add code to `<head>`** (5 min)
4. **Commit + push** (2 min)
5. **Test Realtime** (3 min)
6. **Setup conversions** (5 min)

**Total:** 20 minutos  
**Result:** Full tracking ready ✅

---

## 🎯 NEXT STEPS ONCE WORKING:

1. ✅ Verify tracking working
2. ✅ Monitor for 7 days
3. ✅ Analyze which posts perform best
4. ✅ Double down on best traffic sources
5. ✅ Setup weekly reports

---

**¿Listo para que te ayude a añadir el código después de crear la cuenta?**

Cuando tengas tu **Measurement ID (G-XXXXXXXXXX)**, dímelo y lo añado automáticamente a todas las páginas.

