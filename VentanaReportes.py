import customtkinter
import tkinter
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import VentanaOpciones as Vo

class Reporte:

    def __init__(self):
        self.ventanaReporte = customtkinter.CTk()
        self.ventanaReporte.geometry("1348x665")
        self.ventanaReporte.resizable(False, False)
        self.ventanaReporte.title('Reportes de ventas')

        #  Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
        #  mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.

        #  Obtenemos el largo y  ancho de la pantalla
        wtotal = self.ventanaReporte.winfo_screenwidth()
        htotal = self.ventanaReporte.winfo_screenheight()
        #  Guardamos el largo y alto de la ventana
        wventana = 1348
        hventana = 665

        #  Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal/2-wventana/2)
        pheight = round(htotal/2-hventana/2)

        #  Se lo aplicamos a la geometría de la ventana
        self.ventanaReporte.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))


        customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.panelPrincipal = customtkinter.CTkFrame(self.ventanaReporte, height=1360, width=2660)
        self.panelPrincipal.grid(row=0, column=0, padx=10, pady=10)

        self.panelLabelCalendario = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelLabelCalendario.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

        self.label = customtkinter.CTkLabel(self.panelLabelCalendario, text='Calendario', font=('Helvetica', 16), height=50, width=340)
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.panelLabelTabla = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelLabelTabla.grid(row=0, column=1, padx=5, pady=(10, 5))

        self.labelTabla = customtkinter.CTkLabel(self.panelLabelTabla, text='Reporte de ventas', font=('Helvetica', 16), height=50, width=485)
        self.labelTabla.grid(row=0, column=1, padx=10, pady=10)

        self.panelLabelGraficos = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelLabelGraficos.grid(row=0, column=2, padx=(5, 10), pady=(10, 5))

        self.labelGraficos = customtkinter.CTkLabel(self.panelLabelGraficos, text='Gráficos', font=('Helvetica', 16), height=50, width=400)
        self.labelGraficos.grid(row=0, column=1, padx=10, pady=10)

        self.panelPrincipalGraficoBarras = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelPrincipalGraficoBarras.grid(row=1, column=2, padx=(5, 10), pady=5)

        self.panelGraficoBarras = customtkinter.CTkFrame(self.panelPrincipalGraficoBarras, height=232, width=400)
        self.panelGraficoBarras.grid(row=0, column=0, padx=10, pady=10)

        self.panelPrincipalGraficoLineas = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelPrincipalGraficoLineas.grid(row=2, column=2, padx=(5, 10), pady=(5, 10))

        self.panelGraficoLineas = customtkinter.CTkFrame(self.panelPrincipalGraficoLineas, height=200, width=400)
        self.panelGraficoLineas.grid(row=0, column=0, padx=10, pady=10)

        self.panelPrincipalGraficoLineasVentas = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelPrincipalGraficoLineasVentas.grid(row=2, column=1, padx=5, pady=(5, 10))

        self.panelGraficoLineasVentas = customtkinter.CTkFrame(self.panelPrincipalGraficoLineasVentas, height=200, width=485)
        self.panelGraficoLineasVentas.grid(row=0, column=0, padx=10, pady=10)

        # Fecha para mostrar datos de la fecha seleccionada
        self.fecha_seleccionada = None
        # Lista para almacenar datos del Treeview
        self.datos_treeview = []

        self.fig = None
        self.canvas = None

        self.fig1 = None
        self.canvas1 = None

        self.fig2 = None
        self.canvas2 = None

        self.panelCalendario = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelCalendario.grid(row=1, column=0, padx=(10, 5), pady=5)

        # Ajusta el tamaño del calendario utilizando la opción font
        font_size = 13  # ajusta el tamaño de la fuente según tus necesidades
        cal_font = ('Helvetica', font_size)

        self.cal = Calendar(self.panelCalendario, selectmode='day', locale='en_US', disabledforeground='red',
               cursor="hand2", background=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
               selectbackground=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][1],
               font=cal_font)
        self.cal.grid(row=1, column=0, padx=18, pady=40)

        self.panelTabla = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelTabla.grid(row=1, column=1, padx=5, pady=5)

        style = ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])
        
        #self.espacio = customtkinter.CTkLabel(self.panelTabla, text='', height=5)
        #self.espacio.grid(row=0, column=0)
        
        self.panelScrollTable = customtkinter.CTkScrollableFrame(self.panelTabla, height=200, width=462)
        self.panelScrollTable.grid(row=0, column=0, padx=10, pady=35)

        self.panelScrollTable.config(height=300)

        self.treeview = ttk.Treeview(self.panelScrollTable, columns=("ID", "Producto", "Cantidad", "Total", "Fecha"), show="headings")
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Producto", text="Producto")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Total", text="Total")
        self.treeview.heading("Fecha", text="Fecha")

        self.lista_ventas = [
            [1, "BOTELLA DE AGUA", 10, 10.5, datetime(2024, 2, 25)],
            [2, "Producto2", 15, 10.6, datetime(2024, 2, 23)],
            [3, "Producto3", 20, 5.65, datetime(2024, 2, 15)],
            [4, "Producto3", 20, 5.65, datetime(2024, 1, 15)],
            [5, "Producto3", 20, 5.65, datetime(2024, 1, 5)],
            [6, "Producto3", 20, 5.65, datetime(2024, 1, 1)],
        ]

        # Configurar el ancho de las columnas
        self.treeview.column("ID", width=25)  # Ancho de la columna ID
        self.treeview.column("Producto", width=150)  # Ancho de la columna Producto
        self.treeview.column("Cantidad", width=75)  # Ancho de la columna Cantidad
        self.treeview.column("Total", width=75)  #Ancho de la columna Total
        self.treeview.column("Fecha", width=125)  #Ancho de la columna Fecha

        self.treeview.grid(row=0, column=0, padx=5, pady=5)

        def cerrar_grafico():
            # Cerrar el gráfico de Matplotlib y luego cerrar la ventana principal
            plt.close('all')
            self.ventanaReporte.destroy()

        def ver_grafico():
            # Limpiar los frames antes de mostrar los gráficos
            for widget in self.panelGraficoBarras.winfo_children():
                widget.destroy()

            for widget in self.panelGraficoLineas.winfo_children():
                widget.destroy()

            for widget in self.panelGraficoLineasVentas.winfo_children():
                widget.destroy()

            if self.datos_treeview:
                # Extraer datos para el gráfico
                productos = [venta[1] for venta in self.datos_treeview]
                cantidadVenta = [venta[2] for venta in self.datos_treeview]
                fechas = [venta[4] for venta in self.datos_treeview]
                totalesVenta = [venta[3] for venta in self.datos_treeview]

                # Crear la figura y ejes para el gráfico de barras
                self.fig, ax = plt.subplots(figsize=(self.panelGraficoBarras.winfo_width() / 100, self.panelGraficoBarras.winfo_height() / 100))

                # Crear un gráfico de barras
                ax.bar(productos, cantidadVenta)
                ax.set_xlabel('Productos', fontsize=6)
                ax.set_ylabel('Cantidad vendida', fontsize=6)
                ax.set_title('Gráfico de Ventas por producto', fontsize=6)

                # Ajustar el tamaño de la fuente de las etiquetas del eje x y eje y
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)

                # Crear el widget FigureCanvasTkAgg
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.panelGraficoBarras)
                self.canvas.draw()

                self.canvas.get_tk_widget().pack(fill=customtkinter.BOTH, expand=True)

                #GRAFICO DE BARRAS

                # Crear la figura y ejes para el gráfico de líneas
                self.fig1, ax1 = plt.subplots(figsize=(self.panelGraficoLineas.winfo_width() / 100, self.panelGraficoLineas.winfo_height() / 100))

                # Crear un gráfico de líneas
                ax1.plot(fechas, cantidadVenta, marker='o', linestyle='-', color='b', label='Ventas')

                # Ajustar el formato de las fechas en el eje x
                ax1.xaxis_date()
                plt.gcf().autofmt_xdate()

                # Configurar etiquetas y título
                ax1.set_xlabel('Fechas', fontsize=6)
                ax1.set_ylabel('Cantidad vendida', fontsize=6)
                ax1.set_title('Gráfico de Ventas a lo largo del tiempo', fontsize=6)

                # Ajustar el tamaño de la fuente de las etiquetas del eje x y eje y
                ax1.tick_params(axis='x', labelsize=6)
                ax1.tick_params(axis='y', labelsize=6)

                # Crear el widget FigureCanvasTkAgg
                self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.panelGraficoLineas)
                self.canvas1.draw()

                # Colocar el widget en el frame
                self.canvas1.get_tk_widget().pack(fill=customtkinter.BOTH, expand=True)

                # Crear la figura y ejes para el gráfico de líneas
                self.fig2, ax2 = plt.subplots(figsize=(self.panelGraficoLineasVentas.winfo_width() / 100, self.panelGraficoLineasVentas.winfo_height() / 100))

                # Crear un gráfico de líneas
                ax2.plot(fechas, totalesVenta, marker='o', linestyle='-', color='b', label='Ventas')

                # Ajustar el formato de las fechas en el eje x
                ax2.xaxis_date()
                plt.gcf().autofmt_xdate()

                # Configurar etiquetas y título
                ax2.set_xlabel('Fechas', fontsize=6)
                ax2.set_ylabel('Ganancias (en $)', fontsize=6)
                ax2.set_title('Gráfico de ganancias (en $) a lo largo del tiempo', fontsize=6)

                # Ajustar el tamaño de la fuente de las etiquetas del eje x y eje y
                ax2.tick_params(axis='x', labelsize=6)
                ax2.tick_params(axis='y', labelsize=6)

                # Crear el widget FigureCanvasTkAgg
                self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.panelGraficoLineasVentas)
                self.canvas2.draw()

                # Colocar el widget en el frame
                self.canvas2.get_tk_widget().pack(fill=customtkinter.BOTH, expand=True)

                self.ventanaReporte.protocol("WM_DELETE_WINDOW", cerrar_grafico)

                self.datos_treeview = []
            else:
                plt.close()
                print("No hay datos para mostrar en el gráfico.")

        def mostrar_grafico_existente(fig, lienzo=None):
            # Crear una nueva ventana
            ventana_grafico = tkinter.Toplevel(self.ventanaReporte)
            ventana_grafico.title("Gráfico")
            ventana_grafico.geometry('1000x600')

            # Crear el widget FigureCanvasTkAgg con la figura existente
            canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
            canvas.draw()

            # Colocar el widget en la nueva ventana
            canvas.get_tk_widget().pack(fill=customtkinter.BOTH, expand=True)

            # Añadir un botón para cerrar la ventana
            btn_cerrar = customtkinter.CTkButton(ventana_grafico, text="Cerrar", height=40, command=ventana_grafico.destroy)
            btn_cerrar.pack(pady=10)

        def mostrar_grafico_existente_barras():
            if self.fig:
                mostrar_grafico_existente(self.fig, self.canvas)

        def mostrar_grafico_existente_lineas():
            if self.fig:
                mostrar_grafico_existente(self.fig1, self.canvas1)

        def mostrar_grafico_existente_lineas_ventas():
            if self.fig:
                mostrar_grafico_existente(self.fig2, self.canvas2)

        def filtrar_y_mostrar_por_semana():
            fecha_str = self.cal.get_date()

            # Convertir la cadena de fecha a un objeto datetime
            self.fecha_seleccionada = datetime.strptime(fecha_str, "%m/%d/%y")

            # Calcular la fecha de inicio y fin de la semana
            fecha_inicio_semana = self.fecha_seleccionada - timedelta(days=self.fecha_seleccionada.weekday())
            fecha_fin_semana = fecha_inicio_semana + timedelta(days=6)

            # Filtrar la lista de ventas por el rango de fechas de la semana
            ventas_en_semana = [venta for venta in self.lista_ventas if fecha_inicio_semana <= venta[4] <= fecha_fin_semana]

            self.datos_treeview = ventas_en_semana

            # Limpiar el contenido anterior en el Treeview
            self.treeview.delete(*self.treeview.get_children())

            # Acceder al primer elemento de la lista (índice 0)
            if ventas_en_semana:
                primer_elemento = ventas_en_semana[0]
                print(primer_elemento)

                # Mostrar los resultados en el Treeview
                for venta in ventas_en_semana:
                    fecha_formateada = venta[4].strftime("%Y-%m-%d")
                    self.treeview.insert('', 'end', values=(venta[0], venta[1], venta[2], venta[3], fecha_formateada))
            else:
                print("No hay ventas en la semana seleccionada")

            if self.treeview.get_children():
                # El Treeview tiene datos
                # Realiza las operaciones que necesitas
                print("El Treeview tiene datos.")
                ver_grafico()
            else:
                # El Treeview está vacío
                # Puedes mostrar un mensaje o realizar otras acciones
                print("El Treeview está vacío.")
                self.datos_treeview = []

                self.fig = None
                self.canvas = None

                self.fig1 = None
                self.canvas1 = None

                self.fig2 = None
                self.canvas2 = None

                for widget in self.panelGraficoBarras.winfo_children():
                    widget.destroy()

                for widget in self.panelGraficoLineas.winfo_children():
                    widget.destroy()

                for widget in self.panelGraficoLineasVentas.winfo_children():
                    widget.destroy()

        def filtrar_y_mostrar_por_dia():
            fecha_str = self.cal.get_date()

            # Convertir la cadena de fecha a un objeto datetime
            self.fecha_seleccionada = datetime.strptime(fecha_str, "%m/%d/%y")

            # Limpiar el contenido anterior en el Treeview
            self.treeview.delete(*self.treeview.get_children())

            # Filtrar la lista de ventas por el día seleccionado
            ventas_en_dia = [venta for venta in self.lista_ventas if venta[4].date() == self.fecha_seleccionada.date()]

            self.datos_treeview = ventas_en_dia

            # Acceder al primer elemento de la lista (índice 0)
            if ventas_en_dia:
                primer_elemento = ventas_en_dia[0]
                print(primer_elemento)

                # Mostrar los resultados en el Treeview
                for venta in ventas_en_dia:
                    fecha_formateada = venta[4].strftime("%Y-%m-%d")
                    self.treeview.insert('', 'end', values=(venta[0], venta[1], venta[2], venta[3], fecha_formateada))
            else:
                print("No hay ventas en el día seleccionado")

            if self.treeview.get_children():
                
                # El Treeview tiene datos
                # Realiza las operaciones que necesitas
                print("El Treeview tiene datos.")
                ver_grafico()
            else:
                # El Treeview está vacío
                # Puedes mostrar un mensaje o realizar otras acciones
                print("El Treeview está vacío.")
                self.datos_treeview = []

                self.fig = None
                self.canvas = None

                self.fig1 = None
                self.canvas1 = None

                self.fig2 = None
                self.canvas2 = None

                for widget in self.panelGraficoBarras.winfo_children():
                    widget.destroy()

                for widget in self.panelGraficoLineas.winfo_children():
                    widget.destroy()

                for widget in self.panelGraficoLineasVentas.winfo_children():
                    widget.destroy()

        def filtrar_y_mostrar_por_mes():
            fecha_str = self.cal.get_date()

            # Convertir la cadena de fecha a un objeto datetime
            self.fecha_seleccionada = datetime.strptime(fecha_str, "%m/%d/%y")

            # Limpiar el contenido anterior en el Treeview
            self.treeview.delete(*self.treeview.get_children())

            # Filtrar la lista de ventas por el mes y año seleccionados
            ventas_en_mes = [venta for venta in self.lista_ventas if venta[4].month == self.fecha_seleccionada.month and venta[4].year == self.fecha_seleccionada.year]

            self.datos_treeview = ventas_en_mes

            # Acceder al primer elemento de la lista (índice 0)
            if ventas_en_mes:
                primer_elemento = ventas_en_mes[0]
                print(primer_elemento)

                # Mostrar los resultados en el Treeview
                for venta in ventas_en_mes:
                    fecha_formateada = venta[4].strftime("%Y-%m-%d")
                    self.treeview.insert('', 'end', values=(venta[0], venta[1], venta[2], venta[3], fecha_formateada))
            else:
                print("No hay ventas en el mes seleccionado")

            if self.treeview.get_children():
                # El Treeview tiene datos
                # Realiza las operaciones que necesitas
                print("El Treeview tiene datos.")
                ver_grafico()
            else:
                # El Treeview está vacío
                # Puedes mostrar un mensaje o realizar otras acciones
                print("El Treeview está vacío.")
                self.datos_treeview = []

                self.fig = None
                self.canvas = None

                self.fig1 = None
                self.canvas1 = None

                self.fig2 = None
                self.canvas2 = None

                for widget in self.panelGraficoBarras.winfo_children():
                    widget.destroy()

                for widget in self.panelGraficoLineas.winfo_children():
                    widget.destroy()

                for widget in self.panelGraficoLineasVentas.winfo_children():
                    widget.destroy()

        def volver():
            if(self, "ventanaReporte"):
                self.ventanaReporte.destroy()
            mostrar = Vo.VOpciones()

        self.panelPrincipalBotones = customtkinter.CTkFrame(self.panelPrincipal)
        self.panelPrincipalBotones.grid(row=2, column=0, padx=(10, 5), pady=(5, 10))

        self.labelEspacio = customtkinter.CTkLabel(self.panelPrincipalBotones, text='', width=325)
        self.labelEspacio.grid(row=0, column=0, padx=(10, 5), pady=(5, 10))

        self.panelBotones = customtkinter.CTkFrame(self.panelPrincipalBotones)
        self.panelBotones.grid(row=0, column=0, padx=10, pady=(37, 1))

        self.panelBotonDescarga = customtkinter.CTkFrame(self.panelPrincipalBotones)
        self.panelBotonDescarga.grid(row=1, column=0, padx=10, pady=(1, 37))

        self.boton_ventas_dia = customtkinter.CTkButton(self.panelBotones, text='Ver ventas del día', width=155, height=45, command=filtrar_y_mostrar_por_dia)
        self.boton_ventas_dia.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

        self.boton_ventas_semana = customtkinter.CTkButton(self.panelBotones, text='Ver ventas de la semana', width=155, height=45, command=filtrar_y_mostrar_por_semana)
        self.boton_ventas_semana.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

        self.boton_ventas_mes = customtkinter.CTkButton(self.panelBotones, text='Ver ventas del mes', width=155, height=45, command=filtrar_y_mostrar_por_mes)
        self.boton_ventas_mes.grid(row=2, column=0, padx=(10, 5), pady=(5, 10))

        self.boton_salir = customtkinter.CTkButton(self.panelBotones, text='Volver', width=155, height=45, command=volver)
        self.boton_salir.grid(row=2, column=1, padx=(5, 10), pady=(5, 10))

        self.boton_ventas_descarga = customtkinter.CTkButton(self.panelBotonDescarga, text='Descargar', width=320, height=45)
        self.boton_ventas_descarga.grid(row=2, column=0, padx=10, pady=5)

        self.boton_ver_Barras = customtkinter.CTkButton(self.panelPrincipalGraficoBarras, text='Ver más', width=75, height=20, command=mostrar_grafico_existente_barras)
        self.boton_ver_Barras.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.boton_ver_Lineas = customtkinter.CTkButton(self.panelPrincipalGraficoLineas, text='Ver más', width=75, height=20, command=mostrar_grafico_existente_lineas)
        self.boton_ver_Lineas.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.boton_ver_Lineas_Ventas = customtkinter.CTkButton(self.panelPrincipalGraficoLineasVentas, text='Ver más', width=75, height=20, command=mostrar_grafico_existente_lineas_ventas)
        self.boton_ver_Lineas_Ventas.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.ventanaReporte.mainloop()