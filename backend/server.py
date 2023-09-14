from conexion import obtener_conexion
import controlador
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from datetime import datetime
import os
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["*"]}})
app.config['CORS_HEADERS'] = 'Content-Type'

#Enpoint para probar la conexion con la base de datos
@app.route('/', methods=['GET'])
def index():
    try:
        conexion = obtener_conexion()
        print("CONEXION EXITOSA")
        response = jsonify({'status':'success','Votaciones': "CONEXION EXITOSA"})
        response.status_code = 200
        return response
    except:
        print("NO SE PUEDE ESTABLECER LA CONEXION A LA BASE DE DATOS")
        response = jsonify({'status':'error','Votaciones': "NO SE PUEDE ESTABLECER LA CONEXION A LA BASE DE DATOS"})
        response.status_code = 500
        return response

@app.route('/consulta1', methods=['GET'])
def Consulta1():
    response = jsonify({'status':'success','Votaciones': "CONSULTA 1"})
    return response


if __name__ == '__main__':
    print("SERVIDOR INICIADO EN EL PUERTO: 5000")
    app.run(host="0.0.0.0", port=5000, debug=True)