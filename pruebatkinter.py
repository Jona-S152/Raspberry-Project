import tkinter as tk
import customtkinter
import requests
import datetime

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

ventana = customtkinter.Ctk()
ventana.geometry("800x500")

ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

panel_principal = customtkinter.Frame(ventana)
panel_principal.grid(row=0, column=0, sticky="nsew")

panel_principal.columnconfigure(0, weight=1)
panel_principal.rowconfigure(0, weight=1)

# Crear un panel secundario (Frame) dentro del panel principal
panel_secundario = customtkinter.Frame(panel_principal)
panel_secundario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 

# Configurar el peso de las columnas y filas
panel_secundario.columnconfigure(0, weight=1)
panel_secundario.rowconfigure(0, weight=1)

#LISTAR TODOS LOS PRODUCTOS
#class Producto:
#    def __init__(self, id, state, create_date, modified_date, delete_date, name, image, description, category, price, stock):
#        self.id = id
#        self.state = state
#        self.create_date = create_date
#        self.modified_date = modified_date
#        self.delete_date = delete_date
#        self.name = name
#        self.image = image
#        self.description = description
#        self.category = category
#        self.price = float(price)  # Convertir el precio a float
#        self.stock = int(stock)    # Convertir el stock a entero
#
#def deserialize_and_create_objects(data):
#    productos = []
#    for item in data:
#        producto = Producto(
#            item['id'],
#            item['state'],
#            item['create_date'],
#            item['modified_date'],
#            item['delete_date'],
#            item['name'],
#            item['image'],
#            item['description'],
#            item['category'],
#            item['price'],
#            item['stock']
#        )
#        productos.append(producto)
#    return productos
#
#res = requests.get('http://127.0.0.1:8000/tecsu/products/')
#
#resultado = res.json()
#
#productosResultado = deserialize_and_create_objects(resultado)

# Crear una lista de datos para los widgets
productosResultado = [
    "Widget 1", "Widget 2", "Widget 3", "Widget 4", "Widget 5",
    "Widget 6", "Widget 7", "Widget 8", "Widget 9", "Widget 10",
    "Widget 11", "Widget 12", "Widget 13", "Widget 14", "Widget 15"
]

# Establecer el número de columnas antes de pasar a la siguiente fila
columnas_por_fila = 5

# Colocar los widgets en el grid
for i, dato in enumerate(productosResultado):
    # Calcular la fila y la columna para cada widget
    fila = i // columnas_por_fila
    columna = i % columnas_por_fila

    panel_terciario = customtkinter.Frame(panel_secundario)
    panel_terciario.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew") 

    panel_terciario.columnconfigure(0, weight=1)
    panel_terciario.rowconfigure(0, weight=1)

    # Crear el widget y configurar el grid
    label = customtkinter.Label(panel_terciario, text=dato, width=15, height=2)
    label.place(rely=0.5, relx=0.5, anchor=tkinter.CENTER)

    label.columnconfigure(0, weight=1)
    label.rowconfigure(0, weight=1)

# Configurar el peso de las columnas y filas
for i in range(columnas_por_fila):
    panel_terciario.grid_columnconfigure(i, weight=1)

for i in range(len(productosResultado) // columnas_por_fila + 1):
    panel_terciario.grid_rowconfigure(i, weight=1)

ventana.mainloop()