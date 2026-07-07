# ==============================================
# 📜 SISTEMA DE HISTORIAL Y MOVIMIENTOS
# ==============================================
# Registro completo de todas las acciones
# ==============================================

from datetime import datetime
from config import *
from database import *

# ==============================================
# ➕ REGISTRAR MOVIMIENTO
# ==============================================
def registrar_movimiento(uid, nombre, tipo, monto, descripcion):
    """
    Registra cualquier acción en la base de datos
    tipos: RECARGA, COMPRA, PREMIUM, RETIRO, BONO
    """
    movimiento = {
        "uid": str(uid),
        "nombre": nombre,
        "tipo": tipo,
        "monto": float(monto),
        "descripcion": descripcion,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    # Guardar en MongoDB
    insertar_movimiento_db(movimiento)
    return True

# ==============================================
# 📋 VER HISTORIAL DEL USUARIO
# ==============================================
def ver_historial_usuario(uid):
    """Muestra los últimos 15 movimientos del usuario"""
    movimientos = obtener_movimientos_usuario_db(str(uid))
    
    if not movimientos:
        return "📭 <b>No tienes movimientos aún</b>\n\nRealiza tu primera operación para ver el historial."
    
    texto = "📜 <b>HISTORIAL DE MOVIMIENTOS</b>\n\n"
    
    # Iconos por tipo
    iconos = {
        "RECARGA": "💵",
        "COMPRA": "🛒",
        "PREMIUM": "🎬",
        "RETIRO": "📤",
        "BONO": "🎁"
    }
    
    for mov in reversed(movimientos[-15:]):  # Ultimos 15, ordenados nuevos primero
        icono = iconos.get(mov['tipo'], "🔹")
        texto += f"{icono} <b>{mov['tipo']}</b>\n"
        texto += f"💸 Monto: {MONEDA} {mov['monto']:.2f}\n"
        texto += f"📝 {mov['descripcion']}\n"
        texto += f"⏰ {mov['fecha']}\n"
        texto += "────────────────────\n"
    
    return texto
