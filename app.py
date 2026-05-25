import streamlit as st

from PIL import Image

from predict_gender import predict_gender
from predict_fracture import predict_fracture

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Programa de estudio de huesos",
    layout="wide"
)

# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #d9d9d9;
}

/* HEADER */
.header {
    background-color: #67c7e3;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.header h1 {
    color: black;
    font-size: 40px;
    margin: 0;
}

/* CONTENEDORES */
[data-testid="stVerticalBlock"] > div:has(.custom-box) {
    background-color: #b7dceb;
    padding: 20px;
    border-radius: 15px;
}

/* RESULTADOS */
.result-box {
    background-color: #76c5df;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="header">
    <h1>Programa de estudio de huesos</h1>
</div>
""", unsafe_allow_html=True)

# ==========================================
# COLUMNAS
# ==========================================

left_col, right_col = st.columns(2)

# ==========================================
# PANEL IZQUIERDO
# ==========================================

with left_col:

    st.markdown('<div class="custom-box">', unsafe_allow_html=True)

    st.subheader("Radiografía")

    uploaded_file = st.file_uploader(
        "Selecciona una imagen",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            use_container_width=True
        )

        temp_path = "temp_image.png"

        image.save(temp_path)

        gender_result = predict_gender(temp_path)

        fracture_result = predict_fracture(temp_path)

    else:

        gender_result = "---"

        fracture_result = "---"

        st.info("Sube una radiografía para comenzar")

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PANEL DERECHO
# ==========================================

with right_col:

    st.markdown('<div class="custom-box">', unsafe_allow_html=True)

    # RESULTADO SEXO
    with st.container():

        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.subheader("Clasificación de sexo biológico")

        st.success(gender_result)

        st.markdown('</div>', unsafe_allow_html=True)

    # RESULTADO FRACTURA
    with st.container():

        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.subheader("Estado del hueso")

        st.warning(fracture_result)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)