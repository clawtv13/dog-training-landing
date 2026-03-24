# OBTENER ACCESS TOKEN DE APP YA INSTALADA

Si tu app ya está instalada en la tienda, el access token YA EXISTE.

## 📋 PASOS PARA ENCONTRARLO:

### **Opción 1: Si es Custom App (creada en Shopify Admin)**

1. Ve a: **Shopify Admin** → **Settings** → **Apps and sales channels**
2. Click **"Develop apps"**
3. Encuentra tu app en la lista
4. Click en el nombre de la app
5. Tab: **"API credentials"**
6. Busca: **"Admin API access token"**
7. Ahí está el token (empieza con `shpat_`)
8. Cópialo y pégamelo

---

### **Opción 2: Si es App OAuth (creada en Partners u otra plataforma)**

El access token no es visible en Shopify Admin. En este caso necesitamos:

1. **Re-autorizar la app** para obtener un nuevo token
2. O **rotar el client secret** para forzar nueva autenticación

Para re-autorizar:
- La app necesita hacer el flujo OAuth de nuevo
- Te daré la URL para autorizar
- Me das el código del redirect
- Yo lo cambio por el access token

---

## ❓ PREGUNTA:

¿Dónde creaste esta app?

A) En **Shopify Admin** de tu tienda (Settings → Apps → Develop apps)
B) En **Shopify Partners Dashboard** (partners.shopify.com)
C) No estoy seguro

Si es A → Busca el "Admin API access token" en la página de la app
Si es B → Necesitamos hacer el flujo OAuth

¿Cuál es?
