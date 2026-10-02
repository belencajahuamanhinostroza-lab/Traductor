import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator


# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="TRADUCTOR.",
    page_icon="🎙️",
    layout="centered"
)


# ==================================================
# DISEÑO
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');


/* ==================================================
   FONDO GENERAL
   ================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 5% 10%,
            rgba(255, 220, 242, 0.80),
            transparent 28%
        ),
        radial-gradient(
            circle at 95% 20%,
            rgba(216, 203, 255, 0.80),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(220, 214, 255, 0.70),
            transparent 38%
        ),
        linear-gradient(
            135deg,
            #f9f4ff 0%,
            #f7f3ff 45%,
            #fff5fb 100%
        );

    min-height: 100vh;
    font-family: 'Inter', sans-serif;
}


/* ==================================================
   CONTENEDOR
   ================================================== */

.block-container {
    max-width: 850px !important;
    padding-top: 35px !important;
    padding-bottom: 60px !important;
}


/* ==================================================
   TITULOS
   ================================================== */

h1 {
    color: #30265c !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

h2 {
    color: #393064 !important;
    font-weight: 600 !important;
}

h3 {
    color: #463c70 !important;
    font-weight: 600 !important;
}

p {
    color: #77718c;
}


/* ==================================================
   TITULO PRINCIPAL
   ================================================== */

.stTitle {
    color: #30265c !important;
}


/* ==================================================
   IMAGEN
   MANTIENE TU imagen traduccion.jpg
   ================================================== */

[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin: 15px auto 25px auto;
}

[data-testid="stImage"] img {
    border-radius: 28px;
    box-shadow:
        0 18px 45px rgba(111, 91, 160, 0.15),
        0 0 0 1px rgba(255,255,255,0.7);
}


/* ==================================================
   TEXTO
   ================================================== */

.stMarkdown,
.stText,
.stCaption {
    color: #69627c;
}


/* ==================================================
   SELECTBOX
   TODO QUEDA INTEGRADO AL MISMO FONDO
   ================================================== */

div[data-baseweb="select"] {
    background: transparent !important;
}

div[data-baseweb="select"] > div {
    background:
        rgba(255,255,255,0.35) !important;

    border:
        1px solid rgba(255,255,255,0.75) !important;

    border-radius: 17px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.75),
        0 8px 20px rgba(112, 91, 151, 0.06) !important;

    backdrop-filter: blur(14px);

    color: #40375f !important;
}


/* Texto del select */

div[data-baseweb="select"] span {
    color: #40375f !important;
}


/* ==================================================
   CHECKBOX
   ================================================== */

[data-testid="stCheckbox"] {
    color: #5d5473 !important;
}

[data-testid="stCheckbox"] label {
    color: #5d5473 !important;
}


/* ==================================================
   BOTONES
   ================================================== */

.stButton > button {

    width: 100%;

    min-height: 52px;

    border-radius: 18px;

    border: 1px solid
        rgba(255,255,255,0.75);

    background:
        linear-gradient(
            135deg,
            #9b72ed,
            #bd8be9
        );

    color: white;

    font-family: 'Inter', sans-serif;

    font-size: 14px;

    font-weight: 600;

    letter-spacing: 0.1px;

    box-shadow:
        0 10px 25px
        rgba(137, 94, 204, 0.25);

    transition:
        all 0.2s ease;
}


.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #a27af0,
            #c18fe9
        );

    transform:
        translateY(-2px);

    box-shadow:
        0 14px 30px
        rgba(137, 94, 204, 0.30);

    color: white;
}


.stButton > button:active {

    transform:
        scale(0.98);

}


/* ==================================================
   BOTÓN BOKEH DE ESCUCHAR
   ================================================== */

.bk-btn {

    width: 100% !important;

    height: 55px !important;

    border-radius: 19px !important;

    border:
        1px solid
        rgba(255,255,255,0.75) !important;

    background:
        linear-gradient(
            135deg,
            #9a70eb,
            #bc88e8
        ) !important;

    color: white !important;

    font-family:
        'Inter',
        sans-serif !important;

    font-size: 14px !important;

    font-weight: 600 !important;

    box-shadow:
        0 10px 25px
        rgba(137, 94, 204, 0.25) !important;

}


/* ==================================================
   AUDIO
   ================================================== */

audio {

    width: 100%;

    border-radius: 18px;

    box-shadow:
        0 8px 20px
        rgba(90, 75, 120, 0.10);

}


/* ==================================================
   SIDEBAR
   ================================================== */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            160deg,
            #f8f1ff,
            #fff4fa
        );

    border-right:
        1px solid
        rgba(255,255,255,0.7);

}


section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color: #403467 !important;

}


section[data-testid="stSidebar"] p {

    color: #77718a !important;

}


/* ==================================================
   CAJAS DE INFORMACIÓN
   ================================================== */

.stAlert {

    border-radius: 18px !important;

    background:
        rgba(255,255,255,0.45) !important;

    border:
        1px solid
        rgba(255,255,255,0.7) !important;

}


/* ==================================================
   TEXTO RECONOCIDO
   ================================================== */

[data-testid="stText"] {

    background:
        rgba(255,255,255,0.35);

    border-radius: 18px;

}


/* ==================================================
   SEPARADORES
   ================================================== */

hr {

    border: none;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(145,120,190,0.18),
            transparent
        );

}


/* ==================================================
   MOBILE
   ================================================== */

@media (max-width: 700px) {

    .block-container {

        padding-left: 20px !important;
        padding-right: 20px !important;

    }

    h1 {

        font-size: 30px !important;

    }

}

</style>
""", unsafe_allow_html=True)


# ==================================================
# TU CÓDIGO ORIGINAL
# ==================================================

st.title("TRADUCTOR.")

st.subheader("Escucho lo que quieres traducir.")


# ==================================================
# IMAGEN ORIGINAL
# ==================================================

image = Image.open('traduccion.jpg')

st.image(image, width=300)


# ==================================================
# SIDEBAR ORIGINAL
# ==================================================

with st.sidebar:

    st.subheader("Traductor.")

    st.write(
        "Presiona el botón, cuando escuches la señal "
        "habla lo que quieres traducir, luego selecciona "
        "la configuración de lenguaje que necesites."
    )


# ==================================================
# TEXTO
# ==================================================

st.write(
    "Toca el Botón y habla lo que quires traducir"
)


# ==================================================
# BOTÓN DE VOZ
# ==================================================

stt_button = Button(
    label=" Escuchar  🎤",
    width=300,
    height=50
)


stt_button.js_on_event(
    "button_click",
    CustomJS(code="""

        var recognition =
            new webkitSpeechRecognition();

        recognition.continuous = false;

        recognition.interimResults = true;

        recognition.lang = 'es-ES';


        recognition.onresult = function (e) {

            var value = "";

            for (
                var i = e.resultIndex;
                i < e.results.length;
                ++i
            ) {

                if (e.results[i].isFinal) {

                    value +=
                        e.results[i][0].transcript;

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


        recognition.start();

    """)
)


result = streamlit_bokeh_events(

    stt_button,

    events="GET_TEXT",

    key="listen",

    refresh_on_update=False,

    override_height=75,

    debounce_time=0

)


# ==================================================
# RESULTADO
# ==================================================

if result:

    if "GET_TEXT" in result:

        st.write(
            result.get("GET_TEXT")
        )


    try:

        os.mkdir("temp")

    except:

        pass


    # ==================================================
    # TEXTO A AUDIO
    # ==================================================

    st.title("Texto a Audio")


    translator = Translator()


    text = str(
        result.get("GET_TEXT")
    )


    # ==================================================
    # IDIOMA DE ENTRADA
    # ==================================================

    in_lang = st.selectbox(

        "Selecciona el lenguaje de Entrada",

        (
            "Inglés",
            "Español",
            "Francés",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Alemán",
            "Danés"
        ),

    )


    if in_lang == "Inglés":

        input_language = "en"

    elif in_lang == "Español":

        input_language = "es"

    elif in_lang == "Francés":

        input_language = "fr"

    elif in_lang == "Coreano":

        input_language = "ko"

    elif in_lang == "Mandarín":

        input_language = "zh-cn"

    elif in_lang == "Japonés":

        input_language = "ja"

    elif in_lang == "Alemán":

        input_language = "de"

    elif in_lang == "Danés":

        input_language = "da"


    # ==================================================
    # IDIOMA DE SALIDA
    # ==================================================

    out_lang = st.selectbox(

        "Selecciona el lenguaje de salida",

        (
            "Inglés",
            "Español",
            "Francés",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Alemán",
            "Danés"
        ),

    )


    if out_lang == "Inglés":

        output_language = "en"

    elif out_lang == "Español":

        output_language = "es"

    elif out_lang == "Frances":

        output_language = "fr"

    elif out_lang == "Coreano":

        output_language = "ko"

    elif out_lang == "Mandarín":

        output_language = "zh-cn"

    elif out_lang == "Japonés":

        output_language = "ja"

    elif out_lang == "Alemán":

        out_language = "de"

    elif out_lang == "Danés":

        out_language = "da"


    # ==================================================
    # ACENTO
    # ==================================================

    english_accent = st.selectbox(

        "Selecciona el acento",

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
            "Francia",
        ),

    )


    if english_accent == "Defecto":

        tld = "com"

    elif english_accent == "Español":

        tld = "com.mx"

    elif english_accent == "Reino Unido":

        tld = "co.uk"

    elif english_accent == "Estados Unidos":

        tld = "com"

    elif english_accent == "Canada":

        tld = "ca"

    elif english_accent == "Australia":

        tld = "com.au"

    elif english_accent == "Irlanda":

        tld = "ie"

    elif english_accent == "Sudáfrica":

        tld = "co.za"

    elif english_accent == "Alemania":

        tld = "de"

    elif english_accent == "Francia":

        tld = "fr"

    elif english_accent == "Dinamarca":

        tld = "dk"


    # ==================================================
    # FUNCIÓN DE TEXTO A VOZ
    # ==================================================

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


        try:

            my_file_name = text[0:20]

        except:

            my_file_name = "audio"


        tts.save(
            f"temp/{my_file_name}.mp3"
        )


        return my_file_name, trans_text


    # ==================================================
    # MOSTRAR TEXTO
    # ==================================================

    display_output_text = st.checkbox(
        "Mostrar el texto"
    )


    # ==================================================
    # CONVERTIR
    # ==================================================

    if st.button("convertir"):

        result, output_text = text_to_speech(

            input_language,
            output_language,
            text,
            tld

        )


        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )


        audio_bytes = audio_file.read()


        st.markdown(
            "## Tú audio:"
        )


        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        if display_output_text:

            st.markdown(
                "## Texto de salida:"
            )

            st.write(
                f" {output_text}"
            )


    # ==================================================
    # ELIMINAR ARCHIVOS
    # ==================================================

    def remove_files(n):

        mp3_files = glob.glob(
            "temp/*mp3"
        )


        if len(mp3_files) != 0:

            now = time.time()

            n_days = n * 86400


            for f in mp3_files:

                if os.stat(f).st_mtime < now - n_days:

                    os.remove(f)

                    print(
                        "Deleted ",
                        f
                    )


    remove_files(7)


