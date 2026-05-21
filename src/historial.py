
# ==========================================
# IMPORTACIONES
# ==========================================

import pandas as pd

from datetime import datetime

import os

# ==========================================
# GUARDAR HISTORIAL
# ==========================================

def guardar_historial(

    texto,

    categoria,

    confianza

):

    # ======================================
    # CREAR REGISTRO
    # ======================================

    nuevo_registro = {

        "fecha": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "texto": texto,

        "categoria": categoria,

        "confianza": round(
            confianza,
            2
        )

    }

    # ======================================
    # RUTA ARCHIVO
    # ======================================

    ruta = "reports/historial_predicciones.csv"

    # ======================================
    # SI EXISTE
    # ======================================

    if os.path.exists(ruta):

        df = pd.read_csv(ruta)

        df = pd.concat(

            [
                df,
                pd.DataFrame([nuevo_registro])
            ],

            ignore_index=True

        )

    else:

        df = pd.DataFrame(
            [nuevo_registro]
        )

    # ======================================
    # GUARDAR
    # ======================================

    df.to_csv(

        ruta,

        index=False

    )
    