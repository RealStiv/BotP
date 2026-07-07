# ==============================================
# 🔐 SISTEMA DE GESTIÓN DE USUARIOS
# ==============================================
# ✅ VERSIÓN MONGODB - COMPATIBLE CON RAILWAY
# ==============================================

from datetime import datetime
from pymongo import MongoClient
import certifi
import os
from config import MONGO_URI, MONGO_DB_NAME

# ==============================================
# 🔌 CONEXIÓN SEGURA A MONGODB
# ==============================================
try:
    # 🛡️ Configuración especial para evitar errores SSL
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
    usuarios_col = db["usuarios"]
    print("👥 Módulo Usuarios cargado correctamente")

except Exception as e:
    print(f"❌ Error en Users DB: {str(e)}")
    client = None
    db = None
    usuarios_col = None

# ==============================================
# ✅ VERIFICAR Y REGISTRAR USUARIO
# ==============================================
def verificar_o_crear_usuario(uid, nombre="Usuario"):
    """
    Verifica si el usuario existe en MongoDB.
    Si NO existe: lo crea con datos iniciales.
    Si SÍ existe: solo devuelve los datos.
    """
    if usuarios_col is None:
        return False # Sin conexión
        
    uid = str(uid)
    
    # Buscar en la base de datos
    usuario = usuarios_col.find_one({"id": uid})
    
    if not usuario:
        # 🆕 NUEVO USUARIO - Se registra una sola vez
        datos_nuevo = {
            "id": uid,
            "nombre": nombre,
            "saldo": 0.00,
            "nivel": "👤 Usuario Normal",
            "registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "ultimo_acceso": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "estado": "activo"
        }
        usuarios_col.insert_one(datos_nuevo)
        return True # Retorna True si es nuevo
        
    else:
        # 🔄 USUARIO EXISTENTE - Solo actualizamos última visita
        usuarios_col.update_one(
            {"id": uid},
            {"$set": {"ultimo_acceso": datetime.now().strftime("%d/%m/%Y %H:%M")}}
        )
        return False # Retorna False si ya existía

# ==============================================
# 💰 GESTIÓN DE SALDO
# ==============================================
def actualizar_saldo(uid, cantidad, motivo="Operación"):
    """Suma o resta saldo de forma segura en MongoDB"""
    if usuarios_col is None:
        return 0.00
        
    uid = str(uid)
    
    # Obtener saldo actual
    usuario = usuarios_col.find_one({"id": uid})
    if not usuario:
        return 0.00
        
    saldo_actual = usuario.get("saldo", 0.00)
    nuevo_saldo = round(saldo_actual + cantidad, 2)
    
    # 🏆 Actualizar nivel automáticamente
    if nuevo_saldo >= 1000:
        nivel = "💎 VIP DIAMANTE"
    elif nuevo_saldo >= 500:
        nivel = "🥇 VIP ORO"
    elif nuevo_saldo >= 100:
        nivel = "🥈 VIP PLATA"
    else:
        nivel = "👤 Usuario Normal"
    
    # Guardar en base de datos
    usuarios_col.update_one(
        {"id": uid},
        {"$set": {
            "saldo": nuevo_saldo,
            "nivel": nivel
        }}
    )
    
    return nuevo_saldo

def obtener_saldo(uid):
    if usuarios_col is None:
        return 0.00
    uid = str(uid)
    usuario = usuarios_col.find_one({"id": uid})
    return usuario.get("saldo", 0.00) if usuario else 0.00

def obtener_nivel(uid):
    if usuarios_col is None:
        return "👤 Usuario Normal"
    uid = str(uid)
    usuario = usuarios_col.find_one({"id": uid})
    return usuario.get("nivel", "👤 Usuario Normal") if usuario else "👤 Usuario Normal"

# ==============================================
# 📋 OBTENER DATOS COMPLETOS
# ==============================================
def get_user_data(uid):
    if usuarios_col is None:
        return None
    uid = str(uid)
    return usuarios_col.find_one({"id": uid})

def listar_todos():
    if usuarios_col is None:
        return []
    return list(usuarios_col.find())

# ==============================================
# 🧹 LIMPIEZA Y MANTENIMIENTO
# ==============================================
def usuario_existe(uid):
    if usuarios_col is None:
        return False
    return usuarios_col.find_one({"id": str(uid)}) is not None

# ==============================================
# 🔄 FUNCIONES COMPATIBLES CON EL MAIN
# ==============================================
# Para que no tengas que cambiar nada en el código principal
def verificar_usuario(uid, nombre):
    return verificar_o_crear_usuario(uid, nombre)

def obtener_datos_usuario(uid):
    return get_user_data(uid)
