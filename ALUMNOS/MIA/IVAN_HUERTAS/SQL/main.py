import os, psycopg, requests, random

#URL CONEXIÓN A BD 
#try:
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")
# except:
#     print("Error al conectar con la BD")



def getUsers():
     query = "SELECT * FROM empleados;"
     cur.execute(query)
     print("Nuestros empleados:",cur.fetchall())

getUsers()




def createUser(nombre, departamento_id):
         try:
              query = "INSERT INTO empleados (nombre, departamento_id) VALUES (%s, %s)"
              cur.execute(query, (nombre, departamento_id))
              connection.commit()
              print("Usuario creado")
         except Exception as e:
              print("Error creando usuario:", e)




def createRandomUser():
    
    try:

        response = requests.get("https://randomuser.me/api/")
        response.raise_for_status()
        
        user_data = response.json()['results'][0]['name']
        

        nombre_completo = f"{user_data['first']} {user_data['last']}"
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Random User Generator: {e}. Usando nombre local.")
        import string
        nombre_completo = ''.join(random.choices(string.ascii_lowercase, k=7)).capitalize()


    departamento_id = random.randint(1, 4) 
    
    
    createUser(nombre_completo, departamento_id)

for i in range(5):
     createRandomUser()





connection.commit()

