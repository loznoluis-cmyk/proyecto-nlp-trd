import os
import pandas as pd

from src.lector_documentos import (
    leer_pdf,
    leer_docx,
    leer_imagen
)


def buscar_en_carpetas(
    consulta,
    ruta_base="data/trd"
):

    resultados = []

    consulta = consulta.lower().strip()

    # ==========================================
    # RECORRER TODAS LAS CARPETAS
    # ==========================================

    for root, dirs, files in os.walk(
        ruta_base
    ):

        nombre_carpeta = (
            os.path.basename(root)
            .lower()
        )

        coincidencia_carpeta = (
            consulta in nombre_carpeta
        )

        # ==========================================
        # RECORRER ARCHIVOS
        # ==========================================

        for file in files:

            ruta_archivo = os.path.join(
                root,
                file
            )

            nombre_archivo = (
                file.lower()
            )

            coincidencia_archivo = (
                consulta in nombre_archivo
            )

            coincidencia_contenido = False

            texto = ""

            try:

                extension = (
                    file
                    .split(".")[-1]
                    .lower()
                )

                # ======================================
                # LEER PDF
                # ======================================

                if extension == "pdf":

                    texto = leer_pdf(
                        ruta_archivo
                    )

                # ======================================
                # LEER WORD
                # ======================================

                elif extension == "docx":

                    texto = leer_docx(
                        ruta_archivo
                    )

                # ======================================
                # LEER IMÁGENES
                # ======================================

                elif extension in [
                    "png",
                    "jpg",
                    "jpeg"
                ]:

                    texto = leer_imagen(
                        ruta_archivo
                    )

                # ======================================
                # BUSCAR DENTRO DEL TEXTO
                # ======================================

                if consulta in texto.lower():

                    coincidencia_contenido = True

            except Exception:

                pass

            # ==========================================
            # COINCIDENCIA
            # ==========================================

            if (
                coincidencia_carpeta
                or coincidencia_archivo
                or coincidencia_contenido
            ):

                resultados.append({

                    "archivo":
                    file,

                    "carpeta":
                    os.path.basename(root),

                    "ruta":
                    ruta_archivo,

                    "tipo_busqueda":
                    (
                        "contenido"
                        if coincidencia_contenido
                        else "nombre"
                    )

                })

    # ==========================================
    # RESULTADOS
    # ==========================================

    if len(resultados) > 0:

        return pd.DataFrame(
            resultados
        )

    return pd.DataFrame()