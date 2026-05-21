
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
        "📊 Dashboard Analítico NLP"
    )

    st.write(
        "Monitoreo inteligente de clasificaciones documentales"
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
            "No existe historial todavía"
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
            "Historial vacío"
        )

        return

    # ==========================================
    # KPIs
    # ==========================================

    total_documentos = len(df)

    promedio_confianza = round(
        df["confianza"].mean(),
        2
    )

    categoria_top = (
        df["categoria"]
        .value_counts()
        .idxmax()
    )

    # ==========================================
    # KPIs VISUALES
    # ==========================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📄 Total Clasificaciones",
        total_documentos
    )

    col2.metric(
        "🎯 Confianza Promedio",
        f"{promedio_confianza}%"
    )

    col3.metric(
        "🏆 Categoría Top",
        categoria_top
    )

    st.markdown("---")

    # ==========================================
    # EXPORTAR EXCEL
    # ==========================================

    st.subheader(
        "📥 Exportar Reporte"
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

            label="📥 Descargar historial Excel",

            data=archivo,

            file_name="historial_clasificaciones.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )

    st.markdown("---")

    # ==========================================
    # DISTRIBUCIÓN
    # ==========================================

    st.subheader(
        "📊 Distribución documental"
    )

    conteo = (
        df["categoria"]
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

        title="Cantidad de documentos por categoría"

    )

    st.plotly_chart(
        grafica_barras,
        use_container_width=True
    )

    # ==========================================
    # PIE CHART
    # ==========================================

    st.subheader(
        "🥧 Participación por categoría"
    )

    grafica_pie = px.pie(

        conteo,

        names="Categoria",
        values="Cantidad",

        title="Distribución porcentual"

    )

    st.plotly_chart(
        grafica_pie,
        use_container_width=True
    )

    # ==========================================
    # HISTORIAL
    # ==========================================

    st.subheader(
        "🕒 Últimas clasificaciones"
    )

    st.dataframe(

        df.sort_values(
            by="fecha",
            ascending=False
        ).head(10),

        use_container_width=True

    )

    # ==========================================
    # CONFIANZA HISTÓRICA
    # ==========================================

    st.subheader(
        "📈 Evolución de confianza"
    )

    df["fecha"] = pd.to_datetime(
        df["fecha"]
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
    