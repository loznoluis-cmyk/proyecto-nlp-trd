import re
import spacy


# =========================================
# CARGAR MODELO NLP
# =========================================

nlp = spacy.load(
    "es_core_news_sm"
)


# =========================================
# PALABRAS VACÍAS PERSONALIZADAS
# =========================================

PALABRAS_INVALIDAS = [

    "pdf",
    "docx",
    "electrónico",
    "electronico",
    "papel",
    "archivo",
    "documento",
    "adjunto",
    "señor",
    "señora",
    "doctor",
    "doctora",
    "universidad",
    "gestión",
    "gestion",
    "institucional",
    "administrativo",
    "académica",
    "academica"

]


# =========================================
# LIMPIAR TEXTO
# =========================================

def limpiar_texto(texto):

    # =====================================
    # VALIDAR
    # =====================================

    if texto is None:

        return ""

    texto = str(texto)

    # =====================================
    # MINÚSCULAS
    # =====================================

    texto = texto.lower()

    # =====================================
    # ELIMINAR URLS
    # =====================================

    texto = re.sub(
        r"http\S+",
        " ",
        texto
    )

    # =====================================
    # ELIMINAR EMAILS
    # =====================================

    texto = re.sub(
        r"\S+@\S+",
        " ",
        texto
    )

    # =====================================
    # ELIMINAR CARACTERES ESPECIALES
    # =====================================

    texto = re.sub(
        r"[^a-záéíóúñ0-9\s\-]",
        " ",
        texto
    )

    # =====================================
    # ELIMINAR ESPACIOS DOBLES
    # =====================================

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    texto = texto.strip()

    return texto


# =========================================
# NLP PRINCIPAL
# =========================================

def procesar_texto(texto):

    # =====================================
    # LIMPIEZA
    # =====================================

    texto = limpiar_texto(
        texto
    )

    # =====================================
    # NLP
    # =====================================

    doc = nlp(texto)

    tokens = []

    for token in doc:

        palabra = token.text.strip()

        # =====================================
        # VALIDAR LONGITUD
        # =====================================

        if len(palabra) < 3:

            continue

        # =====================================
        # IGNORAR STOPWORDS
        # =====================================

        if token.is_stop:

            continue

        # =====================================
        # IGNORAR PUNTUACIÓN
        # =====================================

        if token.is_punct:

            continue

        # =====================================
        # IGNORAR ESPACIOS
        # =====================================

        if token.is_space:

            continue

        # =====================================
        # IGNORAR PALABRAS PERSONALIZADAS
        # =====================================

        if palabra in PALABRAS_INVALIDAS:

            continue

        # =====================================
        # LEMATIZAR
        # =====================================

        lema = token.lemma_

        lema = lema.lower().strip()

        # =====================================
        # VALIDAR LEMA
        # =====================================

        if len(lema) < 3:

            continue

        if lema in PALABRAS_INVALIDAS:

            continue

        # =====================================
        # AGREGAR TOKEN
        # =====================================

        tokens.append(
            lema
        )

    # =====================================
    # ELIMINAR DUPLICADOS
    # =====================================

    tokens = list(
        dict.fromkeys(tokens)
    )

    # =====================================
    # TEXTO FINAL
    # =====================================

    texto_final = " ".join(
        tokens
    )

    return texto_final


# =========================================
# EXTRAER PALABRAS CLAVE
# =========================================

def extraer_palabras_clave(
    texto,
    limite=10
):

    texto = procesar_texto(
        texto
    )

    palabras = texto.split()

    return palabras[:limite]


# =========================================
# DETECTAR POSIBLE SERIE TRD
# =========================================

def detectar_tipo_documental(texto):

    texto = procesar_texto(
        texto
    )

    # =====================================
    # REGLAS DOCUMENTALES
    # =====================================

    reglas = {

        "ACTA": [
            "acta",
            "comité",
            "reunión",
            "sesión"
        ],

        "RESOLUCIÓN": [
            "resolución",
            "fallo",
            "sanción"
        ],

        "CONVOCATORIA": [
            "convocatoria",
            "inscripción",
            "aspirante"
        ],

        "INFORME": [
            "informe",
            "resultado",
            "seguimiento"
        ],

        "DERECHO DE PETICIÓN": [
            "petición",
            "solicitud",
            "respuesta"
        ]

    }

    # =====================================
    # BUSCAR COINCIDENCIA
    # =====================================

    for tipo, palabras in reglas.items():

        for palabra in palabras:

            if palabra in texto:

                return tipo

    return "DOCUMENTO GENERAL"


# ==========================================
# DETECTAR DEPENDENCIA
# ==========================================

def detectar_dependencia(texto):

    texto = texto.upper()

    dependencias = {

        "RECTORIA": [

            "RECTORIA",
            "RECTOR"
        ],

        "VICERRECTORIA": [

            "VICERRECTORIA",
            "VICERRECTOR"
        ],

        "JURIDICA": [

            "JURIDICA",
            "ABOGADO",
            "LEGAL",
            "FALLO",
            "SANCION"
        ],

        "TALENTO HUMANO": [

            "NOMBRAMIENTO",
            "CONTRATACION",
            "FUNCIONARIO",
            "EMPLEADO"
        ],

        "ARCHIVO": [

            "TRD",
            "RETENCION",
            "ARCHIVO",
            "DOCUMENTAL"
        ],

        "FINANCIERA": [

            "PAGO",
            "FACTURA",
            "PRESUPUESTO",
            "CONTABILIDAD"
        ],

        "ACADEMICA": [

            "ESTUDIANTE",
            "MATRICULA",
            "DOCENTE",
            "ACADEMICO"
        ]
    }

    for dependencia, palabras in dependencias.items():

        for palabra in palabras:

            if palabra in texto:

                return dependencia

    return "GENERAL"


# ==========================================
# EXTRAER CONSECUTIVO DOCUMENTAL
# ==========================================

def extraer_consecutivo(texto):

    try:

        texto = str(texto)

        texto = texto.upper()

        # =====================================
        # NORMALIZAR GUIONES
        # =====================================

        texto = texto.replace(
            "–",
            "-"
        )

        texto = texto.replace(
            "—",
            "-"
        )

        # =====================================
        # PATRONES
        # =====================================

        patrones = [

            # VA-121
            r"[A-Z]{1,10}\s*-\s*\d{1,10}",

            # VA 121
            r"[A-Z]{1,10}\s+\d{1,10}",

            # ABCD-2025
            r"[A-Z]{2,10}-\d{2,10}"

        ]

        for patron in patrones:

            coincidencias = re.findall(
                patron,
                texto
            )

            if len(coincidencias) > 0:

                consecutivo = coincidencias[0]

                # =================================
                # LIMPIAR ESPACIOS
                # =================================

                consecutivo = re.sub(
                    r"\s+",
                    "",
                    consecutivo
                )

                return consecutivo

        return "NO_ENCONTRADO"

    except Exception as e:

        return f"ERROR_CONSECUTIVO: {e}"
    
    # ==========================================
# DETECTOR ESTRUCTURAL DOCUMENTAL
# ==========================================

def detectar_estructura_documental(texto):

    texto = str(texto).upper()

    scores = {

        "ACTA": 0,
        "RESOLUCION": 0,
        "CIRCULAR": 0,
        "INFORME": 0,
        "PETICION": 0

    }

    # ======================================
    # ACTA
    # ======================================

    patrones_acta = [

        "ACTA",
        "ORDEN DEL DIA",
        "ASISTENTES",
        "REUNION",
        "COMITE",
        "DESARROLLO",
        "SIENDO LAS"

    ]

    # ======================================
    # RESOLUCION
    # ======================================

    patrones_resolucion = [

        "RESOLUCION",
        "RESUELVE",
        "CONSIDERANDO",
        "ARTICULO",
        "POR MEDIO DE LA CUAL"

    ]

    # ======================================
    # CIRCULAR
    # ======================================

    patrones_circular = [

        "CIRCULAR",
        "PARA:",
        "DE:",
        "ASUNTO:",
        "CORDIAL SALUDO"

    ]

    # ======================================
    # INFORME
    # ======================================

    patrones_informe = [

        "INFORME",
        "OBJETIVO",
        "RESULTADOS",
        "CONCLUSIONES",
        "RECOMENDACIONES"

    ]

    # ======================================
    # PETICION
    # ======================================

    patrones_peticion = [

        "DERECHO DE PETICION",
        "PETICION",
        "SOLICITO",
        "RESPUESTA",
        "RADICADO"

    ]

    # ======================================
    # CALCULAR SCORES
    # ======================================

    for patron in patrones_acta:

        if patron in texto:

            scores["ACTA"] += 20

    for patron in patrones_resolucion:

        if patron in texto:

            scores["RESOLUCION"] += 20

    for patron in patrones_circular:

        if patron in texto:

            scores["CIRCULAR"] += 20

    for patron in patrones_informe:

        if patron in texto:

            scores["INFORME"] += 20

    for patron in patrones_peticion:

        if patron in texto:

            scores["PETICION"] += 20

    # ======================================
    # OBTENER MEJOR SCORE
    # ======================================

    tipo_detectado = max(
        scores,
        key=scores.get
    )

    score_final = scores[
        tipo_detectado
    ]

    # ======================================
    # VALIDAR CONFIANZA
    # ======================================

    if score_final < 20:

        tipo_detectado = "DOCUMENTO_GENERAL"

    return {

        "tipo_detectado":
        tipo_detectado,

        "score":
        score_final

    }