
from preprocess import (
    limpiar_texto,
    procesar_texto
)

# =========================
# FUNCIÓN DE PREDICCIÓN
# =========================

def predecir_categoria(
    texto,
    modelo,
    vectorizador,
    encoder
):

    # =========================
    # LIMPIEZA
    # =========================

    texto_limpio = limpiar_texto(texto)

    # =========================
    # PROCESAMIENTO NLP
    # =========================

    texto_procesado = procesar_texto(
        texto_limpio
    )

    # =========================
    # VECTORIZACIÓN
    # =========================

    vector = vectorizador.transform(
        [texto_procesado]
    )

    # =========================
    # PREDICCIÓN
    # =========================

    prediccion = modelo.predict(vector)

    # =========================
    # DECODIFICAR CATEGORÍA
    # =========================

    categoria = encoder.inverse_transform(
        prediccion
    )

    return categoria[0]