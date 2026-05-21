
# ==========================================
# IMPORTAR LIBRERÍAS
# ==========================================

import pandas as pd

from preprocess import (
    limpiar_texto,
    procesar_texto
)

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# MODELOS

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.svm import LinearSVC


# ==========================================
# CARGAR DATASET
# ==========================================

df = pd.read_csv(
    "data/dataset.csv"
)

print("\nDATASET CARGADO\n")


# ==========================================
# LIMPIEZA
# ==========================================

df["texto_limpio"] = df["texto"].apply(
    limpiar_texto
)


# ==========================================
# NLP
# ==========================================

df["texto_procesado"] = df["texto_limpio"].apply(
    procesar_texto
)


# ==========================================
# TF-IDF
# ==========================================

vectorizador = TfidfVectorizer()

X = vectorizador.fit_transform(
    df["texto_procesado"]
)


# ==========================================
# CODIFICAR CATEGORÍAS
# ==========================================

encoder = LabelEncoder()

y = encoder.fit_transform(
    df["categoria"]
)


# ==========================================
# DIVISIÓN TRAIN TEST
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==========================================
# MODELOS
# ==========================================

modelos = {

    "Logistic Regression": LogisticRegression(),

    "Random Forest": RandomForestClassifier(),

    "SVM": LinearSVC()

}


# ==========================================
# LISTA RESULTADOS
# ==========================================

resultados = []


# ==========================================
# COMPARAR MODELOS
# ==========================================

for nombre, modelo in modelos.items():

    print("\n===================================")
    print(f"MODELO: {nombre}")
    print("===================================\n")

    # ENTRENAR

    modelo.fit(
        X_train,
        y_train
    )

    # PREDECIR

    y_pred = modelo.predict(
        X_test
    )

    # MÉTRICAS

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

    # MOSTRAR RESULTADOS

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-Score : {f1:.4f}\n")

    print(
        classification_report(
            y_test,
            y_pred
        )
    )

    # GUARDAR RESULTADOS

    resultados.append({

        "Modelo": nombre,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1

    })


# ==========================================
# DATAFRAME RESULTADOS
# ==========================================

df_resultados = pd.DataFrame(
    resultados
)


# ==========================================
# GUARDAR CSV
# ==========================================

df_resultados.to_csv(

    "reports/metricas/resultados_modelos.csv",

    index=False

)


# ==========================================
# MOSTRAR TABLA FINAL
# ==========================================

print("\n===================================")
print("TABLA FINAL RESULTADOS")
print("===================================\n")

print(df_resultados)


# ==========================================
# MENSAJE FINAL
# ==========================================

print(
    "\nRESULTADOS GUARDADOS EN reports/metricas/\n"
)