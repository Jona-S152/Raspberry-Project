import tkinter
import customtkinter
import ProductosApi as Pa 
import VentanaOpciones as Vo 
import PedidoProducto as clsCp 
import CompraGeneralApi as clsCg
import PedidoDatos as Pd
from CTkSpinbox import *
from PIL import Image, ImageTk
from io import BytesIO
import requests
import EstudiantesApi as Ea 
from CTkMessagebox import CTkMessagebox
import ManejarImgCache as Manejadordeimagen



#import RPi.GPIO as GPIO
#import SimpleMFRC522

class Prueba():

    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.geometry("1060x625")
        self.app.resizable(False, False)
        self.app.title("Compra")

        
        #  Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
        #  mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.

        #  Obtenemos el largo y  ancho de la pantalla
        wtotal = self.app.winfo_screenwidth()
        htotal = self.app.winfo_screenheight()
        #  Guardamos el largo y alto de la ventana
        wventana = 1060
        hventana = 625

        #  Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal/2-wventana/2)
        pheight = round(htotal/2-hventana/2)

        #  Se lo aplicamos a la geometría de la ventana
        self.app.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

        customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        self.lista_productos = []

        self.listaToPedido = []

        self.estudiante = None

        #Instancia objeto producto
        clsProducto = Pa.Producto()
        #Metodo para obtener una lista de productos
        listaProductos = clsProducto.getProducts()

        #self.panelVentana = customtkinter.CTkFrame(self.app, corner_radius=10, height=480, width=800)
        #self.panelVentana.place(relx=0, rely=0, anchor=tkinter.CENTER)

        self.cantidad_producto = 0
        #Configuración panel del titulo o filtro
        self.panelFiltro = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.panelFiltro.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))
        #Label del titulo
        self.titulo = customtkinter.CTkLabel(master = self.panelFiltro, text="PRODUCTOS", height=50, width=625).pack()
        #Configuración panel del carrito
        self.panelCarrito = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.panelCarrito.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))
        #Label del titulo
        self.titulo = customtkinter.CTkLabel(master = self.panelCarrito, text="CARRITO", height=50, width=405).pack()

        #Panel para mostrar los productos de la base de datos
        self.panelProductos = customtkinter.CTkScrollableFrame(master = self.app, height=530, width=603)
        self.panelProductos.grid(row=1, column=0, padx=(10, 5), pady=(5, 10))

        self.cont = 0

        def agregarAlCarrito(value, quantity):
            self.panelProductDetail = customtkinter.CTkFrame(self.panelListaProductosScroll, height=40, width=245)
            self.panelProductDetail.grid(row=self.cont, column=0, padx=0, pady=2)

            self.lblNameProduct = customtkinter.CTkLabel(self.panelProductDetail, text=value.name, height=40, width=170)
            self.lblNameProduct.grid(row=0, column=0, padx=0, pady=0)

            self.lblCant = customtkinter.CTkLabel(self.panelProductDetail, text=quantity, height=40, width=65)
            self.lblCant.grid(row=0, column=1, padx=0, pady=0)

            self.lblPrecio = customtkinter.CTkLabel(self.panelProductDetail, text=value.price, height=40, width=45)
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
            self.ventanaCantidad.title("Selección de cantidad")

            customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
            customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, gree
            self.panelPrincipal = customtkinter.CTkFrame(self.ventanaCantidad)
            self.panelPrincipal.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            #self.panelTitulo = customtkinter.CTkFrame(self.panelPrincipal)
            #self.panelTitulo.grid(row=0, column=0, padx=10, pady=(10, 5)
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
            #self.slider.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER
            #Guarda la cantidad para mostrarla luego en el carrito
            def aceptar_cantidad():
                if self.lista_productos:
                    
                    self.idEncontrado = False

                    for item in self.lista_productos:
                        if value.id == item.product_id:
                            def show_warning():
                                # Show some positive message with the checkmark icon
                                msg = CTkMessagebox(
                                    title="Advertencia!",
                                    message="El producto ya existe en su carrito de compra",
                                    icon="warning",
                                    option_1="Aceptar")

                                if(self, "ventanaCantidad"):
                                    self.ventanaCantidad.destroy()

                            self.idEncontrado = True

                            show_warning()

                            break
                        
                    if not self.idEncontrado:
                        self.cantidad_producto = self.spinbox.get()
                        agregarAlCarrito(value, self.cantidad_producto)#Agrega los detalles a la seccion carrit
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
                else:
                
                    self.cantidad_producto = self.spinbox.get()
                    agregarAlCarrito(value, self.cantidad_producto)#Agrega los detalles a la seccion carrit
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
        
        self.manejador_imagenes = Manejadordeimagen.ManejadorImagenes()

        #Para cada producto que exista en la lista de productos se creará un panel con su información
        for producto in listaProductos:

            # Obtener la imagen desde la caché o descargarla si es necesario
            imagen = self.manejador_imagenes.obtener_imagen_por_producto(producto)

            #response = requests.get(producto.image)
            #img_data = BytesIO(response.content)
            #imagen = Image.open(img_data)
            ## Redimensionar la imagen para ajustarse al panel manteniendo la relación de aspecto
            #imagen.thumbnail((100, 100), Image.ANTIALIAS)
#
            #foto = customtkinter.CTkImage(light_image=imagen,
            #dark_image=imagen,
            #size=(100, 100))

            if(producto.stock > 0):
                panel = customtkinter.CTkFrame(
                    master = self.panelProductos)
                #Etiqueta para mostrar la imagen
                etiqueta = customtkinter.CTkLabel(master=panel, 
                image=imagen, 
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
                    width=144, 
                    command = lambda p=producto: getCantidad(p)).pack()#GetCantidad obtiene el objeto(producto) seleccionado y lo envia como parametro para la ventana de seleccion de cantidad
                panel.grid(row=contador//4, column=contador%4, padx=2.5, pady=2.5)

                contador += 1
        
        self.panelListaProductos = customtkinter.CTkFrame(master = self.app, height=249, width=320)
        self.panelListaProductos.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

        self.panelEncabezado = customtkinter.CTkFrame(master = self.panelListaProductos)
        self.panelEncabezado.grid(row=0, column=0, padx=0, pady=0)

        self.lblNombreProducto = customtkinter.CTkLabel(master = self.panelEncabezado, text="Producto", height=40, width=170)
        self.lblNombreProducto.grid(row=0, column=0, padx=0, pady=0)

        self.lblNombreCantidad = customtkinter.CTkLabel(master = self.panelEncabezado, text="Cant.", height=40, width=75)
        self.lblNombreCantidad.grid(row=0, column=1, padx=0, pady=0)

        self.lblNombrePrecio = customtkinter.CTkLabel(master = self.panelEncabezado, text="Precio", height=40, width=40)
        self.lblNombrePrecio.grid(row=0, column=2, padx=0, pady=0)

        self.lblNombreTotal = customtkinter.CTkLabel(master = self.panelEncabezado, text="Total", height=40, width=70)
        self.lblNombreTotal.grid(row=0, column=3, padx=0, pady=0)

        self.lblEliminar = customtkinter.CTkLabel(master = self.panelEncabezado, text="", height=40, width=50)
        self.lblEliminar.grid(row=0, column=4, padx=0, pady=0)

        self.panelListaProductosScroll = customtkinter.CTkScrollableFrame(master = self.panelListaProductos, height=400, width=382)
        self.panelListaProductosScroll.grid(row=1, column=0, padx=0, pady=(0, 10))

        def confirmar():
            if self.lista_productos:
                self.ventanaConfirmar = tkinter.Toplevel()
                self.ventanaConfirmar.geometry("500x400")
                self.ventanaConfirmar.resizable(False, False)
                self.ventanaConfirmar.title("Confirmación de compra")

                customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
                customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

                self.panelPrincipal = customtkinter.CTkFrame(master = self.ventanaConfirmar)
                self.panelPrincipal.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                self.panelEncabezadoLista = customtkinter.CTkFrame(master = self.panelPrincipal)
                self.panelEncabezadoLista.grid(row=0, column=0, padx=0, pady=0)

                self.lblProductName = customtkinter.CTkLabel(master = self.panelEncabezadoLista, text="Producto", height=35, width=170)
                self.lblProductName.grid(row=0, column=0, padx=0, pady=0)

                self.lblProductQuantity = customtkinter.CTkLabel(master = self.panelEncabezadoLista, text="Cant.", height=35, width=85)
                self.lblProductQuantity.grid(row=0, column=1, padx=0, pady=0)

                self.lblProductPrice = customtkinter.CTkLabel(master = self.panelEncabezadoLista, text="Precio.", height=35, width=85)
                self.lblProductPrice.grid(row=0, column=2, padx=0, pady=0)

                self.lblProductTotalPrice = customtkinter.CTkLabel(master = self.panelEncabezadoLista, text="Total.", height=35, width=92)
                self.lblProductTotalPrice.grid(row=0, column=3, padx=0, pady=0)

                self.panelListaProductosScrollConf = customtkinter.CTkScrollableFrame(master = self.panelPrincipal, height=35, width=410)
                self.panelListaProductosScrollConf.grid(row=1, column=0, padx=0, pady=(0, 2))

                #MOSTRAR PRODUCTOS DEL CARRITO
                self.contadorVentana = 0
                for producto in self.lista_productos:
                    self.lblNombre = customtkinter.CTkLabel(master = self.panelListaProductosScrollConf, text=producto.product_name, height=40, width=165)
                    self.lblNombre.grid(row=self.contadorVentana, column=0, padx=0, pady=0)

                    self.lblNombre = customtkinter.CTkLabel(master = self.panelListaProductosScrollConf, text=producto.quantity, height=40, width=85)
                    self.lblNombre.grid(row=self.contadorVentana, column=1, padx=0, pady=0)

                    self.lblNombre = customtkinter.CTkLabel(master = self.panelListaProductosScrollConf, text=producto.price, height=40, width=85)
                    self.lblNombre.grid(row=self.contadorVentana, column=2, padx=0, pady=0)

                    self.lblNombre = customtkinter.CTkLabel(master = self.panelListaProductosScrollConf, text=f"${producto.total}", height=40, width=92)
                    self.lblNombre.grid(row=self.contadorVentana, column=3, padx=0, pady=0)

                    self.contadorVentana += 1

            self.panelTotal = customtkinter.CTkFrame(master = self.panelPrincipal)
            self.panelTotal.grid(row=2, column=0, padx=0, pady=0)

            self.lblTotalCompra = customtkinter.CTkLabel(master = self.panelTotal, text="Total: ", height=30, width=75)
            self.lblTotalCompra.grid(row=0, column=0, padx=0, pady=0)

            self.lblEspacio = customtkinter.CTkLabel(master = self.panelTotal, text="", height=30, width=290)
            self.lblEspacio.grid(row=0, column=1, padx=0, pady=0)

            self.totalCompra = 0

            for item in self.lista_productos:
                self.totalCompra += item.total

            self.lblTotalGeneral = customtkinter.CTkLabel(master = self.panelTotal, text=f"${round(self.totalCompra, 2)}", height=40, width=65)
            self.lblTotalGeneral.grid(row=0, column=2, padx=0, pady=0)

            self.panelBotones = customtkinter.CTkFrame(master = self.panelPrincipal)
            self.panelBotones.grid(row=3, column=0, padx=0, pady=(2, 0))

            def aceptarCompra():
                if(self, "ventanaConfirmar"):
                    self.ventanaConfirmar.destroy()
                    
                self.ventanaConfirmarUID = tkinter.Toplevel()
                self.ventanaConfirmarUID.geometry("500x250")
                self.ventanaConfirmarUID.resizable(False, False)
                self.ventanaConfirmarUID.title("Verificación UID")

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

                for item in self.lista_productos:
                    pedido = Pd.Pedido()
                    pedido.products = item.product_id
                    pedido.quantity = item.quantity
                    pedido.total = item.total
                    pedido.state = True
                    self.listaToPedido.append(pedido)
                
                #for item in self.listaToPedido:
                #    print(item.products)
                #    print(item.quantity)
                #    print(item.total)
                #    print(item.state)

                self.lblUID = customtkinter.CTkLabel(master = self.panelCodigoUID, text="Código de estudiante", height=40, width=300)
                self.lblUID.grid(row=0, column=0, padx=0, pady=(10, 5))

                self.iCodEstudent = customtkinter.CTkEntry(self.panelCodigoUID)
                self.iCodEstudent.insert(0, "Ej: 0915668421")
                self.iCodEstudent.bind("<Button-1>", lambda e: self.iCodEstudent.delete(0, "end"))
                self.iCodEstudent.grid(row=1, column=0, padx=0, pady=(5, 5))

                def EstudianteCompra():
                    clsEstudiante = Ea.Student()

                    self.estudiante = clsEstudiante.getStudentByCod(self.iCodEstudent.get())

                    if(self.estudiante != None):
                        clsCompra = clsCg.CGeneral()

                        ejecutarCompra = clsCompra.GuardarCompra(self.estudiante.uid, self.listaToPedido, self.totalCompra)
                        #print(ejecutarCompra)
                        print(ejecutarCompra.uid)
                        print(ejecutarCompra.total)
                        print(ejecutarCompra.state)
                        print("Detalles")
                        
                        for item in ejecutarCompra.product_detail:
                            
                            print(item)

                        self.listaToPedido.clear()

                        self.lista_productos.clear()

                        self.estudiante = None

                        if(self, "app"):
                            self.app.destroy()
                        volver = Vo.VOpciones()

                self.botonComprarFinal = customtkinter.CTkButton(master = self.panelCodigoUID, text="Comprar", height=40, width=160, command=EstudianteCompra)
                self.botonComprarFinal.grid(row=2, column=0, padx=0, pady=(5, 10))

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

                

            self.botonComprar = customtkinter.CTkButton(master = self.panelBotones, text="Comprar", height=40, width=201, command=aceptarCompra)
            self.botonComprar.grid(row=0, column=0, padx=(10, 5), pady=10)

            def cancelarCerrar():
                if(self, "ventanaConfirmar"):
                    self.ventanaConfirmar.destroy()

            self.botonCancelarCompra = customtkinter.CTkButton(master = self.panelBotones, text="Cancelar", height=40, width=201, command=cancelarCerrar)
            self.botonCancelarCompra.grid(row=0, column=2, padx=(5, 10), pady=10)
            

        #Volver al Login
        def button_volver():
            self.listaToPedido.clear()

            self.lista_productos.clear()

            self.estudiante = None
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