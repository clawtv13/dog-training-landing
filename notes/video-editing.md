# VIDEO EDITING — Workflow & Learnings

_Last updated: 2026-03-20_

---

## Tech Stack

**Editor:** MoviePy (Python)  
**Models:** Replicate (Flux 1.1 Pro, Stable Diffusion)  
**Voice:** ElevenLabs (TTS)  
**Workspace:** `/root/.openclaw/workspace/video-generator/`

---

## Video Scripts Created

### Dog Training Channel

1. **"Things Your Dog Secretly Hates"**
   - 7 common mistakes owners make
   - Format: Problem → Why it's bad → Better alternative
   - Length: 60-90 seconds

2. **"Signs Your Dog Loves You"**
   - 7 science-backed behaviors
   - Format: Behavior → Science → What it means
   - Emotional hook

3. **"Body Language Decoded"**
   - Whale eye, lip licking, yawning, tail wag types
   - Educational, saves owners from mistakes

4. **"I Tested Viral Dog Hacks"**
   - 5 hacks tested → verdict on each
   - Entertaining + useful

---

## Viral Video Formula

### Hook (0-3s)
- **Shock/Curiosity:** "You're hurting your dog..."
- **Pattern Interrupt:** "This looks crazy but..."
- **Value Promise:** "7 signs your dog loves you"

### Body (3-45s)
- **Listicle format** (7 things, 5 ways, 3 secrets)
- **Visual variety** — cambiar imagen cada 3-5 segundos
- **Text overlays** — una frase por frame

### CTA (45-60s)
- "Follow for more"
- "Comment which one you do"
- "Save this for later"

---

## YouTube Shorts Optimization

**Título:**
- Máximo 60 caracteres
- Curiosity > descripción
- Números específicos

**Descripción:**
- Primera línea = hook (se ve en thumbnail)
- 8-12 hashtags (mezcla popular + nicho)
- CTA al final

**Hashtags que funcionan:**
```
#dogtraining #dogbehavior #dogpsychology 
#doglover #dogowner #puppytraining 
#dogtips #dogcare #shorts
```

---

## MoviePy Issues & Fixes

### ❌ Problema: MoviePy v2 incompatible con Pillow 10+
**Fix:** Downgrade a MoviePy v1.0.3
```bash
pip install moviepy==1.0.3
```

### ❌ Problema: Videos muy pesados
**Fix:** Optimizar bitrate
```python
clip.write_videofile("output.mp4", bitrate="2000k")
```

### ❌ Problema: Text overlay borroso
**Fix:** Usar tamaño de fuente mayor y antialiasing
```python
TextClip(..., fontsize=60, method='caption')
```

---

## Image Generation

### Flux 1.1 Pro (Replicate)
- **Mejor para:** Fotorrealismo, reviews de producto
- **Prompt structure:** `[Subject] [Action] [Style] [Details]`
- **Ejemplo:** `A happy golden retriever playing with a carrot toy, photorealistic, natural lighting, 4K quality`

### Rate Limits
- **Replicate:** 6 requests/min con <$5 crédito
- **Solución:** Batch generation con delays
```python
for i, prompt in enumerate(prompts):
    if i > 0 and i % 6 == 0:
        time.sleep(60)  # Esperar 1 min cada 6
    generate_image(prompt)
```

---

## Workflow

1. **Script** — Escribir guion completo en markdown
2. **Images** — Generar imágenes con Flux/SD
3. **TTS** — Generar voiceover con ElevenLabs (si aplica)
4. **Assembly** — MoviePy: imágenes + text overlays + audio
5. **Export** — 9:16 ratio, 1080x1920, H.264
6. **Upload** — YouTube Shorts con metadata optimizado

---

## Pending Improvements

- [ ] Automatizar text overlay positioning
- [ ] Template system para diferentes formatos
- [ ] Thumbnail auto-generation
- [ ] Batch processing de múltiples scripts
- [ ] Integration con YouTube API para auto-upload
