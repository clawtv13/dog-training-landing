# SHOPIFY OAUTH — INSTRUCCIONES COMPLETAS

## 📋 PASO 1: Verifica el Redirect URI

Ve a tu app en Shopify y verifica qué **redirect URI** configuraste.

Probablemente es uno de estos:
- `https://vitalizen.shop/auth/callback`
- `https://vitalizen.shop/shopify/callback`
- O alguna URL de tu servidor

---

## 🔗 PASO 2: Abre la URL de Autorización

**Para redirect_uri = https://vitalizen.shop/auth/callback:**

```
https://s7ddqj-0v.myshopify.com/admin/oauth/authorize?client_id=76ec024874dd3b48acc3f11fe5b573b0&scope=read_products%2Cwrite_products%2Cread_orders%2Cwrite_orders%2Cread_customers%2Cwrite_customers%2Cread_content%2Cwrite_content%2Cread_themes%2Cwrite_themes&redirect_uri=https%3A%2F%2Fvitalizen.shop%2Fauth%2Fcallback&state=vitalizen-oauth
```

**Para redirect_uri = https://vitalizen.shop/shopify/callback:**

```
https://s7ddqj-0v.myshopify.com/admin/oauth/authorize?client_id=76ec024874dd3b48acc3f11fe5b573b0&scope=read_products%2Cwrite_products%2Cread_orders%2Cwrite_orders%2Cread_customers%2Cwrite_customers%2Cread_content%2Cwrite_content%2Cread_themes%2Cwrite_themes&redirect_uri=https%3A%2F%2Fvitalizen.shop%2Fshopify%2Fcallback&state=vitalizen-oauth
```

---

## 📋 PASO 3: Autoriza la App

1. Abre la URL correspondiente a tu redirect_uri
2. Click **"Install app"** o **"Authorize"**
3. Shopify te redirigirá a tu redirect_uri
4. La URL contendrá: `?code=XXXXXX&...`

---

## 📋 PASO 4: Dame el Código

Copia la **URL COMPLETA** después del redirect y pégamela.

La URL se verá así:
```
https://vitalizen.shop/auth/callback?code=a1b2c3d4e5f6...&hmac=...&state=vitalizen-oauth&...
```

Yo extraeré el `code` y lo cambiaré por el access token.

---

## ⚡ ALTERNATIVA RÁPIDA

Si tu redirect_uri es `https://vitalizen.shop/auth/callback`, simplemente:

1. Abre: https://s7ddqj-0v.myshopify.com/admin/oauth/authorize?client_id=76ec024874dd3b48acc3f11fe5b573b0&scope=read_products%2Cwrite_products%2Cread_orders%2Cwrite_orders%2Cread_customers%2Cwrite_customers%2Cread_content%2Cwrite_content%2Cread_themes%2Cwrite_themes&redirect_uri=https%3A%2F%2Fvitalizen.shop%2Fauth%2Fcallback&state=vitalizen-oauth

2. Autoriza

3. Copia la URL completa del redirect

4. Pégamela aquí
