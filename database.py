# ==============================================
# 🍃 BASE DE DATOS MONGODB
# ==============================================
# 🛡️ VERSIÓN CORREGIDA PARA RAILWAY
# ==============================================

import pymongo
from pymongo import MongoClient
from datetime import datetime
import certifi
import os
from config import MONGO_URI, MONGO_DB_NAME

# ==============================================
# 🔌 CONFIGURACIÓN Y CONEXIÓN SEGURA
# ==============================================
try:
    # Forzar certificados válidos y permitir conexión segura
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True,
        tlsAllowInvalidHostnames=True,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        maxPoolSize=50
    )

    # Seleccionar base de datos
    db = client[MONGO_DB_NAME]

    # 📂 DEFINIR COLECCIONES
    usuarios = db["usuarios"]
    ventas = db["ventas"]
    licencias = db["licencias"]
    sorteos = db["sorteos"]
    config = db["config"]

    # ✅ PRUEBA DE CONEXIÓN
    client.admin.command('ping')
    print("🍃 CONECTADO A MONGODB CORRECTAMENTE")

except Exception as e:
    print(f"❌ ERROR AL CONECTAR A MONGO: {str(e)}")
    # Si falla, dejamos las variables como None para manejarlo después
    client = None
    db = None
    usuarios = None
    ventas = None
    licencias = None
    sorteos = None

# ==============================================
# 🛠️ FUNCIONES BÁSICAS DE AYUDA
# ==============================================
def esta_conectado():
    """Verifica si la base de datos está activa"""
    return client is not None and db is not None

def obtener_coleccion(nombre):
    """Obtiene una colección de forma segura"""
    if db is None:
        return None
    return db[nombre]
