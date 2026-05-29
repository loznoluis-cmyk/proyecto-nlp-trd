import pandas as pd

# ==========================================
# GENERAR RESUMEN SIMPLE
# ==========================================

def generar_resumen(texto):

    try:

        if texto is None:
            return "SIN TEXTO"

        texto = str(texto)

        texto = texto.strip()

        if texto == "":
            return "SIN TEXTO"

        palabras = texto.split()

        resumen = " ".join(
            palabras[:40]
        )

        return resumen

    except Exception as e:

        return f"ERROR RESUMEN: {e}"


# ==========================================
# EXTRAER KEYWORDS
# ==========================================

def extraer_keywords(texto):

    try:

        texto = str(texto)

        palabras = texto.split()

        palabras = [
            p for p in palabras
            if len(p) > 5
        ]

        keywords = list(
            dict.fromkeys(
                palabras[:10]
            )
        )

        return ", ".join(
            keywords
        )

    except Exception as e:

        return f"ERROR KEYWORDS: {e}"


# ==========================================
# ENRIQUECER RESULTADOS
# ==========================================

def enriquecer_resultados(df):

    if len(df) == 0:

        return df

    # ======================================
    # RESUMEN
    # ======================================

    if "texto" in df.columns:

        df["resumen"] = df["texto"].apply(
            generar_resumen
        )

        df["keywords"] = df["texto"].apply(
            extraer_keywords
        )

    else:

        df["resumen"] = "SIN TEXTO"

        df["keywords"] = "SIN KEYWORDS"

    return df