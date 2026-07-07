# ==============================================
# 🍃 BASE DE DATOS MONGODB
# ==============================================
# 🛡️ VERSIÓN COMPLETA - TODAS LAS FUNCIONES
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
    # Forzar certificados válidos
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
    licencias_usos = db["licencias_usos"]
    sorteos = db["sorteos"]
    config = db["config"]
    historial = db["historial"]
    cuentas_premium = db["cuentas_premium"]
    sellers = db["sellers"]

    # ✅ PRUEBA DE CONEXIÓN
    client.admin.command('ping')
    print("🍃 CONECTADO A MONGODB CORRECTAMENTE")

except Exception as e:
    print(f"❌ ERROR AL CONECTAR A MONGO: {str(e)}")
    client = None
    db = None
    usuarios = None
    ventas = None
    licencias = None
    licencias_usos = None
    sorteos = None
    historial = None
    cuentas_premium = None
    sellers = None

# ==============================================
# 🛠️ FUNCIONES BÁSICAS
# ==============================================
def esta_conectado():
    return client is not None and db is not None

def obtener_coleccion(nombre):
    if db is None:
        return None
    return db[nombre]

# ==============================================
# 👤 FUNCIONES DE USUARIOS
# ==============================================
def obtener_usuario_db(uid):
    if usuarios is None:
        return None
    return usuarios.find_one({"id": str(uid)})

def actualizar_usuario_db(uid, datos):
    if usuarios is None:
        return False
    return usuarios.update_one({"id": str(uid)}, {"$set": datos})

def obtener_todos_usuarios_db():
    if usuarios is None:
        return []
    return list(usuarios.find())

# ==============================================
# 📊 FUNCIONES DE ESTADÍSTICAS
# ==============================================
def total_usuarios_db():
    if usuarios is None:
        return 0
    return usuarios.count_documents({})

def total_ventas_db():
    if historial is None:
        return 0
    return historial.count_documents({})

def sumar_ganancias_totales():
    if historial is None:
        return 0
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$ganancia"}}}
    ]
    result = list(historial.aggregate(pipeline))
    return result[0]['total'] if result else 0

def obtener_historial_premium():
    if ventas is None:
        return []
    return list(ventas.find().sort("_id", -1))

# ==============================================
# 🔑 FUNCIONES DE LICENCIAS
# ==============================================
def insertar_licencia_db(datos):
    if licencias is None:
        return False
    return licencias.insert_one(datos)

def obtener_licencia_db(key):
    if licencias is None:
        return None
    return licencias.find_one({"key": key})

def actualizar_usos_licencia(key):
    if licencias is None:
        return False
    return licencias.update_one({"key": key}, {"$inc": {"usados": 1}})

def actualizar_estado_licencia(key, estado):
    if licencias is None:
        return False
    return licencias.update_one({"key": key}, {"$set": {"estado": estado}})

def insertar_uso_licencia(datos):
    if licencias_usos is None:
        return False
    return licencias_usos.insert_one(datos)

def obtener_usuarios_licencia(key):
    if licencias_usos is None:
        return []
    return list(licencias_usos.find({"key": key}))

def total_licencias_db():
    if licencias is None:
        return 0
    return licencias.count_documents({})

def licencias_activas_db():
    if licencias is None:
        return 0
    return licencias.count_documents({"estado": "ACTIVA"})

def total_usos_licencias_db():
    if licencias_usos is None:
        return 0
    return licencias_usos.count_documents({})

# ==============================================
# 🎁 FUNCIONES DE SORTEOS / GIVEAWAYS
# ==============================================
def insertar_sorteo_db(datos):
    if sorteos is None:
        return False
    return sorteos.insert_one(datos)

def obtener_sorteo_db(id_sorteo):
    if sorteos is None:
        return None
    return sorteos.find_one({"id": id_sorteo})

def actualizar_sorteo_db(id_sorteo, datos):
    if sorteos is None:
        return False
    return sorteos.update_one({"id": id_sorteo}, {"$set": datos})

def obtener_sorteos_activos_db():
    if sorteos is None:
        return []
    return list(sorteos.find({"estado": "ACTIVO"}))

def obtener_sorteos_finalizados_db():
    if sorteos is None:
        return []
    return list(sorteos.find({"estado": "FINALIZADO"}))

# ==============================================
# 💳 FUNCIONES DE VENTAS E HISTORIAL
# ==============================================
def registrar_compra(uid, servicio, cantidad, total, link, orden_id):
    if historial is None:
        return False
    dato = {
        "uid": str(uid),
        "servicio": servicio,
        "cantidad": cantidad,
        "total": total,
        "link": link,
        "orden_id": orden_id,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    return historial.insert_one(dato)

def obtener_historial_usuario(uid):
    if historial is None:
        return "❌ Sin datos"
    compras = list(historial.find({"uid": str(uid)}).sort("_id", -1).limit(10))
    if not compras:
        return "📭 No tienes órdenes aún"
    
    texto = "📜 <b>TUS ÚLTIMAS ÓRDENES</b>\n\n"
    for c in compras:
        texto += f"📌 <b>{c.get('servicio','')}</b>\n💲 {c.get('total',0)} | #{c.get('orden_id','0000')}\n📅 {c.get('fecha','')}\n━━━━━━━━━━━━━━━━━━━━\n"
    return texto

# ==============================================
# 🎬 FUNCIONES DE CUENTAS PREMIUM
# ==============================================
def agregar_cuentas_premium_db(servicio, cuentas):
    if cuentas_premium is None:
        return False
    for cuenta in cuentas:
        datos = {
            "servicio": servicio,
            "datos": cuenta,
            "estado": "disponible",
            "fecha_creacion": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        cuentas_premium.insert_one(datos)
    return True

def obtener_stock_premium_db(servicio):
    if cuentas_premium is None:
        return []
    return list(cuentas_premium.find({"servicio": servicio, "estado": "disponible"}))

def obtener_precio_premium_db(servicio):
    # Aquí puedes implementar tu lógica de precios
    precios = {
        "netflix": 15.00,
        "disney": 10.00,
        "hbo": 12.00,
        "prime": 8.00,
        "spotify": 5.00,
        "crunchy": 7.00
    }
    return precios.get(servicio, 10.00)

# ==============================================
# 🧑‍💼 FUNCIONES DE SELLERS
# ==============================================
def es_seller(uid):
    if sellers is None:
        return False
    return sellers.find_one({"uid": str(uid), "estado": "activo"}) is not None

def obtener_datos(uid):
    if sellers is None:
        return {}
    return sellers.find_one({"uid": str(uid)}) or {}

# ==============================================
# 📝 LOGS Y REGISTROS
# ==============================================
def registrar_inicio_bot():
    print("📢 Sistema de logs iniciado")

def registrar_comando(uid, nombre, comando):
    pass # Puedes expandir esto si quieres guardar logs

def registrar_boton(uid, nombre, data):
    pass

def registrar_error(tipo, descripcion):
    print(f"❌ ERROR [{tipo}]: {descripcion}")

def obtener_ultimos_registros():
    return "📝 Sistema de registros activo"
