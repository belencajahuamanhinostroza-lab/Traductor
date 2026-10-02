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

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    min-height: 100%;
}

.stApp {
    background:
        radial-gradient(circle at 10% 15%, rgba(220, 190, 245, 0.32), transparent 30%),
        radial-gradient(circle at 90% 75%, rgba(255, 190, 190, 0.22), transparent 32%),
        linear-gradient(
            120deg,
            #eee5f4 0%,
            #f7f0ef 38%,
            #fbf5eb 62%,
            #fae9e8 100%
        );
    background-attachment: fixed;
    color: #211b2d;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* ============================================================
   ESPACIO GENERAL — inspirado en la referencia
   ============================================================ */

[data-testid="stMainBlockContainer"] {
    max-width: 860px;
    margin: 0 auto;
    padding: 28px 32px 70px 32px;
}

/* ============================================================
   BARRA DE DESPLAZAMIENTO
   ============================================================ */

html {
    scrollbar-width: thin;
    scrollbar-color: #a855f7 #f1e8f5;
}

::-webkit-scrollbar {
    width: 11px;
}

::-webkit-scrollbar-track {
    background: linear-gradient(
        180deg,
        #eee5f4,
        #f7f0ef,
        #fae9e8
    );
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(
        180deg,
        #a855f7,
        #ec4899
    );
    border-radius: 20px;
    border: 2px solid #f7f0ef;
}

/* ============================================================
   TÍTULOS
   ============================================================ */

.main-title {
    text-align: left;
    font-size: 44px;
    line-height: 1.1;
    font-weight: 800;
    color: #211b2d;
    margin: 35px auto 8px auto;
    max-width: 760px;
}

.subtitle {
    text-align: left;
    font-size: 16px;
    line-height: 1.65;
    font-weight: 400;
    color: #655d70;
    margin: 0 auto 42px auto;
    max-width: 760px;
}

/* ============================================================
   CUADROS — contorno violeta/rosado suave
   ============================================================ */

.card {
    width: 100%;
    max-width: 760px;
    margin: 0 auto 26px auto;
    background: rgba(255,255,255,0.30);
    border: 2px solid #b86bea;
    border-radius: 18px;
    padding: 24px 26px;
    box-shadow: 0 8px 28px rgba(125, 74, 155, 0.08);
    backdrop-filter: blur(10px);
    color: #211b2d;
}

.card-title {
    text-align: left;
    font-size: 18px;
    font-weight: 700;
    color: #211b2d;
    margin-bottom: 14px;
}

/* ============================================================
   CAJAS DE TEXTO
   ============================================================ */

.text-box {
    background: rgba(255,255,255,0.62);
    border: 2px solid #c084e9;
    border-radius: 14px;
    padding: 17px 19px;
    font-size: 16px;
    line-height: 1.6;
    font-weight: 500;
    color: #211b2d;
    min-height: 64px;
    text-align: left;
    box-shadow: none;
}

/* ============================================================
   GRILLA DE IDIOMAS
   ============================================================ */

div[data-testid="stHorizontalBlock"] {
    gap: 18px;
}

/* ============================================================
   SELECTORES
   ============================================================ */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.68);
    border: 2px solid #b86bea;
    border-radius: 12px;
    color: #211b2d;
    box-shadow: none;
}

div[data-baseweb="select"] * {
    color: #211b2d;
}

label,
.stSelectbox label,
.stCheckbox label {
    color: #211b2d !important;
    font-weight: 500;
}

/* ============================================================
   BOTÓN ESCUCHAR / BOTONES PRINCIPALES
   ============================================================ */

div.stButton {
    display: flex;
    justify-content: center;
}

div.stButton > button {
    width: 100%;
    max-width: 360px;
    min-height: 56px;
    border-radius: 15px;
    border: 2px solid #9f4ed6;
    background: linear-gradient(
        135deg,
        #a855f7,
        #d946ef
    );
    color: white;
    font-size: 17px;
    font-weight: 700;
    box-shadow: 0 8px 20px rgba(168, 85, 247, 0.20);
    transition: 0.25s;
}

div.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #9333ea,
        #ec4899
    );
    border-color: #ec4899;
    color: white;
    transform: translateY(-2px);
}

/* Botón Bokeh de ESCUCHAR */
.bk-btn {
    border-radius: 15px !important;
    border: 2px solid #9f4ed6 !important;
    background: linear-gradient(
        135deg,
        #a855f7,
        #d946ef
    ) !important;
    color: white !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 20px rgba(168, 85, 247, 0.20) !important;
}

.bk-btn:hover {
    background: linear-gradient(
        135deg,
        #9333ea,
        #ec4899
    ) !important;
    border-color: #ec4899 !important;
}

/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #eee5f4 0%,
            #f7f0ef 50%,
            #fae9e8 100%
        );
    border-right: 1px solid #d8b4e8;
    box-shadow: none;
}

section[data-testid="stSidebar"] > div {
    background: transparent;
}

.sidebar-title {
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    color: #211b2d;
}

.sidebar-text {
    color: #211b2d;
    line-height: 1.7;
    font-size: 14px;
    text-align: center;
}

/* ============================================================
   RESULTADOS
   ============================================================ */

.result-title {
    text-align: left;
    font-size: 20px;
    font-weight: 700;
    color: #211b2d;
    margin-bottom: 12px;
}

.stCheckbox {
    color: #211b2d;
    font-weight: 500;
}

audio {
    width: 100%;
}

div[data-testid="stAlert"] {
    border-radius: 13px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
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

col_img, col_info = st.columns([0.9, 1.6], gap="large")

with col_img:

    image = Image.open("traduccion.jpg")

    st.image(
        image,
        width=280
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


