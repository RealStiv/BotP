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
from logger import *      # 📝 SISTEMA DE LOGS
from database import *    # 🍃 MONGODB

# ==============================================
# ⚙️ CONFIGURACIÓN DE SEGURIDAD
# ==============================================
INTENTOS_MAXIMOS = 30
TIEMPO_BLOQUEO = 300  # 5 minutos en segundos

# ==============================================
# 🗄️ BASE DE DATOS DE BLOQUEOS
# ==============================================
sistema_bloqueos = {}
historial_acciones = {}

# ==============================================
# 🚫 ANTI-SPAM Y ANTI-FLOOD AVANZADO
# ==============================================
def anti_spam(uid, accion="general"):
    """
    Detecta acciones repetitivas y bloquea temporalmente
    """
    uid = str(uid)
    ahora = time.time()
    
    # Inicializar estructuras
    if uid not in historial_acciones:
        historial_acciones[uid] = {}
    if accion not in historial_acciones[uid]:
        historial_acciones[uid][accion] = []
    
    # Limpiar acciones antiguas (mayores a 60 seg)
    historial_acciones[uid][accion] = [
        t for t in historial_acciones[uid][accion] 
        if ahora - t < 60
    ]
    
    # Agregar acción actual
    historial_acciones[uid][accion].append(ahora)
    
    # Verificar límite
    if len(historial_acciones[uid][accion]) > INTENTOS_MAXIMOS:
        if uid not in sistema_bloqueos:
            sistema_bloqueos[uid] = {
                "hasta": ahora + TIEMPO_BLOQUEO,
                "razon": f"Spam en: {accion}",
                "fecha_bloqueo": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            
            # 📝 LOG
            log_warning(f"🔒 USUARIO BLOQUEADO POR SPAM | ID: {uid} | Acción: {accion}")
            
            # Notificar a admin
            try:
                from main import bot
                bot.send_message(ADMIN_ID, f"""
⚠️ <b>ALERTA DE SEGURIDAD</b>

🔒 Usuario bloqueado automáticamente
🆔 ID: <code>{uid}</code>
📝 Motivo: Spam/Flood en {accion}
⏳ Duración: 5 minutos
""", parse_mode="HTML")
            except Exception as e:
                log_error("NOTIFICACION", f"No se pudo avisar a admin: {e}")
            
        return False
    
    return True

# ==============================================
# ⏱️ VERIFICAR ESTADO DE BLOQUEO
# ==============================================
def verificar_bloqueo(uid):
    """
    Retorna: (esta_bloqueado, minutos_restantes)
    """
    uid = str(uid)
    ahora = time.time()
    
    if uid in sistema_bloqueos:
        if ahora < sistema_bloqueos[uid]["hasta"]:
            tiempo_restante = int(sistema_bloqueos[uid]["hasta"] - ahora)
            minutos = tiempo_restante // 60
            return True, minutos
        else:
            # Desbloquear automáticamente
            del sistema_bloqueos[uid]
            log_info(f"✅ USUARIO DESBLOQUEADO | ID: {uid}")
    
    return False, 0

# ==============================================
# 🧹 SANITIZADOR DE TEXTO (ANTI-INYECCIÓN)
# ==============================================
def sanitizar_texto(texto):
    """
    Limpia el texto eliminando caracteres peligrosos
    """
    if not texto:
        return ""
    
    texto = str(texto)[:500]  # Limitar longitud
    
    # Patrones peligrosos
    patrones = [
        r'`', r'~', r'\|', r';', r'\$', 
        r'exec\(', r'eval\(', r'__', r'import',
        r'--', r'\/\*', r'\*\/', r'UNION', r'SELECT'
    ]
    
    for p in patrones:
        texto = re.sub(p, '', texto, flags=re.IGNORECASE)
    
    return texto.strip()

# ==============================================
# 🔒 VALIDADOR DE LINKS SEGUROS
# ==============================================
def validar_link_seguro(link):
    """
    Verifica que el enlace sea de un dominio permitido
    """
    if not link:
        return False
    
    link = link.lower().strip()
    
    # Verificar estructura básica
    if not link.startswith('http'):
        return False
    if len(link) < 15 or len(link) > 500:
        return False
    
    # Dominios permitidos
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
    
    return any(dominio in link for dominio in dominios_permitidos)

# ==============================================
# 🛑 BLOQUEO MANUAL POR ADMIN
# ==============================================
def bloquear_usuario(uid, razon="Manual por Admin"):
    """Bloquear usuario permanentemente o por tiempo"""
    uid = str(uid)
    sistema_bloqueos[uid] = {
        "hasta": time.time() + 86400,  # 24 horas por defecto
        "razon": razon,
        "fecha_bloqueo": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    log_warning(f"⛔ USUARIO BLOQUEADO MANUALMENTE | ID: {uid} | Razón: {razon}")
    return True

def desbloquear_usuario(uid):
    """Desbloquear usuario"""
    uid = str(uid)
    if uid in sistema_bloqueos:
        del sistema_bloqueos[uid]
        log_info(f"✅ USUARIO DESBLOQUEADO | ID: {uid}")
        return True
    return False

# ==============================================
# 📊 ESTADÍSTICAS DE SEGURIDAD
# ==============================================
def stats_seguridad():
    return f"""
🛡️ <b>ESTADÍSTICAS DE SEGURIDAD</b>

👥 Usuarios bloqueados ahora: <code>{len(sistema_bloqueos)}</code>
⚙️ Límite de acciones: <code>{INTENTOS_MAXIMOS}/min</code>
⏳ Tiempo de bloqueo: <code>{TIEMPO_BLOQUEO//60} min</code>
"""

# ==============================================
# 📝 FUNCIÓN LOG_WARNING (SI NO EXISTE EN LOGGER)
# ==============================================
def log_warning(mensaje):
    """Función para logs de advertencia"""
    print(f"[WARNING] {mensaje}")
    try:
        from logger import enviar_a_canal
        txt = f"""
⚠️ <b>ADVERTENCIA DE SEGURIDAD</b>
📝 {mensaje}
📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
        enviar_a_canal(txt)
    except:
        pass
