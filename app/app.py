import sys
import os
import base64
import zipfile
import shutil
import pickle
import pandas as pd
import tempfile
import streamlit as st

from datetime import datetime

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
# IMPORTACIONES PERSONALIZADAS
# ==========================================

from src.preprocess import (
    limpiar_texto,
    procesar_texto,
    detectar_tipo_documental,
    detectar_dependencia,
    extraer_consecutivo,
    detectar_estructura_documental
)

from src.dashboard import (
    mostrar_dashboard
)

from src.lector_documentos import (
    leer_pdf,
    leer_docx,
    leer_imagen
)

from src.explicabilidad import (
    obtener_palabras_clave
)

from src.visualizacion_nlp import (
    mostrar_wordcloud
)

from src.clasificador_trd import (
    cargar_trd,
    mover_documento
)

from src.buscador_semantico import (
    buscar_documentos_semanticos
)

from src.visor_documental import (
    enriquecer_resultados
)

from src.buscador_carpetas import (
    buscar_en_carpetas
)

from src.motor_hibrido import (
    clasificacion_hibrida
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
# ESTILOS
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

    .bloque {
        background-color: white;
        padding: 1.5rem;
        border-radius: 18px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }

    iframe {
        border-radius: 10px;
        border: 1px solid #D1D5DB;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# HEADER
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

st.sidebar.title("⚙️ Navegación")

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
    "Sistema NLP TRD v16.0"
)

# ==========================================
# TABLA TRD
# ==========================================

with st.sidebar.expander("📂 Tabla TRD"):

    try:

        df_trd = cargar_trd()

        st.success(
            "TRD cargada correctamente"
        )

        st.dataframe(
            df_trd.head(20),
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Error cargando TRD: {e}"
        )

# ==========================================
# BÚSQUEDA SEMÁNTICA
# ==========================================

with st.sidebar.expander("🔎 Búsqueda Semántica"):

    consulta_busqueda = st.text_input(
        "Buscar documentos similares"
    )

    if st.button(
        "🔍 Buscar",
        key="buscar_semantico"
    ):

        if consulta_busqueda.strip() != "":

            resultados = buscar_documentos_semanticos(
                consulta_busqueda
            )

            if len(resultados) > 0:

                resultados = enriquecer_resultados(
                    resultados
                )

                st.success(
                    "✅ Resultados encontrados"
                )

                for i, fila in resultados.iterrows():

                    st.markdown("---")

                    st.subheader(
                        f"📄 Resultado {i + 1}"
                    )

                    if "tipo_documental" in fila:

                        st.write(
                            f"📂 Tipo: {fila['tipo_documental']}"
                        )

                    if "dependencia" in fila:

                        st.write(
                            f"🏢 Dependencia: {fila['dependencia']}"
                        )

                    if "resumen" in fila:

                        st.write(
                            fila["resumen"]
                        )

            else:

                st.warning(
                    "⚠️ Sin resultados"
                )

# ==========================================
# BUSCADOR INTELIGENTE
# ==========================================

with st.sidebar.expander("📂 Buscador Inteligente"):

    consulta_carpeta = st.text_input(
        "Buscar carpeta, archivo o consecutivo"
    )

    if st.button(
        "📁 Explorar Carpeta",
        key="explorar_carpeta"
    ):

        if consulta_carpeta.strip() != "":

            resultados_carpetas = buscar_en_carpetas(
                consulta_carpeta
            )

            if len(resultados_carpetas) > 0:

                st.success(
                    f"✅ {len(resultados_carpetas)} archivos encontrados"
                )

                carpetas = (
                    resultados_carpetas[
                        "carpeta"
                    ]
                    .unique()
                )

                for carpeta in carpetas:

                    st.markdown("---")

                    st.subheader(
                        f"🗂 Carpeta: {carpeta}"
                    )

                    archivos = resultados_carpetas[
                        resultados_carpetas[
                            "carpeta"
                        ] == carpeta
                    ]

                    for i, fila in archivos.iterrows():

                        ruta_archivo = fila["ruta"]

                        nombre_archivo = fila["archivo"]

                        st.write(
                            f"📄 {nombre_archivo}"
                        )

                        st.caption(
                            ruta_archivo
                        )

                        if os.path.exists(
                            ruta_archivo
                        ):

                            extension = (
                                nombre_archivo
                                .split(".")[-1]
                                .lower()
                            )

                            # ======================================
                            # PDF
                            # ======================================

                            # ======================================
                            # PDF
                            # ======================================

                            if extension == "pdf":

                                st.info(
                                    "📄 Vista previa PDF"
                                )

                                try:

                                    with open(
                                        ruta_archivo,
                                        "rb"
                                    ) as pdf_file:

                                        pdf_bytes = pdf_file.read()

                                    st.download_button(
                                        label=f"📥 Descargar {nombre_archivo}",
                                        data=pdf_bytes,
                                        file_name=nombre_archivo,
                                        mime="application/pdf",
                                        key=f"pdf_{i}"
                                    )

                                    st.write(
                                        f"📄 Archivo: {nombre_archivo}"
                                    )

                                    st.write(
                                        f"📦 Tamaño: {round(len(pdf_bytes)/1024,2)} KB"
                                    )

                                    texto_pdf = leer_pdf(
                                        ruta_archivo
                                    )

                                    if (
                                        texto_pdf
                                        and not texto_pdf.startswith("ERROR")
                                    ):

                                        st.text_area(
                                            "Contenido detectado",
                                            texto_pdf[:5000],
                                            height=350,
                                            key=f"texto_pdf_{i}"
                                        )

                                    else:

                                        st.warning(
                                            "No fue posible extraer texto del PDF"
                                        )

                                except Exception as e:

                                    st.error(
                                        f"Error visualizando PDF: {e}"
                                    )

                            # ======================================
                            # IMÁGENES
                            # ======================================

                            elif extension in [
                                "png",
                                "jpg",
                                "jpeg"
                            ]:

                                st.image(
                                    ruta_archivo,
                                    use_container_width=True
                                )

                                with open(
                                    ruta_archivo,
                                    "rb"
                                ) as img_file:

                                    img_bytes = img_file.read()

                                st.download_button(
                                    label=f"📥 Descargar {nombre_archivo}",
                                    data=img_bytes,
                                    file_name=nombre_archivo,
                                    mime="image/jpeg",
                                    key=f"img_{i}"
                                )

                            # ======================================
                            # WORD
                            # ======================================

                            elif extension == "docx":

                                st.info(
                                    "📄 Documento Word detectado"
                                )

                                with open(
                                    ruta_archivo,
                                    "rb"
                                ) as docx_file:

                                    docx_bytes = docx_file.read()

                                st.download_button(
                                    label=f"📥 Descargar {nombre_archivo}",
                                    data=docx_bytes,
                                    file_name=nombre_archivo,
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    key=f"docx_{i}"
                                )

                            # ======================================
                            # OTROS
                            # ======================================

                            else:

                                st.info(
                                    "Vista previa no disponible"
                                )

            else:

                st.warning(
                    "⚠️ No se encontraron resultados"
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
    # TECNOLOGÍAS
    # ==========================================

    st.markdown(
        """
        <div class="bloque">
            <h2>🚀 Tecnologías implementadas</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    tecnologias = [

        "NLP avanzado",
        "OCR automático",
        "PDFs escaneados",
        "Machine Learning",
        "Clasificación híbrida TRD",
        "Motor estructural",
        "Procesamiento masivo ZIP",
        "Buscador semántico",
        "Visualizador documental",
        "WordCloud NLP"

    ]

    for tech in tecnologias:

        st.write(f"✅ {tech}")

    st.markdown("---")

    # ==========================================
    # CLASIFICACIÓN INDIVIDUAL
    # ==========================================

    st.subheader(
        "📄 Clasificación Individual"
    )

    archivo = st.file_uploader(
        "Suba PDF, Word o Imagen",
        type=[
            "pdf",
            "docx",
            "png",
            "jpg",
            "jpeg"
        ],
        key="archivo_individual"
    )

    texto_archivo = ""
    ruta_temporal = ""

    if archivo is not None:

        extension = (
            archivo.name
            .split(".")[-1]
            .lower()
        )

        temp_dir = tempfile.gettempdir()

        ruta_temporal = os.path.join(
            temp_dir,
            archivo.name
        )

        with open(
            ruta_temporal,
            "wb"
        ) as f:

            f.write(
                archivo.getbuffer()
            )

        if extension == "pdf":

            texto_archivo = leer_pdf(
                ruta_temporal
            )

        elif extension == "docx":

            texto_archivo = leer_docx(
                ruta_temporal
            )

        else:

            texto_archivo = leer_imagen(
                ruta_temporal
            )

        st.success(
            "✅ Documento leído correctamente"
        )

    texto_usuario = st.text_area(
        "✍️ Texto del documento",
        value=texto_archivo,
        height=250
    )

    if st.button(
        "🚀 Clasificar documento",
        key="clasificar_individual"
    ):

        if texto_usuario.strip() != "":

            texto_limpio = limpiar_texto(
                texto_usuario
            )

            texto_procesado = procesar_texto(
                texto_limpio
            )

            tipo_nlp = detectar_tipo_documental(
                texto_procesado
            )

            dependencia = detectar_dependencia(
                texto_procesado
            )

            resultado_hibrido = clasificacion_hibrida(
                texto_usuario,
                tipo_nlp,
                dependencia
            )

            tipo_documental = resultado_hibrido[
                "tipo_final"
            ]

            score_hibrido = resultado_hibrido[
                "score"
            ]

            fuente_clasificacion = resultado_hibrido[
                "fuente"
            ]

            consecutivo = extraer_consecutivo(
                texto_usuario
            )

            vector = vectorizador.transform(
                [texto_procesado]
            )

            prediccion = modelo.predict(
                vector
            )

            categoria = encoder.inverse_transform(
                prediccion
            )[0]

            probabilidades = modelo.predict_proba(
                vector
            )

            confianza = round(
                max(probabilidades[0]) * 100,
                2
            )

            st.success(
                f"📂 Tipo documental: {tipo_documental}"
            )

            st.info(
                f"🧠 Fuente clasificación: {fuente_clasificacion}"
            )

            st.info(
                f"🎯 Score híbrido: {score_hibrido}"
            )

            st.success(
                f"🏢 Dependencia: {dependencia}"
            )

            st.success(
                f"🔖 Consecutivo: {consecutivo}"
            )

            st.success(
                f"🤖 Categoría IA: {categoria}"
            )

            st.info(
                f"🎯 Confianza IA: {confianza}%"
            )

            # ======================================
            # VALIDACIÓN
            # ======================================

            if confianza < 65:

                st.warning(
                    "⚠️ Documento enviado a revisión manual"
                )

            else:

                if archivo is not None:

                    try:

                        ruta_final = mover_documento(
                            ruta_temporal,
                            tipo_documental,
                            dependencia
                        )

                        st.success(
                            f"✅ Documento organizado en: {ruta_final}"
                        )

                    except Exception as e:

                        st.error(
                            f"Error organizando: {e}"
                        )

            st.subheader(
                "☁️ WordCloud NLP"
            )

            mostrar_wordcloud(
                texto_procesado
            )

            st.subheader(
                "🧠 Explicación IA"
            )

            palabras = obtener_palabras_clave(
                vectorizador,
                vector
            )

            for palabra in palabras:

                st.write(f"• {palabra}")

    # ==========================================
    # PROCESAMIENTO MASIVO ZIP
    # ==========================================

    st.markdown("---")

    st.subheader(
        "📦 Procesamiento Masivo ZIP"
    )

    archivo_zip = st.file_uploader(
        "Suba carpeta ZIP",
        type=["zip"],
        key="zip_uploader"
    )

    if archivo_zip is not None:

        st.success(
            "✅ ZIP cargado correctamente"
        )

        if st.button(
            "🚀 Clasificar documentos ZIP",
            key="clasificar_zip"
        ):

            st.info(
                "Procesando ZIP..."
            )

            temp_dir = tempfile.mkdtemp()

            zip_path = os.path.join(
                temp_dir,
                archivo_zip.name
            )

            with open(
                zip_path,
                "wb"
            ) as f:

                f.write(
                    archivo_zip.getbuffer()
                )

            carpeta_extraida = os.path.join(
                temp_dir,
                "extraido"
            )

            with zipfile.ZipFile(
                zip_path,
                "r"
            ) as zip_ref:

                zip_ref.extractall(
                    carpeta_extraida
                )

            archivos_detectados = []

            for root, dirs, files in os.walk(
                carpeta_extraida
            ):

                for file in files:

                    extension = (
                        file
                        .split(".")[-1]
                        .lower()
                    )

                    if extension in [
                        "pdf",
                        "docx",
                        "png",
                        "jpg",
                        "jpeg"
                    ]:

                        archivos_detectados.append(
                            os.path.join(
                                root,
                                file
                            )
                        )

            st.success(
                f"✅ {len(archivos_detectados)} documentos encontrados"
            )

            barra = st.progress(0)

            resultados = []

            for i, ruta_archivo in enumerate(
                archivos_detectados
            ):

                try:

                    extension = (
                        ruta_archivo
                        .split(".")[-1]
                        .lower()
                    )

                    if extension == "pdf":

                        texto = leer_pdf(
                            ruta_archivo
                        )

                    elif extension == "docx":

                        texto = leer_docx(
                            ruta_archivo
                        )

                    else:

                        texto = leer_imagen(
                            ruta_archivo
                        )

                    texto_limpio = limpiar_texto(
                        texto
                    )

                    texto_procesado = procesar_texto(
                        texto_limpio
                    )

                    tipo_nlp = detectar_tipo_documental(
                        texto_procesado
                    )

                    dependencia = detectar_dependencia(
                        texto_procesado
                    )

                    resultado_hibrido = clasificacion_hibrida(
                        texto,
                        tipo_nlp,
                        dependencia
                    )

                    tipo_documental = resultado_hibrido[
                        "tipo_final"
                    ]

                    score_hibrido = resultado_hibrido[
                        "score"
                    ]

                    fuente = resultado_hibrido[
                        "fuente"
                    ]

                    consecutivo = extraer_consecutivo(
                        texto
                    )

                    vector = vectorizador.transform(
                        [texto_procesado]
                    )

                    prediccion = modelo.predict(
                        vector
                    )

                    categoria = encoder.inverse_transform(
                        prediccion
                    )[0]

                    confianza = round(
                        max(
                            modelo.predict_proba(
                                vector
                            )[0]
                        ) * 100,
                        2
                    )

                    if confianza < 65:

                        carpeta_revision = (
                            "data/revision_manual"
                        )

                        os.makedirs(
                            carpeta_revision,
                            exist_ok=True
                        )

                        destino_revision = os.path.join(
                            carpeta_revision,
                            os.path.basename(
                                ruta_archivo
                            )
                        )

                        shutil.copy(
                            ruta_archivo,
                            destino_revision
                        )

                        ruta_final = destino_revision

                        estado = "REVISIÓN MANUAL"

                    else:

                        ruta_final = mover_documento(
                            ruta_archivo,
                            tipo_documental,
                            dependencia
                        )

                        estado = "CLASIFICADO"

                    resultados.append({

                        "archivo":
                        os.path.basename(
                            ruta_archivo
                        ),

                        "tipo_documental":
                        tipo_documental,

                        "dependencia":
                        dependencia,

                        "categoria_ia":
                        categoria,

                        "confianza":
                        confianza,

                        "score_hibrido":
                        score_hibrido,

                        "fuente":
                        fuente,

                        "estado":
                        estado,

                        "consecutivo":
                        consecutivo,

                        "ruta_final":
                        ruta_final

                    })

                except Exception as e:

                    resultados.append({

                        "archivo":
                        os.path.basename(
                            ruta_archivo
                        ),

                        "error":
                        str(e)

                    })

                progreso = int(
                    ((i + 1) / len(archivos_detectados)) * 100
                )

                barra.progress(
                    progreso
                )

            st.success(
                "✅ Procesamiento masivo finalizado"
            )

            df_resultados = pd.DataFrame(
                resultados
            )

            st.subheader(
                "📊 Resultados procesamiento masivo"
            )

            st.dataframe(
                df_resultados,
                use_container_width=True
            )

            # ======================================
            # EXPORTAR EXCEL
            # ======================================

            excel_path = os.path.join(
                temp_dir,
                "resultado_masivo.xlsx"
            )

            df_resultados.to_excel(
                excel_path,
                index=False
            )

            with open(
                excel_path,
                "rb"
            ) as excel_file:

                st.download_button(
                    label="📥 Descargar reporte Excel",
                    data=excel_file,
                    file_name="resultado_masivo.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Proyecto desarrollado con Python + NLP + OCR + Machine Learning + Streamlit"
)