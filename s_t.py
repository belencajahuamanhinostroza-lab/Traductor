```python
import os
import glob
import time
import streamlit as st

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

from PIL import Image
from gtts import gTTS
from googletrans import Translator


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Traductor por Voz",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ESTILOS DE LA INTERFAZ
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #172554 50%,
        #1e3a8a 100%
    );
    color: white;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* TÍTULO */

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin-top: 10px;
    margin-bottom: 5px;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    color: #bfdbfe;
    font-size: 19px;
    margin-bottom: 30px;
}


/* TARJETAS */

.card {
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 22px;
    padding: 25px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

.card-title {
    font-size: 23px;
    font-weight: 700;
    color: white;
    margin-bottom: 15px;
}


/* CAJA DE TEXTO */

.text-box {
    background: rgba(15,23,42,0.75);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.10);
    font-size: 20px;
    color: #e0f2fe;
    min-height: 80px;
}


/* BOTONES */

div.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(
        90deg,
        #2563eb,
        #06b6d4
    );
    color: white;
    font-size: 19px;
    font-weight: 700;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 25px rgba(6,182,212,0.35);
}


/* SELECTORES */

div[data-baseweb="select"] > div {
    background-color: rgba(15,23,42,0.85);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.15);
    color: white;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a,
        #172554
    );
    border-right: 1px solid rgba(255,255,255,0.10);
}

.sidebar-title {
    font-size: 26px;
    font-weight: 800;
    color: #60a5fa;
}

.sidebar-text {
    color: #cbd5e1;
    line-height: 1.6;
    font-size: 16px;
}


/* RESULTADO */

.result-title {
    font-size: 25px;
    font-weight: 700;
    color: #67e8f9;
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

        2. Espera la señal y habla claramente.

        <br><br>

        3. Selecciona el idioma de entrada.

        <br><br>

        4. Selecciona el idioma de salida.

        <br><br>

        5. Presiona <b>Convertir y traducir</b>.

        <br><br>

        6. Escucha el resultado traducido.

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
# IMAGEN ORIGINAL
# ============================================================

col_img, col_info = st.columns([1, 1.4])


with col_img:

    # IMPORTANTE:
    # Esta es tu imagen original.
    # No se modifica.

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
                "Error de reconocimiento:",
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
# PROCESAMIENTO DEL TEXTO
# ============================================================

if result and "GET_TEXT" in result:

    text = str(result.get("GET_TEXT"))


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
    # CARPETA PARA AUDIOS
    # ========================================================

    try:

        os.mkdir("temp")

    except FileExistsError:

        pass


    # ========================================================
    # TRADUCTOR
    # ========================================================

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


    # ========================================================
    # CONFIGURACIÓN DE TRADUCCIÓN
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


    col1, col2 = st.columns(2)


    # ========================================================
    # IDIOMA DE ENTRADA
    # ========================================================

    with col1:

        in_lang = st.selectbox(
            "🗣️ Idioma de entrada",
            (
                "Inglés",
                "Español",
                "Francés",
                "Coreano",
                "Mandarín",
                "Japonés",
                "Alemán",
                "Danés"
            )
        )


    input_language = language_codes[in_lang]


    # ========================================================
    # IDIOMA DE SALIDA
    # ========================================================

    with col2:

        out_lang = st.selectbox(
            "🌎 Idioma de salida",
            (
                "Inglés",
                "Español",
                "Francés",
                "Coreano",
                "Mandarín",
                "Japonés",
                "Alemán",
                "Danés"
            )
        )


    output_language = language_codes[out_lang]


    # ========================================================
    # ACENTO
    # ========================================================

    english_accent = st.selectbox(
        "🔊 Selecciona el acento",
        (
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
        )
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


    tld = accent_codes[english_accent]


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


        trans_text = translation.text


        tts = gTTS(
            trans_text,
            lang=output_language,
            tld=tld,
            slow=False
        )


        # Crear nombre seguro para el archivo

        my_file_name = text[:20]

        my_file_name = "".join(
            c for c in my_file_name
            if c.isalnum()
            or c in (" ", "_", "-")
        )


        if not my_file_name:

            my_file_name = "audio"


        # Reemplazar espacios

        my_file_name = my_file_name.replace(
            " ",
            "_"
        )


        file_path = (
            f"temp/{my_file_name}.mp3"
        )


        tts.save(file_path)


        return my_file_name, trans_text


    # ========================================================
    # MOSTRAR TEXTO
    # ========================================================

    display_output_text = st.checkbox(
        "📝 Mostrar el texto traducido"
    )


    # ========================================================
    # BOTÓN CONVERTIR
    # ========================================================

    if st.button(
        "🌎  CONVERTIR Y TRADUCIR",
        type="primary"
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
                format="audio/mp3",
                start_time=0
            )


            # =================================================
            # TEXTO TRADUCIDO
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
# ELIMINAR ARCHIVOS ANTIGUOS
# ============================================================

def remove_files(days):

    mp3_files = glob.glob(
        "temp/*.mp3"
    )


    if len(mp3_files) == 0:

        return


    now = time.time()

    seconds = days * 86400


    for file in mp3_files:

        try:

            if os.stat(file).st_mtime < now - seconds:

                os.remove(file)

        except:

            pass


remove_files(7)
```
