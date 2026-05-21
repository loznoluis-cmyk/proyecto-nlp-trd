# ==========================================
# IMPORTACIONES
# ==========================================

import PyPDF2
import docx

# ==========================================
# LEER PDF
# ==========================================

def leer_pdf(archivo):

    texto = ""

    lector = PyPDF2.PdfReader(
        archivo
    )

    for pagina in lector.pages:

        contenido = pagina.extract_text()

        if contenido:

            texto += contenido

    return texto

# ==========================================
# LEER DOCX
# ==========================================

def leer_docx(archivo):

    documento = docx.Document(
        archivo
    )

    texto = ""

    for parrafo in documento.paragraphs:

        texto += parrafo.text + "\n"

    return texto