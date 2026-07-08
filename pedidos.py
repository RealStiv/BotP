# ==============================================
# 📦 SISTEMA DE ESTADOS DE PEDIDOS
# ==============================================
# Seguimiento completo de órdenes
# ==============================================

from datetime import datetime
from config import *
from database import *

# ==============================================
# ➕ CREAR NUEVO PEDIDO
# ==============================================
def crear_pedido(id_usuario, nombre_usuario, servicio, monto, tipo="SERVICIO"):
    """
    Crea un nuevo pedido en la base de datos con estado inicial "PAGADO"
    """
    
    nuevo_pedido = {
        "uid": str(id_usuario),
        "nombre": nombre_usuario,
        "servicio": servicio,
        "monto": float(monto),
        "tipo": tipo,
        "estado": "PAGADO",
        "fecha_creacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "historial_estados": [
            {
                "estado": "PAGADO",
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        ]
    }
    
    insertar_pedido_db(nuevo_pedido)
    return nuevo_pedido

# ==============================================
# 🔄 ACTUALIZAR ESTADO
# ==============================================
def cambiar_estado(id_pedido, nuevo_estado):
    """
    Actualiza el estado del pedido y guarda en el historial
    """
    
    pedido = obtener_pedido_db(id_pedido)
    if not pedido:
        return False
    
    # Registrar cambio
    nuevo_historial = {
        "estado": nuevo_estado,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    pedido['historial_estados'].append(nuevo_historial)
    pedido['estado'] = nuevo_estado
    
    actualizar_pedido_db(id_pedido, pedido)
    return True

# ==============================================
# 📋 VER LISTADO DE PEDIDOS DEL USUARIO
# ==============================================
def ver_mis_pedidos(id_usuario):
    """
    Muestra los últimos 10 pedidos del usuario con su estado
    """
    
    pedidos = obtener_pedidos_usuario_db(str(id_usuario))
    
    if not pedidos:
        return "📭 <b>No tienes pedidos aún</b>"
    
    texto = "📦 <b>MIS PEDIDOS Y ÓRDENES</b>\n\n"
    
    iconos_estado = {
        "PAGADO": "💵",
        "PROCESANDO": "🔄",
        "ENVIADO": "📤",
        "ENTREGADO": "✅",
        "CANCELADO": "❌"
    }
    
    for p in pedidos[-10:]:  # Mostrar solo últimos 10
        icono = iconos_estado.get(p['estado'], "🔹")
        texto += f"{icono} <b>{p['servicio']}</b>\n"
        texto += f"📊 Estado: <b>{p['estado']}</b>\n"
        texto += f"💰 {MONEDA} {p['monto']:.2f}\n"
        texto += f"📅 {p['fecha_creacion']}\n"
        texto += "────────────────────\n"
    
    return texto
