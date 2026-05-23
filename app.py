import streamlit as st

import torch
import torch.nn as nn

from torchvision import transforms
from PIL import Image

# Dispositivo
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# Arquitectura CNN
class CNN(nn.Module):

    def __init__(self):

        super().__init__()

        self.conv = nn.Sequential(

            nn.Conv2d(3,32,3,padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2,2),

            nn.Conv2d(32,64,3,padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2,2),

            nn.Conv2d(64,128,3,padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.fc = nn.Sequential(

            nn.Flatten(),

            nn.Linear(128*28*28,256),
            nn.ReLU(),

            nn.Dropout(0.5),

            nn.Linear(256,2)
        )

    def forward(self, x):

        x = self.conv(x)

        x = self.fc(x)

        return x

# Crear modelo
model = CNN().to(device)

# Cargar pesos
model.load_state_dict(
    torch.load(
        "models/genderModelcnn.pth",
        map_location=device
    )
)

model.eval()

# Transformaciones
transform = transforms.Compose([

    transforms.Resize((224,224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.5,0.5,0.5],
        std=[0.5,0.5,0.5]
    )
])

# Clases
classes = ['femenino', 'masculino']

# Interfaz
st.title("anatomia ósea")

st.write(
    "Sube una radiografía para dar diferentes características."
)

uploaded_file = st.file_uploader(
    "Selecciona una imagen",
    type=["png","jpg","jpeg"]
)

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.image(
        image,
        caption="Radiografía subida",
        use_container_width=True
    )

    # Transformar
    img = transform(image)

    img = img.unsqueeze(0).to(device)

    # Predicción
    with torch.no_grad():

        outputs = model(img)

        _, predicted = torch.max(outputs,1)

    result = classes[predicted.item()]

    st.success(
        f"Predicción: {result}"
    )