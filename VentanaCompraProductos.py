import tkinter
import customtkinter
import ProductosApi as Pa 
import VentanaOpciones as Vo 
import CompraProducto as clsCp 
import CompraGeneral as clsCg
from CTkSpinbox import *
from PIL import Image, ImageTk
from io import BytesIO
import requests

#import RPi.GPIO as GPIO
#import SimpleMFRC522

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
        self.titulo = customtkinter.CTkLabel(master = self.panelFiltro, text="PRODUCTOS", height=100, width=465).pack()
        #Configuración panel del carrito
        self.panelCarrito = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.panelCarrito.grid(row=0, column=1, padx=(0, 1), pady=(10, 5))
        #Label del titulo
        self.titulo = customtkinter.CTkLabel(master = self.panelCarrito, text="CARRITO", height=100, width=300).pack()

        #Panel para mostrar los productos de la base de datos
        self.panelProductos = customtkinter.CTkScrollableFrame(master = self.app, height=330, width=443)
        self.panelProductos.grid(row=1, column=0, padx=(15, 5), pady=(5, 10))

        self.cont = 0

        def agregarAlCarrito(value, quantity):
            self.panelProductDetail = customtkinter.CTkFrame(self.panelListaProductosScroll, height=40, width=245)
            self.panelProductDetail.grid(row=self.cont, column=0, pady=2)

            self.lblNameProduct = customtkinter.CTkLabel(self.panelProductDetail, text=value.name, height=40, width=80)
            self.lblNameProduct.grid(row=0, column=0, padx=0, pady=0)

            self.lblCant = customtkinter.CTkLabel(self.panelProductDetail, text=quantity, height=40, width=55)
            self.lblCant.grid(row=0, column=1, padx=0, pady=0)

            self.lblPrecio = customtkinter.CTkLabel(self.panelProductDetail, text=value.price, height=40, width=43)
            self.lblPrecio.grid(row=0, column=2, padx=0, pady=0)

            total_rounded = float(value.price) * quantity

            self.total = round(total_rounded, 2)

            self.lblTotal = customtkinter.CTkLabel(self.panelProductDetail, text=f"${self.total}", height=40, width=62)
            self.lblTotal.grid(row=0, column=3, padx=0, pady=0)

            self.btnEliminar = customtkinter.CTkButton(self.panelProductDetail, text="X", height=38, width=38, command=lambda panel=self.panelProductDetail: self.eliminarMarco(panel, quantity, value))
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
                agregarAlCarrito(value, self.cantidad_producto)#Agrega los detalles a la seccion carrito
                
                self.varCp = clsCp.ProductoPedido()
                self.varCp.product_id = value.id
                self.varCp.product_name = value.name
                self.varCp.quantity = self.cantidad_producto
                self.varCp.price = value.price
                total_redondear = float(value.price) * self.cantidad_producto
                self.varCp.total = round(total_redondear, 2)

                #Agrega a la lista de productos
                self.lista_productos.append(self.varCp)

                for item in self.lista_productos:
                    print(f"Id: {item.product_id}, Producto: {item.product_name}, cant: {item.quantity}, precio: {item.price}, total: {item.total}")
                    
                print("***********************************************************")

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

            response = requests.get(producto.image)
            img_data = BytesIO(response.content)
            imagen = Image.open(img_data)
            # Redimensionar la imagen para ajustarse al panel manteniendo la relación de aspecto
            imagen.thumbnail((100, 100), Image.ANTIALIAS)

            foto = customtkinter.CTkImage(light_image=imagen,
            dark_image=imagen,
            size=(100, 100))

            if(producto.stock > 0):
                panel = customtkinter.CTkFrame(
                    master = self.panelProductos)
                #Etiqueta para mostrar la imagen
                etiqueta = customtkinter.CTkLabel(master=panel, 
                image=foto, 
                text = "")
                etiqueta.pack(pady=1)
                nombre = customtkinter.CTkLabel(
                    master = panel, 
                    text=producto.name).pack(pady=0)
                precio = customtkinter.CTkLabel(
                    master = panel, 
                    text=f"${producto.price}").pack(pady=0)
                comprar = customtkinter.CTkButton(
                    master = panel, 
                    text="Seleccionar",
                    height=35, 
                    command = lambda p=producto: getCantidad(p)).pack()#GetCantidad obtiene el objeto(producto) seleccionado y lo envia como parametro para la ventana de seleccion de cantidad
                panel.grid(row=contador//3, column=contador%3, padx=2.5, pady=2.5)

                contador += 1
        
        self.panelListaProductos = customtkinter.CTkFrame(master = self.app, height=249, width=220)
        self.panelListaProductos.grid(row=1, column=1, padx=(0, 1), pady=(5, 10))

        self.panelEncabezado = customtkinter.CTkFrame(master = self.panelListaProductos)
        self.panelEncabezado.grid(row=0, column=0, padx=0, pady=0)

        self.lblNombreProducto = customtkinter.CTkLabel(master = self.panelEncabezado, text="Producto", height=40, width=87)
        self.lblNombreProducto.grid(row=0, column=0, padx=0, pady=0)

        self.lblNombreCantidad = customtkinter.CTkLabel(master = self.panelEncabezado, text="Cant.", height=40, width=55)
        self.lblNombreCantidad.grid(row=0, column=1, padx=0, pady=0)

        self.lblNombreCantidad = customtkinter.CTkLabel(master = self.panelEncabezado, text="Precio", height=40, width=40)
        self.lblNombreCantidad.grid(row=0, column=2, padx=0, pady=0)

        self.lblNombreCantidad = customtkinter.CTkLabel(master = self.panelEncabezado, text="Total", height=40, width=70)
        self.lblNombreCantidad.grid(row=0, column=3, padx=0, pady=0)

        self.lblEliminar = customtkinter.CTkLabel(master = self.panelEncabezado, text="", height=40, width=50)
        self.lblEliminar.grid(row=0, column=4, padx=0, pady=0)

        self.panelListaProductosScroll = customtkinter.CTkScrollableFrame(master = self.panelListaProductos, height=200, width=280)
        self.panelListaProductosScroll.grid(row=1, column=0, padx=(0, 1), pady=(0, 10))

        def confirmar():
            if self.lista_productos:
                self.ventanaConfirmar = tkinter.Toplevel()
                self.ventanaConfirmar.geometry("500x400")
                self.ventanaConfirmar.resizable(False, False)

                customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
                customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

                self.panelPrincipal = customtkinter.CTkFrame(master = self.ventanaConfirmar)
                self.panelPrincipal.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                self.panelEncabezadoLista = customtkinter.CTkFrame(master = self.panelPrincipal)
                self.panelEncabezadoLista.grid(row=0, column=0, padx=0, pady=0)

                self.lblProductName = customtkinter.CTkLabel(master = self.panelEncabezadoLista, text="Producto", height=35, width=87)
                self.lblProductName.grid(row=0, column=0, padx=0, pady=0)

                self.lblProductQuantity = customtkinter.CTkLabel(master = self.panelEncabezadoLista, text="Cant.", height=35, width=87)
                self.lblProductQuantity.grid(row=0, column=1, padx=0, pady=0)

                self.lblProductPrice = customtkinter.CTkLabel(master = self.panelEncabezadoLista, text="Precio.", height=35, width=87)
                self.lblProductPrice.grid(row=0, column=2, padx=0, pady=0)

                self.lblProductTotalPrice = customtkinter.CTkLabel(master = self.panelEncabezadoLista, text="Total.", height=35, width=87)
                self.lblProductTotalPrice.grid(row=0, column=3, padx=0, pady=0)

                self.panelListaProductosScrollConf = customtkinter.CTkScrollableFrame(master = self.panelPrincipal, height=35, width=325)
                self.panelListaProductosScrollConf.grid(row=1, column=0, padx=0, pady=(0, 2))

                #MOSTRAR PRODUCTOS DEL CARRITO
                self.contadorVentana = 0
                for producto in self.lista_productos:
                    self.lblNombre = customtkinter.CTkLabel(master = self.panelListaProductosScrollConf, text=producto.product_name, height=40, width=78)
                    self.lblNombre.grid(row=self.contadorVentana, column=0, padx=0, pady=0)

                    self.lblNombre = customtkinter.CTkLabel(master = self.panelListaProductosScrollConf, text=producto.quantity, height=40, width=90)
                    self.lblNombre.grid(row=self.contadorVentana, column=1, padx=0, pady=0)

                    self.lblNombre = customtkinter.CTkLabel(master = self.panelListaProductosScrollConf, text=producto.price, height=40, width=88)
                    self.lblNombre.grid(row=self.contadorVentana, column=2, padx=0, pady=0)

                    self.lblNombre = customtkinter.CTkLabel(master = self.panelListaProductosScrollConf, text=f"${producto.total}", height=40, width=87)
                    self.lblNombre.grid(row=self.contadorVentana, column=3, padx=0, pady=0)

                    self.contadorVentana += 1

            self.panelTotal = customtkinter.CTkFrame(master = self.panelPrincipal)
            self.panelTotal.grid(row=2, column=0, padx=0, pady=0)

            self.lblTotalCompra = customtkinter.CTkLabel(master = self.panelTotal, text="Total: ", height=30, width=75)
            self.lblTotalCompra.grid(row=0, column=0, padx=0, pady=0)

            self.lblEspacio = customtkinter.CTkLabel(master = self.panelTotal, text="", height=30, width=204)
            self.lblEspacio.grid(row=0, column=1, padx=0, pady=0)

            self.totalCompra = 0

            for item in self.lista_productos:
                self.totalCompra += item.total

            self.lblTotalGeneral = customtkinter.CTkLabel(master = self.panelTotal, text=f"${round(self.totalCompra, 2)}", height=40, width=70)
            self.lblTotalGeneral.grid(row=0, column=2, padx=0, pady=0)

            self.panelBotones = customtkinter.CTkFrame(master = self.panelPrincipal)
            self.panelBotones.grid(row=3, column=0, padx=0, pady=(2, 0))

            def aceptarCompra():
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

                self.lblUID = customtkinter.CTkLabel(master = self.panelCodigoUID, text="Código de prueba", height=150, width=300)
                self.lblUID.grid(row=0, column=0, padx=0, pady=0)

            self.botonComprar = customtkinter.CTkButton(master = self.panelBotones, text="Comprar", height=40, width=160, command=aceptarCompra)
            self.botonComprar.grid(row=0, column=0, padx=(10, 5), pady=10)

            def cancelarCerrar():
                if(self, "ventanaConfirmar"):
                    self.ventanaConfirmar.destroy()

            self.botonCancelarCompra = customtkinter.CTkButton(master = self.panelBotones, text="Cancelar", height=40, width=160, command=cancelarCerrar)
            self.botonCancelarCompra.grid(row=0, column=2, padx=(5, 10), pady=10)
            

        #Volver al Login
        def button_volver():
            if(self, "app"):
                self.app.destroy()
            volver = Vo.VOpciones()

        self.buttonConfirmar = customtkinter.CTkButton(master=self.panelListaProductos, text="Confirmar compra", height=35, width=198, command=confirmar)
        self.buttonConfirmar.grid(row=2, column=0, padx=(0, 1), pady=(0, 5))

        self.button = customtkinter.CTkButton(master=self.panelListaProductos, text="Salir", height=35, width=198, command=button_volver)
        self.button.grid(row=3, column=0, padx=(0, 1), pady=(0, 5))

        self.app.mainloop()

    def eliminarMarco(self, panel, cant, producto):
        #eliminar tambien de la lista de productos
        for item in self.lista_productos:
            if(item.product_id == producto.id and item.quantity == cant):
                self.lista_productos.remove(item)
                break

        for item in self.lista_productos:
            print(f"Id: {item.product_id}, Producto: {item.product_name}, cant: {item.quantity}, precio: {item.price}, total: {item.total}")


        print("**********************************************************************")

        # Función para destruir el marco específico del contenedor desplazable
        panel.destroy()