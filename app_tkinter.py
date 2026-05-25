import tkinter as tk

from tkinter import filedialog

from PIL import Image, ImageTk

from predict_gender import predict_gender
from predict_fracture import predict_fracture

# ==========================================
# VENTANA PRINCIPAL
# ==========================================

root = tk.Tk()

root.title("Programa de estudio de huesos")

root.geometry("1100x700")

root.configure(bg="#d9d9d9")

# ==========================================
# BARRA SUPERIOR
# ==========================================

top_bar = tk.Frame(
    root,
    bg="#67c7e3",
    height=90
)

top_bar.pack(fill="x")

title = tk.Label(
    top_bar,
    text="Programa de estudio de huesos",
    font=("Arial", 28, "bold"),
    bg="#67c7e3",
    fg="black"
)

title.place(x=20, y=20)

# ==========================================
# CONTENEDOR PRINCIPAL
# ==========================================

main_container = tk.Frame(
    root,
    bg="#efefef"
)

main_container.pack(
    padx=30,
    pady=25,
    fill="both",
    expand=True
)

# ==========================================
# PANEL IZQUIERDO
# ==========================================

left_panel = tk.Frame(
    main_container,
    bg="#b7dceb",
    width=450,
    height=600
)

left_panel.pack(side="left", padx=15, pady=15)

left_panel.pack_propagate(False)

# Imagen
image_label = tk.Label(
    left_panel,
    bg="#b7dceb"
)

image_label.pack(pady=30)

# ==========================================
# PANEL DERECHO
# ==========================================

right_panel = tk.Frame(
    main_container,
    bg="#8bd0e8",
    width=500,
    height=600
)

right_panel.pack(side="right", padx=15, pady=15)

right_panel.pack_propagate(False)

# ==========================================
# CAJA RESULTADO SUPERIOR
# ==========================================

gender_box = tk.Frame(
    right_panel,
    bg="#76c5df",
    width=450,
    height=180
)

gender_box.pack(pady=25)

gender_box.pack_propagate(False)

gender_title = tk.Label(
    gender_box,
    text="Clasificación de sexo biológico",
    font=("Arial", 18, "bold"),
    bg="#76c5df",
    fg="black"
)

gender_title.pack(pady=20)

gender_label = tk.Label(
    gender_box,
    text="---",
    font=("Arial", 22),
    bg="#76c5df",
    fg="#003366"
)

gender_label.pack()

# ==========================================
# CAJA RESULTADO INFERIOR
# ==========================================

fracture_box = tk.Frame(
    right_panel,
    bg="#76c5df",
    width=450,
    height=180
)

fracture_box.pack(pady=20)

fracture_box.pack_propagate(False)

fracture_title = tk.Label(
    fracture_box,
    text="Estado del hueso",
    font=("Arial", 18, "bold"),
    bg="#76c5df",
    fg="black"
)

fracture_title.pack(pady=20)

fracture_label = tk.Label(
    fracture_box,
    text="---",
    font=("Arial", 22),
    bg="#76c5df",
    fg="#003366"
)

fracture_label.pack()

# ==========================================
# FUNCIÓN SUBIR IMAGEN
# ==========================================

def upload_image():

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )

    if file_path:

        # Abrir imagen
        image = Image.open(file_path)

        image = image.resize((350,350))

        photo = ImageTk.PhotoImage(image)

        # Mostrar imagen
        image_label.config(image=photo)

        image_label.image = photo

        # ==========================================
        # PREDICCIONES
        # ==========================================

        gender_result = predict_gender(file_path)

        fracture_result = predict_fracture(file_path)

        # ==========================================
        # MOSTRAR RESULTADOS
        # ==========================================

        gender_label.config(
            text=f"{gender_result}"
        )

        fracture_label.config(
            text=f"{fracture_result}"
        )

# ==========================================
# BOTÓN SUBIR IMAGEN
# ==========================================

upload_button = tk.Button(
    left_panel,
    text="Seleccionar imagen",
    command=upload_image,
    font=("Arial", 14),
    bg="#4d8fd1",
    fg="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)

upload_button.pack(side="bottom", pady=25)

# ==========================================
# EJECUTAR
# ==========================================

root.mainloop()