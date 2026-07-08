# ==============================================
# 🎫 SISTEMA DE SOPORTE Y TICKETS
# ==============================================
# Módulo de atención al cliente
# ==============================================

from datetime import datetime
from config import *
from database import *
from logger import *

# ==============================================
# 📩 ABRIR NUEVO TICKET
# ==============================================
def abrir_ticket(id_usuario, nombre_usuario, mensaje_usuario):
    """
    Crea un nuevo ticket de soporte en la base de datos.
    Args:
        id_usuario: ID del usuario que contacta
        nombre_usuario: Nombre del usuario
        mensaje_usuario: Texto del consulta o problema
    Returns:
        (bool, str): Éxito y mensaje de confirmación
    """

    nuevo_ticket = {
        "uid": str(id_usuario),
        "nombre": nombre_usuario,
        "mensaje": mensaje_usuario,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estado": "ABIERTO"
    }

    # Guardar en base de datos
    insertar_ticket_db(nuevo_ticket)
    
    # Registro en sistema
    log_info(f"🎫 NUEVO TICKET: Usuario {nombre_usuario} (ID: {id_usuario})")

    # Respuesta al usuario
    return True, "✅ <b>Ticket creado correctamente</b>\nUn administrador te responderá lo antes posible."

# ==============================================
# 📋 VER TICKETS PENDIENTES (PANEL ADMIN)
# ==============================================
def listar_tickets_abiertos():
    """
    Obtiene y formatea todos los tickets con estado 'ABIERTO'
    para que los vea el administrador.
    """
    
    tickets = obtener_tickets_abiertos_db()

    if not tickets:
        return "✅ No hay tickets pendientes de atención en este momento."

    # Construir mensaje formateado
    texto_panel = "🎫 <b>TICKETS DE SOPORTE ABIERTOS</b>\n\n"

    for ticket in tickets:
        texto_panel += f"👤 <b>{ticket['nombre']}</b> (<code>{ticket['uid']}</code>)\n"
        texto_panel += f"💬 {ticket['mensaje']}\n"
        texto_panel += f"⏰ {ticket['fecha']}\n"
        texto_panel += f"🔘 <code>/responder {ticket['uid']} [tu respuesta]</code>\n\n"

    return texto_panel
