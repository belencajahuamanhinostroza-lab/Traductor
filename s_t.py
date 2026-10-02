import os
import glob
import time
import streamlit as st

from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
from gtts import gTTS
from googletrans import Translator


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Traductor por Voz",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DISEÑO
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
    box-sizing: border-box;
}

/* Fondo completo */
html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    min-height: 100%;
}

.stApp {
    background: linear-gradient(
        135deg,
        #ffd6e7 0%,
        #fbcfe8 35%,
        #dbeafe 70%,
        #bae6fd 100%
    );
    background-attachment: fixed;
    color: #000000;
}

/* Mantener el degradado detrás de todo el contenido */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        135deg,
        #ffd6e7 0%,
        #fbcfe8 35%,
        #dbeafe 70%,
        #bae6fd 100%
    );
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Ocultar elementos innecesarios */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ============================================================
   BARRA DE DESPLAZAMIENTO
   ============================================================ */

html {
    scrollbar-width: thin;
    scrollbar-color: #38bdf8 #fbcfe8;
}

::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: linear-gradient(
        180deg,
        #ffd6e7,
        #dbeafe,
        #bae6fd
    );
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(
        180deg,
        #38bdf8,
        #60a5fa,
        #0ea5e9
    );
    border-radius: 20px;
    border: 2px solid #dbeafe;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(
        180deg,
        #0ea5e9,
        #2563eb
    );
}

/* ============================================================
   CONTENEDOR PRINCIPAL EN GRILLA
   ============================================================ */

[data-testid="stMainBlockContainer"] {
    max-width: 1200px;
    margin: 0 auto;
    padding-left: 35px;
    padding-right: 35px;
}

/* ============================================================
   TÍTULO
   ============================================================ */

.main-title {
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-size: 46px;
    font-weight: 800;
    color: #000000;
    margin-top: 10px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    font-weight: 500;
    color: #000000;
    margin-bottom: 30px;
}

/* ============================================================
   TARJETAS CENTRADAS
   ============================================================ */

.card {
    width: 100%;
    max-width: 900px;
    margin: 0 auto 22px auto;
    background: rgba(255,255,255,0.48);
    border: 2px solid #38bdf8;
    border-radius: 24px;
    padding: 25px;
    box-shadow: 0 0 10px rgba(56,189,248,0.22);
    backdrop-filter: blur(12px);
    color: #000000;
}

.card-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    color: #000000;
    margin-bottom: 15px;
}

/* ============================================================
   CAJAS DE TEXTO
   ============================================================ */

.text-box {
    background: rgba(255,255,255,0.72);
    border: 2px solid #38bdf8;
    border-radius: 17px;
    padding: 20px;
    font-size: 18px;
    font-weight: 500;
    color: #000000;
    min-height: 70px;
    text-align: center;
    box-shadow: 0 0 7px rgba(56,189,248,0.18);
}

/* ============================================================
   BOTONES
   ============================================================ */

div.stButton {
    display: flex;
    justify-content: center;
}

div.stButton > button {
    width: 100%;
    max-width: 420px;
    min-height: 55px;
    border-radius: 18px;
    border: 2px solid #38bdf8;
    background: linear-gradient(
        135deg,
        #60a5fa,
        #38bdf8
    );
    color: #000000;
    font-size: 18px;
    font-weight: 700;
    box-shadow: 0 0 8px rgba(56,189,248,0.25);
    transition: 0.25s;
}

div.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #93c5fd,
        #38bdf8
    );
    border-color: #0ea5e9;
    color: #000000;
    transform: translateY(-2px);
}

/* ============================================================
   SELECTORES
   ============================================================ */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.78);
    border: 2px solid #38bdf8;
    border-radius: 14px;
    color: #000000;
    box-shadow: none;
}

div[data-baseweb="select"] * {
    color: #000000;
}

label,
.stSelectbox label,
.stCheckbox label {
    color: #000000 !important;
}

/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffd6e7 0%,
        #fbcfe8 40%,
        #dbeafe 75%,
        #bae6fd 100%
    );
    border-right: 2px solid #38bdf8;
    box-shadow: none;
}

section[data-testid="stSidebar"] > div {
    background: transparent;
}

.sidebar-title {
    text-align: center;
    font-size: 26px;
    font-weight: 800;
    color: #000000;
}

.sidebar-text {
    color: #000000;
    line-height: 1.7;
    font-size: 15px;
    text-align: center;
}

/* ============================================================
   RESULTADOS
   ============================================================ */

.result-title {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    color: #000000;
    margin-bottom: 12px;
}

.stCheckbox {
    color: #000000;
    font-weight: 500;
}

/* ============================================================
   AUDIO
   ============================================================ */

audio {
    width: 100%;
}

/* ============================================================
   ALERTAS
   ============================================================ */

div[data-testid="stAlert"] {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🎤 Traductor</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="sidebar-text">

        <b>¿Cómo utilizar la aplicación?</b>

        <br><br>

        1. Presiona el botón <b>Escuchar</b>.

        <br><br>

        2. Habla claramente.

        <br><br>

        3. Selecciona el idioma de entrada.

        <br><br>

        4. Selecciona el idioma de salida.

        <br><br>

        5. Presiona <b>Convertir y traducir</b>.

        <br><br>

        6. Escucha el resultado.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.caption("🌎 Traducción por voz")


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="main-title">🌎 TRADUCTOR POR VOZ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Escucha, traduce y reproduce tu traducción fácilmente</div>',
    unsafe_allow_html=True
)


# ============================================================
# IMAGEN
# ============================================================

col_img, col_info = st.columns([1, 1.5], gap="large")

with col_img:

    image = Image.open("traduccion.jpg")

    st.image(
        image,
        width=300
    )


with col_info:

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        🎙️ Habla para traducir
        </div>

        <div class="text-box">
        Presiona el botón y habla lo que deseas traducir.
        La aplicación reconocerá tu voz y posteriormente
        convertirá el texto al idioma seleccionado.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RECONOCIMIENTO DE VOZ
# ============================================================

st.markdown(
    """
    <div class="card">

    <div class="card-title">
    🎤 Reconocimiento de voz
    </div>
    """,
    unsafe_allow_html=True
)

stt_button = Button(
    label="🎤  ESCUCHAR",
    width=300,
    height=55
)

stt_button.js_on_event(
    "button_click",
    CustomJS(
        code="""
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
                        {
                            detail: value
                        }
                    )
                );

            }

        };

        recognition.onend = function() {

            console.log(
                "Reconocimiento detenido"
            );

        };

        recognition.onerror = function(event) {

            console.log(
                "Error:",
                event.error
            );

        };

        recognition.start();
        """
    )
)

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# SI SE RECONOCIÓ VOZ
# ============================================================

if result and "GET_TEXT" in result:

    text = str(
        result.get("GET_TEXT")
    )


    # ========================================================
    # TEXTO RECONOCIDO
    # ========================================================

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        📝 Texto reconocido
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="text-box">
        {text}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # CARPETA DE AUDIOS
    # ========================================================

    os.makedirs(
        "temp",
        exist_ok=True
    )

    translator = Translator()


    # ========================================================
    # IDIOMAS
    # ========================================================

    language_codes = {
        "Inglés": "en",
        "Español": "es",
        "Francés": "fr",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja",
        "Alemán": "de",
        "Danés": "da"
    }

    languages = list(
        language_codes.keys()
    )


    # ========================================================
    # CONFIGURACIÓN
    # ========================================================

    st.markdown(
        """
        <div class="card">

        <div class="card-title">
        🌎 Configuración de traducción
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # COLUMNAS DE IDIOMAS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        in_lang = st.selectbox(
            "🗣️ Idioma de entrada",
            languages,
            key="input_language"
        )

    with col2:

        out_lang = st.selectbox(
            "🌎 Idioma de salida",
            languages,
            key="output_language"
        )

    input_language = language_codes[
        in_lang
    ]

    output_language = language_codes[
        out_lang
    ]


    # ========================================================
    # ACENTO
    # ========================================================

    english_accent = st.selectbox(
        "🔊 Selecciona el acento",
        [
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
            "Dinamarca",
            "Francia"
        ],
        key="accent"
    )

    accent_codes = {
        "Defecto": "com",
        "Español": "com.mx",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canada": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za",
        "Dinamarca": "dk",
        "Francia": "fr"
    }

    tld = accent_codes[
        english_accent
    ]

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # FUNCIÓN DE TRADUCCIÓN
    # ========================================================

    def text_to_speech(
        input_language,
        output_language,
        text,
        tld
    ):

        translation = translator.translate(
            text,
            src=input_language,
            dest=output_language
        )

        translated_text = translation.text

        tts = gTTS(
            translated_text,
            lang=output_language,
            tld=tld,
            slow=False
        )

        file_name = text[:20]

        file_name = "".join(
            character
            for character in file_name
            if character.isalnum()
            or character in (" ", "_", "-")
        )

        if not file_name:

            file_name = "audio"

        file_name = file_name.replace(
            " ",
            "_"
        )

        file_path = (
            f"temp/{file_name}.mp3"
        )

        tts.save(
            file_path
        )

        return (
            file_name,
            translated_text
        )


    # ========================================================
    # OPCIÓN MOSTRAR TEXTO
    # ========================================================

    display_output_text = st.checkbox(
        "📝 Mostrar el texto traducido",
        key="show_translation"
    )


    # ========================================================
    # BOTÓN CONVERTIR
    # ========================================================

    if st.button(
        "🌎 CONVERTIR Y TRADUCIR",
        type="primary",
        key="translate_button"
    ):

        try:

            with st.spinner(
                "Traduciendo..."
            ):

                result_file, output_text = text_to_speech(
                    input_language,
                    output_language,
                    text,
                    tld
                )

            st.success(
                "¡Traducción realizada correctamente!"
            )


            # =================================================
            # AUDIO
            # =================================================

            st.markdown(
                """
                <div class="card">

                <div class="result-title">
                🔊 Tu audio
                </div>
                """,
                unsafe_allow_html=True
            )

            audio_path = (
                f"temp/{result_file}.mp3"
            )

            with open(
                audio_path,
                "rb"
            ) as audio_file:

                audio_bytes = audio_file.read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )


            # =================================================
            # TEXTO DE SALIDA
            # =================================================

            if display_output_text:

                st.markdown(
                    "<hr>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div class="result-title">
                    📝 Texto de salida
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="text-box">
                    {output_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        except Exception as error:

            st.error(
                "Ocurrió un error al realizar la traducción."
            )

            st.warning(
                f"Detalles: {error}"
            )


# ============================================================
# LIMPIAR AUDIOS ANTIGUOS
# ============================================================

def remove_files(days):

    if not os.path.exists("temp"):
        return

    files = glob.glob(
        "temp/*.mp3"
    )

    current_time = time.time()

    max_age = days * 86400

    for file in files:

        try:

            if os.stat(file).st_mtime < current_time - max_age:

                os.remove(file)

        except Exception:

            pass


remove_files(7)

