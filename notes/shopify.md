# SHOPIFY — Knowledge Base

_Last updated: 2026-03-20_

---

## Your Stores

### Clever Dog Shop
- **URL:** `https://8zzpeg-a0.myshopify.com`
- **Domain:** `cleverdogmethod.com` (Netlify DNS)
- **Theme ID:** `194675310939`
- **Main Product:** Carrot Snuffle Mat for Dogs
- **Strategy:** Blog + ClickBank affiliate before full store launch

### Vitalizen
- **Product:** VitaGlow Pro LED Therapy Mask
- **Price:** $69.99 (was $129.99)
- **Target:** Women 30-55, USA, anti-aging
- **Bundles:**
  - 1 Mask: $69.99
  - 2 Masks: $109.99 (save $29.99)
  - 3 Masks: $139.99 (save $69.98)

---

## API Access

**Store:** `8zzpeg-a0.myshopify.com`
**Location ID:** `114377523547`
**Shipping Profile ID:** `139898192219`

---

## Lessons Learned

### Product Page Copy
- **Bullets must be benefit-driven**, not feature lists
- **Reviews need to address objections**: skepticism, price, time, results timeline
- **Enriched text breaks** keep attention — use every 2-3 sections
- **Comparison tables** need credibility — give competitors some ✅ checkmarks

### Pricing Strategy
- **Sweet spot:** $59-79 for LED masks (40-60% margin after $25 cost)
- **Bundles work:** 2-pack "Most Popular", 3-pack "Best Value"
- **Psychological anchor:** Show original price crossed out

### Shipping
- **Free shipping is a CTA enhancer** — repeat it everywhere
- **International shipping needs zones** (España, UE, Internacional)

---

## Commands I've Used

```bash
# Create product variant
shopify products variants create --product-id X

# Update shipping rates via GraphQL
curl -X POST https://8zzpeg-a0.myshopify.com/admin/api/2024-01/graphql.json

# Upload images to Shopify CDN
# (via Shopify Files, then select manually in Theme Editor)
```

---

## To-Do

- [ ] Usuario debe cambiar idioma primario a English en Settings → Languages
- [ ] Configurar Markets (USA + USD)
- [ ] Activar métodos de pago
- [ ] Quitar password de la tienda cuando esté lista
