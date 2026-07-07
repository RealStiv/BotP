# ==============================================
# 📦 SISTEMA DE ESTADOS DE PEDIDOS
# ==============================================
# Seguimiento completo de órdenes
# ==============================================

from datetime import datetime
from config import *
from database import *

# ESTADOS POSIBLES: PAGADO | PROCESANDO | ENVIADO | ENTREGADO | CANCELADO

# ==============================================
# ➕ CREAR PEDIDO
# ==============================================
def crear_pedido(uid, nombre, servicio, monto, tipo="SERVICIO"):
    """Crea un nuevo pedido con estado inicial"""
    
    pedido = {
        "uid": str(uid),
        "nombre": nombre,
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
    
    insertar_pedido_db(pedido)
    return pedido

# ==============================================
# 🔄 CAMBIAR ESTADO
# ==============================================
def cambiar_estado(pedido_id, nuevo_estado):
    """Actualiza el estado y guarda el historial"""
    
    pedido = obtener_pedido_db(pedido_id)
    if not pedido:
        return False
    
    # Agregar al historial
    nuevo_historial = {
        "estado": nuevo_estado,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    pedido['historial_estados'].append(nuevo_historial)
    pedido['estado'] = nuevo_estado
    
    actualizar_pedido_db(pedido_id, pedido)
    return True

# ==============================================
# 📋 VER MIS PEDIDOS
# ==============================================
def ver_mis_pedidos(uid):
    pedidos = obtener_pedidos_usuario_db(str(uid))
    
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
    
    for p in pedidos[-10:]:  # Ultimos 10
        icono = iconos_estado.get(p['estado'], "🔹")
        texto += f"{icono} <b>{p['servicio']}</b>\n"
        texto += f"📊 Estado: <b>{p['estado']}</b>\n"
        texto += f"💰 {MONEDA} {p['monto']:.2f}\n"
        texto += f"📅 {p['fecha_creacion']}\n"
        texto += "────────────────────\n"
    
    return texto
