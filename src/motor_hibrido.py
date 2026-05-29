import re

# ==========================================
# MOTOR HÍBRIDO TRD
# ==========================================

def clasificacion_hibrida(

    texto,
    tipo_nlp,
    dependencia

):

    texto_upper = texto.upper()

    score = {}

    # ======================================
    # ACTAS
    # ======================================

    patrones_acta = [

        "ACTA",
        "REUNIÓN",
        "COMITÉ",
        "ASISTENTES",
        "ORDEN DEL DÍA"

    ]

    puntos_acta = sum(

        1 for patron in patrones_acta

        if patron in texto_upper

    )

    score["ACTA"] = puntos_acta

    # ======================================
    # CIRCULARES
    # ======================================

    patrones_circular = [

        "CIRCULAR",
        "PARA:",
        "ASUNTO:",
        "DIRECTRICES"

    ]

    puntos_circular = sum(

        1 for patron in patrones_circular

        if patron in texto_upper

    )

    score["CIRCULAR"] = puntos_circular

    # ======================================
    # CONTRATOS
    # ======================================

    patrones_contrato = [

        "CONTRATO",
        "CLÁUSULA",
        "CONTRATANTE",
        "CONTRATISTA"

    ]

    puntos_contrato = sum(

        1 for patron in patrones_contrato

        if patron in texto_upper

    )

    score["CONTRATO"] = puntos_contrato

    # ======================================
    # RESOLUCIONES
    # ======================================

    patrones_resolucion = [

        "RESOLUCIÓN",
        "RESUELVE",
        "ARTÍCULO"

    ]

    puntos_resolucion = sum(

        1 for patron in patrones_resolucion

        if patron in texto_upper

    )

    score["RESOLUCIÓN"] = puntos_resolucion

    # ======================================
    # GANADOR
    # ======================================

    mejor_tipo = max(
        score,
        key=score.get
    )

    mejor_score = score[
        mejor_tipo
    ]

    # ======================================
    # VALIDACIÓN
    # ======================================

    if mejor_score >= 2:

        tipo_final = mejor_tipo

        fuente = "MOTOR_HIBRIDO"

    else:

        tipo_final = tipo_nlp

        fuente = "NLP"

    return {

        "tipo_final":
        tipo_final,

        "score":
        mejor_score,

        "fuente":
        fuente

    }