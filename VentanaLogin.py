#Importaciones
import customtkinter
import os
from PIL import ImageTk, Image
import VentanaOpciones as Vp
from CTkMessagebox import CTkMessagebox

# ---> Rutas
# Carpeta principal del proyecto
carpeta_principal = os.path.dirname(__file__)
# Carpeta de imágenes
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class Login:
    def __init__(self):
        self.root = customtkinter.CTk()  # create CTk window like you do with the Tk window
        self.root.title("Login")
        #self.root.iconbitmap(os.path.join(carpeta_imagenes, "privacidad.png"))
        self.root.geometry("300x420")
        self.root.resizable(False, False)
        self.root.title("Inicio de sesion")

        # Contenido de la ventana principal
        # Logo
        logo = customtkinter.CTkImage(
            light_image = Image.open(os.path.join(carpeta_imagenes, "privacidad.png")),
            dark_image = Image.open(os.path.join(carpeta_imagenes, "privacidad.png")),
            size = (150, 150)
        )

        #Etiqueta para mostrar la imagen
        etiqueta = customtkinter.CTkLabel(master = self.root, image=logo, text = "")
        etiqueta.pack(pady = 20)

        #Campos de texto Usuario
        customtkinter.CTkLabel(self.root, text="Usuario").pack()
        self.usuario = customtkinter.CTkEntry(self.root)
        self.usuario.insert(0, "Ej: 0915668421")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, "end"))
        self.usuario.pack()

        #Campos de texto Contraseña
        customtkinter.CTkLabel(self.root, text="Contraseña").pack(pady=(5, 0))
        self.contrasena = customtkinter.CTkEntry(self.root, show="•")
        self.contrasena.insert(0, "••••••••••")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, "end"))
        self.contrasena.pack()

        def button_login():
            if(self.usuario.get() == "Admin" and self.contrasena.get() == "Admin"):
                if(self, "root"):
                    self.root.destroy()
                Acceso = Vp.VOpciones()
            else:
                def show_error():
                    # Show some positive message with the checkmark icon
                    CTkMessagebox(
                        title="Error", 
                        message="Credenciales incorrectas", icon="cancel")

                show_error()
            

        #Boton de envio
        customtkinter.CTkButton(self.root, text="Iniciar sesion", height=35, command=button_login).pack(pady = 20)

        self.root.mainloop()