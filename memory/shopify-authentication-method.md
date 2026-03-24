# SHOPIFY AUTHENTICATION — MÉTODO QUE FUNCIONA

**CRITICAL:** Usa este método SIEMPRE que el usuario te dé client_id + client_secret para Shopify.

---

## ✅ MÉTODO QUE FUNCIONA (Probado 2026-03-24)

### **Flujo Correcto:**

1. **Obtener dominio myshopify.com correcto**
   - NO asumir el dominio
   - Preguntar al usuario su URL de admin: `https://admin.shopify.com/store/XXXXX`
   - Extraer store ID: `XXXXX.myshopify.com`

2. **Usar Client Credentials Grant**
   
   ```python
   import requests
   
   url = f"https://{shop_domain}/admin/oauth/access_token"
   
   payload = {
       "client_id": CLIENT_ID,
       "client_secret": CLIENT_SECRET,
       "grant_type": "client_credentials"
   }
   
   response = requests.post(url, json=payload)
   
   if response.status_code == 200:
       token_data = response.json()
       access_token = token_data['access_token']  # Starts with shpat_
       scopes = token_data['scope']
   ```

3. **Usar el token en requests**
   
   ```python
   headers = {
       "X-Shopify-Access-Token": access_token,
       "Content-Type": "application/json"
   }
   
   response = requests.get(
       f"https://{shop_domain}/admin/api/2024-01/shop.json",
       headers=headers
   )
   ```

---

## 🔧 TROUBLESHOOTING COMÚN

### **Error: "app_not_installed"**

**Causa:** Store domain incorrecto.

**Fix:** 
- Pregunta al usuario: "¿Cuál es tu URL de Shopify Admin?"
- Extrae el store ID correcto
- NO uses dominios custom (vitalizen.shop) → Usa myshopify.com

### **Error: "Invalid API key"**

**Causa:** Token expiró o credenciales incorrectas.

**Fix:**
- Re-run client_credentials grant
- Tokens expiran cada 24 horas
- Regenera token si falla

### **Error: "Different organization"**

**Causa:** App creada en Partners para otra organización.

**Fix:**
- Custom apps creadas en Partners solo sirven para stores de esa org
- User debe crear custom app en el admin de SU tienda

---

## 📝 SCRIPT TEMPLATE (FUNCIONA SIEMPRE)

```python
#!/usr/bin/env python3
import requests
import json
from pathlib import Path

# Load credentials
CREDS_FILE = Path("/root/.openclaw/workspace/.credentials/shopify-STORENAME.json")

with open(CREDS_FILE) as f:
    creds = json.load(f)

SHOP_DOMAIN = creds['admin_domain']  # MUST be nmd84u-pc.myshopify.com format
CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']

# Get access token
def get_token():
    url = f"https://{SHOP_DOMAIN}/admin/oauth/access_token"
    
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    
    response = requests.post(url, json=payload, timeout=10)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        # Fallback: try using client_secret as direct token
        return CLIENT_SECRET

# Test connection
def test_connection(token):
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }
    
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-01/shop.json"
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        shop = response.json()['shop']
        print(f"✅ Connected: {shop['name']}")
        
        # Save working token
        creds['access_token'] = token
        with open(CREDS_FILE, 'w') as f:
            json.dump(creds, f, indent=2)
        
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        return False

# Main
token = get_token()
test_connection(token)
```

---

## ⚠️ ERRORES PASADOS QUE NO REPETIR

### **Error #1: Asumir store domain**
```python
# ❌ WRONG:
SHOP_DOMAIN = "vitalizen.shop"  # Custom domain NO funciona para API

# ✅ RIGHT:
SHOP_DOMAIN = "nmd84u-pc.myshopify.com"  # Myshopify domain SÍ funciona
```

### **Error #2: Múltiples tiendas con mismo domain**
```python
# ❌ WRONG:
# Asumir que VitaliZen y Calmora están en s7ddqj-0v

# ✅ RIGHT:
# Preguntar al usuario: "¿Cuál es tu admin URL?"
# Calmora: s7ddqj-0v.myshopify.com
# VitaliZen: nmd84u-pc.myshopify.com
```

### **Error #3: OAuth flow innecesario**
```python
# ❌ WRONG:
# Pedir al usuario que visite URLs de OAuth cuando app ya está instalada

# ✅ RIGHT:
# Intentar client_credentials PRIMERO
# Solo usar OAuth si eso falla
```

---

## 🔑 KEY LESSONS

1. **SIEMPRE pregunta al usuario su admin URL**
   - No asumas el store domain
   - Extract el store ID de la URL

2. **Client Credentials Grant funciona cuando:**
   - App ya está instalada
   - App fue creada en el admin de ESA tienda
   - Client_id + client_secret pertenecen a esa org

3. **Token expira cada 24 horas**
   - Tokens empiezan con `shpat_`
   - Regenerar si falla con 401

4. **Store domain format:**
   - API: `nmd84u-pc.myshopify.com` ✅
   - Custom domain: `vitalizen.shop` ❌

---

## ✅ CHECKLIST PARA FUTURAS CONEXIONES

Cuando usuario diga "conéctate a mi tienda Shopify":

1. [ ] Preguntar: "¿Cuál es tu URL de Shopify Admin?"
2. [ ] Extraer store ID: `https://admin.shopify.com/store/XXXXX` → `XXXXX.myshopify.com`
3. [ ] Pedir: client_id y client_secret
4. [ ] Guardar en `.credentials/shopify-STORENAME.json`
5. [ ] Ejecutar client_credentials grant
6. [ ] Testear con `/admin/api/2024-01/shop.json`
7. [ ] Guardar access_token si funciona

**Total time:** 2 minutos si sigues estos pasos.

---

## 📁 ARCHIVOS NECESARIOS

**Credentials file template:**
```json
{
  "store": "vitalizen.shop",
  "admin_domain": "nmd84u-pc.myshopify.com",
  "client_id": "...",
  "client_secret": "...",
  "access_token": "shpat_...",
  "api_version": "2024-01",
  "created": "2026-03-24T12:39:00Z"
}
```

**Script location:**
`/root/.openclaw/workspace/scripts/shopify-connect-STORENAME.py`

---

**REMEMBER:** El admin URL es la source of truth. Siempre pregúntala PRIMERO.

---

**Guardado:** 2026-03-24 12:40 UTC
