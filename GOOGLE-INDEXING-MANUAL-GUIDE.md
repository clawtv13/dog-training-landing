# Google Search Console - Manual Indexing Request

**Fecha:** 31 Marzo 2026  
**Objetivo:** Acelerar indexación de 3 pillar posts (2-3 días en vez de 7-14)

---

## 🔑 **PASO 1: ACCEDER A GOOGLE SEARCH CONSOLE**

**URL:** https://search.google.com/search-console

**Login con cuenta de Google que posee workless.build**

---

## 📝 **PASO 2: VERIFICAR PROPIEDAD DEL SITIO**

Si **NO está verificado** aún:

### Método A: HTML Tag (más fácil)

1. Google Search Console → **Add Property** → `https://workless.build`
2. Te da un meta tag: `<meta name="google-site-verification" content="CODIGO_UNICO">`
3. Añadir al `<head>` de `index.html`
4. Deploy → **Verify**

### Método B: DNS Record

1. Add TXT record en tu DNS:
   - Name: `@` o root domain
   - Value: `google-site-verification=CODIGO_UNICO`
2. Espera 10-20 min → **Verify**

---

## 🚀 **PASO 3: REQUEST INDEXING (3 URLs)**

**Una vez verificado:**

### URL 1: ChatGPT Prompts

1. Go to: **URL Inspection** (arriba izquierda, icono de lupa)
2. Paste URL:
   ```
   https://workless.build/posts/2026-03-31-the-51-chatgpt-prompts-that-save-solopreneurs-15-hours-every-week.html
   ```
3. Click **Inspect**
4. Si dice "URL is not on Google":
   - Click **REQUEST INDEXING**
   - Espera 1-2 minutos (Google valida la página)
   - ✅ "Indexing requested"

### URL 2: Email Automation

Repetir proceso con:
```
https://workless.build/posts/2026-03-31-how-to-automate-email-followups-without-expensive-crm.html
```

### URL 3: Tech Stack

Repetir proceso con:
```
https://workless.build/posts/2026-03-31-my-50-month-tech-stack-that-replaces-your-500-saas-bill.html
```

---

## ⏰ **TIMING:**

**Después de REQUEST INDEXING:**
- Status cambia a: "URL submitted for indexing"
- Google indexa: 2-48 horas (promedio 12-24h)
- Verifica en: `site:workless.build pillar posts`

---

## 🔍 **ALTERNATIVA: API (más rápido, pero necesita setup)**

Si quieres automatizarlo:

### Setup Google Indexing API

1. **Enable API:** https://console.cloud.google.com/apis/library/indexing.googleapis.com
2. **Create Service Account:**
   - IAM & Admin → Service Accounts → Create
   - Grant role: "Owner" en Search Console
3. **Download JSON key**
4. **Install Python client:**
   ```bash
   pip install google-api-python-client oauth2client
   ```

### Script to submit URLs

```python
#!/usr/bin/env python3
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'service-account-key.json', 
    scopes=SCOPES
)

service = build('indexing', 'v3', credentials=credentials)

# URLs to index
urls = [
    "https://workless.build/posts/2026-03-31-the-51-chatgpt-prompts-that-save-solopreneurs-15-hours-every-week.html",
    "https://workless.build/posts/2026-03-31-how-to-automate-email-followups-without-expensive-crm.html",
    "https://workless.build/posts/2026-03-31-my-50-month-tech-stack-that-replaces-your-500-saas-bill.html"
]

for url in urls:
    body = {
        "url": url,
        "type": "URL_UPDATED"
    }
    
    try:
        response = service.urlNotifications().publish(body=body).execute()
        print(f"✅ Submitted: {url}")
        print(f"   Response: {response}")
    except Exception as e:
        print(f"❌ Error for {url}: {e}")
```

**Run:**
```bash
python3 submit-urls-to-google.py
```

---

## 📊 **VERIFICAR INDEXACIÓN:**

### Método 1: Google Search

```
site:workless.build "51 ChatGPT Prompts"
```

Si aparece → ✅ Indexado

### Método 2: Search Console

1. **Coverage Report** → Check URLs
2. **Performance** → See impressions (después de 2-3 días)

---

## 💡 **TIPS:**

**✅ DO:**
- Request indexing para content importante (pillar posts, product pages)
- Espera 24-48h antes de re-request
- Verifica que sitemap.xml esté actualizado

**❌ DON'T:**
- Request cada post diario (innecesario, Google los encuentra solo)
- Re-request múltiples veces en 24h (no acelera, puede penalizar)
- Request URLs con errores 404 o thin content

---

## ⚡ **QUICK CHECKLIST:**

- [ ] Search Console verificado para workless.build
- [ ] Request indexing para URL 1 (ChatGPT Prompts)
- [ ] Request indexing para URL 2 (Email Automation)
- [ ] Request indexing para URL 3 (Tech Stack)
- [ ] Sitemap.xml actualizado (✅ ya hecho)
- [ ] Monitorear en 24-48h con `site:` search

---

## 🎯 **RESULTADO ESPERADO:**

**Sin request manual:** 7-14 días para indexar  
**Con request manual:** 2-48 horas para indexar  
**Aceleración:** ~10x más rápido

**ROI:** 5 minutos de trabajo → Posts indexados 10 días antes → Traffic orgánico empieza antes

---

**Total tiempo:** 5-10 minutos (manual UI)  
**O:** 20 minutos setup inicial + 30 segundos futuros (API script)
