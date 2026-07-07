# ==============================================
# 🎫 SISTEMA DE SOPORTE Y TICKETS
# ==============================================
# Atención al cliente
# ==============================================

from datetime import datetime
from config import *
from database import *
from logger import *

# ==============================================
# 📩 ABRIR TICKET
# ==============================================
def abrir_ticket(uid, nombre, mensaje):
    """Crea un nuevo ticket de soporte"""
    
    ticket = {
        "uid": str(uid),
        "nombre": nombre,
        "mensaje": mensaje,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estado": "ABIERTO"
    }
    
    insertar_ticket_db(ticket)
    log_info(f"TICKET: Nuevo ticket de {nombre} | ID: {uid}")
    
    return True, "✅ <b>Ticket creado</b>\nUn administrador te responderá pronto."

# ==============================================
# 📋 VER TICKETS PENDIENTES (ADMIN)
# ==============================================
def ver_tickets_abiertos():
    tickets = obtener_tickets_abiertos_db()
    
    if not tickets:
        return "✅ No hay tickets pendientes"
    
    texto = "🎫 <b>TICKETS DE SOPORTE ABIERTOS</b>\n\n"
    
    for t in tickets:
        texto += f"👤 <b>{t['nombre']}</b> (<code>{t['uid']}</code>)\n"
        texto += f"💬 {t['mensaje']}\n"
        texto += f"⏰ {t['fecha']}\n"
        texto += f"🔘 /responder {t['uid']} [texto]\n\n"
    
    return texto
