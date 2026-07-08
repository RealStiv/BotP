# ==============================================
# 🔐 SISTEMA DE GESTIÓN DE USUARIOS
# ==============================================
# ✅ VERSIÓN MONGODB - COMPATIBLE CON RAILWAY
# ==============================================
from datetime import datetime
from pymongo import MongoClient
import certifi
from config import MONGO_URI, MONGO_DB_NAME

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
    usuarios_col = db["usuarios"]
    
    print("✅ USERS: Conectado a MongoDB")
    
except Exception as e:
    print(f"❌ USERS: Error de conexión: {str(e)}")
    client = None
    db = None
    usuarios_col = None

# ==============================================
# ✅ VERIFICAR Y REGISTRAR
# ==============================================
def verificar_o_crear_usuario(id_usuario, nombre="Usuario"):
    if usuarios_col is None:
        print("⚠️ Sin conexión a base de datos")
        return False
        
    id_usuario = str(id_usuario)
    usuario = usuarios_col.find_one({"id": id_usuario})
    
    if not usuario:
        datos_nuevo = {
            "id": id_usuario,
            "nombre": nombre,
            "saldo": 0.00,
            "nivel": "👤 Usuario Normal",
            "registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "ultimo_acceso": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "estado": "activo"
        }
        usuarios_col.insert_one(datos_nuevo)
        return True  # Retorna True si es nuevo
    else:
        usuarios_col.update_one(
            {"id": id_usuario},
            {"$set": {"ultimo_acceso": datetime.now().strftime("%d/%m/%Y %H:%M")}}
        )
        return False  # Retorna False si ya existía

# ==============================================
# 💰 GESTIÓN DE SALDO
# ==============================================
def actualizar_saldo(id_usuario, cantidad, motivo="Operación"):
    if usuarios_col is None:
        return 0.00
        
    id_usuario = str(id_usuario)
    usuario = usuarios_col.find_one({"id": id_usuario})
    if not usuario:
        return 0.00
        
    saldo_actual = usuario.get("saldo", 0.00)
    nuevo_saldo = round(saldo_actual + cantidad, 2)
    
    # Auto-asignar nivel según saldo
    if nuevo_saldo >= 1000:
        nivel = "💎 VIP DIAMANTE"
    elif nuevo_saldo >= 500:
        nivel = "🥇 VIP ORO"
    elif nuevo_saldo >= 100:
        nivel = "🥈 VIP PLATA"
    else:
        nivel = "👤 Usuario Normal"
    
    usuarios_col.update_one(
        {"id": id_usuario},
        {"$set": {"saldo": nuevo_saldo, "nivel": nivel}}
    )
    return nuevo_saldo

def obtener_saldo(id_usuario):
    if usuarios_col is None:
        return 0.00
    id_usuario = str(id_usuario)
    usuario = usuarios_col.find_one({"id": id_usuario})
    return usuario.get("saldo", 0.00) if usuario else 0.00

def obtener_nivel(id_usuario):
    if usuarios_col is None:
        return "👤 Usuario Normal"
    id_usuario = str(id_usuario)
    usuario = usuarios_col.find_one({"id": id_usuario})
    return usuario.get("nivel", "👤 Usuario Normal") if usuario else "👤 Usuario Normal"

# ==============================================
# 📋 OBTENER DATOS
# ==============================================
def get_user_data(id_usuario):
    if usuarios_col is None:
        return None
    return usuarios_col.find_one({"id": str(id_usuario)})

def obtener_datos_usuario(id_usuario):
    return get_user_data(id_usuario)

def listar_todos():
    if usuarios_col is None:
        return []
    return list(usuarios_col.find())

def usuario_existe(id_usuario):
    if usuarios_col is None:
        return False
    return usuarios_col.find_one({"id": str(id_usuario)}) is not None

# ==============================================
# 🔄 ALIAS PARA COMPATIBILIDAD
# ==============================================
def verificar_usuario(id_usuario, nombre):
    return verificar_o_crear_usuario(id_usuario, nombre)
