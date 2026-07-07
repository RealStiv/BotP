# ==============================================
# ⚙️ PANEL DE CONFIGURACIÓN GLOBAL
# ==============================================
# Control total del bot sin tocar código
# ==============================================

from datetime import datetime
import telebot
from config import *
from database import *
from logger import *

# ==============================================
# 📋 MENÚ PRINCIPAL DE CONFIGURACIÓN
# ==============================================
def panel_configuracion(bot, msg):
    uid = str(msg.from_user.id)
    
    if str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "❌ Acceso denegado.", parse_mode="HTML")
        return
    
    # Obtener configuración actual
    config = obtener_configuracion_db()
    
    estado_mantenimiento = "🔴 ACTIVO" if config.get('mantenimiento', False) else "🟢 INACTIVO"
    mensaje_bienvenida = config.get('bienvenida', '¡Hola! Bienvenido al bot.')
    oferta_del_dia = config.get('oferta', 'No hay oferta activa')
    
    texto = f"""
⚙️ <b>PANEL DE CONFIGURACIÓN GLOBAL</b>

🔧 <b>ESTADO DEL SISTEMA:</b>
• 🛠️ Mantenimiento: <b>{estado_mantenimiento}</b>
• 🤖 Bot: <b>ONLINE</b>

📝 <b>MENSAJES:</b>
• ✉️ Bienvenida: <code>{len(mensaje_bienvenida)} caracteres</code>
• 🏷️ Oferta del día: <i>{oferta_del_dia}</i>

🔘 <b>Selecciona qué deseas cambiar:</b>
"""
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    b1 = telebot.types.InlineKeyboardButton("🛑 Activar/Desactivar Mantenimiento", callback_data="toggle_mantenimiento")
    b2 = telebot.types.InlineKeyboardButton("✏️ Cambiar Mensaje Bienvenida", callback_data="edit_bienvenida")
    b3 = telebot.types.InlineKeyboardButton("🏷️ Poner Oferta del Día", callback_data="edit_oferta")
    b4 = telebot.types.InlineKeyboardButton("🔙 Volver al Admin", callback_data="admin_menu")
    markup.add(b1, b2, b3, b4)
    
    bot.send_message(msg.chat.id, texto, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 🔄 CAMBIAR ESTADO DE MANTENIMIENTO
# ==============================================
def toggle_mantenimiento():
    config = obtener_configuracion_db()
    nuevo_estado = not config.get('mantenimiento', False)
    
    actualizar_configuracion_db({"mantenimiento": nuevo_estado})
    
    if nuevo_estado:
        log_info("CONFIG: MODO MANTENIMIENTO ACTIVADO")
        return "🔴 <b>MODO MANTENIMIENTO ACTIVADO</b>\nLos usuarios no podrán usar el bot."
    else:
        log_info("CONFIG: MODO MANTENIMIENTO DESACTIVADO")
        return "🟢 <b>SISTEMA ACTIVO</b>\nTodos los servicios funcionan normal."

# ==============================================
# ✏️ ACTUALIZAR TEXTOS
# ==============================================
def actualizar_texto(tipo, texto_nuevo):
    if tipo == "bienvenida":
        actualizar_configuracion_db({"bienvenida": texto_nuevo})
        log_info("CONFIG: Mensaje de bienvenida actualizado")
        return "✅ <b>Mensaje de bienvenida actualizado!</b>"
    
    elif tipo == "oferta":
        actualizar_configuracion_db({"oferta": texto_nuevo})
        log_info("CONFIG: Oferta del día actualizada")
        return "✅ <b>Oferta del día actualizada!</b>"
