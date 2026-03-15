# 📱 APP SHOPIFY: AdAngle AI

> *"Find the perfect angle to sell any product"*

## Concepto Core
App que **descubre múltiples ángulos de venta** para un producto y genera copy específico para cada ángulo. No es "genera copy", es "encuentra las 10 formas de vender tu producto".

## Diferenciadores

1. **Angle Discovery:** Analiza producto → sugiere 10+ ángulos de venta únicos
2. **Multi-modelo:** Cada copy usa modelos diferentes (Claude, GPT-4, Llama) = variedad real
3. **Específico para ads:** No descripciones genéricas, sino copy para Facebook/TikTok/Instagram
4. **Audiencias sugeridas:** Cada ángulo incluye a quién targetear

---

## El Problema que Resuelve

Un producto puede venderse de 10 formas diferentes a 10 audiencias diferentes.

**Ejemplo - Back Stretcher:**

| Ángulo | Target | Hook |
|--------|--------|------|
| Chiropractor Killer | Gasta en quiro | "I was spending $80/week..." |
| Desk Worker | Oficinistas WFH | "If you sit 8+ hours a day..." |
| Morning Pain | Rigidez matutina | "Tired of waking up feeling 80?" |
| Skeptic | Escépticos | "I almost scrolled past this..." |
| Gift | Hijos comprando para padres | "Best $40 I spent on my dad" |
| Sciatica | Problema específico | "Finally something for my sciatic nerve" |
| Gym/Recovery | Fitness | "Post-workout decompression" |
| Parent | Padres mayores | "My mom is 72 and uses it daily" |
| Pregnant | Embarazadas | "7 months pregnant, back was killing me" |
| Driver | Uber/truckers | "I drive 10 hours, this saves me" |

**1 producto → 10 ángulos → 50+ ads únicos**

---

## Flujo del Usuario

```
1. Conecta tienda Shopify
              ↓
2. Selecciona producto
              ↓
3. IA analiza:
   - ¿Qué problema resuelve?
   - ¿Qué alternativas reemplaza?
   - ¿Quién sufre más este problema?
   - ¿Cuándo lo sufren?
   - ¿Qué objeciones tienen?
              ↓
4. Muestra 10 ángulos sugeridos con:
   - Nombre del ángulo
   - Audiencia target
   - Hook principal  
   - Objeción que resuelve
              ↓
5. Usuario elige ángulo
              ↓
6. Genera 5 copies (multi-modelo)
              ↓
7. Copia y pega en Ads Manager
```

---

## Features

### MVP (Semanas 1-4)
- ✅ OAuth Shopify
- ✅ Importa productos automático
- ✅ **Angle Discovery** (10 ángulos por producto)
- ✅ Genera 5 copies por ángulo (multi-modelo)
- ✅ Exportar/copiar

### V1.1 (Semanas 5-6)
- ✅ Video scripts por ángulo
- ✅ Teleprompter mode
- ✅ Hooks probados por categoría
- ✅ Audiencias sugeridas para Facebook

### V2 (Semanas 7-8)
- ✅  (Ad Library)
- ✅ Análisis de qué ángulos usan otros
- ✅ Guardar ángulos favoritos
- ✅ Historial de generaciones

---

## Stack Técnico

| Componente | Tecnología |
|------------|------------|
| Frontend | React + Polaris |
| Backend | Node.js |
| Database | PostgreSQL |
| AI | **OpenRouter** (multi-modelo) |
| Hosting | Vercel + Railway |
| Pagos | Shopify Billing API |

---

## Modelos por Tarea (OpenRouter)

| Tarea | Modelo | Por qué |
|-------|--------|---------|
| Angle Discovery | Claude 3.5 Sonnet | Mejor razonamiento |
| Ad Copy creativo | Claude + GPT-4 mix | Variedad |
| Video Scripts | GPT-4o | Buena estructura |
| Hooks rápidos | Llama 3 70B | Barato y bueno |

---

## Prompt: Angle Discovery

```
Eres un experto en marketing y psicología del consumidor.

PRODUCTO:
Nombre: {{title}}
Descripción: {{description}}
Precio: {{price}} (antes {{compare_price}})
Categoría: {{category}}

ANALIZA Y GENERA 10 ÁNGULOS DE VENTA ÚNICOS.

Para cada ángulo incluye:
1. NOMBRE: (ej: "The Chiropractor Killer")
2. AUDIENCIA: Quién exactamente (demografía + situación)
3. DOLOR: Qué problema específico tienen
4. HOOK: Primera frase del ad (para el scroll)
5. OBJECIÓN: Qué duda resuelve este ángulo
6. EMOCIÓN: Qué emoción principal activa

REGLAS:
- Cada ángulo debe ser COMPLETAMENTE diferente
- Piensa en diferentes situaciones de uso
- Piensa en diferentes momentos de compra (para sí, regalo, urgencia)
- Incluye al menos 1 ángulo de escasez/urgencia
- Incluye al menos 1 ángulo de prueba social
- NO repitas la misma audiencia
```

---

## Prompt: Copy por Ángulo

```
Eres un copywriter experto en Facebook/TikTok Ads.

PRODUCTO:
{{product_info}}

ÁNGULO SELECCIONADO:
Nombre: {{angle_name}}
Audiencia: {{audience}}
Dolor: {{pain_point}}
Hook: {{hook}}
Emoción: {{emotion}}

GENERA 5 VARIACIONES DE AD COPY.

Cada variación debe:
- Empezar con un hook diferente (basado en el ángulo)
- Longitud: 80-150 palabras
- Tono: conversacional, auténtico
- Incluir CTA al final
- NO hacer claims médicos
- NO usar emojis excesivos

Las 5 variaciones deben tener ESTILOS diferentes:
1. Storytelling personal
2. Problema-solución directo
3. Comparación (vs alternativa cara)
4. Social proof
5. Urgencia/escasez
```

---

## Database Schema

```sql
-- Shops
CREATE TABLE shops (
  id SERIAL PRIMARY KEY,
  shopify_domain VARCHAR(255) UNIQUE,
  access_token TEXT,
  plan VARCHAR(50) DEFAULT 'free',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Products analyzed
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  shop_id INT REFERENCES shops(id),
  shopify_product_id VARCHAR(255),
  title VARCHAR(255),
  data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Discovered angles
CREATE TABLE angles (
  id SERIAL PRIMARY KEY,
  product_id INT REFERENCES products(id),
  name VARCHAR(100),
  audience TEXT,
  pain_point TEXT,
  hook TEXT,
  objection TEXT,
  emotion VARCHAR(50),
  is_favorite BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Generated copies
CREATE TABLE copies (
  id SERIAL PRIMARY KEY,
  angle_id INT REFERENCES angles(id),
  model_used VARCHAR(100),
  content TEXT,
  type VARCHAR(50), -- 'ad_copy' | 'video_script'
  created_at TIMESTAMP DEFAULT NOW()
);

-- Usage tracking
CREATE TABLE usage (
  id SERIAL PRIMARY KEY,
  shop_id INT REFERENCES shops(id),
  month VARCHAR(7), -- '2026-03'
  angles_discovered INT DEFAULT 0,
  copies_generated INT DEFAULT 0
);
```

---

## Pricing

| Plan | Precio | Límites |
|------|--------|---------|
| **Free** | $0 | 3 ángulos/mes, 15 copies |
| **Starter** | $29/mes | 30 ángulos, copies ilimitados, video scripts |
| **Pro** | $79/mes | Unlimited + Teleprompter + Audiencias |

**Neto (después 20% Shopify):**
- Starter: $23.20
- Pro: $63.20

---

## Unit Economics

| Métrica | Valor |
|---------|-------|
| Coste por Angle Discovery | ~$0.02 (Claude) |
| Coste por 5 copies | ~$0.05 (mix modelos) |
| Coste total por producto | ~$0.07 |
| Usuario Starter genera ~20 productos/mes | $1.40 coste |
| Cobras | $29 |
| **Margen** | **95%** |

---

## Timeline

| Semana | Entregable |
|--------|------------|
| 0 | Setup cuentas |
| 1 | Auth Shopify |
| 2 | Importar productos + UI |
| 3 | **Angle Discovery** (core feature) |
| 4 | Generación copy multi-modelo |
| 5 | Video scripts + teleprompter |
| 6 | Polish + audiencias sugeridas |
| 7 | Billing + planes |
| 8 | Launch + conseguir reviews |

---

## Posicionamiento

**Tagline:** *"Find the perfect angle to sell any product"*

**No somos:** Otro generador de copy AI

**Somos:** La herramienta que descubre CÓMO vender tu producto (los ángulos) y luego genera el copy

---

## Competencia

| Competidor | Qué hace | Por qué ganamos |
|------------|----------|-----------------|
| Jasper | Copy genérico | No descubre ángulos, no está en Shopify |
| Copy.ai | Copy genérico | Mismo problema |
| ChatGPT | Manual | No integrado, no descubre ángulos |
| Apps Shopify actuales | Solo descripciones | NO hacen ads, NO descubren ángulos |

**Nadie hace Angle Discovery + Ad Copy específico para Shopify.**

---

## Go-to-Market

### Semana 1-2 post-launch:
1. 50 emails fríos a tiendas dropshipping
2. Posts en r/shopify, r/dropshipping, r/facebook ads
3. Grupos Facebook de ecom
4. Tweet threads sobre "ángulos de venta"

### Meta:
- 50 instalaciones semana 1
- 30 reviews mes 1
- 100 usuarios pagos mes 3

---

## Checklist Pre-Launch

- [ ] Shopify Partners account
- [ ] OpenRouter con créditos
- [ ] Dominio (adangle.ai?)
- [ ] OAuth funcionando
- [ ] Lee productos
- [ ] **Angle Discovery funciona** (10 ángulos)
- [ ] Genera 5 copies multi-modelo
- [ ] Video scripts
- [ ] Teleprompter
- [ ] Billing configurado
- [ ] App Store listing
- [ ] Screenshots profesionales
- [ ] 30 tiendas contactadas

---

*Actualizado: 2026-03-15*
*Estado: VALIDADO - READY TO BUILD*
*Concepto: Angle Discovery + Multi-Model Copy*
