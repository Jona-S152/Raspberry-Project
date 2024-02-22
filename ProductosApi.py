import requests
import datetime

#LISTAR TODOS LOS PRODUCTOS
class Producto:

    id = ""
    state = ""
    create_date = ""
    modified_date = ""
    delete_date = ""
    name = ""
    image = ""
    description = ""
    category = ""
    price = ""  
    stock = ""  


    def getProducts(self):
        def deserialize_and_create_objects(data):
            productos = []
            for item in data:
                producto = Producto()

                producto.id = item['id']
                producto.state = item['state']
                producto.create_date = item['create_date']
                producto.modified_date = item['modified_date']
                producto.delete_date = item['delete_date']
                producto.name = item['name']
                producto.image = item['image']
                producto.description = item['description']
                producto.category = item['category']
                producto.price = item['price']
                producto.stock = item['stock']

                productos.append(producto)
            return productos

    
        res = requests.get('https://servertecsu.azurewebsites.net/tecsu/products/')

        resultado = res.json()

        productosResultado = deserialize_and_create_objects(resultado)

        return productosResultado

#for item in productosResultado:
#    print("id:" , item.id)
#    print("state: " , item.state)
#    print("create_date: " , item.create_date)
#    print("modified_date: " , item.modified_date)
#    print("name: " , item.name)
#    print("image: " , item.image)
#    print("description: " , item.description)
#    print("category: " , item.category)
#    print("price: " , item.price)
#    print("stock" , item.stock)
#    print("************************************************************")

