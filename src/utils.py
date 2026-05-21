
# ==========================================
# IMPORTACIONES
# ==========================================

import pandas as pd

# ==========================================
# OBTENER TOP CATEGORÍAS
# ==========================================

def obtener_top_categorias(

    modelo,

    vector,

    encoder,

    top_n=3

):

    # ======================================
    # PROBABILIDADES
    # ======================================

    probabilidades = modelo.predict_proba(
        vector
    )[0]

    # ======================================
    # DATAFRAME
    # ======================================

    df_probabilidades = pd.DataFrame({

        "categoria": encoder.classes_,

        "probabilidad": probabilidades

    })

    # ======================================
    # ORDENAR
    # ======================================

    df_probabilidades = df_probabilidades.sort_values(

        by="probabilidad",

        ascending=False

    )

    # ======================================
    # TOP N
    # ======================================

    top = df_probabilidades.head(
        top_n
    )

    return top