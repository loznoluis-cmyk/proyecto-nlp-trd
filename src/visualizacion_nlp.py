
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

# ==========================================
# GENERAR WORDCLOUD
# ==========================================

def mostrar_wordcloud(texto):

    # ==========================================
    # VALIDAR TEXTO
    # ==========================================

    if texto.strip() == "":

        return

    # ==========================================
    # WORDCLOUD
    # ==========================================

    nube = WordCloud(

        width=800,

        height=400,

        background_color="white",

        colormap="viridis"

    ).generate(texto)

    # ==========================================
    # GRAFICAR
    # ==========================================

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.imshow(
        nube,
        interpolation="bilinear"
    )

    ax.axis("off")

    # ==========================================
    # MOSTRAR STREAMLIT
    # ==========================================

    st.pyplot(fig)