import os
import time
import glob
import html
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
    page_title="TRADUCTOR.",
    page_icon="🎙️",
    layout="centered"
)


# =========================================================
# ESTADOS
# =========================================================

if "texto" not in st.session_state:
    st.session_state.texto = ""

if "traduccion" not in st.session_state:
    st.session_state.traduccion = ""

if "audio" not in st.session_state:
    st.session_state.audio = None

if "historial" not in st.session_state:
    st.session_state.historial = []

if "idioma_entrada" not in st.session_state:
    st.session_state.idioma_entrada = "Español"

if "idioma_salida" not in st.session_state:
    st.session_state.idioma_salida = "Inglés"


# =========================================================
# COLORES Y DISEÑO
# =========================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
);


/* =====================================================
   FONDO
   ===================================================== */

.stApp {

    background:

        radial-gradient(
            circle at 5% 8%,
            rgba(255, 220, 242, .80),
            transparent 28%
        ),

        radial-gradient(
            circle at 95% 15%,
            rgba(214, 202, 255, .85),
            transparent 30%
        ),

        radial-gradient(
            circle at 50% 100%,
            rgba(217, 218, 255, .70),
            transparent 38%
        ),

        linear-gradient(
            135deg,
            #faf5ff 0%,
            #f7f3ff 45%,
            #fff4fb 100%
        );

    min-height: 100vh;

    font-family:
        'Inter',
        sans-serif;
}


/* =====================================================
   CONTENEDOR
   ===================================================== */

.block-container {

    max-width: 780px !important;

    padding-top: 35px !important;

    padding-bottom: 70px !important;
}


/* =====================================================
   TEXTO
   ===================================================== */

h1 {

    color: #30275d !important;

    font-weight: 700 !important;

    letter-spacing: -1px;
}


h2 {

    color: #393064 !important;

    font-weight: 650 !important;
}


h3 {

    color: #463c70 !important;

    font-weight: 600 !important;
}


p {

    color: #77718c;
}


/* =====================================================
   HEADER
   ===================================================== */

.app-header {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-bottom: 20px;
}


.logo-area {

    display: flex;

    align-items: center;

    gap: 12px;
}


.logo {

    width: 46px;

    height: 46px;

    border-radius: 16px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #9870ec,
            #c28de9
        );

    color: white;

    font-size: 22px;

    box-shadow:
        0 10px 25px
        rgba(137, 94, 204, .25);
}


.brand {

    font-size: 18px;

    font-weight: 700;

    color: #32295d;
}


.brand-sub {

    font-size: 11px;

    color: #9690a8;

    margin-top: 2px;
}


.profile {

    width: 40px;

    height: 40px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(255,255,255,.55);

    border:
        1px solid
        rgba(255,255,255,.8);

    color: #8463c9;

    box-shadow:
        0 8px 20px
        rgba(100,80,130,.08);
}


/* =====================================================
   HERO
   ===================================================== */

.hero {

    padding: 25px;

    border-radius: 30px;

    background:
        rgba(255,255,255,.42);

    border:
        1px solid
        rgba(255,255,255,.78);

    box-shadow:
        0 20px 50px
        rgba(103,82,145,.10),

        inset 0 1px 0
        rgba(255,255,255,.8);

    backdrop-filter:
        blur(20px);

    text-align: center;

    margin-bottom: 22px;
}


.hero-small {

    font-size: 10px;

    letter-spacing: 2px;

    color: #8975b6;

    font-weight: 600;
}


.hero-title {

    font-size: 26px;

    color: #332b60;

    font-weight: 700;

    margin-top: 7px;
}


.hero-description {

    color: #928ca4;

    font-size: 13px;

    margin-top: 4px;
}


/* =====================================================
   ORBE
   ===================================================== */

.orb-area {

    height: 220px;

    display: flex;

    align-items: center;

    justify-content: center;
}


.orb {

    width: 145px;

    height: 145px;

    border-radius: 50%;

    background:

        radial-gradient(
            circle at 25% 25%,
            #ffffff,
            transparent 18%
        ),

        radial-gradient(
            circle at 70% 30%,
            #d7baff,
            transparent 42%
        ),

        radial-gradient(
            circle at 30% 70%,
            #9c81e7,
            transparent 52%
        ),

        linear-gradient(
            135deg,
            #bda5ff,
            #e5b6ef,
            #91a7f1
        );

    box-shadow:

        inset -18px -18px 35px
        rgba(72,52,130,.15),

        inset 15px 12px 25px
        rgba(255,255,255,.65),

        0 25px 40px
        rgba(125,88,190,.22);

    animation:
        floating 4s ease-in-out infinite;
}


@keyframes floating {

    0%,100% {

        transform:
            translateY(0px)
            rotate(0deg);

    }

    50% {

        transform:
            translateY(-8px)
            rotate(3deg);

    }
}


/* =====================================================
   BOTÓN MICRO
   ===================================================== */

.mic-decoration {

    width: 62px;

    height: 62px;

    margin:
        -5px auto 0;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #9970eb,
            #bf8be9
        );

    color: white;

    font-size: 25px;

    box-shadow:

        0 10px 25px
        rgba(137,94,204,.28),

        0 0 0 8px
        rgba(177,143,235,.12);
}


/* =====================================================
   SECCIONES
   ===================================================== */

.section-title {

    color: #40366b;

    font-size: 15px;

    font-weight: 650;

    margin:
        20px 2px 9px;
}


/* =====================================================
   TARJETAS
   ===================================================== */

.glass-card {

    padding: 18px;

    border-radius: 22px;

    background:
        rgba(255,255,255,.42);

    border:
        1px solid
        rgba(255,255,255,.78);

    box-shadow:

        0 12px 30px
        rgba(100,80,130,.07),

        inset 0 1px 0
        rgba(255,255,255,.7);

    backdrop-filter:
        blur(15px);

    margin-bottom: 12px;
}


.card-label {

    color: #958da8;

    font-size: 9px;

    letter-spacing: 1.3px;

    text-transform: uppercase;

    margin-bottom: 7px;
}


.card-text {

    color: #38314d;

    font-size: 16px;

    line-height: 1.5;
}


/* =====================================================
   SELECTBOX
   ===================================================== */

div[data-baseweb="select"] {

    background:
        transparent !important;
}


div[data-baseweb="select"] > div {

    background:
        rgba(255,255,255,.30) !important;

    border:
        1px solid
        rgba(255,255,255,.75) !important;

    border-radius:
        17px !important;

    box-shadow:

        inset 0 1px 0
        rgba(255,255,255,.75),

        0 7px 20px
        rgba(110,88,150,.05) !important;

    color:
        #40375f !important;
}


div[data-baseweb="select"] span {

    color:
        #40375f !important;
}


/* =====================================================
   BOTONES
   ===================================================== */

.stButton > button {

    width: 100%;

    min-height: 50px;

    border-radius: 18px;

    border:
        1px solid
        rgba(255,255,255,.75);

    background:
        linear-gradient(
            135deg,
            #9970eb,
            #bd89e9
        );

    color: white;

    font-size: 14px;

    font-weight: 600;

    box-shadow:
        0 10px 24px
        rgba(137,94,204,.24);

    transition:
        .2s ease;
}


.stButton > button:hover {

    transform:
        translateY(-2px);

    color: white;

    box-shadow:
        0 14px 30px
        rgba(137,94,204,.30);
}


.stButton > button:active {

    transform:
        scale(.98);
}


/* =====================================================
   BOKEH
   ===================================================== */

.bk-btn {

    width: 100% !important;

    height: 55px !important;

    border-radius: 19px !important;

    border:
        1px solid
        rgba(255,255,255,.75) !important;

    background:
        linear-gradient(
            135deg,
            #9970eb,
            #bd89e9
        ) !important;

    color:
        white !important;

    font-family:
        'Inter',
        sans-serif !important;

    font-size:
        14px !important;

    font-weight:
        600 !important;

    box-shadow:
        0 10px 24px
        rgba(137,94,204,.24) !important;
}


/* =====================================================
   BOTÓN SECUNDARIO
   ===================================================== */

.secondary-button button {

    background:
        rgba(255,255,255,.40) !important;

    color:
        #6c5b9a !important;

    box-shadow:
        none !important;
}


/* =====================================================
   AUDIO
   ===================================================== */

audio {

    width: 100%;

    border-radius: 16px;

    margin-top: 5px;
}


/* =====================================================
   HISTORIAL
   ===================================================== */

.history-item {

    padding: 13px 15px;

    border-radius: 17px;

    background:
        rgba(255,255,255,.32);

    border:
        1px solid
        rgba(255,255,255,.60);

    margin-bottom: 8px;
}


.history-languages {

    font-size: 9px;

    color: #8d7db2;

    letter-spacing: .8px;

    text-transform: uppercase;
}


.history-text {

    color: #514866;

    font-size: 12px;

    margin-top: 4px;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            160deg,
            #f8f1ff,
            #fff3fa
        );
}


section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color:
        #403467 !important;
}


section[data-testid="stSidebar"] p {

    color:
        #77718a !important;
}


/* =====================================================
   CHECKBOX
   ===================================================== */

[data-testid="stCheckbox"] label {

    color:
        #625975 !important;
}


/* =====================================================
   ALERTAS
   ===================================================== */

.stAlert {

    border-radius:
        17px !important;

    background:
        rgba(255,255,255,.42) !important;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {

    .block-container {

        padding-left:
            18px !important;

        padding-right:
            18px !important;
    }


    .hero {

        padding:
            22px 17px;
    }


    .hero-title {

        font-size:
            23px;
    }


    .orb-area {

        height:
            195px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER DE LA APP
# =========================================================

st.markdown("""
<div class="app-header">

    <div class="logo-area">

        <div class="logo">
            ✦
        </div>

        <div>

            <div class="brand">
                TRADUCTOR.
            </div>

            <div class="brand-sub">
                Traducción inteligente por voz
            </div>

        </div>

    </div>

    <div class="profile">
        ◉
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-small">
        TRADUCCIÓN POR VOZ
    </div>

    <div class="hero-title">
        Escucho lo que quieres traducir
    </div>

    <div class="hero-description">
        Habla naturalmente y convierte tu voz en texto
    </div>

    <div class="orb-area">
        <div class="orb"></div>
    </div>

    <div class="mic-decoration">
        🎙️
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# IMAGEN ORIGINAL
# =========================================================

try:

    image = Image.open("traduccion.jpg")

    st.image(
        image,
        width=300
    )

except:

    pass


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.subheader("🎙️ Traductor")

    st.write(
        "Presiona el botón y habla cuando escuches "
        "la señal. Luego selecciona el idioma "
        "que deseas traducir."
    )

    st.markdown("---")

    st.write("✨ Consejos")

    st.write(
        "• Habla con claridad."
    )

    st.write(
        "• Evita hablar demasiado rápido."
    )

    st.write(
        "• Puedes cambiar los idiomas."
    )


# =========================================================
# ESCUCHAR
# =========================================================

st.markdown(
    '<div class="section-title">Escuchar</div>',
    unsafe_allow_html=True
)


stt_button = Button(
    label="🎙️  Escuchar y convertir a texto",
    width=500,
    height=55
)


# =========================================================
# RECONOCIMIENTO DE VOZ
# ESTA ES LA FUNCIÓN PRINCIPAL
# =========================================================

stt_button.js_on_event(
    "button_click",

    CustomJS(code="""

        var recognition =
            new webkitSpeechRecognition();

        recognition.continuous =
            false;

        recognition.interimResults =
            true;

        recognition.lang =
            'es-ES';


        recognition.onresult =
            function(e) {

                var value = "";

                for (
                    var i = e.resultIndex;
                    i < e.results.length;
                    ++i
                ) {

                    if (
                        e.results[i].isFinal
                    ) {

                        value +=
                            e.results[i][0]
                            .transcript;

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


        recognition.onend =
            function() {

                console.log(
                    "Reconocimiento terminado"
                );

            };


        recognition.onerror =
            function(event) {

                console.log(
                    "Error:",
                    event.error
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


# =========================================================
# GUARDAR VOZ COMO TEXTO
# =========================================================

if result:

    if "GET_TEXT" in result:

        st.session_state.texto = (
            result.get("GET_TEXT")
        )


# =========================================================
# TEXTO DETECTADO
# =========================================================

if st.session_state.texto:

    st.markdown(
        '<div class="section-title">'
        'Lo que dijiste'
        '</div>',
        unsafe_allow_html=True
    )


    texto_seguro = html.escape(
        st.session_state.texto
    )


    st.markdown(
        f"""
        <div class="glass-card">

            <div class="card-label">
                🎙️ TEXTO DETECTADO
            </div>

            <div class="card-text">
                {texto_seguro}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # ACCIONES
    # =====================================================

    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🗑️ Limpiar texto"
        ):

            st.session_state.texto = ""

            st.session_state.traduccion = ""

            st.session_state.audio = None

            st.rerun()


    with col2:

        st.markdown(
            '<div class="secondary-button">',
            unsafe_allow_html=True
        )

        st.button(
            "🔄 Nueva grabación"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# TRADUCCIÓN
# =========================================================

if st.session_state.texto:

    st.markdown(
        '<div class="section-title">'
        'Configura tu traducción'
        '</div>',
        unsafe_allow_html=True
    )


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


    # =====================================================
    # IDIOMAS
    # =====================================================

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            """
            <div class="card-label">
                IDIOMA DE ENTRADA
            </div>
            """,
            unsafe_allow_html=True
        )


        input_name = st.selectbox(

            "Entrada",

            list(languages.keys()),

            index=list(
                languages.keys()
            ).index(
                st.session_state.idioma_entrada
            ),

            label_visibility="collapsed"

        )


    with col2:

        st.markdown(
            """
            <div class="card-label">
                IDIOMA DE SALIDA
            </div>
            """,
            unsafe_allow_html=True
        )


        output_name = st.selectbox(

            "Salida",

            list(languages.keys()),

            index=list(
                languages.keys()
            ).index(
                st.session_state.idioma_salida
            ),

            label_visibility="collapsed"

        )


    st.session_state.idioma_entrada = input_name

    st.session_state.idioma_salida = output_name


    input_language = languages[input_name]

    output_language = languages[output_name]


    # =====================================================
    # INTERCAMBIAR
    # =====================================================

    if st.button(
        "⇄  Intercambiar idiomas"
    ):

        temp = (
            st.session_state.idioma_entrada
        )

        st.session_state.idioma_entrada = (
            st.session_state.idioma_salida
        )

        st.session_state.idioma_salida = temp

        st.rerun()


    # =====================================================
    # ACENTO
    # =====================================================

    st.markdown(
        """
        <div class="card-label"
             style="margin-top:18px;">
            ACENTO DE VOZ
        </div>
        """,
        unsafe_allow_html=True
    )


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


    tld = accents[
        english_accent
    ]


    # =====================================================
    # CONVERTIR
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)


    if st.button(
        "✦  Traducir y generar audio"
    ):

        try:

            translator = Translator()


            text = (
                st.session_state.texto
            )


            translation = translator.translate(

                text,

                src=input_language,

                dest=output_language

            )


            trans_text = (
                translation.text
            )


            os.makedirs(
                "temp",
                exist_ok=True
            )


            # ---------------------------------------------
            # NOMBRE SEGURO
            # ---------------------------------------------

            safe_name = ""

            for char in text[:20]:

                if (
                    char.isalnum()
                    or char in (" ", "_", "-")
                ):

                    safe_name += char


            safe_name = (
                safe_name.strip()
            )


            if not safe_name:

                safe_name = "audio"


            # ---------------------------------------------
            # GENERAR AUDIO
            # ---------------------------------------------

            tts = gTTS(

                trans_text,

                lang=output_language,

                tld=tld,

                slow=False

            )


            file_path = (
                f"temp/{safe_name}.mp3"
            )


            tts.save(
                file_path
            )


            # ---------------------------------------------
            # GUARDAR RESULTADOS
            # ---------------------------------------------

            st.session_state.traduccion = (
                trans_text
            )

            st.session_state.audio = (
                file_path
            )


            # ---------------------------------------------
            # HISTORIAL
            # ---------------------------------------------

            nuevo = {

                "entrada":
                    input_name,

                "salida":
                    output_name,

                "original":
                    text,

                "traduccion":
                    trans_text

            }


            st.session_state.historial.insert(
                0,
                nuevo
            )


            # Máximo 10 traducciones

            st.session_state.historial = (
                st.session_state.historial[:10]
            )


            st.success(
                "✨ Traducción realizada"
            )


        except Exception as e:

            st.error(
                f"No se pudo realizar la traducción: {e}"
            )


# =========================================================
# RESULTADO
# =========================================================

if st.session_state.traduccion:

    st.markdown(
        '<div class="section-title">'
        'Resultado'
        '</div>',
        unsafe_allow_html=True
    )


    traduccion_segura = html.escape(
        st.session_state.traduccion
    )


    st.markdown(
        f"""
        <div class="glass-card">

            <div class="card-label">
                ✦ TRADUCCIÓN
            </div>

            <div class="card-text">
                {traduccion_segura}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # MOSTRAR TEXTO
    # =====================================================

    display_output_text = st.checkbox(
        "Mostrar texto de salida"
    )


    if display_output_text:

        st.write(
            st.session_state.traduccion
        )


# =========================================================
# AUDIO
# =========================================================

if (
    st.session_state.audio
    and os.path.exists(
        st.session_state.audio
    )
):

    st.markdown(
        '<div class="section-title">'
        'Escucha la traducción'
        '</div>',
        unsafe_allow_html=True
    )


    with open(
        st.session_state.audio,
        "rb"
    ) as audio_file:

        audio_bytes = (
            audio_file.read()
        )


    st.audio(
        audio_bytes,
        format="audio/mp3"
    )


# =========================================================
# HISTORIAL
# =========================================================

if st.session_state.historial:

    st.markdown(
        '<div class="section-title">'
        '🕘 Historial reciente'
        '</div>',
        unsafe_allow_html=True
    )


    for item in (
        st.session_state.historial[:5]
    ):

        original = html.escape(
            item["original"]
        )

        translated = html.escape(
            item["traduccion"]
        )


        st.markdown(
            f"""
            <div class="history-item">

                <div class="history-languages">
                    {item["entrada"]}
                    →
                    {item["salida"]}
                </div>

                <div class="history-text">
                    {original}
                    →
                    {translated}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# LIMPIAR ARCHIVOS ANTIGUOS
# =========================================================

def remove_files(n):

    mp3_files = glob.glob(
        "temp/*mp3"
    )


    if len(mp3_files) != 0:

        now = time.time()

        n_days = n * 86400


        for f in mp3_files:

            try:

                if (
                    os.stat(f).st_mtime
                    <
                    now - n_days
                ):

                    os.remove(f)

            except:

                pass


remove_files(7)

