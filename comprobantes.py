# ==============================================
# 📸 SISTEMA DE COMPROBANTES DE PAGO
# ==============================================
# Subida y almacenamiento de fotos
# ==============================================

from datetime import datetime
from config import *
from database import *
from logger import *

# ==============================================
# 📤 SUBIR COMPROBANTE
# ==============================================
def guardar_comprobante(id_usuario, nombre_usuario, monto, metodo, file_id):
    """
    Guarda la imagen del comprobante en la base de datos
    file_id: ID de la foto enviada por Telegram
    """
    
    comprobante = {
        "uid": str(id_usuario),
        "nombre": nombre_usuario,
        "monto": float(monto),
        "metodo": metodo,
        "foto_id": file_id,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estado": "PENDIENTE"
    }
    
    insertar_comprobante_db(comprobante)
    log_info(f"COMPROBANTE: Recibido de {nombre_usuario} | Monto: {monto}")
    
    return True, """
✅ <b>¡COMPROBANTE ENVIADO!</b>

📸 Tu pago ha sido registrado.
⏳ Será verificado y acreditado en breve.

Gracias por tu paciencia 🙏
"""

# ==============================================
# 🔍 VER COMPROBANTES PENDIENTES (ADMIN)
# ==============================================
def ver_comprobantes_pendientes():
    """Muestra lista de pagos esperando aprobación"""
    
    compras = obtener_comprobantes_pendientes_db()
    
    if not compras:
        return "✅ No hay pagos pendientes", None
    
    texto = "📸 <b>COMPROBANTES PENDIENTES DE APROBACIÓN</b>\n\n"
    
    for c in compras:
        texto += f"👤 <b>{c['nombre']}</b>\n"
        texto += f"💰 Monto: {MONEDA} {c['monto']:.2f}\n"
        texto += f"💳 Método: {c['metodo']}\n"
        texto += f"🆔 ID: <code>{c['uid']}</code>\n"
        texto += f"📅 {c['fecha']}\n"
        texto += "────────────────────\n"
    
    return texto, compras
