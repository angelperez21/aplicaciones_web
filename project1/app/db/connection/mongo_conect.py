"""Moudlo para realizar la conexión a MongoDB."""

from pymongo import MongoClient


class Connection:
    """Clase con la que realizamos la conexión a la DB."""

    # URL con la que hacemos la conexión con MongoDB
    MONGO_URI = 'mongodb://127.0.0.1'
    # Cliente con el que nos conectaremos con MongoDB
    client = MongoClient(MONGO_URI)
    # Base de datos a utilizar
    db = client.kinder
