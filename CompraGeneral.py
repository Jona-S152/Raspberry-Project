import json
import requests

class CGeneral():
    id_shopping = 0
    code_students = 0
    product_detail = []
    total = 0

    def GuardarCompra(self, id_compra, cod_estudiante, detalles, total_compra):

        compra = CGeneral(
            id_shopping = id_compra,
            code_students = cod_estudiante,
            product_detail = detalles,
            total = total_compra
        )

        json_data = compra.to_json()

        url = 'https://servertecsu.azurewebsites.net//tecsu/procesar-compra/'

        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json_data, headers=headers)


#FORMATO PARAMETROS
#{
#  "id_shopping": 2,
#  "uid": "0321654987",
#  "product_detail": [
#    {
#      "id": 1,
#      "products": 1,
#      "quantity": 2,
#      "total": 2.0,
#      "state": true
#    },
#    {
#      "id": 2,
#      "products": 2,
#      "quantity": 3,
#      "total": 1.50,
#      "state": true
#    }
#  ],
#  "total": 3.75,
#  "state": true
#}
