import requests
import datetime
import json

#LISTAR TODOS LOS ESTUDIANTES REGISTRADOS
#Funcion para filtrar a un solo estudiante, uso: buscar por codigo uid al momento de la compra
class Student:
    id = 0
    cedula_estudiante = 0
    uid = 0
    name = 0
    last_name = 0
    balance = 0
    Representative = 0
        
    def getStudentByCod(self, value):
        def deserialize(data):
            json_dict = json.loads(data)

            student = Student()

            student.id = json_dict['id']
            student.cedula_estudiante = json_dict['cedula_estudiante']
            student.uid = json_dict['uid']
            student.name = json_dict['name']
            student.last_name = json_dict['last_name']
            student.balance = json_dict['balance']
            student.Representative = json_dict['Representative']

            return student

        parametro = { 'cedula_estudiante' : value }

        headers = {'Content-Type': 'application/json'}
        cuerpo_json = json.dumps(parametro)

        res = requests.post('https://servertecsu.azurewebsites.net/tecsu/estudent/search/', data=cuerpo_json, headers=headers)

        if res.status_code == 200:
            # Deserializar el JSON
            data = res.json()

            # Verificar si los campos importantes contienen valores vacíos o nulos
            if data['cedula_estudiante'] == "" and data['uid'] == "" and data['name'] == "" and data['last_name'] == "" and data['balance'] is None and data['Representative'] is None:
                studiante = Student()
                studiante = None
                return studiante
            else:
                # Procesar los datos encontrados
                resultado = res.text

                estudianteResultado = deserialize(resultado)

                print(estudianteResultado.uid)

                return estudianteResultado
        else:
            print(f"Error en la solicitud GET. Código de estado: {res.status_code}")

        
    def updateStudent(self, value):
        def to_json():
            # Convertir la instancia de la clase a un diccionario
            data_dict = {
                "cedula_estudiante": value.cedula_estudiante,
                "uid": value.uid,
                "name": value.name,
                "last_name": value.last_name
            }
            
            # Convertir el diccionario a una cadena JSON
            json_data = json.dumps(data_dict)
            return json_data

        json_data = to_json()

        print(json_data)

        url = f'https://servertecsu.azurewebsites.net/tecsu/estudent/update/{value.id}/'

        headers = {'Content-Type': 'application/json'}

        response = requests.put(url, data=json_data, headers=headers)

        res = response.text

        print(res)
#print("id:" , estudiantesResultado.id)
#print("code_students: " , estudiantesResultado.code_students)
#print("name: " , estudiantesResultado.name)
#print("last_name: " , estudiantesResultado.last_name)
#print("balance: " , estudiantesResultado.balance)
#print("Representative: " , estudiantesResultado.Representative)
#print("************************************************************")

