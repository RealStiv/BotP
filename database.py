# ==============================================
# 🔐 SISTEMA DE GESTIÓN DE USUARIOS
# ==============================================
from datetime import datetime

# 🗄️ BASE DE DATOS DE USUARIOS (Solo se crea UNO por ID)
usuarios = {}

# ==============================================
# ✅ VERIFICAR Y REGISTRAR USUARIO
# ==============================================
def verificar_o_crear_usuario(uid, nombre="Usuario"):
    """
    Verifica si el usuario existe.
    Si NO existe: lo crea con datos iniciales.
    Si SÍ existe: solo devuelve los datos.
    ¡NUNCA DUPLICA!
    """
    uid = str(uid) # Convertimos a string para seguridad
    
    if uid not in usuarios:
        # 🆕 NUEVO USUARIO - Se registra una sola vez
        usuarios[uid] = {
            "nombre": nombre,
            "id": uid,
            "saldo": 0.00,
            "nivel": "👤 Usuario Normal",
            "registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "ultimo_acceso": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        print(f"✅ Nuevo usuario registrado: {nombre} (ID: {uid})")
        return True # Retorna True si es nuevo
        
    else:
        # 🔄 USUARIO EXISTENTE - Solo actualizamos última visita
        usuarios[uid]["ultimo_acceso"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        return False # Retorna False si ya existía

# ==============================================
# 💰 GESTIÓN DE SALDO
# ==============================================
def actualizar_saldo(uid, cantidad, motivo="Operación"):
    """Suma o resta saldo de forma segura"""
    uid = str(uid)
    
    if uid not in usuarios:
        return 0 # Error si no existe
        
    usuarios[uid]["saldo"] += cantidad
    usuarios[uid]["saldo"] = round(usuarios[uid]["saldo"], 2) # Redondear a 2 decimales
    
    # 🏆 Actualizar nivel automáticamente
    saldo_actual = usuarios[uid]["saldo"]
    if saldo_actual >= 1000:
        usuarios[uid]["nivel"] = "💎 VIP DIAMANTE"
    elif saldo_actual >= 500:
        usuarios[uid]["nivel"] = "🥇 VIP ORO"
    elif saldo_actual >= 100:
        usuarios[uid]["nivel"] = "🥈 VIP PLATA"
    else:
        usuarios[uid]["nivel"] = "👤 Usuario Normal"
        
    return usuarios[uid]["saldo"]

def obtener_saldo(uid):
    uid = str(uid)
    return usuarios.get(uid, {}).get("saldo", 0.00)

def obtener_nivel(uid):
    uid = str(uid)
    return usuarios.get(uid, {}).get("nivel", "👤 Usuario Normal")

# ==============================================
# 📋 OBTENER DATOS COMPLETOS
# ==============================================
def get_user_data(uid):
    uid = str(uid)
    return usuarios.get(uid, None)

def listar_todos():
    return usuarios

# ==============================================
# 🧹 LIMPIEZA Y MANTENIMIENTO
# ==============================================
def usuario_existe(uid):
    return str(uid) in usuarios
