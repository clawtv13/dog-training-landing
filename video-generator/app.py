"""
Video Generator - Web UI (Streamlit)
Estilo CapCut "Create with AI"
"""

import streamlit as st
import asyncio
from pathlib import Path
import time
import os

# Configure page
st.set_page_config(
    page_title="Video Generator AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for CapCut-like styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1000px;
    }
    
    /* Header */
    .header-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #00d4aa, #00b894);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Generate button */
    .stButton > button {
        background: linear-gradient(90deg, #00d4aa, #00b894);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 212, 170, 0.4);
    }
    
    /* Progress */
    .stProgress > div > div {
        background-color: #00d4aa;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="header-title">🎬 Video Generator AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">Crea videos con IA desde texto • Estilo CapCut</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📹 Script to Video", "🎙️ Text to Speech", "⚙️ Settings"])

with tab1:
    # Script input
    script = st.text_area(
        "Tu guión / script",
        placeholder='''Ejemplo:
Is THIS your life right now? Constant barking. Destroyed furniture. A dog that just won't listen. You've tried everything but nothing works. What if the problem isn't your dog? It's how you've been trained to train them. Discover the brain training method that's transforming stubborn dogs into obedient best friends. No treats. No punishment. Just science. Link in bio.''',
        height=180,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # === VIDEO SOURCE SELECTION ===
    st.markdown("### 🎨 Fuente de video")
    
    video_source = st.radio(
        "Elige cómo generar las imágenes:",
        options=[
            ("📹 Stock Videos (Gratis)", "stock"),
            ("🎨 Imágenes IA - Flux (desde $0.003/img)", "ai"),
        ],
        format_func=lambda x: x[0],
        horizontal=True
    )
    
    # AI Image options (only show if AI selected)
    if video_source[1] == "ai":
        col_ai1, col_ai2 = st.columns(2)
        
        with col_ai1:
            ai_model = st.selectbox(
                "🤖 Modelo Flux",
                options=[
                    ("⚡ Schnell (rápido, $0.003)", "schnell"),
                    ("✨ Pro 1.1 (alta calidad, $0.04)", "pro"),
                    ("🌟 Pro 2 (mejor calidad, $0.05)", "pro2"),
                ],
                format_func=lambda x: x[0]
            )
        
        with col_ai2:
            ai_style = st.selectbox(
                "🎭 Estilo Visual",
                options=[
                    ("🎬 Película Realista", "realistic_film"),
                    ("📸 Fotorrealista", "photorealistic"),
                    ("🎥 Cinematográfico", "cinematic"),
                    ("🎨 Arte Digital", "digital_art"),
                    ("🌸 Anime", "anime"),
                    ("🧊 3D Render", "3d_render"),
                    ("📷 Vintage", "vintage"),
                    ("⬜ Minimalista", "minimalist"),
                ],
                format_func=lambda x: x[0]
            )
        
        # Check for API key
        replicate_key = os.getenv("REPLICATE_API_TOKEN")
        if not replicate_key:
            st.warning("⚠️ Necesitas configurar REPLICATE_API_TOKEN en .env para usar imágenes IA")
    
    st.markdown("---")
    
    # === VOICE AND SUBTITLES ===
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        voice = st.selectbox(
            "🎙️ Voz",
            options=[
                ("🧔 Guy (US)", "en-US-GuyNeural"),
                ("👩 Jenny (US)", "en-US-JennyNeural"),
                ("👩 Aria (US)", "en-US-AriaNeural"),
                ("🧔 Ryan (UK)", "en-GB-RyanNeural"),
                ("👩 Sonia (UK)", "en-GB-SoniaNeural"),
                ("🧔 William (AU)", "en-AU-WilliamNeural"),
            ],
            format_func=lambda x: x[0]
        )
    
    with col2:
        subtitle_style = st.selectbox(
            "💬 Subtítulos",
            options=[
                ("✨ Karaoke", "karaoke"),
                ("🔄 Bounce", "bounce"),
                ("🎯 Highlight", "highlight_box"),
                ("🌊 Wave", "wave"),
                ("📝 Simple", "bold"),
            ],
            format_func=lambda x: x[0]
        )
    
    with col3:
        aspect_ratio = st.selectbox(
            "📐 Formato",
            options=[
                ("📱 9:16 (TikTok)", "9:16"),
                ("🖥️ 16:9 (YouTube)", "16:9"),
                ("⬛ 1:1 (Instagram)", "1:1"),
            ],
            format_func=lambda x: x[0]
        )
    
    with col4:
        music_mood = st.selectbox(
            "🎵 Música",
            options=[
                ("🚫 Sin música", None),
                ("😌 Calm", "calm"),
                ("⚡ Energetic", "energetic"),
                ("🎭 Dramatic", "dramatic"),
                ("😊 Happy", "happy"),
                ("😢 Sad", "sad"),
            ],
            format_func=lambda x: x[0]
        )
    
    # Advanced options (collapsible)
    with st.expander("⚙️ Opciones avanzadas"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            add_effects = st.checkbox("🎥 Efectos Ken Burns", value=True)
        with col2:
            add_transitions = st.checkbox("🔄 Transiciones", value=True)
        with col3:
            transition_type = st.selectbox(
                "Tipo de transición",
                ["fade", "slide", "zoom", "swipe", "random"],
                disabled=not add_transitions
            )
        
        output_name = st.text_input("Nombre del archivo", value="video_output")
    
    # Generate button
    st.markdown("<br>", unsafe_allow_html=True)
    
    generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
    
    with generate_col2:
        generate_button = st.button("✨ Generar Video", use_container_width=True, type="primary")
    
    # Generation logic
    if generate_button:
        if not script.strip():
            st.error("⚠️ Por favor, escribe un guión primero")
        else:
            try:
                from generator import (
                    parse_script_to_scenes,
                    get_videos_for_scenes,
                    generate_speech_for_scenes,
                    generate_subtitles_from_timings,
                    cleanup_temp_files
                )
                from generator.composer import compose_video
                from config import OUTPUT_DIR
                
                # Progress container
                progress_container = st.empty()
                status_container = st.empty()
                
                async def generate():
                    orientation = "portrait" if aspect_ratio[1] == "9:16" else "landscape"
                    
                    # Step 1: Parse script
                    status_container.info("🎬 Analizando script con IA...")
                    scenes = await parse_script_to_scenes(script)
                    progress_container.progress(15)
                    
                    # Step 2: Generate voice
                    status_container.info("🎙️ Generando voz...")
                    audio_path, word_timings = await generate_speech_for_scenes(scenes, voice[1])
                    progress_container.progress(30)
                    
                    # Step 3: Get visuals (stock or AI)
                    if video_source[1] == "ai":
                        # AI-generated images
                        status_container.info(f"🎨 Generando imágenes con Flux ({ai_model[1]})...")
                        from generator.image_gen import generate_images_for_scenes
                        image_paths = await generate_images_for_scenes(
                            scenes=scenes,
                            style=ai_style[1],
                            model=ai_model[1],
                            aspect_ratio=aspect_ratio[1]
                        )
                        # Convert images to video clips format
                        video_clips = image_paths
                    else:
                        # Stock videos
                        status_container.info("🎥 Descargando clips de video...")
                        video_clips = await get_videos_for_scenes(scenes, orientation)
                    
                    progress_container.progress(60)
                    
                    # Step 4: Create subtitles
                    status_container.info("📝 Creando subtítulos...")
                    static_subtitles = generate_subtitles_from_timings(word_timings)
                    progress_container.progress(70)
                    
                    # Step 5: Compose video
                    status_container.info("🎞️ Componiendo video final...")
                    
                    # Determine if using images (need different processing)
                    use_images = video_source[1] == "ai"
                    
                    output_path = compose_video(
                        video_clips=video_clips,
                        audio_path=audio_path,
                        subtitles=static_subtitles,
                        word_timings=word_timings,
                        scenes=scenes,
                        output_name=output_name,
                        aspect_ratio=aspect_ratio[1],
                        animated_subtitles=True,
                        subtitle_animation=subtitle_style[1],
                        add_effects=add_effects,
                        add_transitions=add_transitions,
                        transition_type=transition_type if add_transitions else "fade",
                        add_music=music_mood[1] is not None if music_mood else False,
                        music_mood=music_mood[1] if music_mood and music_mood[1] else "calm",
                        use_images=use_images,
                    )
                    progress_container.progress(100)
                    
                    cleanup_temp_files()
                    return output_path
                
                # Run async generation
                output_path = asyncio.run(generate())
                
                # Success!
                status_container.empty()
                progress_container.empty()
                
                st.success("✅ ¡Video generado exitosamente!")
                
                # Show video
                st.video(str(output_path))
                
                # Download button
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Descargar Video",
                        data=f,
                        file_name=f"{output_name}.mp4",
                        mime="video/mp4"
                    )
                
            except ImportError as e:
                st.error(f"❌ Error: Faltan dependencias. Ejecuta: pip install -r requirements.txt\n{e}")
            except Exception as e:
                st.error(f"❌ Error al generar video: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

with tab2:
    st.markdown("### 🎙️ Text to Speech")
    st.markdown("Genera solo el audio sin video")
    
    tts_text = st.text_area("Texto para convertir a voz", height=150, key="tts_text")
    
    col1, col2 = st.columns(2)
    with col1:
        tts_voice = st.selectbox(
            "Voz",
            options=[
                ("🧔 Guy (US)", "en-US-GuyNeural"),
                ("👩 Jenny (US)", "en-US-JennyNeural"),
                ("👩 Aria (US)", "en-US-AriaNeural"),
                ("🧔 Ryan (UK)", "en-GB-RyanNeural"),
            ],
            format_func=lambda x: x[0],
            key="tts_voice"
        )
    
    if st.button("🎙️ Generar Audio", key="tts_button"):
        if tts_text.strip():
            try:
                from generator.tts import generate_speech_sync
                from config import OUTPUT_DIR
                
                with st.spinner("Generando audio..."):
                    output_path = OUTPUT_DIR / "tts_output.mp3"
                    audio_path, _ = generate_speech_sync(tts_text, tts_voice[1], output_path)
                
                st.audio(str(audio_path))
                
                with open(audio_path, "rb") as f:
                    st.download_button(
                        label="📥 Descargar Audio",
                        data=f,
                        file_name="audio.mp3",
                        mime="audio/mpeg"
                    )
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Escribe algo primero")

with tab3:
    st.markdown("### ⚙️ Configuración")
    
    st.markdown("#### API Keys Status")
    
    from config import PEXELS_API_KEY, PIXABAY_API_KEY, OPENROUTER_API_KEY
    replicate_key = os.getenv("REPLICATE_API_TOKEN")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Gratis:**")
        if PEXELS_API_KEY:
            st.success("✅ Pexels API (videos)")
        else:
            st.error("❌ Pexels API")
        
        if PIXABAY_API_KEY:
            st.success("✅ Pixabay API (videos)")
        else:
            st.warning("⚠️ Pixabay (opcional)")
        
        st.success("✅ Edge TTS (voz) - Sin API")
    
    with col2:
        st.markdown("**De pago:**")
        if OPENROUTER_API_KEY:
            st.success("✅ OpenRouter (LLM)")
        else:
            st.warning("⚠️ OpenRouter")
        
        if replicate_key:
            st.success("✅ Replicate (Flux AI)")
        else:
            st.warning("⚠️ Replicate (imágenes IA)")
    
    st.markdown("---")
    st.markdown("#### Costos estimados por video")
    st.markdown("""
    | Componente | Costo |
    |------------|-------|
    | Stock videos (Pexels) | **Gratis** |
    | Voz (Edge TTS) | **Gratis** |
    | LLM (OpenRouter) | ~$0.001 |
    | Flux Schnell (10 imgs) | ~$0.03 |
    | Flux Pro 2 (10 imgs) | ~$0.50 |
    """)
    
    st.markdown("---")
    st.markdown("#### Output Directory")
    from config import OUTPUT_DIR
    st.code(str(OUTPUT_DIR))

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #999; font-size: 12px;">Video Generator AI • Tu clon de CapCut • Stock gratis + IA opcional</p>',
    unsafe_allow_html=True
)
