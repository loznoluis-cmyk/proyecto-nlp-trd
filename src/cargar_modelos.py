
# ==========================================
# IMPORTAR LIBRERÍAS
# ==========================================

import pickle


# ==========================================
# FUNCIÓN CARGAR MODELOS
# ==========================================

def cargar_modelos():

    # ==============================
    # CARGAR MODELO NLP
    # ==============================

    with open(
        "models/modelo_nlp.pkl",
        "rb"
    ) as archivo_modelo:

        modelo = pickle.load(
            archivo_modelo
        )

    # ==============================
    # CARGAR VECTORIZADOR
    # ==============================

    with open(
        "models/vectorizador.pkl",
        "rb"
    ) as archivo_vectorizador:

        vectorizador = pickle.load(
            archivo_vectorizador
        )

    # ==============================
    # CARGAR ENCODER
    # ==============================

    with open(
        "models/encoder.pkl",
        "rb"
    ) as archivo_encoder:

        encoder = pickle.load(
            archivo_encoder
        )

    # ==============================
    # RETORNAR
    # ==============================

    return modelo, vectorizador, encoder