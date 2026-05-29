# ==========================================
# IMPORTACIONES
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# DASHBOARD
# ==========================================

def mostrar_dashboard():

    st.title(
        "📊 Dashboard Inteligente TRD"
    )

    st.write(
        "Monitoreo analítico de clasificación documental"
    )

    ruta_historial = (
        "reports/historial.csv"
    )

    # ==========================================
    # VALIDAR HISTORIAL
    # ==========================================

    if not os.path.exists(
        ruta_historial
    ):

        st.warning(
            "⚠️ No existe historial todavía"
        )

        return

    # ==========================================
    # LEER HISTORIAL
    # ==========================================

    df = pd.read_csv(
        ruta_historial
    )

    # ==========================================
    # VALIDAR DATOS
    # ==========================================

    if len(df) == 0:

        st.warning(
            "⚠️ Historial vacío"
        )

        return

    # ==========================================
    # NORMALIZAR COLUMNAS
    # ==========================================

    columnas = df.columns.tolist()

    # Compatibilidad versiones anteriores
    if "categoria" in columnas:

        df["categoria_ia"] = df["categoria"]

    if "estado_documental" not in columnas:

        df["estado_documental"] = "SIN VALIDAR"

    if "dependencia" not in columnas:

        df["dependencia"] = "GENERAL"

    if "tipo_documental" not in columnas:

        df["tipo_documental"] = "OTRO"

    # ==========================================
    # FECHA
    # ==========================================

    df["fecha"] = pd.to_datetime(
        df["fecha"],
        errors="coerce"
    )

    # ==========================================
    # KPIs PRINCIPALES
    # ==========================================

    total_documentos = len(df)

    promedio_confianza = round(
        df["confianza"].mean(),
        2
    )

    categoria_top = (
        df["categoria_ia"]
        .value_counts()
        .idxmax()
    )

    dependencia_top = (
        df["dependencia"]
        .value_counts()
        .idxmax()
    )

    # ==========================================
    # KPIs VISUALES
    # ==========================================

    st.subheader(
        "📌 Indicadores principales"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📄 Documentos",
        total_documentos
    )

    col2.metric(
        "🎯 Confianza",
        f"{promedio_confianza}%"
    )

    col3.metric(
        "🏆 Categoría Top",
        categoria_top
    )

    col4.metric(
        "🏢 Dependencia Top",
        dependencia_top
    )

    st.markdown("---")

    # ==========================================
    # ESTADOS DOCUMENTALES
    # ==========================================

    st.subheader(
        "🚦 Estado documental"
    )

    estados = (
        df["estado_documental"]
        .value_counts()
        .reset_index()
    )

    estados.columns = [
        "Estado",
        "Cantidad"
    ]

    grafica_estados = px.bar(

        estados,

        x="Estado",
        y="Cantidad",

        color="Estado",

        title="Estado de validación documental"

    )

    st.plotly_chart(
        grafica_estados,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # DISTRIBUCIÓN IA
    # ==========================================

    st.subheader(
        "📊 Distribución IA"
    )

    conteo = (
        df["categoria_ia"]
        .value_counts()
        .reset_index()
    )

    conteo.columns = [
        "Categoria",
        "Cantidad"
    ]

    grafica_barras = px.bar(

        conteo,

        x="Categoria",
        y="Cantidad",

        color="Categoria",

        title="Documentos por categoría IA"

    )

    st.plotly_chart(
        grafica_barras,
        use_container_width=True
    )

    # ==========================================
    # DEPENDENCIAS
    # ==========================================

    st.subheader(
        "🏢 Dependencias institucionales"
    )

    dependencias = (
        df["dependencia"]
        .value_counts()
        .reset_index()
    )

    dependencias.columns = [
        "Dependencia",
        "Cantidad"
    ]

    grafica_dependencias = px.pie(

        dependencias,

        names="Dependencia",
        values="Cantidad",

        title="Distribución por dependencia"

    )

    st.plotly_chart(
        grafica_dependencias,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # TIPOS DOCUMENTALES
    # ==========================================

    st.subheader(
        "📂 Tipos documentales"
    )

    tipos = (
        df["tipo_documental"]
        .value_counts()
        .reset_index()
    )

    tipos.columns = [
        "Tipo",
        "Cantidad"
    ]

    grafica_tipos = px.bar(

        tipos,

        x="Tipo",
        y="Cantidad",

        color="Tipo",

        title="Tipos documentales detectados"

    )

    st.plotly_chart(
        grafica_tipos,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # CONFIANZA HISTÓRICA
    # ==========================================

    st.subheader(
        "📈 Evolución de confianza IA"
    )

    grafica_linea = px.line(

        df,

        x="fecha",
        y="confianza",

        title="Confianza del modelo en el tiempo"

    )

    st.plotly_chart(
        grafica_linea,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # ALERTAS DOCUMENTALES
    # ==========================================

    st.subheader(
        "🚨 Alertas documentales"
    )

    df_alertas = df[
        df["estado_documental"]
        == "VALIDACIÓN MANUAL"
    ]

    total_alertas = len(
        df_alertas
    )

    if total_alertas > 0:

        st.error(
            f"⚠️ Existen {total_alertas} documentos que requieren validación manual"
        )

        st.dataframe(
            df_alertas.sort_values(
                by="fecha",
                ascending=False
            ),
            use_container_width=True
        )

    else:

        st.success(
            "✅ No existen alertas documentales"
        )

    st.markdown("---")

    # ==========================================
    # HISTORIAL RECIENTE
    # ==========================================

    st.subheader(
        "🕒 Últimas clasificaciones"
    )

    st.dataframe(

        df.sort_values(
            by="fecha",
            ascending=False
        ).head(15),

        use_container_width=True

    )

    st.markdown("---")

    # ==========================================
    # EXPORTAR EXCEL
    # ==========================================

    st.subheader(
        "📥 Exportar reporte institucional"
    )

    archivo_excel = (
        "reports/historial_clasificaciones.xlsx"
    )

    df.to_excel(
        archivo_excel,
        index=False
    )

    with open(
        archivo_excel,
        "rb"
    ) as archivo:

        st.download_button(

            label="📥 Descargar reporte Excel",

            data=archivo,

            file_name="historial_clasificaciones.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )