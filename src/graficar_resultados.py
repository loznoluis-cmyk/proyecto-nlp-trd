
# ==========================================
# IMPORTAR LIBRERÍAS
# ==========================================

import pandas as pd

import matplotlib.pyplot as plt


# ==========================================
# CARGAR RESULTADOS
# ==========================================

df = pd.read_csv(
    "reports/metricas/resultados_modelos.csv"
)

print("\nRESULTADOS CARGADOS\n")

print(df)


# ==========================================
# CONFIGURAR FIGURA
# ==========================================

plt.figure(
    figsize=(10, 6)
)


# ==========================================
# GRÁFICAS
# ==========================================

plt.plot(
    df["Modelo"],
    df["Accuracy"],
    marker="o",
    label="Accuracy"
)

plt.plot(
    df["Modelo"],
    df["Precision"],
    marker="o",
    label="Precision"
)

plt.plot(
    df["Modelo"],
    df["Recall"],
    marker="o",
    label="Recall"
)

plt.plot(
    df["Modelo"],
    df["F1-Score"],
    marker="o",
    label="F1-Score"
)


# ==========================================
# TÍTULOS
# ==========================================

plt.title(
    "Comparación de Modelos NLP"
)

plt.xlabel(
    "Modelos"
)

plt.ylabel(
    "Valor Métrica"
)


# ==========================================
# GRID Y LEYENDA
# ==========================================

plt.grid(True)

plt.legend()


# ==========================================
# GUARDAR IMAGEN
# ==========================================

plt.savefig(
    "reports/metricas/grafica_modelos.png"
)


# ==========================================
# MOSTRAR
# ==========================================

plt.show()


# ==========================================
# MENSAJE FINAL
# ==========================================

print(
    "\nGRÁFICA GUARDADA EN reports/metricas/\n"
)