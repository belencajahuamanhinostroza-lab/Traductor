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
}

.stApp {
    background: linear-gradient(
        135deg,
        #ffd6e7 0%,
        #fbcfe8 35%,
        #dbeafe 70%,
        #bae6fd 100%
    );
    color: #164e63;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ============================================================
   TÍTULO
   ============================================================ */

.main-title {
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-size: 46px;
    font-weight: 800;
    color: #164e63;
    margin-top: 10px;
    margin-bottom: 5px;
    text-shadow: 0 0 12px rgba(34,211,238,0.35);
}

.subtitle {
    text-align: center;
    font-size: 18px;
    font-weight: 500;
    color: #475569;
    margin-bottom: 30px;
}


/* ============================================================
   TARJETAS
   ============================================================ */

.card {
    background: rgba(255,255,255,0.55);
    border: 2px solid #67e8f9;
    border-radius: 24px;
    padding: 25px;
    margin-bottom: 22px;
    box-shadow:
        0 0 8px rgba(34,211,238,0.75),
        0 0 20px rgba(34,211,238,0.35);
    backdrop-filter: blur(12px);
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #164e63;
    margin-bottom: 15px;
}


/* ============================================================
   TEXTO
   ============================================================ */

.text-box {
    background: rgba(255,255,255,0.78);
    border: 2px solid #67e8f9;
    border-radius: 17px;
    padding: 20px;
    font-size: 18px;
    font-weight: 500;
    color: #334155;
    min-height: 70px;
    box-shadow:
        0 0 7px rgba(34,211,238,0.55);
}


/* ============================================================
   BOTONES
   ============================================================ */

div.stButton > button {
    width: 100%;
    min-height: 55px;
    border-radius: 18px;
    border: 2px solid #38bdf8;
    background: linear-gradient(
        135deg,
        #60a5fa,
        #38bdf8
    );
    color: white;
    font-size: 18px;
    font-weight: 700;
    box-shadow:
        0 0 8px rgba(56,189,248,0.75),
        0 5px 18px rgba(37,99,235,0.30);
    transition: 0.25s;
}

div.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #3b82f6,
        #0ea5e9
    );
    border-color: #22d3ee;
    box-shadow:
        0 0 12px #22d3ee,
        0 0 25px rgba(34,211,238,0.55);
    transform: translateY(-2px);
}


/* ============================================================
   SELECTORES
   ============================================================ */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.80);
    border: 2px solid #67e8f9;
    border-radius: 14px;
    color: #164e63;
    box-shadow:
        0 0 6px rgba(34,211,238,0.45);
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #fbcfe8 0%,
        #dbeafe 100%
    );
    border-right: 2px solid #67e8f9;
    box-shadow:
        0 0 15px rgba(34,211,238,0.35);
}

.sidebar-title {
    font-size: 26px;
    font-weight: 800;
    color: #164e63;
}

.sidebar-text {
    color: #334155;
    line-height: 1.7;
    font-size: 15px;
}


/* ============================================================
   RESULTADO
   ============================================================ */

.result-title {
    font-size: 24px;
    font-weight: 700;
    color: #0891b2;
    margin-bottom: 12px;
}


/* ============================================================
   CHECKBOX
   ============================================================ */

.stCheckbox {
    color: #164e63;
    font-weight: 500;
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
```

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

col_img, col_info = st.columns([1, 1.5])

with col_img:

```
image = Image.open("traduccion.jpg")

st.image(
    image,
    width=300
)
```

with col_info:

```
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
```

# ============================================================

# RECONOCIMIENTO DE VOZ

# ============================================================

st.markdown(
""" <div class="card">

```
<div class="card-title">
🎤 Reconocimiento de voz
</div>
""",
unsafe_allow_html=True
```

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

```
    var recognition =
        new webkitSpeechRecognition();

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
```

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

```
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
```

# ============================================================

# LIMPIAR AUDIOS ANTIGUOS

# ============================================================

def remove_files(days):

```
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
```

remove_files(7)



