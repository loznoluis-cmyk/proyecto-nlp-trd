import pandas as pd

from preprocess import (
    limpiar_texto,
    procesar_texto
)

from train import (
    entrenar_modelo
)

from predict import (
    predecir_categoria
)

# =========================
# CARGAR DATASET
# =========================

df = pd.read_csv(
    "data/dataset.csv"
)

# =========================
# LIMPIEZA NLP
# =========================

df["texto_limpio"] = df["texto"].apply(
    limpiar_texto
)

# =========================
# PROCESAMIENTO NLP
# =========================

df["texto_procesado"] = df[
    "texto_limpio"
].apply(
    procesar_texto
)

# =========================
# ENTRENAR MODELO
# =========================

modelo, vectorizador, encoder = (
    entrenar_modelo(df)
)

# =========================
# NUEVO TEXTO
# =========================

nuevo_documento = (
    "solicitud de certificado académico"
)

# =========================
# PREDICCIÓN
# =========================

categoria = predecir_categoria(
    nuevo_documento,
    modelo,
    vectorizador,
    encoder
)

# =========================
# RESULTADO FINAL
# =========================

print(
    "\\nCATEGORÍA PREDICHA:\\n"
)

print(categoria)