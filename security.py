# ==============================================
# 🛡️ SISTEMA DE SEGURIDAD NIVEL DIOS - v6.0
# ==============================================
# ✅ Anti-Spam, Anti-Flood, Protección SQL Injection
# ✅ Validación de Links y Textos
# ✅ Logs de Seguridad
# ==============================================

import re
import time
from datetime import datetime
from config import *
from logger import *      # 📝 Sistema de registros
from database import *    # 🍃 Conexión MongoDB

# ==============================================
# ⚙️ CONFIGURACIÓN GLOBAL
# ==============================================
INTENTOS_MAXIMOS = 30       # Acciones por minuto
TIEMPO_BLOQUEO = 300       # Segundos (5 minutos)

# ==============================================
# 🗄️ BASE DE DATOS TEMPORAL
# ==============================================
sistema_bloqueos = {}
historial_acciones = {}

# ==============================================
# 🚫 SISTEMA ANTI-SPAM Y ANTI-FLOOD
# ==============================================
def anti_spam(id_usuario, accion="general"):
    """
    Detecta acciones repetitivas y bloquea temporalmente.
    Retorna True si puede continuar, False si está bloqueado.
    """
    id_usuario = str(id_usuario)
    ahora = time.time()
    
    # Inicializar estructuras si no existen
    if id_usuario not in historial_acciones:
        historial_acciones[id_usuario] = {}
    if accion not in historial_acciones[id_usuario]:
        historial_acciones[id_usuario][accion] = []
    
    # Limpiar acciones antiguas (mayores a 60 seg)
    historial_acciones[id_usuario][accion] = [
        t for t in historial_acciones[id_usuario][accion]
        if ahora - t < 60
    ]
    
    # Registrar acción actual
    historial_acciones[id_usuario][accion].append(ahora)
    
    # Verificar límite
    if len(historial_acciones[id_usuario][accion]) > INTENTOS_MAXIMOS:
        if id_usuario not in sistema_bloqueos:
            sistema_bloqueos[id_usuario] = {
                "hasta": ahora + TIEMPO_BLOQUEO,
                "razon": f"Spam/Flood en: {accion}",
                "fecha_bloqueo": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            
            # 📝 Registro en sistema
            log_warning(f"🔒 USUARIO BLOQUEADO | ID: {id_usuario} | Motivo: {accion}")
            
            # Notificar al administrador
            try:
                from main import bot
                bot.send_message(ADMIN_ID, f"""
⚠️ <b>ALERTA DE SEGURIDAD</b>

🔒 Usuario bloqueado automáticamente
🆔 ID: <code>{id_usuario}</code>
📝 Motivo: Spam/Flood en {accion}
⏳ Duración: {TIEMPO_BLOQUEO//60} minutos
""", parse_mode="HTML")
            except Exception as e:
                log_error("NOTIFICACIÓN", f"No se pudo avisar al admin: {e}")
        
        return False  # Bloquear acción
    
    return True  # Permitir acción

# ==============================================
# ⏱️ VERIFICAR ESTADO DE BLOQUEO
# ==============================================
def verificar_bloqueo(id_usuario):
    """
    Retorna: (esta_bloqueado, minutos_restantes)
    """
    id_usuario = str(id_usuario)
    ahora = time.time()
    
    if id_usuario in sistema_bloqueos:
        if ahora < sistema_bloqueos[id_usuario]["hasta"]:
            tiempo_restante = int(sistema_bloqueos[id_usuario]["hasta"] - ahora)
            minutos = tiempo_restante // 60
            return True, minutos
        else:
            # Desbloqueo automático
            del sistema_bloqueos[id_usuario]
            log_info(f"✅ USUARIO DESBLOQUEADO | ID: {id_usuario}")
    
    return False, 0

# ==============================================
# 🧹 SANITIZADOR DE TEXTO (ANTI-INYECCIÓN)
# ==============================================
def sanitizar_texto(texto):
    """
    Limpia el texto eliminando caracteres peligrosos
    y limita la longitud máxima.
    """
    if not texto:
        return ""
    
    texto = str(texto)[:500]  # Límite de seguridad
    
    # Patrones a eliminar
    patrones_peligrosos = [
        r'`', r'~', r'\|', r';', r'\$',
        r'exec\(', r'eval\(', r'__', r'import',
        r'--', r'\/\*', r'\*\/', r'UNION', r'SELECT'
    ]
    
    for patron in patrones_peligrosos:
        texto = re.sub(patron, '', texto, flags=re.IGNORECASE)
    
    return texto.strip()

# ==============================================
# 🔒 VALIDADOR DE LINKS SEGUROS
# ==============================================
def validar_link_seguro(enlace):
    """
    Verifica que el enlace sea de un dominio permitido y seguro.
    """
    if not enlace:
        return False
    
    enlace = enlace.lower().strip()
    
    # Validación básica de estructura
    if not enlace.startswith('http'):
        return False
    if len(enlace) < 15 or len(enlace) > 500:
        return False
    
    # Lista blanca de dominios
    dominios_permitidos = [
        'tiktok.com',
        'instagram.com',
        'facebook.com',
        'youtube.com',
        'youtu.be',
        'telegram.org',
        't.me',
        'twitter.com',
        'x.com',
        'whatsapp.com'
    ]
    
    return any(dominio in enlace for dominio in dominios_permitidos)

# ==============================================
# 🛑 CONTROL MANUAL POR ADMIN
# ==============================================
def bloquear_usuario(id_usuario, razon="Manual por Admin"):
    """Bloquear usuario manualmente (por defecto 24h)"""
    id_usuario = str(id_usuario)
    sistema_bloqueos[id_usuario] = {
        "hasta": time.time() + 86400,  # 24 horas
        "razon": razon,
        "fecha_bloqueo": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    log_warning(f"⛔ BLOQUEO MANUAL | ID: {id_usuario} | Razón: {razon}")
    return True

def desbloquear_usuario(id_usuario):
    """Quitar bloqueo a un usuario"""
    id_usuario = str(id_usuario)
    if id_usuario in sistema_bloqueos:
        del sistema_bloqueos[id_usuario]
        log_info(f"✅ DESBLOQUEO MANUAL | ID: {id_usuario}")
        return True
    return False

# ==============================================
# 📊 ESTADÍSTICAS
# ==============================================
def stats_seguridad():
    return f"""
🛡️ <b>ESTADÍSTICAS DE SEGURIDAD</b>

👥 Usuarios bloqueados ahora: <code>{len(sistema_bloqueos)}</code>
⚙️ Límite de acciones: <code>{INTENTOS_MAXIMOS}/min</code>
⏳ Tiempo de bloqueo: <code>{TIEMPO_BLOQUEO//60} min</code>
"""
