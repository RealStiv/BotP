# ==============================================
# 📢 SISTEMA DE NOTIFICACIONES MASIVAS
# ==============================================
# Enviar mensaje a todos los usuarios
# ==============================================

from config import *
from database import *
from logger import *

def enviar_broadcast(bot, mensaje, admin_id):
    """Envía mensaje a TODOS los usuarios"""
    
    if str(admin_id) != str(ADMIN_ID):
        return "❌ No permitido"
    
    usuarios = obtener_todos_usuarios_db()
    enviados = 0
    fallidos = 0
    
    log_info(f"BROADCAST: Iniciando envío a {len(usuarios)} usuarios")
    
    for usuario in usuarios:
        try:
            uid = int(usuario['id'])
            bot.send_message(uid, mensaje, parse_mode="HTML")
            enviados += 1
        except:
            fallidos += 1
    
    resultado = f"""
📢 <b>ENVÍO COMPLETO</b>

✅ Enviados: <code>{enviados}</code>
❌ Fallidos: <code>{fallidos}</code>
📊 Total: <code>{len(usuarios)}</code>
"""
    
    log_info(f"BROADCAST: Finalizado | OK: {enviados} | FAIL: {fallidos}")
    return resultado
