import customtkinter
import tkinter
import VentanaCompraProductos as Vcproduct
import VentanaValidarTarjeta as Vt 
import VentanaLogin as Vl
from VentanaReportes import Reporte

class VOpciones():
    def __init__(self):
        self.ventana = customtkinter.CTk()
        self.ventana.geometry("500x250")
        self.ventana.resizable(False, False)

        #  Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
        #  mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.

        #  Obtenemos el largo y  ancho de la pantalla
        wtotal = self.ventana.winfo_screenwidth()
        htotal = self.ventana.winfo_screenheight()
        #  Guardamos el largo y alto de la ventana
        wventana = 500
        hventana = 250

        #  Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal/2-wventana/2)
        pheight = round(htotal/2-hventana/2)

        #  Se lo aplicamos a la geometría de la ventana
        self.ventana.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))


        customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        self.panelPrincipal = customtkinter.CTkFrame(self.ventana)
        self.panelPrincipal.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        def comprar():
            if(self, "ventana"):
                self.ventana.destroy()
            Acceso = Vcproduct.Prueba()

        self.boton = customtkinter.CTkButton(self.panelPrincipal, text="Comprar", height=35, command=comprar)
        self.boton.grid(row=0, column=0, padx=10, pady=(5, 5))

        def validar():
            if(self, "ventana"):
                self.ventana.destroy()
            Acceso = Vt.VTarjeta()
        
        self.botonValidar = customtkinter.CTkButton(self.panelPrincipal, text="Validar Tarjeta", height=35, command=validar)
        self.botonValidar.grid(row=1, column=0, padx=10, pady=(5, 5))

        def reporte():
            if(self, "ventana"):
                self.ventana.destroy()
            ventana = Reporte()
        
        self.botonReportes = customtkinter.CTkButton(self.panelPrincipal, text="Reportes", height=35, command=reporte)
        self.botonReportes.grid(row=2, column=0, padx=10, pady=(5, 5))


        def salir():
            if(self, "ventana"):
                self.ventana.destroy()
            volver = Vl.Login()

        self.buttonSalir = customtkinter.CTkButton(master=self.panelPrincipal, text="Salir", height=35, command=salir)
        self.buttonSalir.grid(row=3, column=0, padx=(0, 1), pady=(5, 10))

        self.ventana.mainloop()