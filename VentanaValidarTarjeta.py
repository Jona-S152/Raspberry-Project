import tkinter
import customtkinter
import requests
import VentanaOpciones as Vo 
import EstudiantesApi as Ea 

class VTarjeta():
    def __init__(self):
        self.ventana = customtkinter.CTk()
        self.ventana.geometry("800x475")
        self.ventana.resizable(False, False)

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

        def buscar(value):#Agregar parametro para obtener el estudiante por su id
            self.ventanaDatos = tkinter.Toplevel()
            self.ventanaDatos.geometry("500x250")
            self.ventanaDatos.resizable(False, False)

            customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
            customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

            self.panelDatosEstudiante = customtkinter.CTkFrame(self.ventanaDatos)
            self.panelDatosEstudiante.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            clsEstudiante = Ea.Student()

            estudiante = clsEstudiante.getStudentByCod(value)

            print(estudiante)

            if(estudiante != None):
                self.lblDatos = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Datos del estudiante")
                self.lblDatos.grid(row=0, column=0, padx=10, pady=(10, 0))

                self.lblNombre = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Nombre:")
                self.lblNombre.grid(row=1, column=0, padx=10, pady=(10, 5))

                self.lblNombreVar = customtkinter.CTkLabel(self.panelDatosEstudiante, text=estudiante.name)
                self.lblNombreVar.grid(row=1, column=1, padx=10, pady=(10, 5))

                self.lblApellido = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Apellido:")
                self.lblApellido.grid(row=2, column=0, padx=10, pady=(5, 5))

                self.lblApellidoVar = customtkinter.CTkLabel(self.panelDatosEstudiante, text=estudiante.last_name)
                self.lblApellidoVar.grid(row=2, column=1, padx=10, pady=(5, 5))

                self.lblSaldo = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Saldo disponible:")
                self.lblSaldo.grid(row=3, column=0, padx=10, pady=(5, 5))

                self.lblSaldoVar = customtkinter.CTkLabel(self.panelDatosEstudiante, text=f"${estudiante.balance}")
                self.lblSaldoVar.grid(row=3, column=1, padx=10, pady=(5, 5)) 

                def getUID():
                    self.ventanaConfirmarUID = tkinter.Toplevel()
                    self.ventanaConfirmarUID.geometry("500x250")
                    self.ventanaConfirmarUID.resizable(False, False)

                    customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
                    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

                    self.panelPrincipalUID = customtkinter.CTkFrame(master = self.ventanaConfirmarUID)
                    self.panelPrincipalUID.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                    self.panelTituloUID = customtkinter.CTkFrame(master = self.panelPrincipalUID)
                    self.panelTituloUID.grid(row=0, column=0, padx=10, pady=(10, 5))

                    self.lblTitulo = customtkinter.CTkLabel(master = self.panelTituloUID, text="Por favor, coloque su tarjeta en el lector", height=40, width=300)
                    self.lblTitulo.grid(row=0, column=0, padx=0, pady=0)

                    self.panelCodigoUID = customtkinter.CTkFrame(master = self.panelPrincipalUID)
                    self.panelCodigoUID.grid(row=1, column=0, padx=10, pady=(5, 10))

                    self.lblUID = customtkinter.CTkLabel(master = self.panelCodigoUID, text="Código de prueba", height=150, width=300)
                    self.lblUID.grid(row=0, column=0, padx=0, pady=0)

                    if(self, "ventanaDatos"):
                        self.ventanaDatos.destroy()

                    #self.reader = SimpleMFRC522.SimpleMFRC522()
#   
                    #self.card_id = 0
#   
                    #try:
                    #    while True:
                    #        self.card_id = self.reader.read()
                    #        print(self.card_id)
                    #finally:
                    #    GPIO.cleanup()

                    

                self.botonConfirmarUID = customtkinter.CTkButton(self.panelDatosEstudiante, text="Aceptar", height=35, command=getUID)
                self.botonConfirmarUID.grid(row=4, column=0, padx=(10, 5), pady=(5, 10))

                def volveraValidar():
                    if(self, "ventanaDatos"):
                        self.ventanaDatos.destroy()

                self.botonVolverValidar = customtkinter.CTkButton(self.panelDatosEstudiante, text="Volver", height=35, command=volveraValidar)
                self.botonVolverValidar.grid(row=4, column=1, padx=10, pady=(5, 10))
            else:
                self.lblError = customtkinter.CTkLabel(self.panelDatosEstudiante, text="Error: Estudiante no encontrado")
                self.lblError.grid(row=0, column=0, padx=(5, 10), pady=(10, 5))

                def volveraValidar():
                    if(self, "ventanaDatos"):
                        self.ventanaDatos.destroy()

                self.botonVolverValidar = customtkinter.CTkButton(self.panelDatosEstudiante, text="Aceptar", height=35, command=volveraValidar)
                self.botonVolverValidar.grid(row=4, column=1, padx=10, pady=(5, 10))

        #self.codigo = self.cod_estudiante.get()

        self.botonBuscar = customtkinter.CTkButton(
            self.panelDatos, 
            text="buscar", 
            height=35, 
            command= lambda : buscar(self.cod_estudiante.get()))
        self.botonBuscar.grid(row=1, column=1, padx=10, pady=(5, 10))

        #Campos de texto Cod_tarjeta
        self.lblCod_tarjeta = customtkinter.CTkLabel(self.panelDatos, text="Código UID")
        self.lblCod_tarjeta.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.Cod_tarjeta = customtkinter.CTkEntry(self.panelDatos, height=35)
        self.Cod_tarjeta.insert(0, "Ej: 4495176584")
        self.Cod_tarjeta.bind("<Button-1>", lambda e: self.Cod_tarjeta.delete(0, "end"))
        self.Cod_tarjeta.grid(row=3, column=0, padx=10, pady=(5, 10))

        self.botonAceptar = customtkinter.CTkButton(
            self.panelDatos, 
            text="Aceptar", 
            height=35
            )
        self.botonAceptar.grid(row=3, column=1, padx=10, pady=(5, 10))

        def volver():
            if(self, "ventana"):
                self.ventana.destroy()
            acceso = Vo.VOpciones()

        self.botonVolver = customtkinter.CTkButton(self.panelPrincipal, text="Volver", height=35, command=volver)
        self.botonVolver.grid(row=1, column=0, padx=10, pady=(5, 10))

        self.ventana.mainloop()