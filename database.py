# ==============================================
# 🗄️ SISTEMA DE BASE DE DATOS - COMPLETO
# ==============================================
# ✅ Compatible con TODOS los módulos
# ✅ MongoDB - Conexión Segura
# ==============================================

from datetime import datetime
from pymongo import MongoClient
import certifi
from config import *

# ==============================================
# 🔌 CONEXIÓN SEGURA
# ==============================================
try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True,
        tlsAllowInvalidHostnames=True,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000
    )
    
    db = client[MONGO_DB_NAME]
    
    # 📂 COLECCIONES
    usuarios_col = db["usuarios"]
    movimientos_col = db["movimientos"]
    pedidos_col = db["pedidos"]
    comprobantes_col = db["comprobantes"]
    cupones_col = db["cupones"]
    tickets_col = db["tickets"]
    configuracion_col = db["configuracion"]
    cuentas_premium_col = db["cuentas_premium"]
    precios_col = db["precios"]
    
    print("✅ DATABASE: Conectado correctamente")
    
except Exception as e:
    print(f"❌ DATABASE: Error de conexión: {str(e)}")
    client = None
    db = None
    usuarios_col = None
    movimientos_col = None
    pedidos_col = None
    comprobantes_col = None
    cupones_col = None
    tickets_col = None
    configuracion_col = None
    cuentas_premium_col = None
    precios_col = None

# ==============================================
# 👥 USUARIOS
# ==============================================
def obtener_usuario_db(id_usuario):
    if not usuarios_col: return None
    return usuarios_col.find_one({"id": str(id_usuario)})

def actualizar_usuario_db(id_usuario, datos):
    if not usuarios_col: return False
    return usuarios_col.update_one({"id": str(id_usuario)}, {"$set": datos})

def obtener_todos_usuarios_db():
    if not usuarios_col: return []
    return list(usuarios_col.find())

def total_usuarios_db():
    if not usuarios_col: return 0
    return usuarios_col.count_documents({})

def agregar_saldo_db(id_usuario, monto):
    if not usuarios_col: return False
    usuario = obtener_usuario_db(id_usuario)
    if not usuario: return False
    nuevo_saldo = usuario.get('saldo', 0) + monto
    return actualizar_usuario_db(id_usuario, {"saldo": nuevo_saldo})

def descontar_saldo(id_usuario, monto):
    if not usuarios_col: return False
    usuario = obtener_usuario_db(id_usuario)
    if not usuario: return False
    nuevo_saldo = usuario.get('saldo', 0) - monto
    return actualizar_usuario_db(id_usuario, {"saldo": nuevo_saldo})

def obtener_saldo(id_usuario):
    usuario = obtener_usuario_db(id_usuario)
    return usuario.get('saldo', 0) if usuario else 0

# ==============================================
# 📜 MOVIMIENTOS
# ==============================================
def insertar_movimiento_db(movimiento):
    if not movimientos_col: return False
    return movimientos_col.insert_one(movimiento)

def obtener_movimientos_usuario_db(id_usuario):
    if not movimientos_col: return []
    return list(movimientos_col.find({"uid": str(id_usuario)}))

def obtener_movimientos_fecha_db(fecha):
    if not movimientos_col: return []
    return list(movimientos_col.find({"fecha": fecha}))

def obtener_movimientos_rango_db(fecha_inicio, fecha_fin):
    if not movimientos_col: return []
    return list(movimientos_col.find({
        "fecha": {
            "$gte": fecha_inicio.strftime("%d/%m/%Y"),
            "$lte": fecha_fin.strftime("%d/%m/%Y")
        }
    }))

def sumar_ganancias_totales():
    if not movimientos_col: return 0
    pipeline = [
        {"$match": {"tipo": {"$in": ["RECARGA", "COMPRA", "PREMIUM"]}}},
        {"$group": {"_id": None, "total": {"$sum": "$monto"}}}
    ]
    resultado = list(movimientos_col.aggregate(pipeline))
    return resultado[0]['total'] if resultado else 0

def total_ventas_db():
    if not movimientos_col: return 0
    return movimientos_col.count_documents({"tipo": {"$in": ["COMPRA", "PREMIUM"]}})

def registrar_compra_db(id_usuario, nombre, producto, monto, estado):
    movimiento = {
        "uid": str(id_usuario),
        "nombre": nombre,
        "producto": producto,
        "monto": monto,
        "estado": estado,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": "COMPRA"
    }
    return insertar_movimiento_db(movimiento)

# ==============================================
# 📦 PEDIDOS
# ==============================================
def insertar_pedido_db(pedido):
    if not pedidos_col: return False
    return pedidos_col.insert_one(pedido)

def obtener_pedido_db(pedido_id):
    if not pedidos_col: return None
    return pedidos_col.find_one({"_id": pedido_id})

def actualizar_pedido_db(pedido_id, datos):
    if not pedidos_col: return False
    return pedidos_col.update_one({"_id": pedido_id}, {"$set": datos})

def obtener_pedidos_usuario_db(id_usuario):
    if not pedidos_col: return []
    return list(pedidos_col.find({"uid": str(id_usuario)}))

# ==============================================
# 📸 COMPROBANTES
# ==============================================
def insertar_comprobante_db(comprobante):
    if not comprobantes_col: return False
    return comprobantes_col.insert_one(comprobante)

def obtener_comprobantes_pendientes_db():
    if not comprobantes_col: return []
    return list(comprobantes_col.find({"estado": "PENDIENTE"}))

# ==============================================
# 🎫 CUPONES
# ==============================================
def insertar_cupon_db(cupon):
    if not cupones_col: return False
    return cupones_col.insert_one(cupon)

def buscar_cupon_db(codigo):
    if not cupones_col: return None
    return cupones_col.find_one({"codigo": codigo.upper()})

def actualizar_usos_cupon_db(codigo):
    if not cupones_col: return False
    cupon = buscar_cupon_db(codigo)
    if not cupon: return False
    nuevos_usos = cupon.get('usados', 0) + 1
    return cupones_col.update_one({"codigo": codigo.upper()}, {"$set": {"usados": nuevos_usos}})

def obtener_todos_cupones_db():
    if not cupones_col: return []
    return list(cupones_col.find())

# ==============================================
# 🎫 TICKETS DE SOPORTE
# ==============================================
def insertar_ticket_db(ticket):
    if not tickets_col: return False
    return tickets_col.insert_one(ticket)

def obtener_tickets_abiertos_db():
    if not tickets_col: return []
    return list(tickets_col.find({"estado": "ABIERTO"}))

# ==============================================
# ⚙️ CONFIGURACIÓN
# ==============================================
def obtener_configuracion_db():
    if not configuracion_col: return {}
    config = configuracion_col.find_one()
    if not config:
        default = {
            "mantenimiento": False,
            "bienvenida": "¡Hola! Bienvenido al bot.",
            "oferta": "No hay oferta activa"
        }
        configuracion_col.insert_one(default)
        return default
    return config

def actualizar_configuracion_db(datos):
    if not configuracion_col: return False
    return configuracion_col.update_one({}, {"$set": datos}, upsert=True)

# ==============================================
# 🎬 CUENTAS PREMIUM
# ==============================================
def agregar_cuentas_premium_db(servicio, cuentas):
    if not cuentas_premium_col: return False
    for cuenta_texto in cuentas:
        partes = cuenta_texto.split('|')
        if len(partes) >= 3:
            cuenta = {
                "servicio": servicio,
                "usuario": partes[0].strip(),
                "contraseña": partes[1].strip(),
                "dias": int(partes[2].strip()),
                "estado": "DISPONIBLE"
            }
            cuentas_premium_col.insert_one(cuenta)
    return True

def obtener_stock_premium_db(servicio):
    if not cuentas_premium_col: return []
    return list(cuentas_premium_col.find({"servicio": servicio, "estado": "DISPONIBLE"}))

def obtener_precio_premium_db(servicio):
    if not precios_col: return 0
    precio_data = precios_col.find_one({"servicio": servicio})
    return precio_data.get("precio", 0) if precio_data else 0

def actualizar_precio_premium_db(servicio, precio):
    if not precios_col: return False
    return precios_col.update_one(
        {"servicio": servicio},
        {"$set": {"precio": precio}},
        upsert=True
    )

def obtener_historial_premium():
    if not movimientos_col: return []
    return list(movimientos_col.find({"tipo": "PREMIUM"}))

# ==============================================
# 📊 ESTADÍSTICAS
# ==============================================
def total_usuarios_db():
    if not usuarios_col: return 0
    return usuarios_col.count_documents({})

def sumar_ganancias_totales():
    if not movimientos_col: return 0
    pipeline = [
        {"$match": {"tipo": {"$in": ["RECARGA", "COMPRA", "PREMIUM"]}}},
        {"$group": {"_id": None, "total": {"$sum": "$monto"}}}
    ]
    resultado = list(movimientos_col.aggregate(pipeline))
    return resultado[0]['total'] if resultado else 0
