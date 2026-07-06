# ==============================================
# 🔐 SISTEMA DE GESTIÓN DE USUARIOS
# ==============================================
# ✅ VERSIÓN MONGODB - COMPATIBLE CON RAILWAY
# ==============================================
from datetime import datetime
from pymongo import MongoClient
import os

# 🍃 CONEXIÓN DIRECTA A MONGODB
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME")]

# 📂 COLECCIÓN
usuarios_col = db["usuarios"]

# ==============================================
# ✅ VERIFICAR Y REGISTRAR USUARIO
# ==============================================
def verificar_o_crear_usuario(uid, nombre="Usuario"):
    """
    Verifica si el usuario existe en MongoDB.
    Si NO existe: lo crea con datos iniciales.
    Si SÍ existe: solo devuelve los datos.
    """
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
    uid = str(uid)
    usuario = usuarios_col.find_one({"id": uid})
    return usuario.get("saldo", 0.00) if usuario else 0.00

def obtener_nivel(uid):
    uid = str(uid)
    usuario = usuarios_col.find_one({"id": uid})
    return usuario.get("nivel", "👤 Usuario Normal") if usuario else "👤 Usuario Normal"

# ==============================================
# 📋 OBTENER DATOS COMPLETOS
# ==============================================
def get_user_data(uid):
    uid = str(uid)
    return usuarios_col.find_one({"id": uid})

def listar_todos():
    return list(usuarios_col.find())

# ==============================================
# 🧹 LIMPIEZA Y MANTENIMIENTO
# ==============================================
def usuario_existe(uid):
    return usuarios_col.find_one({"id": str(uid)}) is not None

# ==============================================
# 🔄 FUNCIONES COMPATIBLES CON EL MAIN
# ==============================================
# Para que no tengas que cambiar nada en el código principal
def verificar_usuario(uid, nombre):
    return verificar_o_crear_usuario(uid, nombre)

def obtener_datos_usuario(uid):
    return get_user_data(uid)
