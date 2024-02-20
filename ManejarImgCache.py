from functools import lru_cache
from urllib.parse import urlparse
import requests
from PIL import Image, ImageTk
from io import BytesIO
import joblib
import os
import customtkinter
import concurrent.futures
        
class ManejadorImagenes:
    CACHE_FILE = "cache_imagenes"
    CARPETA_IMAGENES = "imagenes_guardadas"

    def __init__(self):
        try:
            self.cache = self.cargar_cache()
        except (FileNotFoundError, EOFError):
            self.cache = {}

    def guardar_cache(self):
        joblib.dump(self.cache, self.CACHE_FILE)

    def cargar_cache(self):
        try:
            return joblib.load(self.CACHE_FILE)
        except (FileNotFoundError, EOFError):
            return {}

    @lru_cache(maxsize=128)
    def obtener_imagen_por_producto(self, producto):
        url = producto.image
        if url not in self.cache:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                imagen_pillow = Image.open(BytesIO(respuesta.content))
                imagen_pillow.thumbnail((100, 100), Image.ANTIALIAS)

                foto = customtkinter.CTkImage(light_image=imagen_pillow,
                dark_image=imagen_pillow,
                size=(100, 100))

                # Guardar la imagen física en una carpeta
                nombre_archivo = self.obtener_nombre_archivo(url)
                ruta_archivo = os.path.join(self.CARPETA_IMAGENES, nombre_archivo)

                if not os.path.exists(self.CARPETA_IMAGENES):
                    os.makedirs(self.CARPETA_IMAGENES)

                imagen_pillow.save(ruta_archivo)

                # Actualizar la caché con la ruta del archivo
                self.cache[url] = ruta_archivo
                self.guardar_cache()

                return foto
            else:
                print(f"Error al descargar imagen. Código de estado: {respuesta.status_code}")
                return None
        else:
            # Obtener la imagen desde la caché
            ruta_archivo = self.cache[url]
            imagen_pillow = Image.open(ruta_archivo)
            imagen_pillow.thumbnail((100, 100), Image.ANTIALIAS)

            foto = customtkinter.CTkImage(light_image=imagen_pillow,
                dark_image=imagen_pillow,
                size=(100, 100))
            return foto

    def obtener_nombre_archivo(self, url):
        # Obtener la extensión de la imagen desde la URL
        extension = os.path.splitext(urlparse(url).path)[1]
        # Generar un nombre de archivo único basado en la URL con extensión
        return f"{hash(url)}{extension if extension else '.jpg'}"