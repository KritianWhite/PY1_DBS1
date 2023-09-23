# Manual Técnico - Sistema de Gestión Electoral

## Introducción
Este manual técnico describe las funciones y características de un sistema de gestión electoral implementado en Python con una base de datos MySQL. El sistema se encarga de gestionar información relacionada con candidatos, votaciones, ciudadanos y otros elementos relevantes para un proceso electoral.

## Requisitos Previos
Asegúrate de tener los siguientes requisitos previos configurados antes de ejecutar el sistema:

- **Python:** El sistema está implementado en Python, por lo que debes tener Python instalado en tu entorno de desarrollo.

- **MySQL:** Se utiliza MySQL como sistema de gestión de bases de datos. Debes tener un servidor MySQL configurado y funcionando correctamente.

- **Conector MySQL para Python:** Debes instalar el paquete `mysql-connector-python`, que permite interactuar con la base de datos MySQL desde Python. Puedes instalarlo usando pip:

pip install mysql-connector-python

- **Variables de Entorno:** El sistema utiliza variables de entorno para almacenar información sensible como las credenciales de la base de datos. Crea un archivo `.env` en el directorio raíz del proyecto y configura las siguientes variables de entorno:

```makefile
DATABASE_HOST=nombre_del_servidor_de_la_base_de_datos
DATABASE_USER=nombre_de_usuario_de_la_base_de_datos
DATABASE_PASSWORD=contraseña_de_la_base_de_datos
DATABASE_NAME=nombre_de_la_base_de_datos
DATABASE_PORT=puerto_de_la_base_de_datos
```

## Tablas de la Base de Datos

### 1. Tabla CARGO

La tabla `CARGO` almacena información sobre los cargos electorales que están en juego en una elección. Cada cargo tiene un identificador único (`id_cargo`) y un nombre (`cargo`) que describe el puesto.

```sql
CREATE TABLE CARGO (
    id_cargo INTEGER NOT NULL PRIMARY KEY,
    cargo VARCHAR(50) NOT NULL
);
```

### 2. Tabla PARTIDO

La tabla PARTIDO almacena información sobre los partidos políticos que participan en una elección. Cada partido tiene un identificador único (id_partido), un nombre (nombre_partido), siglas (siglas), y la fecha de fundación (fundacion) del partido.

```sql
CREATE TABLE PARTIDO (
    id_partido INTEGER NOT NULL PRIMARY KEY,
    nombre_partido VARCHAR(75) NOT NULL,
    siglas VARCHAR(15) NOT NULL,
    fundacion DATE NOT NULL
);
```

### 3. Tabla DEPARTAMENTO

La tabla DEPARTAMENTO almacena información sobre los departamentos geográficos en una región o país. Cada departamento tiene un identificador único (id_departamento) y un nombre (nombre) que representa su nombre geográfico.

```sql
CREATE TABLE DEPARTAMENTO (
    id_departamento INTEGER NOT NULL PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL
);
```

### 4. Tabla MESA

La tabla MESA almacena información sobre las mesas de votación. Cada mesa de votación tiene un identificador único (id_mesa) y está asociada a un departamento (id_departamento) utilizando una clave foránea (FOREIGN KEY).

```sql
CREATE TABLE MESA (
    id_mesa INTEGER NOT NULL PRIMARY KEY,
    id_departamento INTEGER,
    FOREIGN KEY (id_departamento) REFERENCES DEPARTAMENTO (id_departamento)
);
```

### 5. Tabla CIUDADANO

La tabla CIUDADANO almacena información sobre los votantes o ciudadanos. Cada ciudadano tiene un número de DPI (Documento Personal de Identificación) único (dpi_ciudadano), nombre (nombre), apellido (apellido), dirección (direccion), número de teléfono (telefono), edad (edad), y género (genero).

```sql
CREATE TABLE CIUDADANO (
    dpi_ciudadano BIGINT NOT NULL PRIMARY KEY,
    nombre VARCHAR(15) NOT NULL,
    apellido VARCHAR(15) NOT NULL,
    direccion VARCHAR(250) NOT NULL,
    telefono INTEGER NOT NULL,
    edad INTEGER NOT NULL,
    genero CHAR(1) NOT NULL
);
```

### 6. Tabla VOTACION

La tabla VOTACION almacena información sobre las votaciones realizadas por los ciudadanos. Cada votación tiene un identificador único (id_voto), está asociada a una mesa de votación (id_mesa) y a un ciudadano (dpi_ciudadano) utilizando claves foráneas (FOREIGN KEY), y también registra la fecha y hora (fecha_hora) en que se realizó la votación.

```sql
CREATE TABLE VOTACION (
    id_voto INTEGER NOT NULL PRIMARY KEY,
    id_mesa INTEGER NOT NULL,
    dpi_ciudadano BIGINT NOT NULL,
    fecha_hora TIMESTAMP NOT NULL,
    FOREIGN KEY (id_mesa) REFERENCES MESA (id_mesa),
    FOREIGN KEY (dpi_ciudadano) REFERENCES CIUDADANO (dpi_ciudadano)
);
```

### 7. Tabla CANDIDATO

La tabla CANDIDATO almacena información sobre los candidatos a cargos electorales. Cada candidato tiene un identificador único (id_candidato), está asociado a un cargo electoral (id_cargo) y a un partido político (id_partido) utilizando claves foráneas (FOREIGN KEY), y también registra el nombre (nombre) del candidato y su fecha de nacimiento (fecha_nacimiento).

```sql
CREATE TABLE CANDIDATO (
    id_candidato INTEGER NOT NULL PRIMARY KEY,
    id_cargo INTEGER NOT NULL,
    id_partido INTEGER NOT NULL,
    nombre VARCHAR(25) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    FOREIGN KEY (id_cargo) REFERENCES CARGO (id_cargo),
    FOREIGN KEY (id_partido) REFERENCES PARTIDO (id_partido)
);
```

### 8. Tabla CANDIDATO_VOTADO

La tabla CANDIDATO_VOTADO almacena información sobre los candidatos por los que los ciudadanos han votado en una elección específica. Cada registro en esta tabla tiene un identificador único (id_votado), está asociado a una votación (id_voto)

```sql
CREATE TABLE CANDIDATO_VOTADO(
    id_votado INTEGER NOT NULL PRIMARY KEY,
    id_voto INTEGER NOT NULL,
    id_candidato INTEGER NOT NULL,
    FOREIGN KEY (id_voto) REFERENCES VOTACION (id_voto),
    FOREIGN KEY (id_candidato) REFERENCES CANDIDATO (id_candidato)
);
```

## Establecimiento de Conexión a MySQL en Python

```python
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def obtener_conexion():
    return mysql.connector.connect(
        host=os.environ.get('DATABASE_HOST'),
        user=os.environ.get('DATABASE_USER'),
        password=os.environ.get('DATABASE_PASSWORD'),
        db=os.environ.get('DATABASE_NAME'),
        port=os.environ.get('DATABASE_PORT')
    )
```

El código Python mostrado anteriormente se encarga de establecer una conexión a una base de datos MySQL utilizando la biblioteca `mysql.connector`. Además, utiliza la biblioteca `dotenv` para cargar las variables de entorno desde un archivo `.env`.

### Importación de Módulos:

- Se importa el módulo `mysql.connector` para interactuar con la base de datos MySQL.
- Se importa el módulo `os` para trabajar con variables de entorno y el sistema operativo.
- Se importa la función `load_dotenv` del módulo `dotenv` para cargar variables de entorno desde un archivo `.env`.

### Carga de Variables de Entorno:

- Se utiliza `load_dotenv()` para cargar las variables de entorno desde un archivo `.env`. Esto es útil para mantener de forma segura información sensible como las credenciales de la base de datos.

### Función `obtener_conexion()`:

- Se define una función llamada `obtener_conexion()` que se encarga de establecer una conexión a la base de datos MySQL.
- La función utiliza los valores de las variables de entorno para configurar la conexión, incluyendo el host, usuario, contraseña, nombre de la base de datos y puerto.
- La función retorna la conexión establecida.

## Server.py

### Función MostrarTablas()
Esta función se encarga de mostrar la lista de tablas disponibles en la base de datos. Utiliza la consulta SHOW TABLES; para obtener el listado de tablas y lo retorna como una lista.

```python
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

```

### Función LimpiarTablas()
La función LimpiarTablas() se encarga de eliminar todos los registros de las tablas de la base de datos en un orden específico. Primero, define el orden en el que se desean eliminar las tablas y luego ejecuta una instrucción DELETE FROM para borrar todos los registros de cada tabla. Finalmente, confirma los cambios en la base de datos.

```python
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
```

### Función EliminarTablas()
EliminarTablas() tiene la función de eliminar completamente las tablas de la base de datos. Al igual que la función anterior, define el orden en el que se desean eliminar las tablas y ejecuta la instrucción DROP TABLE IF EXISTS para eliminar cada tabla. Luego, confirma los cambios en la base de datos.

```python
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
```

### Función CrearTablas()
CrearTablas() se encarga de crear todas las tablas necesarias en la base de datos si no existen previamente. Define las instrucciones CREATE TABLE para cada tabla en el orden adecuado y las ejecuta en la base de datos. Luego, confirma los cambios.

```python
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
```

## Controlador.py

### Importación de Librerías y Módulos:

- La aplicación utiliza Flask para crear la API web.
- Se importa la función `obtener_conexion` del módulo `conexion`, que se utiliza para establecer una conexión a la base de datos MySQL.

```python
from conexion import obtener_conexion
conexion = obtener_conexion()
```

### Funciones para Operaciones en la Base de Datos:

- `MostrarTablas()`: Esta función obtiene una lista de tablas disponibles en la base de datos mediante la consulta `SHOW TABLES;`. Luego, devuelve esa lista.

```python
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
```

- `LimpiarTablas()`: Elimina todos los registros de las tablas en un orden específico definido en `tablas_a_eliminar`. Para cada tabla, ejecuta la instrucción `DELETE FROM`.

```python
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
```

- `EliminarTablas()`: Elimina completamente todas las tablas de la base de datos en el mismo orden definido en `tablas_a_eliminar`. Utiliza `DROP TABLE IF EXISTS`.

```python
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
```

- `CrearTablas()`: Crea las tablas necesarias en la base de datos si no existen previamente. Define las instrucciones `CREATE TABLE` para cada tabla y las ejecuta.

```python
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
```

- Otras funciones como `InsertarCargo`, `InsertarPartido`, `InsertarDepartamento`, `InsertarMesa`, `InsertarCiudadano`, `InsertarVotacion`, `InsertarCandidato`, `InsertarCandidatoVotado` se utilizan para insertar registros en diferentes tablas de la base de datos.

### Funciones para Consultas de Datos:

- `mostrar_candidatos_presidente_vicepresidente()`: Realiza una consulta SQL para mostrar los nombres de los candidatos a presidente y vicepresidente junto con el nombre del partido al que pertenecen.

```python
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
```

- `mostrar_candidatos_diputados()`: Consulta la cantidad de candidatos por partido que se postulan para cargos de diputados.

```python
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
```

- `mostrar_candidatos_alcalde()`: Muestra los candidatos a alcalde junto con el nombre de su partido.

```python
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
```

- `mostrar_candidatos_por_partido()`: Calcula y muestra la cantidad de candidatos por partido en diferentes cargos.

```python
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
```

- `votaciones_por_departamento()`: Consulta la cantidad de votaciones por departamento.

```python
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
```

- `cantidad_votos_nulos()`: Obtiene la cantidad de votos nulos.

```python
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
```

- `Top10EdadCiudadanos()`: Muestra los 10 ciudadanos más jóvenes que han votado.

```python
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
```

- `Top10CandidatosMasVotadosPresidenteVicepresidente()`: Muestra los 10 candidatos más votados para presidente y vicepresidente.

```python
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
```

- `Top5MesasMasFrecuentadas()`: Muestra las 5 mesas de votación más frecuentadas.

```python
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
```

- `Top5HoraMasConcurrida()`: Indica las 5 horas más concurridas en las votaciones.

```python
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
```

- `CantidadVotosPorGenero()`: Consulta la cantidad de votos por género.

```python
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
```