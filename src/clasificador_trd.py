import os
import shutil
import pandas as pd

from datetime import datetime


# =========================================
# RUTA BASE TRD
# =========================================

BASE_TRD = "data/trd"


# =========================================
# CARGAR TRD
# =========================================

def cargar_trd():

    ruta_excel = (
        "data/trd/configuracion/TRD.xlsx"
    )

    df = pd.read_excel(
        ruta_excel,
        header=None
    )

    # =====================================
    # LIMPIAR
    # =====================================

    df = df.dropna(
        how="all"
    )

    df = df.fillna("")

    df = df.astype(str)

    return df


# =========================================
# LIMPIAR TEXTO
# =========================================

def limpiar_texto(texto):

    texto = str(texto)

    texto = texto.upper()

    texto = texto.strip()

    texto = texto.replace(
        "\n",
        " "
    )

    texto = texto.replace(
        "/",
        "_"
    )

    texto = texto.replace(
        "\\",
        "_"
    )

    texto = texto.replace(
        ":",
        ""
    )

    texto = texto.replace(
        "*",
        ""
    )

    texto = texto.replace(
        "?",
        ""
    )

    texto = texto.replace(
        '"',
        ""
    )

    texto = texto.replace(
        "<",
        ""
    )

    texto = texto.replace(
        ">",
        ""
    )

    texto = texto.replace(
        "|",
        ""
    )

    # =====================================
    # ELIMINAR DOBLES ESPACIOS
    # =====================================

    texto = " ".join(
        texto.split()
    )

    return texto


# =========================================
# EXTRAER SERIES TRD
# =========================================

def extraer_series_trd():

    df = cargar_trd()

    series_detectadas = []

    for _, fila in df.iterrows():

        fila_texto = " ".join(
            fila.values
        )

        fila_texto = limpiar_texto(
            fila_texto
        )

        # =====================================
        # FILTRAR BASURA
        # =====================================

        palabras_invalidas = [

            "FORMATO",
            "RETENCIÓN",
            "DOCUMENTAL",
            "VERSIÓN",
            "CÓDIGO",
            "PROCEDIMIENTO",
            "VIGENTE",
            "SERIE",
            "SUBSERIE",
            "TIPOS",
            "DOCUMENTALES",
            "TABLAS"
        ]

        invalida = False

        for palabra in palabras_invalidas:

            if palabra in fila_texto:

                invalida = True
                break

        # =====================================
        # VALIDAR LONGITUD
        # =====================================

        if (

            invalida is False

            and len(fila_texto) > 8

            and len(fila_texto) < 180

        ):

            primeras = fila_texto.split()

            if len(primeras) > 1:

                codigo = primeras[0]

                if codigo.isdigit():

                    series_detectadas.append(
                        fila_texto
                    )

    # =====================================
    # ELIMINAR DUPLICADOS
    # =====================================

    series_detectadas = list(
        set(series_detectadas)
    )

    series_detectadas.sort()

    return series_detectadas


# =========================================
# CREAR CARPETAS TRD
# =========================================

def crear_carpetas_trd():

    series = extraer_series_trd()

    carpetas_creadas = []

    for serie in series:

        nombre_carpeta = limpiar_texto(
            serie
        )

        ruta_carpeta = os.path.join(
            BASE_TRD,
            nombre_carpeta
        )

        os.makedirs(
            ruta_carpeta,
            exist_ok=True
        )

        carpetas_creadas.append(
            ruta_carpeta
        )

    return carpetas_creadas


# =========================================
# CALCULAR SCORE TRD
# =========================================

def calcular_score_trd(
    carpeta,
    tipo_documental,
    dependencia
):

    score = 0

    carpeta_upper = limpiar_texto(
        carpeta
    )

    tipo_documental = limpiar_texto(
        tipo_documental
    )

    dependencia = limpiar_texto(
        dependencia
    )

    # =====================================
    # SCORE TIPO DOCUMENTAL
    # =====================================

    palabras_tipo = tipo_documental.split()

    for palabra in palabras_tipo:

        if len(palabra) > 3:

            if palabra in carpeta_upper:

                score += 10

    # =====================================
    # SCORE DEPENDENCIA
    # =====================================

    palabras_dependencia = dependencia.split()

    for palabra in palabras_dependencia:

        if len(palabra) > 4:

            if palabra in carpeta_upper:

                score += 5

    return score


# =========================================
# BUSCAR MEJOR SERIE TRD
# =========================================

def buscar_serie_trd(
    tipo_documental,
    dependencia="GENERAL"
):

    carpetas = os.listdir(
        BASE_TRD
    )

    mejor_score = -1

    mejor_carpeta = None

    for carpeta in carpetas:

        ruta_completa = os.path.join(
            BASE_TRD,
            carpeta
        )

        # =====================================
        # IGNORAR ARCHIVOS
        # =====================================

        if not os.path.isdir(
            ruta_completa
        ):

            continue

        score = calcular_score_trd(
            carpeta,
            tipo_documental,
            dependencia
        )

        # =====================================
        # GUARDAR MEJOR SCORE
        # =====================================

        if score > mejor_score:

            mejor_score = score

            mejor_carpeta = carpeta

    # =====================================
    # SI NO ENCUENTRA
    # =====================================

    if (
        mejor_carpeta is None
        or mejor_score <= 0
    ):

        ruta_otros = os.path.join(
            BASE_TRD,
            "OTROS"
        )

        os.makedirs(
            ruta_otros,
            exist_ok=True
        )

        return ruta_otros

    return os.path.join(
        BASE_TRD,
        mejor_carpeta
    )


# =========================================
# GENERAR NOMBRE DOCUMENTAL
# =========================================

def generar_nombre_documental(
    tipo_documental,
    extension
):

    fecha_actual = datetime.now()

    fecha_texto = fecha_actual.strftime(
        "%Y_%m_%d"
    )

    tipo_documental = limpiar_texto(
        tipo_documental
    )

    carpeta_destino = buscar_serie_trd(
        tipo_documental
    )

    archivos = os.listdir(
        carpeta_destino
    )

    consecutivo = len(
        archivos
    ) + 1

    consecutivo_texto = str(
        consecutivo
    ).zfill(4)

    nombre_final = (

        f"{tipo_documental}_"
        f"{fecha_texto}_"
        f"{consecutivo_texto}."
        f"{extension}"

    )

    return nombre_final


# =========================================
# MOVER DOCUMENTO
# =========================================

def mover_documento(
    ruta_archivo,
    tipo_documental,
    dependencia="GENERAL"
):

    carpeta_destino = buscar_serie_trd(
        tipo_documental,
        dependencia
    )

    # =====================================
    # EXTENSIÓN
    # =====================================

    extension = ruta_archivo.split(
        "."
    )[-1]

    # =====================================
    # NUEVO NOMBRE
    # =====================================

    nuevo_nombre = generar_nombre_documental(
        tipo_documental,
        extension
    )

    destino_final = os.path.join(
        carpeta_destino,
        nuevo_nombre
    )

    shutil.move(
        ruta_archivo,
        destino_final
    )

    return destino_final


# =========================================
# MOSTRAR TRD
# =========================================

def mostrar_trd():

    carpetas = crear_carpetas_trd()

    print("\n===== CARPETAS TRD =====\n")

    for carpeta in carpetas:

        print(f"✅ {carpeta}")

    print("\n===== TOTAL =====\n")

    print(len(carpetas))


# =========================================
# EJECUCIÓN DIRECTA
# =========================================

if __name__ == "__main__":

    mostrar_trd()