# ==========================================
# IMPORTACIONES
# ==========================================

import pandas as pd
import os

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

# ==========================================
# BUSCADOR SEMÁNTICO
# ==========================================

def buscar_documentos_semanticos(
    consulta,
    top_k=5
):

    ruta_historial = (
        "reports/historial.csv"
    )

    # ======================================
    # VALIDAR HISTORIAL
    # ======================================

    if not os.path.exists(
        ruta_historial
    ):

        return pd.DataFrame()

    # ======================================
    # LEER HISTORIAL
    # ======================================

    df = pd.read_csv(
        ruta_historial
    )

    # ======================================
    # VALIDAR TEXTO
    # ======================================

    if "texto" not in df.columns:

        return pd.DataFrame()

    # ======================================
    # LIMPIAR
    # ======================================

    df = df.fillna("")

    textos = df["texto"].astype(str)

    # ======================================
    # TF-IDF
    # ======================================

    vectorizador = TfidfVectorizer()

    matriz = vectorizador.fit_transform(
        textos
    )

    consulta_vector = vectorizador.transform(
        [consulta]
    )

    # ======================================
    # SIMILITUD COSENO
    # ======================================

    similitudes = cosine_similarity(

        consulta_vector,
        matriz

    )[0]

    # ======================================
    # AGREGAR SCORE
    # ======================================

    df["score_semantico"] = similitudes

    # ======================================
    # ORDENAR
    # ======================================

    resultados = df.sort_values(

        by="score_semantico",

        ascending=False

    )

    # ======================================
    # TOP RESULTADOS
    # ======================================

    resultados = resultados.head(
        top_k
    )

    return resultados