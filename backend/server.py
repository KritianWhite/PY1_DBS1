from conexion import obtener_conexion
import controlador
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import csv

from votacionTemp import VotacionTemp 



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
    
@app.route('/mostrartablas', methods=['GET'])
def MostrarTablas():
    try:
        datos = controlador.MostrarTablas()
        if datos is not None:
            response = jsonify({'status':'success', 'Votaciones':'DATOS OBTENIDOS EXITOSAMENTE', 'datos':datos})
            response.status_code = 200
            return response 
        else:
            response = jsonify({'status':'error','Votaciones': 'ERROR EN LA OBTENCION DE TABLAS','datos':datos})
            response.status_code = 500
            return response
    except:
        response = jsonify({'status':'error','Votaciones': 'ERROR DE COMUNICACION','datos':None})
        response.status_code = 500
        return response

# csv1 = "../tests/candidatos.csv"
# csv2 = "../tests/cargos.csv"
# csv3 = "../tests/ciudadanos.csv"
# csv4 = "../tests/departamentos.csv"
# csv5 = "../tests/mesas.csv"
# csv6 = "../tests/partidos.csv"
# csv7 = "../tests/votaciones.csv"

@app.route('/cargamasiva')
def CargaMasiva():
    # Initialize cursor within app context
    datos_partidos = cargar_datos_desde_csv('../tests/partidos.csv')
    for partido in datos_partidos:
        pass
        # print(partido[0], partido[1], partido[2], partido[3])
        controlador.InsertarPartido(partido[0], partido[1], partido[2], partido[3])
    print("--> SE CARGO PARTIDOS")
    datos_cargo = cargar_datos_desde_csv('../tests/cargos.csv')
    for cargo in datos_cargo:
        pass
        # print(cargo[0], cargo[1])
        controlador.InsertarCargo(cargo[0], cargo[1])
    print("--> SE CARGO CARGOS")
    datos_candidatos = cargar_datos_desde_csv('../tests/candidatos.csv')
    for candidato in datos_candidatos:
        pass
        # print(candidato[0], candidato[1], candidato[2], candidato[3], candidato[4])
        controlador.InsertarCandidato(candidato[0], candidato[1], candidato[2], candidato[3], candidato[4])
    print("--> SE CARGO CANDIDATOS")
    datos_departamentos = cargar_datos_desde_csv('../tests/departamentos.csv')
    for departamento in datos_departamentos:
        pass
        # print(departamento[0], departamento[1])
        controlador.InsertarDepartamento(departamento[0], departamento[1])
    print("--> SE CARGO DEPARTAMENTOS")
    datos_mesa = cargar_datos_desde_csv('../tests/mesas.csv')
    for mesa in datos_mesa:
        pass
        # print(mesa[0], mesa[1])
        controlador.InsertarMesa(mesa[0], mesa[1])
    print("--> SE CARGO MESAS")

    response = jsonify({'status':'error','Votaciones': '','datos':None})
    response.status_code = 500
    return response

@app.route('/ciudadanos')
def Ciudadanos():
    datos_ciudadano = cargar_datos_desde_csv('../tests/ciudadanos.csv')
    if datos_ciudadano is not None:
        for ciudadano in datos_ciudadano:
            pass
            print(ciudadano[0], ciudadano[1], ciudadano[2], ciudadano[3], ciudadano[4], ciudadano[5], ciudadano[6])
            controlador.InsertarCiudadano(ciudadano[0], ciudadano[1], ciudadano[2], ciudadano[3], ciudadano[4], ciudadano[5], ciudadano[6])
        print("--> SE CARGO CIUDADANOS")
        response = jsonify({'status':'error','Votaciones': '','datos':None})
        response.status_code = 500
        return response

@app.route('/votaciones')
def Votaciones():
    datos_votacion = cargar_datos_desde_csv('../tests/votaciones.csv')
    votaciones_dict = {}
    if datos_votacion is not None:
        for indice, votacion in enumerate(datos_votacion):
            voto_id = votacion[0]
            id_candidato = votacion[1]
            if id_candidato != -1:
                if voto_id in votaciones_dict:
                    votaciones_dict[voto_id].agregar_candidato(id_candidato)
                else:
                    nueva_votacion = VotacionTemp(
                        voto_id, votacion[3], votacion[2], votacion[4])
                    nueva_votacion.agregar_candidato(id_candidato)
                    votaciones_dict[voto_id] = nueva_votacion
        # Ahora tendrás un diccionario donde las claves son los voto_id y los valores son instancias de VotacionTemp
        for voto_id, votacion_temp in votaciones_dict.items():
            pass
            # votacion_temp.ciudadano_dpi = votacion_temp.ciudadano_dpi[:-3]
            # print(f"Voto ID: {voto_id}, Ciudadano DPI: {votacion_temp.ciudadano_dpi}, Mesa ID: {votacion_temp.mesa_id}, Fecha: {votacion_temp.fecha_hora}")
            controlador.InsertarVotacion(voto_id, votacion_temp.ciudadano_dpi, votacion_temp.mesa_id, votacion_temp.fecha_hora)
            for candidato_id in votacion_temp.candidatos:
                pass
                # print(f"Voto ID: {voto_id} - Candidato ID: {candidato_id}")
                # if candidato_id != "-1":
                # print("hola", candidato_id, candidato_id != -1)
                controlador.InsertarCandidatoVotado(voto_id, candidato_id)
        print("--> SE CARGO VOTACIONES")
        response = jsonify({'status':'error','Votaciones': '','datos':None})
        response.status_code = 500
        return response


@app.route('/eliminartablas')
def EliminarTablas():
    try:
        controlador.EliminarTablas()
        response = jsonify({'status':'success', 'Votaciones':'TABLAS ELIMINADAS EXITOSAMENTE'})
        response.status_code = 200
        return response 
    except:
        response = jsonify({'status':'error','Votaciones': 'ERROR AL ELIMINAR LAS TABLAS'})
        response.status_code = 500
        return response

@app.route('/creartablas')
def CrearTablas():
    try:
        controlador.CrearTablas()
        response = jsonify({'status':'success', 'Votaciones':'TABLAS CREADAS EXITOSAMENTE'})
        response.status_code = 200
        return response 
    except:
        response = jsonify({'status':'error','Votaciones': 'ERROR AL CREAR LAS TABLAS'})
        response.status_code = 500
        return response

@app.route('/limpiartablas')
def LimpiarTablas():
    try:
        controlador.LimpiarTablas()
        response = jsonify({'status':'success', 'Votaciones':'LAS TABLAS SE LIMPIARON CORRECTAMENTE'})
        response.status_code = 200
        return response 
    except:
        response = jsonify({'status':'error','Votaciones': 'ERROR AL LIMPIAR LAS TABLAS'})
        response.status_code = 500
        return response


@app.route('/reporte/1', methods=['GET'])
def MostrarNumeroCandidatosDiputadosPorPartido():
    try:
        data = controlador.MostrarNumeroCandidatosDiputadosPorPartido()
        response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO', 'datos':data})
        response.status_code = 200
        return response 
    except:
        response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE', 'data':None})
        response.status_code = 500
        return response

# @app.route('/reporte/2', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response

# @app.route('/reporte/3', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response

# @app.route('/reporte/4', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response

# @app.route('/reporte/5', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response

# @app.route('/reporte/6', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response

# @app.route('/reporte/7', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response

# @app.route('/reporte/8', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response

# @app.route('/reporte/9', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response

# @app.route('/reporte/10', methods=['GET'])
# def LimpiarTablas():
#     try:
#         controlador.LimpiarTablas()
#         response = jsonify({'status':'success', 'Votaciones':'REPORTE CON EXITO'})
#         response.status_code = 200
#         return response 
#     except:
#         response = jsonify({'status':'error','Votaciones': 'ERROR AL MOSTRAR EL REPORTE'})
#         response.status_code = 500
#         return response






def cargar_datos_desde_csv(nombre_archivo):
    datos = []
    with open(nombre_archivo, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Para omitir la primera fila (encabezados)
        for row in csvreader:
            if row != None:
                datos.append(row)
    return datos


if __name__ == '__main__':
    print("SERVIDOR INICIADO EN EL PUERTO: 5000")
    app.run(host="0.0.0.0", port=5000, debug=True)