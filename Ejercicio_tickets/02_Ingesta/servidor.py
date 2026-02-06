import flask 

#Creamos la instancia de aplicación (levantamos el servidor)
app = flask.Flask(__name__)

#Ruta1
@app.route('/ingestion', methods=['POST'])
def ruta1():
    a=1




    