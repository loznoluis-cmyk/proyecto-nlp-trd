
import re
import spacy

# =========================
# CARGAR MODELO NLP
# =========================

nlp = spacy.load("es_core_news_sm")

# =========================
# LIMPIEZA DE TEXTO
# =========================

def limpiar_texto(texto):

    # Convertir a minúsculas
    texto = texto.lower()

    # Eliminar caracteres especiales
    texto = re.sub(r'[^a-záéíóúñ\s]', '', texto)

    return texto

# =========================
# TOKENIZACIÓN + STOPWORDS
# =========================

def procesar_texto(texto):

    doc = nlp(texto)

    tokens = []

    for token in doc:

        # Ignorar stopwords y puntuación
        if not token.is_stop and not token.is_punct:

            tokens.append(token.text)

    return " ".join(tokens)