# ==============================================
# 🎁 SISTEMA DE SORTEOS PRO
# ==============================================
# ✅ Crear, Participar, Elegir Ganadores
# ✅ Base de Datos MONGODB 🍃
# ==============================================

import random
import time
from datetime import datetime, timedelta
from config import *
from logger import *
from database import *  # 🍃 Conexión MongoDB

# ==============================================
# 🆕 CREAR NUEVO SORTEO
# ==============================================
def crear_sorteo(titulo, premio, tipo="saldo", cantidad=0, dias_duracion=7):
    """Crea un nuevo sorteo en la base de datos"""
    
    id_sorteo = f"SORTEO-{int(time.time())}"
    fecha_inicio = datetime.now()
    fecha_fin = fecha_inicio + timedelta(days=dias_duracion)
    
    sorteo = {
        "id": id_sorteo,
        "titulo": titulo,
        "premio": premio,
        "tipo": tipo,
        "cantidad": cantidad,
        "inicio": fecha_inicio.strftime("%d/%m/%Y %H:%M"),
        "fin": fecha_fin.strftime("%d/%m/%Y %H:%M"),
        "participantes": [],
        "ganadores": [],
        "estado": "ACTIVO"
    }
    
    insertar_sorteo_db(sorteo)
    
    # 📝 LOG
    log_info(f"SORTEO CREADO | ID: {id_sorteo} | TITULO: {titulo} | PREMIO: {premio}")
    
    return id_sorteo

# ==============================================
# 🎟️ SISTEMA DE PARTICIPACIÓN
# ==============================================
def participar(id_usuario, id_sorteo):
    """Registra al usuario en el sorteo si es válido"""
    
    id_usuario = str(id_usuario)
    sorteo = obtener_sorteo_db(id_sorteo)
    
    if not sorteo:
        return False, "❌ Sorteo no encontrado"
    
    if sorteo["estado"] != "ACTIVO":
        return False, "⏳ Sorteo finalizado o cerrado"
    
    if id_usuario in sorteo["participantes"]:
        return False, "✅ Ya estás participando! 🍀"
    
    # Agregar participante
    sorteo["participantes"].append(id_usuario)
    actualizar_sorteo_db(id_sorteo, {"participantes": sorteo["participantes"]})
    
    return True, f"🎉 ¡Registrado!\n👥 Total: {len(sorteo['participantes'])} participantes"

# ==============================================
# 🏆 ELEGIR GANADORES
# ==============================================
def elegir_ganadores(id_sorteo, cantidad=1):
    """Selecciona ganadores al azar y cierra el sorteo"""
    
    sorteo = obtener_sorteo_db(id_sorteo)
    
    if not sorteo:
        return None, "❌ Sorteo no existe"
    
    if len(sorteo["participantes"]) == 0:
        return [], "⚠️ No hay participantes para elegir"
    
    # Selección aleatoria
    random.shuffle(sorteo["participantes"])
    ganadores_ids = sorteo["participantes"][:cantidad]
    
    # Actualizar estado
    datos_actualizar = {
        "estado": "FINALIZADO",
        "ganadores": ganadores_ids
    }
    actualizar_sorteo_db(id_sorteo, datos_actualizar)
    
    # 📝 LOG
    log_info(f"SORTEO FINALIZADO | ID: {id_sorteo} | GANADORES: {len(ganadores_ids)}")
    
    return ganadores_ids, "✅ Sorteo finalizado"

# ==============================================
# 💸 ENTREGAR PREMIO AUTOMÁTICO
# ==============================================
def entregar_premio(id_sorteo):
    """Aplica el premio en la cuenta de los ganadores"""
    
    sorteo = obtener_sorteo_db(id_sorteo)
    
    if not sorteo or not sorteo.get("ganadores"):
        return False
    
    for id_usuario in sorteo["ganadores"]:
        if sorteo["tipo"] == "saldo":
            # Agregar saldo
            actualizar_usuario_db(id_usuario, {"$inc": {"saldo": sorteo["cantidad"]}})
            
            # 📝 LOG
            log_info(f"PREMIO ENTREGADO | USUARIO: {id_usuario} | MONTO: {sorteo['cantidad']}")
            
            # Notificación
            try:
                from main import bot
                mensaje = f"""
🎉 <b>¡FELICIDADES! ERES GANADOR 🎉</b>

🏆 Sorteo: <b>{sorteo['titulo']}</b>
🎁 Has ganado: <b>{MONEDA} {sorteo['cantidad']:.2f}</b>
💰 Saldo agregado a tu cuenta!
"""
                bot.send_message(id_usuario, mensaje, parse_mode="HTML")
            except:
                pass
    
    return True

# ==============================================
# 📋 LISTAR SORTEOS ACTIVOS
# ==============================================
def listar_sorteos():
    """Muestra todos los sorteos abiertos actualmente"""
    
    sorteos = obtener_sorteos_activos_db()
    
    if not sorteos:
        return "📭 <b>No hay sorteos activos por el momento</b>"
    
    texto = "🎁 <b>SORTEOS ACTIVOS</b>\n\n"
    
    for s in sorteos:
        texto += f"""
━━━━━━━━━━━━━━━━━━━━━
🏆 <b>{s['titulo']}</b>
🎁 Premio: {s['premio']}
👥 Participantes: {len(s['participantes'])}
📅 Finaliza: {s['fin']}
🆔 ID: <code>{s['id']}</code>
━━━━━━━━━━━━━━━━━━━━━
"""
    texto += "\n🔘 Usa /participar [ID]"
    return texto

# ==============================================
# 📜 HISTORIAL
# ==============================================
def historial_sorteos():
    """Obtiene lista de sorteos finalizados"""
    return obtener_sorteos_finalizados_db()
