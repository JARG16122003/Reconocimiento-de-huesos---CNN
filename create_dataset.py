import os
import shutil
import pandas as pd

# Leer CSV
df = pd.read_csv(
    r"C:\Users\crist\Downloads\costillas\train_gender.csv"
)

ruta = r"C:\Users\crist\Downloads\costillas\kaggle\kaggle\train"
print(os.path.exists(ruta))
print(os.listdir(ruta)[:10])


# Crear carpetas
os.makedirs(r"C:\Users\crist\Desktop\dataset\male", exist_ok=True)
os.makedirs(r"C:\Users\crist\Desktop\dataset\female", exist_ok=True)

for _, row in df.iterrows():

    # Nombre imagen
    filename = f"{int(row['imageId']):06d}.png"

    # Ruta origen
    src = (
        r"C:\Users\crist\Downloads\costillas\kaggle\kaggle\train"
        rf"\{filename}"
    )

    # Destino
    if row['gender'] == 1:
        dst = rf"C:\Users\crist\Desktop\dataset\male\{filename}"
    else:
        dst = rf"C:\Users\crist\Desktop\dataset\female\{filename}"

    # Mover
    if os.path.exists(src):
        shutil.move(src, dst)
    else:
        print(f"No existe: {src}")

print("Dataset organizado.")