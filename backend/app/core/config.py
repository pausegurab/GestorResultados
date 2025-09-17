import os
from typing import Annotated
from dotenv import load_dotenv
from pydantic import AnyUrl, BeforeValidator
import mysql.connector
from mysql.connector import Error

load_dotenv()

class Config:
    @staticmethod
    def create_database_if_not_exists():
        """Crea la base de datos MySQL si no existe."""
        try:
            connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                port=Config.MYSQL_PORT
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
                print(f"La base de datos '{Config.MYSQL_DB}' ha sido creada o ya existía.")
                cursor.close()
        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
        finally:
            if connection.is_connected():
                connection.close()
                print("Conexión cerrada.")
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    if ENVIRONMENT == "local":
        MYSQL_DB = os.getenv("MYSQL_DB")
    elif ENVIRONMENT == "testing":
        MYSQL_DB = os.getenv("MYSQL_DB_TEST")
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


    

