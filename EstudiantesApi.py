import requests
import datetime

#LISTAR TODOS LOS ESTUDIANTES REGISTRADOS
#Funcion para filtrar a un solo estudiante, uso: buscar por codigo uid al momento de la compra
class Student:
    def __init__(self, id, code_students, name, last_name, balance, Representative):
        self.id = id
        self.code_students = code_students
        self.name = name
        self.last_name = last_name
        self.balance = float(balance)
        self.Representative = Representative

def deserialize(data):
    students = []
    for item in data:
        student = Student(
            item['id'],
            item['code_students'],
            item['name'],
            item['last_name'],
            item['balance'],
            item['Representative']
        )
        students.append(student)
    return students

res = requests.get('http://127.0.0.1:8000/tecsu/estudent/list/')

resultado = res.json()

estudiantesResultado = deserialize(resultado)

for item in estudiantesResultado:
    print("id:" , item.id)
    print("code_students: " , item.code_students)
    print("name: " , item.name)
    print("last_name: " , item.last_name)
    print("balance: " , item.balance)
    print("Representative: " , item.Representative)
    print("************************************************************")


#Funcion para filtrar a un solo estudiante, uso: buscar por codigo uid al momento de la compra
def getEstudiante():
    for item in estudiantesResultado:
        if(item.last_name == "PEREIRA"):
            return item

estudiante = getEstudiante()

print("id:" , estudiante.id)
print("code_students: " , estudiante.code_students)
print("name: " , estudiante.name)
print("last_name: " , estudiante.last_name)
print("balance: " , estudiante.balance)
print("Representative: " , estudiante.Representative)

