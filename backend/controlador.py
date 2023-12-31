from flask import Flask, jsonify, request
from conexion import obtener_conexion


def MostrarTablas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "SHOW TABLES;"
            print("adento del with")
            cursor.execute(query)
            tablas = cursor.fetchall()
            return tablas
    except:
        return None
    finally:
        conexion.close()

def LimpiarTablas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Define el orden en el que deseas eliminar las tablas
            tablas_a_eliminar = [
                "CANDIDATO_VOTADO",
                "VOTACION",
                "CANDIDATO",
                "CARGO",
                "PARTIDO",
                "MESA",
                "CIUDADANO",
                "DEPARTAMENTO"
            ]
            
            for tabla in tablas_a_eliminar:
                # Ejecuta la instrucción DELETE FROM para eliminar todos los registros de la tabla
                query = f"DELETE FROM {tabla};"
                cursor.execute(query)
                print(f"Registros eliminados de la tabla {tabla}")
            
            # Confirma los cambios
            conexion.commit()
            print("Todos los registros de todas las tablas han sido eliminados con éxito.")
    except Exception as e:
        print(f"Error al limpiar las tablas: {str(e)}")
    finally:
        conexion.close()

def EliminarTablas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Define el orden en el que deseas eliminar las tablas
            tablas_a_eliminar = [
                "CANDIDATO_VOTADO",
                "VOTACION",
                "CANDIDATO",
                "CARGO",
                "PARTIDO",
                "MESA",
                "CIUDADANO",
                "DEPARTAMENTO"
            ]
            
            for tabla in tablas_a_eliminar:
                # Ejecuta la instrucción DROP TABLE para eliminar la tabla
                query = f"DROP TABLE IF EXISTS {tabla};"
                cursor.execute(query)
                print(f"Tabla {tabla} eliminada")
            
            # Confirma los cambios
            conexion.commit()
            print("Todas las tablas han sido eliminadas con éxito.")
    except Exception as e:
        print(f"Error al eliminar las tablas: {str(e)}")
    finally:
        conexion.close()

def CrearTablas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Define las instrucciones CREATE TABLE en el orden adecuado
            instrucciones_create = [
                """
                CREATE TABLE IF NOT EXISTS CARGO (
                    id_cargo INTEGER NOT NULL PRIMARY KEY,
                    cargo VARCHAR(50) NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS PARTIDO (
                    id_partido INTEGER NOT NULL PRIMARY KEY,
                    nombre_partido VARCHAR(75) NOT NULL,
                    siglas VARCHAR(15) NOT NULL,
                    fundacion DATE NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS DEPARTAMENTO (
                    id_departamento INTEGER NOT NULL PRIMARY KEY,
                    nombre VARCHAR(25) NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS MESA (
                    id_mesa INTEGER NOT NULL PRIMARY KEY,
                    id_departamento INTEGER,
                    FOREIGN KEY (id_departamento) REFERENCES DEPARTAMENTO (id_departamento)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS CIUDADANO (
                    dpi_ciudadano BIGINT NOT NULL PRIMARY KEY,
                    nombre VARCHAR(15) NOT NULL,
                    apellido VARCHAR(15) NOT NULL,
                    direccion VARCHAR(250) NOT NULL,
                    telefono INTEGER NOT NULL,
                    edad INTEGER NOT NULL,
                    genero CHAR(1) NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS VOTACION (
                    id_voto INTEGER NOT NULL PRIMARY KEY,
                    id_mesa INTEGER NOT NULL,
                    dpi_ciudadano BIGINT NOT NULL,
                    fecha_hora TIMESTAMP NOT NULL,
                    FOREIGN KEY (id_mesa) REFERENCES MESA (id_mesa),
                    FOREIGN KEY (dpi_ciudadano) REFERENCES CIUDADANO (dpi_ciudadano)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS CANDIDATO (
                    id_candidato INTEGER NOT NULL PRIMARY KEY,
                    id_cargo INTEGER NOT NULL,
                    id_partido INTEGER NOT NULL,
                    nombre VARCHAR(25) NOT NULL,
                    fecha_nacimiento DATE NOT NULL,
                    FOREIGN KEY (id_cargo) REFERENCES CARGO (id_cargo),
                    FOREIGN KEY (id_partido) REFERENCES PARTIDO (id_partido)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS CANDIDATO_VOTADO (
                    id_votado INTEGER NOT NULL PRIMARY KEY,
                    id_voto INTEGER NOT NULL,
                    id_candidato INTEGER NOT NULL,
                    FOREIGN KEY (id_voto) REFERENCES VOTACION (id_voto),
                    FOREIGN KEY (id_candidato) REFERENCES CANDIDATO (id_candidato)
                );
                """
            ]
            
            for instruccion in instrucciones_create:
                cursor.execute(instruccion)
                print("Tabla creada:", instruccion.split('\n')[1].strip())
            
            # Confirma los cambios
            conexion.commit()
            print("Todas las tablas han sido creadas con éxito.")
    except Exception as e:
        print(f"Error al crear las tablas: {str(e)}")
    finally:
        conexion.close()

def InsertarCargo(id_cargo, cargo):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO CARGO (id_cargo, cargo) VALUES (%s, %s);"
            cursor.execute(query, (id_cargo, cargo))
            conexion.commit()
    except:
        conexion.rollback() 
    finally:
        conexion.close()

def InsertarPartido(id_partido, nombre_partido, siglas, fundacion):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO PARTIDO (id_partido, nombre_partido, siglas, fundacion) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (id_partido, nombre_partido, siglas, fundacion))
            conexion.commit()
    except:
        conexion.rollback()
    finally:
        conexion.close()

def InsertarDepartamento(id_departamento, nombre):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO DEPARTAMENTO (id_departamento, nombre) VALUES (%s, %s);"
            cursor.execute(query, (id_departamento, nombre))
            conexion.commit()
    except:
        conexion.rollback()
    finally:
        conexion.close()

def InsertarMesa(id_mesa, id_departamento):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO MESA (id_mesa, id_departamento) VALUES (%s, %s);"
            cursor.execute(query, (id_mesa, id_departamento))
            conexion.commit()
    except:
        conexion.rollback()
    finally:
        conexion.close()

def InsertarCiudadano(dpi_ciudadano, nombre, apellido, direccion, telefono, edad, genero):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO CIUDADANO (dpi_ciudadano, nombre, apellido, direccion, telefono, edad, genero) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(query, (dpi_ciudadano, nombre, apellido, direccion, telefono, edad, genero))
            conexion.commit()
    except:
        conexion.rollback()
    finally:
        conexion.close()

def InsertarVotacion(id_voto, id_mesa, dpi_ciudadano, fecha_hora):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO VOTACION (id_voto, id_mesa, dpi_ciudadano, fecha_hora) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (id_voto, id_mesa, dpi_ciudadano, fecha_hora))
            conexion.commit()
    except:
        conexion.rollback()
    finally:
        conexion.close()

def InsertarCandidato(id_candidato, nombre, fecha_nacimiento, id_partido, id_cargo):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO CANDIDATO (id_candidato, id_cargo, id_partido, nombre, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query, (id_candidato, id_cargo, id_partido, nombre, fecha_nacimiento))
            conexion.commit()
    except:
        conexion.rollback()
    finally:
        conexion.close()

def InsertarCandidatoVotado(id_votado, id_voto, id_candidato):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO CANDIDATO_VOTADO (id_votado, id_voto, id_candidato) VALUES (%s, %s, %s);"
            cursor.execute(query, (id_votado, id_voto, id_candidato))
            conexion.commit()
    except:
        conexion.rollback()
    finally:
        conexion.close()


def mostrar_candidatos_presidente_vicepresidente():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT
                    p1.nombre AS nombre_presidente,
                    p2.nombre AS nombre_vicepresidente,
                    partido.nombre_partido AS partido
                FROM
                    CANDIDATO AS p1
                JOIN
                    CANDIDATO AS p2 ON p1.id_partido = p2.id_partido AND p1.id_cargo = 1 AND p2.id_cargo = 2
                JOIN
                    PARTIDO ON p1.id_partido = PARTIDO.id_partido;

            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            return jsonify({'response' :resultados})
    except:
        return None
    finally:
        conexion.close()

def mostrar_candidatos_diputados():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT p.nombre_partido, COUNT(c.id_candidato) AS num_candidatos
                FROM PARTIDO p
                LEFT JOIN CANDIDATO c ON p.id_partido = c.id_partido
                WHERE c.id_cargo IN (3, 4, 5) -- IDs de los cargos de diputados
                GROUP BY p.nombre_partido;

            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            resultados_json = [{'partido': partido, 'num_candidatos': num_candidatos} for partido, num_candidatos in resultados]
            return jsonify(resultados=resultados_json)
    except:
        return None
    finally:
        conexion.close()

def mostrar_candidatos_alcalde():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT p.nombre_partido, ca.nombre AS nombre_candidato
                FROM PARTIDO p
                JOIN CANDIDATO ca ON p.id_partido = ca.id_partido
                WHERE ca.id_cargo = 6; -- ID del cargo de alcalde

            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            return jsonify({'response' :resultados})
    except:
        return None
    finally:
        conexion.close()

def mostrar_candidatos_por_partido():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT p.nombre_partido,
                    SUM(CASE WHEN ca.id_cargo = 1 THEN 1 ELSE 0 END) AS presidentes,
                    SUM(CASE WHEN ca.id_cargo = 2 THEN 1 ELSE 0 END) AS vicepresidentes,
                    SUM(CASE WHEN ca.id_cargo = 6 THEN 1 ELSE 0 END) AS alcaldes,
                    SUM(CASE WHEN ca.id_cargo IN (3, 4, 5) THEN 1 ELSE 0 END) AS diputados
                FROM PARTIDO p
                LEFT JOIN CANDIDATO ca ON p.id_partido = ca.id_partido
                GROUP BY p.nombre_partido;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            formatted_results = []
            for row in resultados:
                partido_info = {
                    "partido": row[0],
                    "cantidad_presidente": row[1],
                    "cantidad_vicepresidente": row[2],
                    "cantidad_alcalde": row[3],
                    "cantidad_diputados": row[4]
                }
            formatted_results.append(partido_info)
            return jsonify({ "response": formatted_results})
    except:
        return None
    finally:
        conexion.close()

def votaciones_por_departamento():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT d.nombre AS departamento,
                    COUNT(v.id_voto) AS cantidad_votaciones
                FROM VOTACION v
                JOIN MESA m ON v.id_mesa = m.id_mesa
                JOIN DEPARTAMENTO d ON m.id_departamento = d.id_departamento
                GROUP BY d.nombre;

            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            formatted_results = []
            for row in resultados:
                departamento_info = {
                    "departamento": row[0],
                    "cantidad_votaciones": row[1]
                }
                formatted_results.append(departamento_info)

            return jsonify({"response": formatted_results})
    except:
        return None
    finally:
        conexion.close()

def cantidad_votos_nulos():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT COUNT(*) AS cantidad_votos_nulos
                FROM CANDIDATO_VOTADO
                WHERE id_candidato = -1;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cantidad_votos_nulos = resultados[0]
        return jsonify({"cantidad_votos_nulos": cantidad_votos_nulos})
    except:
        return None
    finally:
        conexion.close()

def Top10EdadCiudadanos():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT v.dpi_ciudadano, c.nombre, c.apellido, c.edad
                FROM VOTACION v
                LEFT JOIN CIUDADANO c ON v.dpi_ciudadano = c.dpi_ciudadano
                GROUP BY v.dpi_ciudadano, c.nombre, c.apellido, c.edad
                ORDER BY c.edad DESC
                LIMIT 10;
            """
            response = []
            cursor.execute(query)
            resultados = cursor.fetchall()
            for resultado in resultados:
                response.append({
                    "dpi_ciudadano": resultado[0],
                    "nombre": resultado[1],
                    "apellido": resultado[2],
                    "edad": resultado[3]
                })
            return jsonify({'response' : response})
    except:
        return None
    finally:
        conexion.close()

def Top10CandidatosMasVotadosPresidenteVicepresidente():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT C.nombre, COUNT(*) AS "cantidad_votos"
                FROM VOTACION V
                INNER JOIN CANDIDATO C ON V.id_candidato = C.id_candidato
                WHERE C.id_cargo IN (1, 2) -- Suponiendo que los ID de cargo para presidente y vicepresidente son 1 y 2 respectivamente
                GROUP BY C.nombre
                ORDER BY COUNT(*) DESC
                LIMIT 10;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
    except:
        return None
    finally:
        conexion.close()

def Top5MesasMasFrecuentadas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT M.id_mesa, D.nombre AS "departamento"
                FROM MESA M
                INNER JOIN DEPARTAMENTO D ON M.id_departamento = D.id_departamento
                GROUP BY M.id_mesa, D.nombre
                ORDER BY COUNT(*) DESC
                LIMIT 5;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
    except:
        return None
    finally:
        conexion.close()

def Top5HoraMasConcurrida():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT HOUR(fecha_hora) AS "hora", COUNT(*) AS "cantidad_votaciones"
                FROM VOTACION
                GROUP BY HOUR(fecha_hora)
                ORDER BY COUNT(*) DESC
                LIMIT 5;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
    except:
        return None
    finally:
        conexion.close()

def CantidadVotosPorGenero():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """
                SELECT genero, COUNT(*) AS "cantidad_votos"
                FROM CIUDADANO C
                INNER JOIN VOTACION V ON C.dpi_ciudadano = V.dpi_ciudadano
                GROUP BY genero;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
    except:
        return None
    finally:
        conexion.close()
