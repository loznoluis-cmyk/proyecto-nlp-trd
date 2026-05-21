
import sys
import os

# ==========================================
# CONFIGURAR RUTA DEL PROYECTO
# ==========================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# ==========================================
# IMPORTACIONES
# ==========================================

import streamlit as st
import pickle
import pandas as pd

from datetime import datetime

from src.preprocess import (
    limpiar_texto,
    procesar_texto
)

from src.dashboard import (
    mostrar_dashboard
)

from src.lector_documentos import (
    leer_pdf,
    leer_docx
)

from src.explicabilidad import (
    obtener_palabras_clave
)

from src.visualizacion_nlp import (
    mostrar_wordcloud
)

# ==========================================
# CONFIG STREAMLIT
# ==========================================

st.set_page_config(

    page_title="Sistema NLP TRD",

    page_icon="📄",

    layout="wide"

)

# ==========================================
# ESTILOS PERSONALIZADOS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F3F4F6;
    }

    h1, h2, h3 {
        color: #111827;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {

        background-color: #E5E7EB;

        border-right: 1px solid #D1D5DB;
    }

    .stButton > button {

        background: linear-gradient(
            90deg,
            #2563EB,
            #1D4ED8
        );

        color: white;

        border-radius: 10px;

        border: none;

        padding: 0.7rem 1.3rem;

        font-weight: bold;

        font-size: 15px;
    }

    .stButton > button:hover {

        background: linear-gradient(
            90deg,
            #1D4ED8,
            #1E3A8A
        );

        color: white;
    }

    .bloque {

        background-color: white;

        padding: 1.5rem;

        border-radius: 18px;

        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);

        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# HEADER CORPORATIVO
# ==========================================

col1, col2 = st.columns([1, 5])

with col1:

    ruta_logo = "assets/banner.png"

    if os.path.exists(ruta_logo):

        st.image(
            ruta_logo,
            width=180
        )

with col2:

    st.markdown(
        """
        # 📄 Sistema Inteligente de Clasificación Documental
        
        ### Proyecto NLP aplicado a Tablas de Retención Documental (TRD)
        """
    )

st.markdown("---")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title(
    "⚙️ Navegación"
)

st.sidebar.markdown("---")

opcion = st.sidebar.radio(

    "Seleccione una opción",

    [
        "Clasificador",
        "Dashboard"
    ]

)

st.sidebar.markdown("---")

st.sidebar.success(
    "Sistema NLP TRD v1.0"
)

# ==========================================
# DASHBOARD
# ==========================================

if opcion == "Dashboard":

    mostrar_dashboard()

# ==========================================
# CLASIFICADOR
# ==========================================

else:

    # ==========================================
    # CARGAR MODELOS
    # ==========================================

    with open(
        "models/modelo_nlp.pkl",
        "rb"
    ) as archivo_modelo:

        modelo = pickle.load(
            archivo_modelo
        )

    with open(
        "models/vectorizador.pkl",
        "rb"
    ) as archivo_vectorizador:

        vectorizador = pickle.load(
            archivo_vectorizador
        )

    with open(
        "models/encoder.pkl",
        "rb"
    ) as archivo_encoder:

        encoder = pickle.load(
            archivo_encoder
        )

    # ==========================================
    # TECNOLOGÍAS IMPLEMENTADAS
    # ==========================================

    st.markdown(
        """
        <div class="bloque">
            <h2>🚀 Tecnologías implementadas</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("✅ NLP (Procesamiento de Lenguaje Natural)")
    st.write("✅ TF-IDF")
    st.write("✅ Machine Learning")
    st.write("✅ Clasificación automática documental")
    st.write("✅ Lectura automática de PDFs y Word")
    st.write("✅ Dashboard analítico")
    st.write("✅ IA explicable")
    st.write("✅ WordCloud NLP")

    st.markdown("---")

    # ==========================================
    # SUBIR DOCUMENTO
    # ==========================================

    archivo = st.file_uploader(

        "📂 Suba un archivo PDF o Word",

        type=[
            "pdf",
            "docx"
        ]

    )

    texto_archivo = ""

    # ==========================================
    # LEER DOCUMENTOS
    # ==========================================

    if archivo is not None:

        extension = (
            archivo.name
            .split(".")[-1]
            .lower()
        )

        if extension == "pdf":

            texto_archivo = leer_pdf(
                archivo
            )

        elif extension == "docx":

            texto_archivo = leer_docx(
                archivo
            )

        st.success(
            "✅ Documento leído correctamente"
        )

    # ==========================================
    # TEXTO MANUAL
    # ==========================================

    texto_usuario = st.text_area(

        "✍️ O escriba el texto manualmente:",

        value=texto_archivo,

        height=220,

        placeholder="Ejemplo: solicitud de matrícula académica"

    )

    # ==========================================
    # BOTÓN CLASIFICAR
    # ==========================================

    if st.button(
        "🚀 Clasificar documento"
    ):

        # ==========================================
        # VALIDAR TEXTO
        # ==========================================

        if texto_usuario.strip() == "":

            st.warning(
                "⚠️ Por favor ingrese un texto"
            )

        else:

            # ==========================================
            # LIMPIEZA
            # ==========================================

            texto_limpio = limpiar_texto(
                texto_usuario
            )

            # ==========================================
            # NLP
            # ==========================================

            texto_procesado = procesar_texto(
                texto_limpio
            )

            # ==========================================
            # TF-IDF
            # ==========================================

            vector = vectorizador.transform(
                [texto_procesado]
            )

            # ==========================================
            # PREDICCIÓN
            # ==========================================

            prediccion = modelo.predict(
                vector
            )

            categoria = encoder.inverse_transform(
                prediccion
            )

            # ==========================================
            # PROBABILIDADES
            # ==========================================

            probabilidades = modelo.predict_proba(
                vector
            )

            confianza = max(
                probabilidades[0]
            ) * 100

            # ==========================================
            # RESULTADOS
            # ==========================================

            st.success(
                f"📁 Categoría predicha: {categoria[0]}"
            )

            st.info(
                f"🎯 Confianza del modelo: {confianza:.2f}%"
            )

            # ==========================================
            # ALERTA
            # ==========================================

            if confianza < 60:

                st.warning(
                    "⚠️ Baja confianza en la clasificación"
                )

            # ==========================================
            # TABLA PROBABILIDADES
            # ==========================================

            st.subheader(
                "📊 Probabilidades por categoría"
            )

            clases = encoder.classes_

            df_probabilidades = pd.DataFrame({

                "Categoría": clases,

                "Probabilidad": probabilidades[0]

            })

            df_probabilidades["Probabilidad"] = (
                df_probabilidades["Probabilidad"] * 100
            )

            df_probabilidades = (
                df_probabilidades.sort_values(
                    by="Probabilidad",
                    ascending=False
                )
            )

            st.dataframe(
                df_probabilidades,
                use_container_width=True
            )

            # ==========================================
            # IA EXPLICABLE
            # ==========================================

            st.subheader(
                "🧠 Explicación de la IA"
            )

            palabras_clave = obtener_palabras_clave(
                vectorizador,
                vector
            )

            st.write(
                "El modelo detectó las siguientes palabras importantes:"
            )

            for palabra in palabras_clave:

                st.write(
                    f"• {palabra}"
                )

            # ==========================================
            # WORDCLOUD
            # ==========================================

            st.subheader(
                "☁️ Nube de palabras NLP"
            )

            mostrar_wordcloud(
                texto_procesado
            )

            # ==========================================
            # HISTORIAL
            # ==========================================

            historial = pd.DataFrame([{

                "fecha": datetime.now(),

                "texto": texto_usuario,

                "categoria": categoria[0],

                "confianza": round(
                    confianza,
                    2
                )

            }])

            ruta_historial = (
                "reports/historial.csv"
            )

            if os.path.exists(
                ruta_historial
            ):

                historial.to_csv(

                    ruta_historial,

                    mode="a",

                    header=False,

                    index=False

                )

            else:

                historial.to_csv(

                    ruta_historial,

                    index=False

                )

            st.success(
                "✅ Historial guardado correctamente"
            )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Proyecto desarrollado en Python + NLP + Machine Learning + Streamlit"
)