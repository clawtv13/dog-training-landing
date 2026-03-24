# 🎬 Video Generator - Script to Video AI

**Tu propio clon de CapCut "Create with AI"** - 100% gratis e ilimitado.

## ✨ Features (100% CapCut)

| Feature | Descripción |
|---------|-------------|
| ✅ **Script → Scenes** | LLM divide tu texto en escenas automáticamente |
| ✅ **Stock Videos** | Pexels + Pixabay con fallback automático |
| ✅ **TTS Voiceover** | Edge TTS (Microsoft) - gratis, ilimitado, 300+ voces |
| ✅ **Subtítulos Animados** | Karaoke, bounce, highlight - estilo TikTok |
| ✅ **Efectos Visuales** | Ken Burns (zoom), pan, zoom pulse |
| ✅ **Transiciones** | Fade, slide, zoom, swipe entre clips |
| ✅ **Música de Fondo** | Auto-fetch + auto-ducking cuando hay voz |
| ✅ **Logo/Watermark** | Añade tu marca al video |

## 🚀 Quick Start

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar APIs (gratis)
cp .env.example .env
# Edita .env y añade:
# - PEXELS_API_KEY (https://www.pexels.com/api/)
# - PIXABAY_API_KEY (https://pixabay.com/api/docs/)

# 3. Generar un video
python main.py "My dog used to bark all night. The neighbors complained. Then I discovered brain training. Everything changed in 7 days."
```

## 📖 Uso Completo

### Básico
```bash
python main.py "Tu script aquí"
```

### Con todas las opciones
```bash
python main.py "Script completo aquí" \
  --voice en-US-JennyNeural \
  --format 9:16 \
  --subtitle-style karaoke \
  --transitions \
  --transition-type fade \
  --effects \
  --music calm \
  --logo logo.png \
  --output mi_video
```

### Desde archivo
```bash
python main.py --script-file guion.txt --music energetic
```

## 🎨 Estilos de Subtítulos

| Estilo | Descripción |
|--------|-------------|
| `karaoke` | Palabra activa cambia de color (estilo TikTok) |
| `bounce` | Palabra activa escala +15% |
| `highlight_box` | Palabra activa con fondo de color |
| `wave` | Palabras aparecen una por una |
| `bold` | Estático con borde negro |
| `minimal` | Estático simple |

```bash
python main.py "Script" --subtitle-style bounce
```

## 🎬 Efectos Visuales

- **Ken Burns**: Zoom lento (1.0 → 1.15) durante el clip
- **Pan**: Movimiento horizontal/vertical suave
- **Zoom Pulse**: Zoom rítmico con easing

```bash
python main.py "Script" --effects  # Activado por defecto
python main.py "Script" --no-effects  # Desactivar
```

## 🔄 Transiciones

| Tipo | Descripción |
|------|-------------|
| `fade` | Crossfade suave |
| `slide` | Clip entra desde un lado |
| `zoom` | Zoom out → zoom in |
| `swipe` | Barrido horizontal |
| `random` | Aleatorio |

```bash
python main.py "Script" --transition-type slide
```

## 🎵 Música de Fondo

Moods disponibles:
- `calm` - Relajante
- `energetic` - Activo, movimiento
- `dramatic` - Épico, cinematográfico
- `happy` - Alegre
- `sad` - Melancólico
- `mysterious` - Intrigante
- `romantic` - Amor
- `neutral` - Corporativo

```bash
python main.py "Script" --music dramatic
```

La música tiene **auto-ducking**: baja al 20% cuando hay voz, sube al 80% en silencios.

## 🎙️ Voces Disponibles

```bash
python main.py --list-voices
```

| Voice ID | Descripción |
|----------|-------------|
| en-US-GuyNeural | Hombre US, casual |
| en-US-JennyNeural | Mujer US, casual |
| en-US-AriaNeural | Mujer US, profesional |
| en-GB-RyanNeural | Hombre UK |
| en-GB-SoniaNeural | Mujer UK |
| en-AU-WilliamNeural | Hombre Australia |

## 📐 Formatos de Video

| Formato | Uso | Dimensiones |
|---------|-----|-------------|
| `9:16` | TikTok, Reels, Shorts | 1080x1920 |
| `16:9` | YouTube | 1920x1080 |
| `1:1` | Instagram Feed | 1080x1080 |

## 🏗️ Arquitectura

```
Script Input
     ↓
[LLM] Parse into scenes + keywords
     ↓
[Pexels/Pixabay] Fetch video clips
     ↓
[Edge TTS] Generate voiceover + word timings
     ↓
[Effects] Apply Ken Burns/pan to clips
     ↓
[Transitions] Fade/slide/zoom between clips  
     ↓
[Subtitles] Animated word-by-word
     ↓
[Music] Auto-ducking background music
     ↓
[Composer] Merge everything → MP4
```

## 💰 Costes

| Componente | Coste |
|------------|-------|
| Edge TTS | GRATIS |
| Pexels API | GRATIS |
| Pixabay API | GRATIS |
| LLM (OpenRouter) | ~$0.001/video |
| **Total** | **~$0** |

## 🔧 API Keys Necesarias

1. **Pexels** (GRATIS): https://www.pexels.com/api/
2. **Pixabay** (GRATIS): https://pixabay.com/api/docs/
3. **OpenRouter** (opcional): https://openrouter.ai/

## 📁 Estructura

```
video-generator/
├── main.py              # CLI principal
├── config.py            # Configuración
├── generator/
│   ├── llm.py          # Script → scenes
│   ├── stock.py        # Pexels + Pixabay
│   ├── tts.py          # Edge TTS
│   ├── music.py        # Background music + ducking
│   ├── effects.py      # Ken Burns, pan, zoom
│   ├── transitions.py  # Fade, slide, swipe
│   ├── subtitles.py    # Animated subtitles
│   └── composer.py     # Final composition
├── output/             # Videos generados
├── temp/               # Archivos temporales
└── assets/             # Logos, fuentes, etc.
```

## 🐍 Uso Programático

```python
import asyncio
from main import generate_video

video_path = asyncio.run(generate_video(
    script="Your script here...",
    voice="en-US-JennyNeural",
    aspect_ratio="9:16",
    subtitle_style="karaoke",
    animated_subtitles=True,
    add_effects=True,
    add_transitions=True,
    transition_type="fade",
    add_music=True,
    music_mood="dramatic",
    output_name="my_video"
))

print(f"Video saved to: {video_path}")
```

## 🚧 Roadmap

- [ ] UI Web (Streamlit/Gradio)
- [ ] API REST
- [ ] Templates predefinidos
- [ ] Generación de video con IA (Runway/Stability)
- [ ] Más estilos de subtítulos
- [ ] Soporte para español

## 📝 License

MIT - Haz lo que quieras con esto.

---

**Creado porque CapCut tiene límites.** 🚀
