import tkinter
import customtkinter
import ProductosApi as Pa 
import VentanaOpciones as Vo 
from CTkSpinbox import *

class Prueba():

    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.geometry("800x475")
        self.app.resizable(False, False)

        customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        #self.panelVentana = customtkinter.CTkFrame(self.app, corner_radius=10, height=480, width=800)
        #self.panelVentana.place(relx=0, rely=0, anchor=tkinter.CENTER)

        self.cantidad_producto = 0
        #Configuración panel del titulo o filtro
        self.panelFiltro = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.panelFiltro.grid(row=0, column=0, padx=(8, 0), pady=(10, 5))
        #Label del titulo
        self.titulo = customtkinter.CTkLabel(master = self.panelFiltro, text="PRODUCTOS", height=100, width=545).pack()
        #Configuración panel del carrito
        self.panelCarrito = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.panelCarrito.grid(row=0, column=1, padx=(0, 1), pady=(10, 5))
        #Label del titulo
        self.titulo = customtkinter.CTkLabel(master = self.panelCarrito, text="CARRITO", height=100, width=220).pack()

        #Panel para mostrar los productos de la base de datos
        self.panelProductos = customtkinter.CTkScrollableFrame(master = self.app, height=330, width=523)
        self.panelProductos.grid(row=1, column=0, padx=(15, 5), pady=(5, 10))
        
        #Metodo para abrir el spinbox para seleccionar la cantidad del producto
        def getCantidad(value):#value es el producto seleccionado para obtener el stock de tal producto
            self.ventanaCantidad = tkinter.Toplevel()
            self.ventanaCantidad.geometry("500x250")
            self.ventanaCantidad.resizable(False, False)

            customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
            customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

            self.panelPrincipal = customtkinter.CTkFrame(self.ventanaCantidad)
            self.panelPrincipal.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            #self.panelTitulo = customtkinter.CTkFrame(self.panelPrincipal)
            #self.panelTitulo.grid(row=0, column=0, padx=10, pady=(10, 5))

            self.nombreProducto = customtkinter.CTkLabel(self.panelPrincipal, text=value.name)
            self.nombreProducto.grid(row=0, column=0, padx=10, pady=(10, 5))
                
            #self.spin_var = customtkinter.IntVar()
            self.spinbox = CTkSpinbox(
                master= self.panelPrincipal, 
                start_value=1, 
                min_value = 1, 
                max_value =value.stock,
                scroll_value = 1)
            self.spinbox.grid(row=1, column=0, padx=10, pady=(5, 5))
            #self.slider.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            #Guarda la cantidad para mostrarla luego en el carrito
            def aceptar_cantidad():
                self.cantidad_producto = self.spinbox.get()
                print(self.cantidad_producto)
                if(self, "ventanaCantidad"):
                    self.ventanaCantidad.destroy()
            
            def cancelar():
                if(self, "ventanaCantidad"):
                    self.ventanaCantidad.destroy()

            #Boton de envio
            self.boton = customtkinter.CTkButton(self.panelPrincipal, text="Aceptar", height=35, command=aceptar_cantidad)
            self.boton.grid(row=2, column=0, padx=10, pady=(5, 5))
            self.botonCancelar = customtkinter.CTkButton(self.panelPrincipal, text="Cancelar", height=35, command=cancelar)
            self.botonCancelar.grid(row=3, column=0, padx=10, pady=(5, 10))

        contador = 0
        #Instancia objeto producto
        clsProducto = Pa.Producto()
        #Metodo para obtener una lista de productos
        listaProductos = clsProducto.getProducts()

        #Para cada producto que exista en la lista de productos se creará un panel con su información
        for producto in listaProductos:
            panel = customtkinter.CTkFrame(
                master = self.panelProductos)
            nombre = customtkinter.CTkLabel(
                master = panel, 
                text=producto.name).pack(pady=(1, 0))
            precio = customtkinter.CTkLabel(
                master = panel, 
                text=producto.price).pack(pady=(0, 1))
            comprar = customtkinter.CTkButton(
                master = panel, 
                text="Seleccionar",
                height=35, 
                command = lambda p=producto: getCantidad(p)).pack()#GetCantidad obtiene el objeto(producto) seleccionado y lo envia como parametro para la ventana de seleccion de cantidad
            panel.grid(row=contador//3, column=contador%3, padx=15, pady=15)

            contador += 1
        
        self.panelListaProductos = customtkinter.CTkFrame(master = self.app, height=249, width=220)
        self.panelListaProductos.grid(row=1, column=1, padx=(0, 1), pady=(5, 10))

        self.panelListaProductosScroll = customtkinter.CTkScrollableFrame(master = self.panelListaProductos, height=240, width=198)
        self.panelListaProductosScroll.grid(row=0, column=0, padx=(0, 1), pady=(0, 10))

        #Volver al Login
        def button_volver():
            if(self, "app"):
                self.app.destroy()
            volver = Vo.VOpciones()

        # Use CTkButton instead of tkinter Button
        self.buttonConfirmar = customtkinter.CTkButton(master=self.panelListaProductos, text="Confirmar compra", height=35, width=198)
        #self.button.place(relx=0, rely=0, anchor=tkinter.CENTER)
        self.buttonConfirmar.grid(row=1, column=0, padx=(0, 1), pady=(0, 5))

        self.button = customtkinter.CTkButton(master=self.panelListaProductos, text="Salir", height=35, width=198, command=button_volver)
        #self.button.place(relx=0, rely=0, anchor=tkinter.CENTER)
        self.button.grid(row=2, column=0, padx=(0, 1), pady=(0, 5))

        self.app.mainloop()