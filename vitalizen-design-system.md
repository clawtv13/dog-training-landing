# VitaliZen Design System Documentation

## Overview

These enhanced sections were designed to **perfectly match** the existing VitaliZen brand aesthetic. Every design choice was extracted from the live site at `https://vitalizen.shop/products/vitaglow-pro-led-face-mask`.

---

## Brand Colors

### Primary Colors
| Name | Value | Usage |
|------|-------|-------|
| Background Primary | `#f8f8f6` | Main page background (warm off-white) |
| Background White | `#ffffff` | Cards, modals, sections |
| Background Dark | `#1c1c1c` | Headers, countdowns, dark sections |
| Background Muted | `#f3f1ec` | Subtle highlights, alternating rows |

### Text Colors
| Name | Value | Usage |
|------|-------|-------|
| Text Primary | `rgba(43, 43, 43, 0.75)` | Body text |
| Text Dark | `#2b2b2b` | Headings, emphasis |
| Text White | `#ffffff` | Text on dark backgrounds |
| Text Muted | `rgba(43, 43, 43, 0.6)` | Secondary text, captions |

### Accent Colors
| Name | Value | Usage |
|------|-------|-------|
| Olive Green | `rgb(75, 88, 62)` / `#4b583e` | Brand accent, links, highlights |
| Success Green | `#53af01` | Checkmarks, success states |
| Error Red | `#dc3545` | Error states |

### Button Colors
| Name | Value | Usage |
|------|-------|-------|
| Button Background | `#1c1c1c` | Primary CTA buttons |
| Button Text | `#ffffff` | Button text color |

---

## Typography

### Font Families
```css
--vz-font-body: Inter, sans-serif;
--vz-font-heading: Jost, sans-serif;
```

### Heading Styles
- **Font**: Jost
- **Weight**: 800 (Extra Bold)
- **Letter Spacing**: 0.06rem (scaled with font)
- **Style**: Normal

### Body Styles
- **Font**: Inter
- **Weight**: 400 (Regular), 700 (Bold)
- **Size**: 1.5rem (mobile), 1.6rem (desktop)
- **Line Height**: calc(1 + 0.8 / font-scale)
- **Letter Spacing**: 0.06rem

### Font Sizes (Reference)
| Element | Size |
|---------|------|
| H1/H2 Headings | 2.4rem |
| H3 Subheadings | 2rem |
| Body Text | 1.5rem / 1.6rem |
| Captions | 1.2rem |
| Small Text | 0.9rem |

---

## Spacing

### Section Padding
```css
--vz-section-padding: 36px;          /* Desktop */
--vz-section-padding-mobile: 27px;   /* Mobile */
```

### Border Radius
```css
--vz-button-radius: 6px;    /* Buttons, inputs */
--vz-card-radius: 10px;     /* Cards, modals, media */
```

### Shadows
```css
--vz-shadow-subtle: 0 2px 8px rgba(0, 0, 0, 0.06);
--vz-shadow-medium: 0 4px 12px rgba(0, 0, 0, 0.08);
```

---

## Component Patterns

### Buttons
```css
.button {
  background: #1c1c1c;
  color: #ffffff;
  font-family: Inter, sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  padding: 1.2rem 2.4rem;
  border-radius: 6px;
  border: 1px solid #1c1c1c;
  transition: opacity 0.2s ease;
}

.button:hover {
  opacity: 0.9;
}
```

### Tables (Comparison Style)
- Header: Dark background (`#121212`), white text
- Rows: Alternating subtle backgrounds
- Highlighted Row: Muted background (`#f3f1ec`)
- Cell Separator: `rgba(43, 43, 43, 0.1)`

### Trust Badges
- Emoji-prefixed text
- Small font (1.2rem)
- Flexbox layout with gaps
- Muted text color

---

## Responsive Breakpoints

```css
/* Mobile-first approach */
@media screen and (min-width: 750px) {
  /* Desktop styles */
}

@media screen and (max-width: 749px) {
  /* Mobile-specific overrides */
}
```

---

## Installation Instructions

### Option 1: Add to theme.liquid (Recommended)

1. Open **Online Store > Themes > Edit Code**
2. Find `theme.liquid` in the Layout folder
3. Add the entire contents of `vitalizen-redesigned-sections.liquid` just before `</body>`

### Option 2: Create Individual Snippets

1. Create new snippets in **Snippets** folder:
   - `vz-price-comparison.liquid`
   - `vz-cta-section.liquid`
   - `vz-countdown.liquid`
   - `vz-sticky-cart.liquid`
   - `vz-exit-popup.liquid`

2. Split the code by section and include in product template:
   ```liquid
   {% render 'vz-countdown' %}
   {% render 'vz-price-comparison' %}
   {% render 'vz-cta-section' %}
   {% render 'vz-sticky-cart' %}
   {% render 'vz-exit-popup' %}
   ```

### Exact Positioning

| Section | Position | Notes |
|---------|----------|-------|
| **Countdown Timer** | Above product form OR in announcement bar | Replace existing countdown or add above price |
| **Price Comparison** | Below "VitaGlow Pro vs. Competitors" table | Complements existing comparison |
| **CTA Section** | After testimonials (before footer) | Final conversion push |
| **Sticky Cart** | Auto-positioned (fixed to bottom) | Mobile only, shows on scroll |
| **Exit Popup** | Auto-positioned (overlay) | Triggers on exit intent |

---

## Customization

### Changing Colors
All colors are defined as CSS custom properties in `:root`. To customize:

```css
:root {
  --vz-accent-olive: #your-color;
  --vz-button-bg: #your-button-color;
}
```

### Discount Codes
Update the exit popup discount code in the HTML:
```liquid
<span class="vz-exit-popup__offer-code">YOUR_CODE</span>
```

### Timer Duration
The countdown resets at midnight each day. To change:
```javascript
// In the countdown script, modify getEndTime()
function getEndTime() {
  const now = new Date();
  const end = new Date(now);
  // Change this line for different end time
  end.setHours(23, 59, 59, 999);
  return end;
}
```

### Exit Popup Cooldown
Default is 24 hours. To change:
```javascript
const COOLDOWN_HOURS = 24; // Change this value
```

---

## Design Principles Applied

1. **No garish gradients** - All backgrounds are solid colors matching the site
2. **Matching typography** - Exact font families, weights, and sizes
3. **Brand colors only** - Using extracted color palette
4. **Consistent spacing** - Same padding/margins as existing sections
5. **Professional/clinical vibe** - Clean, minimal, medical aesthetic
6. **Non-aggressive urgency** - Subtle countdown, gentle popup copy

---

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- iOS Safari 14+
- Android Chrome
- Graceful degradation for older browsers

---

## Performance Notes

- CSS is inlined to avoid extra HTTP requests
- JavaScript is vanilla (no jQuery dependency)
- Lazy loading on images
- Passive scroll listeners
- RequestAnimationFrame for scroll handlers

---

## Files Included

1. `vitalizen-redesigned-sections.liquid` - Complete code (CSS + HTML + JS)
2. `vitalizen-design-system.md` - This documentation file
