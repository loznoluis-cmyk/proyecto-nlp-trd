
# ==========================================
# PALABRAS MÁS IMPORTANTES
# ==========================================

import numpy as np

def obtener_palabras_clave(
    vectorizador,
    vector,
    top_n=10
):

    # ==========================================
    # OBTENER FEATURES
    # ==========================================

    palabras = (
        vectorizador.get_feature_names_out()
    )

    # ==========================================
    # VECTOR TFIDF
    # ==========================================

    valores = (
        vector.toarray()[0]
    )

    # ==========================================
    # ORDENAR IMPORTANCIA
    # ==========================================

    indices = np.argsort(
        valores
    )[::-1]

    # ==========================================
    # EXTRAER TOP
    # ==========================================

    palabras_clave = []

    for i in indices:

        if valores[i] > 0:

            palabras_clave.append(
                palabras[i]
            )

        if len(palabras_clave) >= top_n:

            break

    return palabras_clave