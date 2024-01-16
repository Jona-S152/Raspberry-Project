import requests
import datetime
import json

#LISTAR TODOS LOS ESTUDIANTES REGISTRADOS
#Funcion para filtrar a un solo estudiante, uso: buscar por codigo uid al momento de la compra
class Student:
    id = 0
    code_students = 0
    name = 0
    last_name = 0
    balance = 0
    Representative = 0
        
    def getStudentByCod(self, value):
        def deserialize(data):
            json_dict = json.loads(data)

            student = Student()

            student.id = json_dict['id']
            student.code_students = json_dict['code_students']
            student.name = json_dict['name']
            student.last_name = json_dict['last_name']
            student.balance = json_dict['balance']
            student.Representative = json_dict['Representative']

            return student

        parametro = { 'code_students' : value }

        headers = {'Content-Type': 'application/json'}
        cuerpo_json = json.dumps(parametro)

        res = requests.post('http://127.0.0.1:8000/tecsu/estudent/search/', data=cuerpo_json, headers=headers)

        if res.status_code == 200:
            # Deserializar el JSON
            data = res.json()

            # Verificar si los campos importantes contienen valores vacíos o nulos
            if data['code_students'] == "" and data['name'] == "" and data['last_name'] == "" and data['balance'] is None and data['Representative'] is None:
                studiante = Student()
                studiante = None
                return studiante
            else:
                # Procesar los datos encontrados
                resultado = res.text

                estudianteResultado = deserialize(resultado)

                return estudianteResultado
        else:
            print(f"Error en la solicitud GET. Código de estado: {res.status_code}")

        

#print("id:" , estudiantesResultado.id)
#print("code_students: " , estudiantesResultado.code_students)
#print("name: " , estudiantesResultado.name)
#print("last_name: " , estudiantesResultado.last_name)
#print("balance: " , estudiantesResultado.balance)
#print("Representative: " , estudiantesResultado.Representative)
#print("************************************************************")

