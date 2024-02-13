import tkinter
import customtkinter
import VentanaOpciones as Vo 
import EstudiantesApi as Ea 
from CTkMessagebox import CTkMessagebox

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class VTarjeta():
    def __init__(self):
        self.ventana = customtkinter.CTk()
        self.ventana.geometry("800x475")
        self.ventana.resizable(False, False)
        self.ventana.title("Validación de tarjeta")

        customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        #Configuración panel del titulo o filtro
        self.panelTitulo = customtkinter.CTkFrame(self.ventana, corner_radius=10)
        self.panelTitulo.grid(row=0, column=0, padx=(8, 0), pady=(10, 5))
        #Label del titulo
        self.titulo = customtkinter.CTkLabel(master = self.panelTitulo, text="VALIDAR", height=75, width=785).pack()

        self.panelPrincipal = customtkinter.CTkFrame(master = self.ventana, height=330, width=785)
        self.panelPrincipal.grid(row=1, column=0, padx=(15, 5), pady=(5, 10))

        self.panelDatos = customtkinter.CTkFrame(master = self.panelPrincipal, height=330, width=785)
        self.panelDatos.grid(row=0, column=0, padx=10, pady=(10, 5))

        #Campos de texto Cod_estudiante
        self.lblCod_estudiante = customtkinter.CTkLabel(self.panelDatos, text="Código de estudiante")
        self.lblCod_estudiante.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.cod_estudiante = customtkinter.CTkEntry(self.panelDatos, height=35)
        self.cod_estudiante.insert(0, "Ej: 4864884251")
        self.cod_estudiante.bind("<Button-1>", lambda e: self.cod_estudiante.delete(0, "end"))
        self.cod_estudiante.grid(row=1, column=0, padx=10, pady=(5, 10))

        clsEstudiante = Ea.Student()

        self.estudiante = None

        self.UID = None

        def buscar(value):#Agregar parametro para obtener el estudiante por su id
            self.estudiante = clsEstudiante.getStudentByCod(value)

            self.cod_estudiante.configure(state=customtkinter.DISABLED)

            if(self.estudiante != None):
                self.ventanaDatos = tkinter.Toplevel()
                self.ventanaDatos.geometry("500x250")
                self.ventanaDatos.resizable(False, False)
                self.ventanaDatos.title("Validación de Estudiante")

                customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
                customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

                self.panelDatosEstudiante = customtkinter.CTkFrame(self.ventanaDatos)
                self.panelDatosEstudiante.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            
                self.lblDatos = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Datos del estudiante")
                self.lblDatos.grid(row=0, column=0, padx=10, pady=(10, 0))

                self.lblNombre = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Nombre:")
                self.lblNombre.grid(row=1, column=0, padx=10, pady=(10, 5))

                self.lblNombreVar = customtkinter.CTkLabel(self.panelDatosEstudiante, text=self.estudiante.name)
                self.lblNombreVar.grid(row=1, column=1, padx=10, pady=(10, 5))

                self.lblApellido = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Apellido:")
                self.lblApellido.grid(row=2, column=0, padx=10, pady=(5, 5))

                self.lblApellidoVar = customtkinter.CTkLabel(self.panelDatosEstudiante, text=self.estudiante.last_name)
                self.lblApellidoVar.grid(row=2, column=1, padx=10, pady=(5, 5))

                self.lblSaldo = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Saldo disponible:")
                self.lblSaldo.grid(row=3, column=0, padx=10, pady=(5, 5))

                self.lblSaldoVar = customtkinter.CTkLabel(self.panelDatosEstudiante, text=f"${self.estudiante.balance}")
                self.lblSaldoVar.grid(row=3, column=1, padx=10, pady=(5, 5)) 

                self.botonBuscar.configure(state=customtkinter.DISABLED)

                def ok():
                    if(self, "ventanaDatos"):
                        self.ventanaDatos.destroy()

                self.botonConfirmarUID = customtkinter.CTkButton(self.panelDatosEstudiante, text="Aceptar", height=35, command=ok)
                self.botonConfirmarUID.grid(row=4, column=1, padx=(10, 5), pady=(5, 10))
            else:
                def show_warning():
                    msg = CTkMessagebox(
                        title="Advertencia!",
                        message="Estudiante no encontrado",
                        icon="warning",
                        option_1="Aceptar")

                show_warning()

        #self.codigo = self.cod_estudiante.get()

        self.botonBuscar = customtkinter.CTkButton(
            self.panelDatos, 
            text="buscar", 
            height=35, 
            command= lambda : buscar(self.cod_estudiante.get()))
        self.botonBuscar.grid(row=1, column=1, padx=10, pady=(5, 10))

        

        def getUID():
            if self.estudiante != None:
                self.ventanaConfirmarUID = tkinter.Toplevel()
                self.ventanaConfirmarUID.geometry("500x250")
                self.ventanaConfirmarUID.resizable(False, False)

                customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
                customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

                self.panelPrincipalUID = customtkinter.CTkFrame(master = self.ventanaConfirmarUID)
                self.panelPrincipalUID.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                self.panelTituloUID = customtkinter.CTkFrame(master = self.panelPrincipalUID)
                self.panelTituloUID.grid(row=0, column=0, padx=10, pady=(10, 5))

                self.lblTitulo = customtkinter.CTkLabel(master = self.panelTituloUID, text="Por favor, coloque su tarjeta en el lector", height=40, width=300)
                self.lblTitulo.grid(row=0, column=0, padx=0, pady=0)

                self.panelCodigoUID = customtkinter.CTkFrame(master = self.panelPrincipalUID)
                self.panelCodigoUID.grid(row=1, column=0, padx=10, pady=(5, 10))

                self.lblUID = customtkinter.CTkLabel(master = self.panelCodigoUID, text="Esperando codigo...", height=150, width=300)
                self.lblUID.grid(row=0, column=0, padx=0, pady=0)

                def startRead():
                    reader = SimpleMFRC522()

                    try:
                        id, text = reader.read()
                        self.UID = id
                        print(f"Id de la tarjeta: { id }")
                    finally:
                        GPIO.cleanup()
                        if(self, "lblUID"):
                            self.lblUID.destroy()
                        self.lblUID = customtkinter.CTkLabel(master = self.panelCodigoUID, text=id, height=150, width=300)
                        self.lblUID.grid(row=0, column=0, padx=0, pady=0)

                        self.botonReadUID.configure(state=customtkinter.DISABLED)
                        

                self.ventanaConfirmarUID.after(2000, startRead)

                def closeWindow():
                    if(self, "ventanaConfirmarUID"):
                        self.ventanaConfirmarUID.destroy()

                self.ventanaConfirmarUID.after(5000, closeWindow)
 

        #Boton para obtener uid
        self.botonReadUID = customtkinter.CTkButton(
            self.panelDatos, 
            text="Leer UID", 
            height=35, 
            command = getUID
            )
        self.botonReadUID.grid(row=3, column=0, padx=10, pady=(5, 10))

        def asignarUID():
            if self.UID != None:
                self.estudiante.uid = self.UID
                clsEstudiante.updateStudent(self.estudiante)
                if(self, "ventana"):
                    self.ventana.destroy()
                acceso = Vo.VOpciones()   

        self.botonAceptar = customtkinter.CTkButton(
            self.panelDatos, 
            text="Aceptar", 
            height=35, 
            command = asignarUID
            )
        self.botonAceptar.grid(row=3, column=1, padx=10, pady=(5, 10))

        def volver():
            if(self, "ventana"):
                self.ventana.destroy()
            acceso = Vo.VOpciones()

        self.botonVolver = customtkinter.CTkButton(self.panelPrincipal, text="Volver", height=35, command=volver)
        self.botonVolver.grid(row=1, column=0, padx=10, pady=(5, 10))

        self.ventana.mainloop()