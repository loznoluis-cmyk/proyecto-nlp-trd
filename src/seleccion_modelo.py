
# ==========================================
# IMPORTACIONES
# ==========================================

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.svm import SVC

from sklearn.metrics import accuracy_score

# ==========================================
# ENTRENAR Y SELECCIONAR
# ==========================================

def seleccionar_mejor_modelo(

    x_train,
    x_test,

    y_train,
    y_test

):

    # ==========================================
    # MODELOS
    # ==========================================

    modelos = {

        "Logistic Regression": LogisticRegression(),

        "Random Forest": RandomForestClassifier(),

        "SVM": SVC(
            probability=True
        )

    }

    # ==========================================
    # VARIABLES
    # ==========================================

    mejor_modelo = None

    mejor_accuracy = 0

    nombre_mejor = ""

    resultados = []

    # ==========================================
    # ITERAR MODELOS
    # ==========================================

    for nombre, modelo in modelos.items():

        # ==========================================
        # ENTRENAR
        # ==========================================

        modelo.fit(

            x_train,

            y_train

        )

        # ==========================================
        # PREDECIR
        # ==========================================

        y_pred = modelo.predict(
            x_test
        )

        # ==========================================
        # ACCURACY
        # ==========================================

        accuracy = accuracy_score(

            y_test,

            y_pred

        )

        # ==========================================
        # GUARDAR RESULTADO
        # ==========================================

        resultados.append({

            "modelo": nombre,

            "accuracy": accuracy

        })

        # ==========================================
        # VALIDAR MEJOR
        # ==========================================

        if accuracy > mejor_accuracy:

            mejor_accuracy = accuracy

            mejor_modelo = modelo

            nombre_mejor = nombre

    # ==========================================
    # RETORNAR
    # ==========================================

    return (

        mejor_modelo,

        nombre_mejor,

        mejor_accuracy,

        resultados

    )
