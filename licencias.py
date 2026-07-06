# ==============================================
# 🔑 SISTEMA DE LICENCIAS Y KEYS - VERSIÓN DIOS
# ==============================================
# ✅ Generación, Validación, Activación y Control
# ✅ Base de Datos MONGODB 🍃
# ✅ Logs Automáticos y Notificaciones
# ==============================================

import random
import string
from datetime import datetime, timedelta
from config import *
from logger import *
from database import *  # 🍃 Conexión MongoDB

# ==============================================
# 🔧 GENERADOR DE KEYS ÚNICAS
# ==============================================
def generar_key(longitud=16):
    """Generar una key en formato XXXX-XXXX-XXXX-XXXX"""
    caracteres = string.ascii_uppercase + string.digits
    key = '-'.join([
        ''.join(random.choice(caracteres) for _ in range(4))
        for _ in range(4)
    ])
    return key

# ==============================================
# ➕ CREAR NUEVA LICENCIA
# ==============================================
def crear_licencia(tipo="PREMIUM", duracion=30, usos_max=1):
    """
    Crear una nueva licencia
    tipo: Nombre del plan
    duracion: días de validez
    usos_max: cantidad de activaciones permitidas
    """
    key = generar_key()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    licencia = {
        "key": key,
        "tipo": tipo,
        "duracion": duracion,
        "usos_max": usos_max,
        "usados": 0,
        "fecha_creacion": fecha,
        "estado": "ACTIVA"
    }
    
    # Insertar en MongoDB
    insertar_licencia_db(licencia)
    
    # 📝 LOG
    log_info(f"LICENCIA CREADA | KEY: {key} | TIPO: {tipo} | DURACION: {duracion}d | USOS: {usos_max}")
    
    return key

# ==============================================
# ✅ VALIDAR LICENCIA
# ==============================================
def validar_licencia(key):
    """Verificar si la key existe y está activa"""
    data = obtener_licencia_db(key)
    
    if not data:
        return False, "❌ Key no existe o es inválida"
    
    if data['estado'] != "ACTIVA":
        return False, "🔒 Esta key ha sido desactivada"
    
    if data['usados'] >= data['usos_max']:
        return False, "⚠️ Esta key ya ha sido usada completamente"
    
    return True, data

# ==============================================
# 🚀 ACTIVAR LICENCIA
# ==============================================
def activar_licencia(uid, nombre, key):
    """Activar licencia para un usuario específico"""
    
    valido, datos = validar_licencia(key)
    
    if not valido:
        return False, datos
    
    # Verificar si ya la usó este usuario
    if verificar_uso_licencia(key, uid):
        return False, "✅ Ya tienes activada esta licencia"
    
    # Calcular fecha de expiración
    dias = datos['duracion']
    fecha_inicio = datetime.now()
    fecha_fin = fecha_inicio + timedelta(days=dias)
    
    # Actualizar contador de usos
    actualizar_usos_licencia(key)
    
    # Registrar uso
    registro_uso = {
        "key": key,
        "uid": str(uid),
        "nombre": nombre,
        "fecha_uso": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    insertar_uso_licencia(registro_uso)
    
    # 📝 GUARDAR EN DATOS DEL USUARIO
    actualizar_licencia_usuario(uid, datos['tipo'], dias, fecha_fin.strftime("%d/%m/%Y"))
    
    # 📢 LOG EN CANAL
    txt = f"""
🔑 <b>✅ LICENCIA ACTIVADA</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Usuario: <code>{nombre}</code>
🆔 ID: <code>{uid}</code>
🔐 Key: <code>{key}</code>
💎 Plan: <b>{datos['tipo']}</b>
📅 Expira: <code>{fecha_fin.strftime("%d/%m/%Y")}</code>
"""
    log_info(f"LICENCIA ACTIVADA | USUARIO: {uid} | KEY: {key} | PLAN: {datos['tipo']}")
    enviar_a_canal(txt)
    
    return True, f"""
✅ <b>¡LICENCIA ACTIVADA CORRECTAMENTE!</b>

💎 Plan: <b>{datos['tipo']}</b>
📅 Válido hasta: <code>{fecha_fin.strftime("%d/%m/%Y")}</code>

¡Disfruta de todas las funciones! 🚀
"""

# ==============================================
# 👤 GESTIÓN POR USUARIO
# ==============================================
def actualizar_licencia_usuario(uid, plan, dias, fecha_fin):
    """Actualizar datos de licencia en la colección usuarios"""
    datos = {
        "licencia_plan": plan,
        "licencia_fin": fecha_fin
    }
    actualizar_usuario_db(uid, datos)

def verificar_licencia_usuario(uid):
    """Verificar si el usuario tiene licencia activa"""
    usuario = obtener_usuario_db(uid)
    
    if not usuario or 'licencia_plan' not in usuario or not usuario['licencia_plan']:
        return False, "🔒 Necesitas una licencia para usar el bot"
    
    # Verificar fecha de expiración
    try:
        fecha_fin = datetime.strptime(usuario['licencia_fin'], "%d/%m/%Y")
        if datetime.now() > fecha_fin:
            return False, "⏳ Tu licencia ha expirado"
    except:
        pass
    
    return True, usuario['licencia_plan']

# ==============================================
# 📋 VER INFORMACIÓN DE UNA KEY
# ==============================================
def ver_info_key(key):
    data = obtener_licencia_db(key)
    
    if not data:
        return "❌ Key no encontrada"
    
    # Obtener historial de usos
    usos = obtener_usuarios_licencia(key)
    
    texto = f"""
🔐 <b>INFORMACIÓN DE LICENCIA</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 Key: <code>{data['key']}</code>
💎 Plan: <b>{data['tipo']}</b>
⏳ Duración: <code>{data['duracion']} días</code>
🔢 Usos: <code>{data['usados']}/{data['usos_max']}</code>
📅 Creada: <code>{data['fecha_creacion']}</code>
📊 Estado: <b>{data['estado']}</b>

👥 <b>Usuarios que la usaron:</b>
"""
    for u in usos:
        texto += f"• {u['nombre']} - {u['fecha_uso']}\n"
    
    return texto

# ==============================================
# ⛔ DESACTIVAR KEY
# ==============================================
def desactivar_key(key):
    actualizar_estado_licencia(key, "DESACTIVADA")
    log_info(f"KEY DESACTIVADA | {key}")
    return "✅ Key desactivada correctamente"

# ==============================================
# 📊 ESTADÍSTICAS
# ==============================================
def stats_licencias():
    total = total_licencias_db()
    activas = licencias_activas_db()
    usos = total_usos_licencias_db()
    
    return f"""
📊 <b>ESTADÍSTICAS DE LICENCIAS</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 Total creadas: <code>{total}</code>
✅ Activas: <code>{activas}</code>
🔄 Total usos: <code>{usos}</code>
"""
