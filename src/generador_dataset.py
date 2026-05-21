
import pandas as pd
import random

# ==========================================
# CATEGORÍAS Y FRASES
# ==========================================

categorias = {

    "Academico": [

        "solicitud de certificado académico",
        "reporte de notas semestrales",
        "historial académico del estudiante",
        "solicitud de homologación de materias",
        "matrícula académica ordinaria",
        "cancelación de semestre académico",
        "solicitud de paz y salvo",
        "certificado de estudios",
        "registro de calificaciones",
        "acta de grado universitario"

    ],

    "Financiero": [

        "factura de pago institucional",
        "estado financiero trimestral",
        "reporte contable mensual",
        "solicitud de presupuesto anual",
        "comprobante de egreso",
        "balance general financiero",
        "informe de tesorería",
        "control de cartera vencida",
        "reporte de ingresos económicos",
        "orden de pago administrativa"

    ],

    "Administrativo": [

        "memorando administrativo interno",
        "circular administrativa general",
        "acta de comité institucional",
        "solicitud administrativa interna",
        "reporte de gestión administrativa",
        "comunicado organizacional",
        "registro documental interno",
        "control de inventario",
        "plan operativo institucional",
        "acta de reunión administrativa"

    ],

    "Juridico": [

        "contrato de prestación de servicios",
        "demanda administrativa",
        "derecho de petición",
        "acción de tutela",
        "concepto jurídico institucional",
        "proceso disciplinario",
        "resolución jurídica",
        "documento legal contractual",
        "notificación judicial",
        "acuerdo jurídico"

    ],

    "Talento_Humano": [

        "solicitud de vacaciones",
        "incapacidad médica laboral",
        "contrato laboral",
        "evaluación de desempeño",
        "hoja de vida institucional",
        "reporte de nómina",
        "proceso de selección",
        "solicitud de permisos laborales",
        "afiliación de seguridad social",
        "certificación laboral"

    ]
}

# ==========================================
# FUNCIÓN PARA GENERAR VARIACIONES
# ==========================================

def generar_variacion(texto):

    conectores = [

        "urgente",
        "prioritario",
        "interno",
        "externo",
        "institucional",
        "oficial",
        "general",
        "confidencial"

    ]

    complemento = random.choice(conectores)

    estructuras = [

        f"{texto} {complemento}",
        f"{complemento} {texto}",
        f"se requiere {texto}",
        f"solicitud relacionada con {texto}",
        f"proceso correspondiente a {texto}",
        f"documento asociado a {texto}"

    ]

    return random.choice(estructuras)

# ==========================================
# GENERAR DATASET
# ==========================================

datos = []

cantidad_por_categoria = 3000

for categoria, textos in categorias.items():

    for _ in range(cantidad_por_categoria):

        texto_base = random.choice(textos)

        texto_generado = generar_variacion(
            texto_base
        )

        datos.append([

            texto_generado,
            categoria

        ])

# ==========================================
# CREAR DATAFRAME
# ==========================================

df = pd.DataFrame(

    datos,
    columns=[

        "texto",
        "categoria"

    ]

)

# ==========================================
# MEZCLAR DATASET
# ==========================================

df = df.sample(

    frac=1,
    random_state=42

).reset_index(drop=True)

# ==========================================
# GUARDAR CSV
# ==========================================

df.to_csv(

    "data/dataset.csv",
    index=False

)

# ==========================================
# RESULTADO
# ==========================================

print("\nDATASET GENERADO CORRECTAMENTE\n")

print(df.head())

print("\nTOTAL REGISTROS:\n")

print(len(df))
