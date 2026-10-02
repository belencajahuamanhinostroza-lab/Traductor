import os
import time
import glob
import streamlit as st

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

from gtts import gTTS
from googletrans import Translator


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Luma Translate",
    page_icon="◉",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# ESTADOS
# =========================================================

if "spoken_text" not in st.session_state:
    st.session_state.spoken_text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ------------------------------
   GENERAL
------------------------------ */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(221, 203, 255, 0.65), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(255, 216, 239, 0.75), transparent 30%),
        radial-gradient(circle at 50% 90%, rgba(214, 226, 255, 0.75), transparent 35%),
        linear-gradient(135deg, #f8f4ff 0%, #f8f6ff 45%, #fdf4fa 100%);
    min-height: 100vh;
}

/* Quitar padding excesivo */

.block-container {
    max-width: 480px !important;
    padding-top: 25px !important;
    padding-bottom: 100px !important;
}

/* ------------------------------
   HEADER
------------------------------ */

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}

.logo-area {
    display: flex;
    align-items: center;
    gap: 11px;
}

.logo {
    width: 43px;
    height: 43px;
    border-radius: 15px;
    background: linear-gradient(135deg, #9c6cff, #c9a7ff);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 21px;
    box-shadow: 0 8px 20px rgba(145, 101, 220, 0.25);
}

.brand {
    font-size: 17px;
    font-weight: 700;
    color: #25232d;
}

.subtitle-brand {
    font-size: 11px;
    color: #9995a5;
    margin-top: 2px;
}

.profile {
    width: 39px;
    height: 39px;
    border-radius: 50%;
    background: linear-gradient(135deg, #eee6ff, #ffffff);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8d68d9;
    font-size: 18px;
    box-shadow: 0 5px 15px rgba(100,80,130,0.08);
}

/* ------------------------------
   TITULO
------------------------------ */

.welcome {
    margin-top: 12px;
    margin-bottom: 18px;
}

.welcome-small {
    color: #9b96a7;
    font-size: 13px;
    margin-bottom: 5px;
}

.welcome-title {
    color: #272431;
    font-size: 28px;
    line-height: 1.2;
    font-weight: 700;
    letter-spacing: -0.8px;
}

.welcome-title span {
    background: linear-gradient(90deg, #8d62dc, #bd82d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ------------------------------
   MAIN VOICE CARD
------------------------------ */

.voice-card {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 30px;
    padding: 27px 22px 24px 22px;
    box-shadow:
        0 20px 45px rgba(116, 94, 151, 0.12),
        inset 0 1px 0 rgba(255,255,255,0.8);
    backdrop-filter: blur(20px);
    text-align: center;
    margin-bottom: 17px;
}

.voice-label {
    font-size: 12px;
    color: #aaa5b4;
    margin-bottom: 6px;
}

.voice-title {
    font-size: 20px;
    font-weight: 600;
    color: #34303e;
}

.voice-description {
    font-size: 12px;
    color: #9994a3;
    margin-top: 7px;
}

/* ------------------------------
   ORBE
------------------------------ */

.orb-container {
    height: 230px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.orb {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    position: relative;
    background:
        radial-gradient(circle at 28% 25%, #ffffff 0%, rgba(255,255,255,0.8) 8%, transparent 20%),
        radial-gradient(circle at 70% 30%, #e4c9ff 0%, #b78cf4 25%, transparent 55%),
        radial-gradient(circle at 30% 70%, #8e72dc 0%, #dca5e8 35%, transparent 65%),
        linear-gradient(135deg, #b8a2ff, #e5b5ed, #9b83e9);
    box-shadow:
        inset -18px -18px 35px rgba(82, 51, 140, 0.18),
        inset 15px 12px 25px rgba(255,255,255,0.65),
        0 20px 35px rgba(132, 92, 189, 0.22);
    animation: floating 4s ease-in-out infinite;
}

.orb::before {
    content: "";
    position: absolute;
    width: 65px;
    height: 65px;
    border-radius: 50%;
    top: 20px;
    left: 30px;
    background: rgba(255,255,255,0.22);
    filter: blur(10px);
}

.orb::after {
    content: "";
    position: absolute;
    width: 105px;
    height: 105px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.4);
    top: 23px;
    left: 22px;
}

@keyframes floating {
    0%,100% {
        transform: translateY(0px) rotate(0deg);
    }

    50% {
        transform: translateY(-8px) rotate(3deg);
    }
}

/* ------------------------------
   MICROFONO
------------------------------ */

.mic-wrapper {
    margin-top: -10px;
    display: flex;
    justify-content: center;
}

.mic-circle {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    background: linear-gradient(135deg, #9b6ee7, #bd8ce9);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 25px;
    box-shadow:
        0 10px 25px rgba(139, 96, 206, 0.28),
        0 0 0 8px rgba(181, 147, 235, 0.12);
}

/* ------------------------------
   TARJETAS
------------------------------ */

.section-title {
    font-size: 14px;
    font-weight: 600;
    color: #403b4a;
    margin: 20px 2px 10px;
}

.option-card {
    background: rgba(255,255,255,0.73);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 22px;
    padding: 17px;
    box-shadow: 0 12px 30px rgba(100,80,130,0.08);
    margin-bottom: 11px;
}

.option-row {
    display: flex;
    align-items: center;
    gap: 13px;
}

.option-icon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: #f1eaff;
    color: #956dd9;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
}

.option-title {
    color: #393541;
    font-size: 13px;
    font-weight: 600;
}

.option-description {
    color: #a19ba9;
    font-size: 10px;
    margin-top: 3px;
}

/* ------------------------------
   RESULTADO
------------------------------ */

.result-card {
    background: rgba(255,255,255,0.82);
    border-radius: 23px;
    padding: 18px;
    margin-top: 14px;
    border: 1px solid rgba(255,255,255,0.95);
    box-shadow: 0 12px 30px rgba(90,70,120,0.08);
}

.result-label {
    color: #a09baa;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 7px;
}

.result-text {
    color: #35313d;
    font-size: 15px;
    line-height: 1.5;
}

/* ------------------------------
   SELECTBOX
------------------------------ */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.78) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(220,214,230,0.8) !important;
    min-height: 46px;
}

/* ------------------------------
   BOTONES STREAMLIT
------------------------------ */

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 18px;
    border: none;
    background: linear-gradient(135deg, #9b6de5, #b886e9);
    color: white;
    font-size: 14px;
    font-weight: 600;
    box-shadow: 0 10px 22px rgba(137, 91, 198, 0.23);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 13px 27px rgba(137, 91, 198, 0.3);
    color: white;
}

.stButton > button:active {
    transform: scale(0.98);
}

/* ------------------------------
   BOKEH BOTÓN
------------------------------ */

.bk-btn {
    width: 100% !important;
    height: 55px !important;
    border-radius: 19px !important;
    border: none !important;
    background: linear-gradient(135deg, #9b6de5, #b886e9) !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    box-shadow: 0 10px 22px rgba(137, 91, 198, 0.23) !important;
}

/* ------------------------------
   AUDIO
------------------------------ */

audio {
    width: 100%;
    border-radius: 15px;
}

/* ------------------------------
   NAVEGACIÓN INFERIOR
------------------------------ */

.bottom-nav {
    position: fixed;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    width: min(430px, calc(100% - 30px));
    height: 67px;
    border-radius: 25px;
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(255,255,255,0.95);
    backdrop-filter: blur(18px);
    box-shadow: 0 15px 35px rgba(91,75,118,0.15);
    display: flex;
    align-items: center;
    justify-content: space-around;
    z-index: 999;
}

.nav-item {
    color: #aaa4b2;
    font-size: 19px;
    text-align: center;
}

.nav-item span {
    display: block;
    font-size: 9px;
    margin-top: 3px;
}

.nav-active {
    width: 48px;
    height: 48px;
    border-radius: 16px;
    background: linear-gradient(135deg, #9d70e6, #bd8ae8);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    box-shadow: 0 8px 20px rgba(142,93,202,0.28);
}

/* ------------------------------
   SIDEBAR
------------------------------ */

section[data-testid="stSidebar"] {
    background: #f8f4ff;
}

section[data-testid="stSidebar"] * {
    color: #3c3747;
}

/* ------------------------------
   MOBILE
------------------------------ */

@media (max-width: 600px) {

    .block-container {
        padding-left: 18px !important;
        padding-right: 18px !important;
    }

    .welcome-title {
        font-size: 26px;
    }

    .voice-card {
        padding: 24px 18px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header">

    <div class="logo-area">
        <div class="logo">✦</div>
        <div>
            <div class="brand">Luma Translate</div>
            <div class="subtitle-brand">Traducción inteligente</div>
        </div>
    </div>

    <div class="profile">◉</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# BIENVENIDA
# =========================================================

st.markdown("""
<div class="welcome">

    <div class="welcome-small">
        Hola, bienvenida 👋
    </div>

    <div class="welcome-title">
        ¿Qué quieres <span>traducir</span> hoy?
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# TARJETA PRINCIPAL
# =========================================================

st.markdown("""
<div class="voice-card">

    <div class="voice-label">
        TRADUCCIÓN POR VOZ
    </div>

    <div class="voice-title">
        Habla y yo traduzco
    </div>

    <div class="voice-description">
        Presiona el botón y comienza a hablar
    </div>

    <div class="orb-container">
        <div class="orb"></div>
    </div>

    <div class="mic-wrapper">
        <div class="mic-circle">
            🎙
        </div>
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# BOTÓN DE RECONOCIMIENTO
# =========================================================

st.markdown("""
<div class="section-title">
    Escuchar
</div>
""", unsafe_allow_html=True)


stt_button = Button(
    label="🎙  Presiona para hablar",
    width=400,
    height=55
)


stt_button.js_on_event(
    "button_click",
    CustomJS(code="""

        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'es-ES';

        recognition.onresult = function(e) {

            var value = "";

            for (
                var i = e.resultIndex;
                i < e.results.length;
                ++i
            ) {

                if (e.results[i].isFinal) {

                    value += e.results[i][0].transcript;

                }

            }

            if (value != "") {

                document.dispatchEvent(
                    new CustomEvent(
                        "GET_TEXT",
                        {detail: value}
                    )
                );

            }

        };

        recognition.onend = function() {
            console.log("Reconocimiento terminado");
        };

        recognition.onerror = function(event) {
            console.log("Error:", event.error);
        };

        recognition.start();

    """)
)


result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=70,
    debounce_time=0
)


# =========================================================
# GUARDAR TEXTO
# =========================================================

if result and "GET_TEXT" in result:

    st.session_state.spoken_text = result.get("GET_TEXT")


# =========================================================
# TEXTO DETECTADO
# =========================================================

if st.session_state.spoken_text:

    st.markdown("""
    <div class="section-title">
        Lo que dijiste
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-label">
                Texto detectado
            </div>

            <div class="result-text">
                {st.session_state.spoken_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CONFIGURACIÓN
# =========================================================

if st.session_state.spoken_text:

    st.markdown("""
    <div class="section-title">
        Configura tu traducción
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------
    # IDIOMAS
    # -----------------------------------------

    languages = {
        "Español": "es",
        "Inglés": "en",
        "Francés": "fr",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja",
        "Alemán": "de",
        "Danés": "da"
    }

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="option-card">

            <div class="option-row">

                <div class="option-icon">
                    ◉
                </div>

                <div>
                    <div class="option-title">
                        Idioma de entrada
                    </div>

                    <div class="option-description">
                        Lo que estás hablando
                    </div>
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

        input_name = st.selectbox(
            "Idioma de entrada",
            list(languages.keys()),
            label_visibility="collapsed"
        )

    with col2:

        st.markdown("""
        <div class="option-card">

            <div class="option-row">

                <div class="option-icon">
                    ✦
                </div>

                <div>
                    <div class="option-title">
                        Idioma de salida
                    </div>

                    <div class="option-description">
                        Resultado traducido
                    </div>
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

        output_name = st.selectbox(
            "Idioma de salida",
            list(languages.keys()),
            index=1,
            label_visibility="collapsed"
        )


    input_language = languages[input_name]
    output_language = languages[output_name]


    # =====================================================
    # ACENTO
    # =====================================================

    st.markdown("""
    <div class="option-card">

        <div class="option-row">

            <div class="option-icon">
                ♫
            </div>

            <div>
                <div class="option-title">
                    Acento de voz
                </div>

                <div class="option-description">
                    Personaliza cómo sonará la traducción
                </div>
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    accents = {
        "Predeterminado": "com",
        "Español": "com.mx",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canadá": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za",
        "Alemania": "de",
        "Francia": "fr",
        "Dinamarca": "dk"
    }


    english_accent = st.selectbox(
        "Acento",
        list(accents.keys()),
        label_visibility="collapsed"
    )

    tld = accents[english_accent]


    # =====================================================
    # CONVERTIR
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✦  Traducir y generar audio"):

        try:

            translator = Translator()

            text = st.session_state.spoken_text

            translation = translator.translate(
                text,
                src=input_language,
                dest=output_language
            )

            translated_text = translation.text

            os.makedirs("temp", exist_ok=True)

            safe_name = "".join(
                c for c in text[:20]
                if c.isalnum() or c in (" ", "_", "-")
            ).strip()

            if not safe_name:
                safe_name = "audio"

            file_path = f"temp/{safe_name}.mp3"

            tts = gTTS(
                translated_text,
                lang=output_language,
                tld=tld,
                slow=False
            )

            tts.save(file_path)

            st.session_state.translated_text = translated_text
            st.session_state.audio_file = file_path

            st.success("Traducción realizada ✨")

        except Exception as e:

            st.error(
                f"No se pudo realizar la traducción: {e}"
            )


# =========================================================
# RESULTADO DE TRADUCCIÓN
# =========================================================

if st.session_state.translated_text:

    st.markdown("""
    <div class="section-title">
        Resultado
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-label">
                Traducción
            </div>

            <div class="result-text">
                {st.session_state.translated_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# AUDIO
# =========================================================

if (
    st.session_state.audio_file
    and os.path.exists(st.session_state.audio_file)
):

    st.markdown("""
    <div class="section-title">
        Escucha la traducción
    </div>
    """, unsafe_allow_html=True)

    with open(
        st.session_state.audio_file,
        "rb"
    ) as audio_file:

        audio_bytes = audio_file.read()

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )


# =========================================================
# LIMPIEZA DE ARCHIVOS
# =========================================================

def remove_files(days):

    mp3_files = glob.glob("temp/*.mp3")

    if len(mp3_files) == 0:
        return

    now = time.time()

    limit = days * 86400

    for file in mp3_files:

        try:

            if os.stat(file).st_mtime < now - limit:

                os.remove(file)

        except:
            pass


remove_files(7)


# =========================================================
# NAVEGACIÓN INFERIOR
# =========================================================

st.markdown("""
<div class="bottom-nav">

    <div class="nav-item">
        ⌂
        <span>Inicio</span>
    </div>

    <div class="nav-item">
        ◷
        <span>Historial</span>
    </div>

    <div class="nav-active">
        🎙
    </div>

    <div class="nav-item">
        ♡
        <span>Favoritos</span>
    </div>

    <div class="nav-item">
        ⚙
        <span>Ajustes</span>
    </div>

</div>
""", unsafe_allow_html=True)


        
    



        
    


