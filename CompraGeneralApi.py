import json
import requests

class CGeneral():
    uid = 0
    product_detail = []
    total = 0
    state = 0

    def GuardarCompra(self, cod_uid, detalles, total_compra):

        compra = CGeneral()
        compra.uid = cod_uid

        compra.product_detail = [
            {
                "products": producto.products, 
                "quantity": producto.quantity, 
                "total": producto.total, 
                "state": producto.state
            } 
            for producto in detalles
        ]
        
        compra.total = total_compra
        compra.state = True
        
        def to_json():
            # Convertir la instancia de la clase a un diccionario
            data_dict = {
                "uid": compra.uid,
                "product_detail": compra.product_detail,
                "total": compra.total,
                "state": compra.state    
            }
            
            # Convertir el diccionario a una cadena JSON
            json_data = json.dumps(data_dict)
            return json_data

        

        json_data = to_json()

        print(json_data)

        url = 'https://servertecsu.azurewebsites.net//tecsu/procesar-compra/'

        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json_data, headers=headers)

        res = response.json()

        print(res)

        return response


