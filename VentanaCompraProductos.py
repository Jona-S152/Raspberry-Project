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

        self.lista_productos = []

        #self.panelVentana = customtkinter.CTkFrame(self.app, corner_radius=10, height=480, width=800)
        #self.panelVentana.place(relx=0, rely=0, anchor=tkinter.CENTER)

        self.cantidad_producto = 0
        #Configuración panel del titulo o filtro
        self.panelFiltro = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.panelFiltro.grid(row=0, column=0, padx=(10, 0), pady=(10, 5))
        #Label del titulo
        self.titulo = customtkinter.CTkLabel(master = self.panelFiltro, text="PRODUCTOS", height=100, width=456).pack()
        #Configuración panel del carrito
        self.panelCarrito = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.panelCarrito.grid(row=0, column=1, padx=(0, 1), pady=(10, 5))
        #Label del titulo
        self.titulo = customtkinter.CTkLabel(master = self.panelCarrito, text="CARRITO", height=100, width=310).pack()

        #Panel para mostrar los productos de la base de datos
        self.panelProductos = customtkinter.CTkScrollableFrame(master = self.app, height=330, width=433)
        self.panelProductos.grid(row=1, column=0, padx=(15, 5), pady=(5, 10))

        self.cont = 0

        def agregarAlCarrito(value, quantity):
            self.panelProductDetail = customtkinter.CTkFrame(self.panelListaProductosScroll, height=40, width=245)
            self.panelProductDetail.grid(row=self.cont, column=0)

            self.lblNameProduct = customtkinter.CTkLabel(self.panelProductDetail, text=value.name, height=40, width=90)
            self.lblNameProduct.grid(row=0, column=0, padx=0, pady=0)

            self.lblCant = customtkinter.CTkLabel(self.panelProductDetail, text=quantity, height=40, width=55)
            self.lblCant.grid(row=0, column=1, padx=0, pady=0)

            self.lblPrecio = customtkinter.CTkLabel(self.panelProductDetail, text=value.price, height=40, width=40)
            self.lblPrecio.grid(row=0, column=2, padx=0, pady=0)

            total_rounded = float(value.price) * quantity

            self.total = round(total_rounded, 2)

            self.lblTotal = customtkinter.CTkLabel(self.panelProductDetail, text=f"${self.total}", height=40, width=50)
            self.lblTotal.grid(row=0, column=3, padx=0, pady=0)

            self.btnEliminar = customtkinter.CTkButton(self.panelProductDetail, text="x", height=40, width=40, command=lambda panel=self.panelProductDetail: self.eliminarMarco(panel))
            self.btnEliminar.grid(row=0, column=4, padx=0, pady=0)
            
            self.cont += 1
        
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
                agregarAlCarrito(value, self.cantidad_producto)#Agrega los detalles al carrito
                #Agregar a la lista de productos
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
            if(producto.stock > 0):
                panel = customtkinter.CTkFrame(
                    master = self.panelProductos)
                nombre = customtkinter.CTkLabel(
                    master = panel, 
                    text=producto.name).pack(pady=(0, 1))
                precio = customtkinter.CTkLabel(
                    master = panel, 
                    text=f"${producto.price}").pack(pady=(0, 1))
                comprar = customtkinter.CTkButton(
                    master = panel, 
                    text="Seleccionar",
                    height=35, 
                    command = lambda p=producto: getCantidad(p)).pack()#GetCantidad obtiene el objeto(producto) seleccionado y lo envia como parametro para la ventana de seleccion de cantidad
                panel.grid(row=contador//3, column=contador%3, padx=10, pady=10)

                contador += 1
        
        self.panelListaProductos = customtkinter.CTkFrame(master = self.app, height=249, width=220)
        self.panelListaProductos.grid(row=1, column=1, padx=(0, 1), pady=(5, 10))

        self.panelEncabezado = customtkinter.CTkFrame(master = self.panelListaProductos)
        self.panelEncabezado.grid(row=0, column=0, padx=0, pady=0)

        self.lblNombreProducto = customtkinter.CTkLabel(master = self.panelEncabezado, text="Producto", height=40, width=95)
        self.lblNombreProducto.grid(row=0, column=0, padx=0, pady=0)

        self.lblNombreCantidad = customtkinter.CTkLabel(master = self.panelEncabezado, text="Cant.", height=40, width=55)
        self.lblNombreCantidad.grid(row=0, column=1, padx=0, pady=0)

        self.lblNombreCantidad = customtkinter.CTkLabel(master = self.panelEncabezado, text="Precio", height=40, width=40)
        self.lblNombreCantidad.grid(row=0, column=2, padx=0, pady=0)

        self.lblNombreCantidad = customtkinter.CTkLabel(master = self.panelEncabezado, text="Total", height=40, width=70)
        self.lblNombreCantidad.grid(row=0, column=3, padx=0, pady=0)

        self.lblEliminar = customtkinter.CTkLabel(master = self.panelEncabezado, text="", height=40, width=50)
        self.lblEliminar.grid(row=0, column=4, padx=0, pady=0)

        self.panelListaProductosScroll = customtkinter.CTkScrollableFrame(master = self.panelListaProductos, height=200, width=288)
        self.panelListaProductosScroll.grid(row=1, column=0, padx=(0, 1), pady=(0, 10))

        #Volver al Login
        def button_volver():
            if(self, "app"):
                self.app.destroy()
            volver = Vo.VOpciones()

        self.buttonConfirmar = customtkinter.CTkButton(master=self.panelListaProductos, text="Confirmar compra", height=35, width=198)
        self.buttonConfirmar.grid(row=2, column=0, padx=(0, 1), pady=(0, 5))

        self.button = customtkinter.CTkButton(master=self.panelListaProductos, text="Salir", height=35, width=198, command=button_volver)
        self.button.grid(row=3, column=0, padx=(0, 1), pady=(0, 5))

        self.app.mainloop()

    def eliminarMarco(self, panel):
        # Función para destruir el marco específico del contenedor desplazable
        #eliminar tambien de la lista de productos
        panel.destroy()