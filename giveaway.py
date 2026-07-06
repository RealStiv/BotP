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
# 🆕 CREAR SORTEO
# ==============================================
def crear_sorteo(titulo, premio, tipo="saldo", cantidad=0, dias_duracion=7):
    id_sorteo = f"SORTEO-{int(time.time())}"
    inicio = datetime.now()
    fin = inicio + timedelta(days=dias_duracion)
    
    sorteo = {
        "id": id_sorteo,
        "titulo": titulo,
        "premio": premio,
        "tipo": tipo,
        "cantidad": cantidad,
        "inicio": inicio.strftime("%d/%m/%Y %H:%M"),
        "fin": fin.strftime("%d/%m/%Y %H:%M"),
        "participantes": [],
        "ganadores": [],
        "estado": "ACTIVO"
    }
    
    # Guardar en MongoDB
    insertar_sorteo_db(sorteo)
    
    # 📝 LOG
    log_info(f"SORTEO CREADO | ID: {id_sorteo} | TITULO: {titulo} | PREMIO: {premio}")
    
    return id_sorteo

# ==============================================
# 🎟️ PARTICIPAR
# ==============================================
def participar(uid, id_sorteo):
    uid = str(uid)
    
    # Obtener sorteo
    sorteo = obtener_sorteo_db(id_sorteo)
    
    if not sorteo:
        return False, "❌ Sorteo no encontrado"
    
    if sorteo["estado"] != "ACTIVO":
        return False, "⏳ Sorteo finalizado"
    
    if uid in sorteo["participantes"]:
        return False, "✅ Ya estás participando! 🍀"
    
    # Agregar participante
    sorteo["participantes"].append(uid)
    actualizar_sorteo_db(id_sorteo, {"participantes": sorteo["participantes"]})
    
    return True, f"🎉 ¡Registrado!\n👥 Total: {len(sorteo['participantes'])}"

# ==============================================
# 🏆 ELEGIR GANADORES
# ==============================================
def elegir_ganadores(id_sorteo, cantidad=1):
    sorteo = obtener_sorteo_db(id_sorteo)
    
    if not sorteo:
        return None, "No existe"
    
    if len(sorteo["participantes"]) == 0:
        return [], "Sin participantes"
    
    # Seleccionar ganadores
    random.shuffle(sorteo["participantes"])
    ganadores_ids = sorteo["participantes"][:cantidad]
    
    # Actualizar estado y guardar ganadores
    datos_actualizar = {
        "estado": "FINALIZADO",
        "ganadores": ganadores_ids
    }
    actualizar_sorteo_db(id_sorteo, datos_actualizar)
    
    # 📝 LOG
    log_info(f"SORTEO FINALIZADO | ID: {id_sorteo} | GANADORES: {len(ganadores_ids)}")
    
    return ganadores_ids, "Finalizado"

# ==============================================
# 💸 ENTREGAR PREMIO
# ==============================================
def entregar_premio(id_sorteo):
    """Entrega el premio usando la base de datos MongoDB"""
    sorteo = obtener_sorteo_db(id_sorteo)
    
    if not sorteo or not sorteo.get("ganadores"):
        return False
    
    for uid in sorteo["ganadores"]:
        if sorteo["tipo"] == "saldo":
            # Agregar saldo al usuario
            actualizar_usuario_db(uid, {"$inc": {"saldo": sorteo["cantidad"]}})
            
            # 📝 LOG
            log_info(f"PREMIO ENTREGADO | USUARIO: {uid} | MONTO: {sorteo['cantidad']}")
            
            # Notificar al usuario
            try:
                from main import bot
                bot.send_message(uid, f"""
🎉 <b>¡FELICIDADES! ERES GANADOR 🎉</b>

🏆 Sorteo: <b>{sorteo['titulo']}</b>
🎁 Has ganado: <b>{MONEDA} {sorteo['cantidad']:.2f}</b>
💰 Saldo agregado a tu cuenta!
""")
            except:
                pass
    
    return True

# ==============================================
# 📋 LISTAR SORTEOS ACTIVOS
# ==============================================
def listar_sorteos():
    sorteos = obtener_sorteos_activos_db()
    
    if not sorteos:
        return "📭 No hay sorteos activos"
    
    texto = "🎁 <b>SORTEOS ACTIVOS</b>\n\n"
    for s in sorteos:
        texto += f"""
━━━━━━━━━━━━━━━━━━━━━
🏆 <b>{s['titulo']}</b>
🎁 Premio: {s['premio']}
👥 Participantes: {len(s['participantes'])}
📅 Fin: {s['fin']}
🆔 ID: <code>{s['id']}</code>
━━━━━━━━━━━━━━━━━━━━━
"""
    texto += "\n🔘 Usa /participar [ID]"
    return texto

# ==============================================
# 📜 VER HISTORIAL DE SORTEOS
# ==============================================
def historial_sorteos():
    return obtener_sorteos_finalizados_db()
