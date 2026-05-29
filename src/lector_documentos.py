import fitz
import docx
import pytesseract

from PIL import Image


# ==========================================
# LEER PDF
# ==========================================

def leer_pdf(ruta_pdf):

    try:

        texto = ""

        pdf = fitz.open(
            ruta_pdf
        )

        for pagina in pdf:

            texto += pagina.get_text()

        pdf.close()

        # ======================================
        # SI EL PDF NO TIENE TEXTO
        # ======================================

        if texto.strip() == "":

            texto = ocr_pdf(
                ruta_pdf
            )

        return texto

    except Exception as e:

        return f"ERROR PDF: {e}"


# ==========================================
# OCR PDF ESCANEADO
# ==========================================

def ocr_pdf(ruta_pdf):

    try:

        texto = ""

        pdf = fitz.open(
            ruta_pdf
        )

        for pagina in pdf:

            pix = pagina.get_pixmap()

            imagen = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            texto += pytesseract.image_to_string(
                imagen,
                lang="spa"
            )

        pdf.close()

        return texto

    except Exception as e:

        return f"ERROR OCR PDF: {e}"


# ==========================================
# LEER WORD
# ==========================================

def leer_docx(ruta_docx):

    try:

        documento = docx.Document(
            ruta_docx
        )

        texto = ""

        for parrafo in documento.paragraphs:

            texto += (
                parrafo.text + "\n"
            )

        return texto

    except Exception as e:

        return f"ERROR DOCX: {e}"


# ==========================================
# LEER IMAGEN
# ==========================================

def leer_imagen(ruta_imagen):

    try:

        imagen = Image.open(
            ruta_imagen
        )

        texto = pytesseract.image_to_string(
            imagen,
            lang="spa"
        )

        return texto

    except Exception as e:

        return f"ERROR OCR IMAGEN: {e}"