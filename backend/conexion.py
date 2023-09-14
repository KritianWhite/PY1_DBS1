import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def obtener_conexion():
    return mysql.connector.connect(host=os.environ.get('DATABASE_HOST'),
                                user=os.environ.get('DATABASE_USER'),
                                password=os.environ.get('DATABASE_PASSWORD'),
                                db=os.environ.get('DATABASE_NAME'),
                                port=os.environ.get('DATABASE_PORT'))