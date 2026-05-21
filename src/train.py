
import pickle

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    LabelEncoder
)

from sklearn.metrics import (

    classification_report,

    confusion_matrix,

    accuracy_score,

    precision_score,

    recall_score,

    f1_score

)

# ==========================================
# IMPORT LOCAL
# ==========================================

from seleccion_modelo import (
    seleccionar_mejor_modelo
)

# ==========================================
# ENTRENAMIENTO DEL MODELO
# ==========================================

def entrenar_modelo(df):

    # ==========================================
    # TF-IDF
    # ==========================================

    vectorizador = TfidfVectorizer()

    X = vectorizador.fit_transform(
        df["texto_procesado"]
    )

    # ==========================================
    # VARIABLE OBJETIVO
    # ==========================================

    y = df["categoria"]

    # ==========================================
    # CODIFICAR ETIQUETAS
    # ==========================================

    encoder = LabelEncoder()

    y_encoded = encoder.fit_transform(
        y
    )

    # ==========================================
    # DIVISIÓN DE DATOS
    # ==========================================

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y_encoded,

        test_size=0.2,

        random_state=42

    )

    # ==========================================
    # SELECCIÓN AUTOMÁTICA
    # ==========================================

    (
        modelo,
        nombre_modelo,
        accuracy_modelo,
        resultados_modelos

    ) = seleccionar_mejor_modelo(

        X_train,
        X_test,

        y_train,
        y_test

    )

    # ==========================================
    # MOSTRAR MEJOR MODELO
    # ==========================================

    print(
        "\n===================================="
    )

    print(
        "🏆 MEJOR MODELO SELECCIONADO"
    )

    print(
        "====================================\n"
    )

    print(
        f"Modelo: {nombre_modelo}"
    )

    print(
        f"Accuracy: {accuracy_modelo:.4f}\n"
    )

    # ==========================================
    # PREDICCIONES
    # ==========================================

    y_pred = modelo.predict(
        X_test
    )

    # ==========================================
    # MÉTRICAS
    # ==========================================

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted"
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted"
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted"
    )

    # ==========================================
    # REPORTE
    # ==========================================

    print(
        "\n===================================="
    )

    print(
        "📊 REPORTE DE CLASIFICACIÓN"
    )

    print(
        "====================================\n"
    )

    print(

        classification_report(
            y_test,
            y_pred
        )

    )

    # ==========================================
    # MATRIZ CONFUSIÓN
    # ==========================================

    matriz = confusion_matrix(

        y_test,

        y_pred

    )

    # ==========================================
    # GRAFICAR MATRIZ
    # ==========================================

    plt.figure(
        figsize=(8, 5)
    )

    sns.heatmap(

        matriz,

        annot=True,

        fmt='d',

        cmap='Blues'

    )

    plt.title(
        f'Matriz de Confusión - {nombre_modelo}'
    )

    plt.xlabel(
        'Predicción'
    )

    plt.ylabel(
        'Valor Real'
    )

    # ==========================================
    # GUARDAR MATRIZ
    # ==========================================

    plt.savefig(
        "reports/matriz_confusion.png"
    )

    plt.close()

    # ==========================================
    # RESULTADOS MODELOS
    # ==========================================

    df_resultados = pd.DataFrame(
        resultados_modelos
    )

    df_resultados.to_csv(

        "reports/metricas/resultados_modelos.csv",

        index=False

    )

    # ==========================================
    # GUARDAR MODELO
    # ==========================================

    with open(

        "models/modelo_nlp.pkl",

        "wb"

    ) as archivo_modelo:

        pickle.dump(

            modelo,

            archivo_modelo

        )

    # ==========================================
    # GUARDAR VECTORIZADOR
    # ==========================================

    with open(

        "models/vectorizador.pkl",

        "wb"

    ) as archivo_vectorizador:

        pickle.dump(

            vectorizador,

            archivo_vectorizador

        )

    # ==========================================
    # GUARDAR ENCODER
    # ==========================================

    with open(

        "models/encoder.pkl",

        "wb"

    ) as archivo_encoder:

        pickle.dump(

            encoder,

            archivo_encoder

        )

    # ==========================================
    # RESUMEN FINAL
    # ==========================================

    print(
        "\n===================================="
    )

    print(
        "✅ MODELOS GUARDADOS"
    )

    print(
        "====================================\n"
    )

    print(
        "📁 models/modelo_nlp.pkl"
    )

    print(
        "📁 models/vectorizador.pkl"
    )

    print(
        "📁 models/encoder.pkl"
    )

    print(
        "\n📊 MATRIZ:"
    )

    print(
        "reports/matriz_confusion.png"
    )

    print(
        "\n📈 MÉTRICAS:"
    )

    print(
        "reports/metricas/resultados_modelos.csv\n"
    )

    # ==========================================
    # RETORNAR
    # ==========================================

    return (

        modelo,

        vectorizador,

        encoder

    )