# ==============================================
# 📜 SISTEMA DE HISTORIAL Y MOVIMIENTOS
# ==============================================
# Registro completo de todas las acciones
# ==============================================

from datetime import datetime
from config import *
from database import *

# ==============================================
# ➕ REGISTRAR ACCIÓN EN LA DB
# ==============================================
def registrar_movimiento(id_usuario, nombre_usuario, tipo, monto, descripcion):
    """
    Guarda cualquier operación en la base de datos.
    Tipos: RECARGA, COMPRA, PREMIUM, RETIRO, BONO
    """
    
    nuevo_movimiento = {
        "uid": str(id_usuario),
        "nombre": nombre_usuario,
        "tipo": tipo,
        "monto": float(monto),
        "descripcion": descripcion,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    insertar_movimiento_db(nuevo_movimiento)
    return True

# ==============================================
# 📋 VER HISTORIAL DEL USUARIO
# ==============================================
def ver_historial_usuario(id_usuario):
    """
    Muestra los últimos 15 movimientos ordenados del más nuevo al más viejo.
    """
    
    movimientos = obtener_movimientos_usuario_db(str(id_usuario))
    
    if not movimientos:
        return "📭 <b>No tienes movimientos aún</b>\n\nRealiza tu primera operación para ver el historial."
    
    texto = "📜 <b>HISTORIAL DE MOVIMIENTOS</b>\n\n"
    
    # Iconos según el tipo de movimiento
    iconos = {
        "RECARGA": "💵",
        "COMPRA": "🛒",
        "PREMIUM": "🎬",
        "RETIRO": "📤",
        "BONO": "🎁"
    }
    
    # Mostrar últimos 15, ordenados nuevos primero
    for mov in reversed(movimientos[-15:]):
        icono = iconos.get(mov['tipo'], "🔹")
        texto += f"{icono} <b>{mov['tipo']}</b>\n"
        texto += f"💸 Monto: {MONEDA} {mov['monto']:.2f}\n"
        texto += f"📝 {mov['descripcion']}\n"
        texto += f"⏰ {mov['fecha']}\n"
        texto += "────────────────────\n"
    
    return texto
