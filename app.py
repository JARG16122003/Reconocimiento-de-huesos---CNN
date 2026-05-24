import streamlit as st

from PIL import Image

from predict_gender import predict_gender
from predict_fracture import predict_fracture

# Título
st.title("Sistema Inteligente de Análisis Óseo")

st.write(
    "Sube una radiografía para analizar:"
)

st.write("- Sexo biológico")
st.write("- Estado del hueso (fractura o sano)")

# Upload
uploaded_file = st.file_uploader(
    "Selecciona una radiografía",
    type=["png","jpg","jpeg"]
)

# Si sube imagen
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    # Mostrar imagen
    st.image(
        image,
        caption="Radiografía subida",
        use_container_width=True
    )

    # Guardar temporalmente
    temp_path = "temp_image.png"

    image.save(temp_path)

    # Predicción género
    gender_result = predict_gender(temp_path)

    # Predicción fractura
    fracture_result = predict_fracture(temp_path)

    # Mostrar resultados
    st.success(
        f"Sexo biológico: {gender_result}"
    )

    st.warning(
        f"Estado del hueso: {fracture_result}"
    )