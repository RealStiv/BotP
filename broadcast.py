# ==============================================
# 📢 SISTEMA DE NOTIFICACIONES MASIVAS
# ==============================================
# Enviar mensaje a todos los usuarios
# ==============================================

from config import *
from database import *
from logger import *

# ==============================================
# 📨 FUNCIÓN PRINCIPAL
# ==============================================
def enviar_broadcast(bot, mensaje, id_admin):
    """
    Envía un mensaje HTML a todos los usuarios registrados
    """
    
    # Verificar permisos
    if str(id_admin) != str(ADMIN_ID):
        return "❌ Acceso denegado."
    
    # Obtener lista de usuarios
    usuarios = obtener_todos_usuarios_db()
    
    if not usuarios:
        return "📭 No hay usuarios registrados aún."
    
    contador_exitos = 0
    contador_errores = 0
    
    # 📝 LOG de inicio
    log_info(f"BROADCAST: Iniciando envío a {len(usuarios)} usuarios")
    
    for usuario in usuarios:
        try:
            id_destino = int(usuario['id'])
            bot.send_message(id_destino, mensaje, parse_mode="HTML")
            contador_exitos += 1
        except:
            contador_errores += 1
    
    # Reporte final
    resultado = f"""
📢 <b>ENVÍO COMPLETO</b>

✅ Enviados: <code>{contador_exitos}</code>
❌ Fallidos: <code>{contador_errores}</code>
📊 Total: <code>{len(usuarios)}</code>
"""
    
    log_info(f"BROADCAST: Finalizado | OK: {contador_exitos} | FAIL: {contador_errores}")
    return resultado
