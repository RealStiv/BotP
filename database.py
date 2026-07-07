# ==============================================
# 🍃 CONEXIÓN A MONGODB - VERSIÓN CORREGIDA
# ==============================================
import pymongo
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, MONGO_DB_NAME

# ==============================================
# 🔌 CONECTAR A MONGODB
# ==============================================
try:
    # 🛡️ Configuración especial para Railway y SSL
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,
        tlsAllowInvalidHostnames=True,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000
    )
    
    db = client[MONGO_DB_NAME]
    
    # 📂 COLECCIONES
    usuarios_col = db["usuarios"]
    ventas_col = db["ventas"]
    licencias_col = db["licencias"]
    sorteos_col = db["sorteos"]
    
    print("✅ CONECTADO A MONGODB CORRECTAMENTE")
    
except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN MONGO: {str(e)}")
    exit()

# ==============================================
# ✅ VERIFICAR Y REGISTRAR USUARIO
# ==============================================
def verificar_usuario(uid, nombre="Usuario"):
    """Verifica si existe, si no, lo crea"""
    uid = str(uid)
    
    usuario = usuarios_col.find_one({"id": uid})
    
    if not usuario:
        nuevo_usuario = {
            "id": uid,
            "nombre": nombre,
            "saldo": 0.00,
            "nivel": "👤 Usuario Normal",
            "registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "ultimo_acceso": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "estado": "activo",
            "es_seller": False,
            "comision": 0
        }
        usuarios_col.insert_one(nuevo_usuario)
        print(f"✅ Nuevo usuario: {nombre}")
        return True # Es nuevo
    else:
        # Actualizar última visita
        usuarios_col.update_one(
            {"id": uid},
            {"$set": {"ultimo_acceso": datetime.now().strftime("%d/%m/%Y %H:%M")}}
        )
        return False # Ya existía

# ==============================================
# 💰 GESTIÓN DE SALDO
# ==============================================
def actualizar_saldo(uid, cantidad, motivo="Operación"):
    uid = str(uid)
    usuario = usuarios_col.find_one({"id": uid})
    
    if not usuario:
        return 0
        
    nuevo_saldo = usuario["saldo"] + cantidad
    nuevo_saldo = round(nuevo_saldo, 2)
    
    # Actualizar saldo
    usuarios_col.update_one(
        {"id": uid},
        {"$set": {"saldo": nuevo_saldo}}
    )
    
    # Actualizar nivel automáticamente
    if nuevo_saldo >= 1000:
        nivel = "💎 VIP DIAMANTE"
    elif nuevo_saldo >= 500:
        nivel = "🥇 VIP ORO"
    elif nuevo_saldo >= 100:
        nivel = "🥈 VIP PLATA"
    else:
        nivel = "👤 Usuario Normal"
        
    usuarios_col.update_one(
        {"id": uid},
        {"$set": {"nivel": nivel}}
    )
    
    return nuevo_saldo

def obtener_saldo(uid):
    uid = str(uid)
    usuario = usuarios_col.find_one({"id": uid})
    return usuario.get("saldo", 0.00) if usuario else 0.00

def obtener_nivel(uid):
    uid = str(uid)
    usuario = usuarios_col.find_one({"id": uid})
    return usuario.get("nivel", "👤 Usuario Normal") if usuario else "👤 Usuario Normal"

# ==============================================
# 📋 OBTENER DATOS
# ==============================================
def obtener_datos(uid):
    uid = str(uid)
    return usuarios_col.find_one({"id": uid})

# ==============================================
# 📊 ESTADÍSTICAS
# ==============================================
def total_usuarios_db():
    return usuarios_col.count_documents({})

def obtener_todos_usuarios_db():
    return list(usuarios_col.find())

def obtener_historial_premium():
    return list(ventas_col.find())

def total_ventas_db():
    return ventas_col.count_documents({})
