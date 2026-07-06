# ==============================================
# 👑 PANEL DE ADMINISTRACIÓN MAESTRO
# ==============================================
# SISTEMA COMPLETO CON BOTONES INTERACTIVOS
# ==============================================

import telebot
import os
import sys
from config import *
from logger import *
from database import *
from licencias import *
from giveaway import *
from botones import *
from admin_premium import *
from datetime import datetime

# ==============================================
# 🛡️ VARIABLES DEL SISTEMA
# ==============================================
MODO_MANTENIMIENTO = False
ULTIMO_REINICIO = datetime.now()

# ==============================================
# 📋 MENÚ PRINCIPAL DE ADMIN
# ==============================================
def panel_admin(bot, msg):
    uid = str(msg.from_user.id)
    
    if str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "❌ Acceso denegado.", parse_mode="HTML")
        return
    
    estado = "✅ ACTIVO" if not MODO_MANTENIMIENTO else "🔧 MANTENIMIENTO"
    total_usuarios = total_usuarios_db()
    total_ventas = total_ventas_db()
    ganancias = sumar_ganancias_totales()
    
    menu = """
╔══════════════════════════════════╗
║        ⚙️  PANEL MAESTRO    ║
╚══════════════════════════════════╝

👑 Bienvenido, Administrador

📊 ESTADÍSTICAS:
👥 Usuarios: <code>{}</code>
🛒 Ventas totales: <code>{}</code>
💰 Ganancias: <code>{} {}</code>

⚙️ ESTADO: {}
🕒 Último reinicio: <code>{}</code>

🔘 <b>Selecciona una opción:</b>
""".format(
    total_usuarios, total_ventas, MONEDA, ganancias,
    estado, ULTIMO_REINICIO.strftime("%d/%m %H:%M")
)

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    b1 = telebot.types.InlineKeyboardButton("📊 Estadísticas", callback_data="admin_stats")
    b2 = telebot.types.InlineKeyboardButton("👤 Usuarios", callback_data="admin_users_menu")
    b3 = telebot.types.InlineKeyboardButton("🤝 Sellers", callback_data="admin_sellers_menu")
    b4 = telebot.types.InlineKeyboardButton("🎬 Premium", callback_data="admin_premium_menu")
    b5 = telebot.types.InlineKeyboardButton("🔑 Licencias", callback_data="admin_licencias_menu")
    b6 = telebot.types.InlineKeyboardButton("🎁 Giveaways", callback_data="admin_giveaways_menu")
    b7 = telebot.types.InlineKeyboardButton("📦 Servicios", callback_data="admin_servicios")
    b8 = telebot.types.InlineKeyboardButton("📝 Registros", callback_data="admin_logs")
    b9 = telebot.types.InlineKeyboardButton("🔧 Mantenimiento", callback_data="admin_mantenimiento")
    b10 = telebot.types.InlineKeyboardButton("🔄 Reiniciar", callback_data="admin_reiniciar")
    b11 = telebot.types.InlineKeyboardButton("⛔ Cerrar", callback_data="admin_cerrar")
    b12 = telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_menu")
    
    markup.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12)
    bot.send_message(msg.chat.id, menu, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 🎛️ PROCESAR OPCIONES DE ADMIN
# ==============================================
def procesar_admin(bot, call):
    data = call.data
    uid = str(call.from_user.id)
    
    if str(uid) != str(ADMIN_ID):
        bot.answer_callback_query(call.id, "❌ No permitido", show_alert=True)
        return

    # 📊 ESTADÍSTICAS
    if data == "admin_stats":
        total_u = total_usuarios_db()
        u_hoy = contar_usuarios_hoy()
        total_v = total_ventas_db()
        sum_v = sumar_ventas_totales()
        gan = sumar_ganancias_totales()
        
        texto = f"""
📊 <b>ESTADÍSTICAS GENERALES</b>

👥 Total usuarios: <code>{total_u}</code>
🆕 Nuevos hoy: <code>{u_hoy}</code>
🛒 Órdenes totales: <code>{total_v}</code>
💸 Ventas: <code>{MONEDA} {sum_v}</code>
💰 Ganancia: <code>{MONEDA} {gan}</code>

📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=menu_volver_admin(), parse_mode="HTML")

    # 👤 MENU USUARIOS
    elif data == "admin_users_menu":
        texto = """
👤 <b>GESTIÓN DE USUARIOS</b>

Selecciona una acción:
"""
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("➕ Agregar Saldo", callback_data="cmd_addsaldo"),
            telebot.types.InlineKeyboardButton("➖ Restar Saldo", callback_data="cmd_restarsaldo"),
            telebot.types.InlineKeyboardButton("🔒 Banear Usuario", callback_data="cmd_ban"),
            telebot.types.InlineKeyboardButton("🔓 Desbanear", callback_data="cmd_unban"),
            telebot.types.InlineKeyboardButton("ℹ️ Info Usuario", callback_data="cmd_info"),
            telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_admin")
        )
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")

    # 🤝 MENU SELLERS
    elif data == "admin_sellers_menu":
        from sellers import obtener_estadisticas_sellers
        stats = obtener_estadisticas_sellers()
        
        texto = f"""
🤝 <b>PANEL DE VENDEDORES</b>

📊 Stats:
• Total: <code>{stats['total']}</code>
• Activos: <code>{stats['activos']}</code>
• Ventas: <code>{stats['ventas']}</code>
"""
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("🆕 Crear Seller", callback_data="cmd_crearseller"),
            telebot.types.InlineKeyboardButton("📋 Ver Todos", callback_data="cmd_versellers"),
            telebot.types.InlineKeyboardButton("ℹ️ Info Seller", callback_data="cmd_infoseller"),
            telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_admin")
        )
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")

    # 🔑 MENU LICENCIAS
    elif data == "admin_licencias_menu":
        texto = """
🔑 <b>GESTIÓN DE LICENCIAS</b>

Selecciona una opción:
"""
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("🆕 Crear Licencia", callback_data="cmd_crearlicencia"),
            telebot.types.InlineKeyboardButton("📋 Ver Licencias", callback_data="cmd_verlicencias"),
            telebot.types.InlineKeyboardButton("🔍 Info Key", callback_data="cmd_infokey"),
            telebot.types.InlineKeyboardButton("📊 Estadísticas", callback_data="cmd_statslicencias"),
            telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_admin")
        )
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")

    # 🎁 MENU GIVEAWAYS
    elif data == "admin_giveaways_menu":
        texto = """
🎁 <b>GESTIÓN DE GIVEAWAYS</b>

Acciones disponibles:
"""
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("🆕 Crear Giveaway", callback_data="cmd_creargiveaway"),
            telebot.types.InlineKeyboardButton("📋 Ver Activos", callback_data="cmd_vergiveaways"),
            telebot.types.InlineKeyboardButton("✅ Finalizar", callback_data="cmd_finalizargiveaway"),
            telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_admin")
        )
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")

    # 🎬 PANEL PREMIUM
    elif data == "admin_premium_menu":
        panel_admin_premium(bot, call.message)

    # 📦 SERVICIOS
    elif data == "admin_servicios":
        from services import SERVICIOS
        texto = f"""
📦 <b>GESTIÓN DE SERVICIOS SMM</b>

Total: <code>{len(SERVICIOS)}</code> servicios
"""
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("➕ Agregar", callback_data="cmd_addservicio"),
            telebot.types.InlineKeyboardButton("✏️ Editar", callback_data="cmd_editservicio"),
            telebot.types.InlineKeyboardButton("🗑️ Eliminar", callback_data="cmd_delservicio"),
            telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_admin")
        )
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")

    # 📝 REGISTROS
    elif data == "admin_logs":
        logs = obtener_ultimos_registros()
        texto = "📝 <b>ÚLTIMOS MOVIMIENTOS</b>\n\n" + logs
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=menu_volver_admin(), parse_mode="HTML")

    # 🔧 MANTENIMIENTO
    elif data == "admin_mantenimiento":
        global MODO_MANTENIMIENTO
        MODO_MANTENIMIENTO = not MODO_MANTENIMIENTO
        
        if MODO_MANTENIMIENTO:
            texto = "🔧 <b>MODO MANTENIMIENTO ACTIVADO</b>\n✅ Sistema en mantenimiento."
        else:
            texto = "✅ <b>MODO MANTENIMIENTO DESACTIVADO</b>\n✅ Sistema activo."
        
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=menu_volver_admin(), parse_mode="HTML")

    # 🔄 REINICIAR
    elif data == "admin_reiniciar":
        texto = "🔄 <b>¿Seguro que quieres reiniciar el bot?</b>"
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("✅ SÍ, REINICIAR", callback_data="confirmar_reinicio"),
            telebot.types.InlineKeyboardButton("❌ NO", callback_data="volver_admin")
        )
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")

    # ⛔ CERRAR
    elif data == "admin_cerrar":
        texto = "⛔ <b>¿Seguro que quieres APAGAR el bot?</b>"
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("✅ SÍ, CERRAR", callback_data="confirmar_cerrar"),
            telebot.types.InlineKeyboardButton("❌ NO", callback_data="volver_admin")
        )
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id,
                              reply_markup=markup, parse_mode="HTML")

    # ✅ CONFIRMAR REINICIO
    elif data == "confirmar_reinicio":
        bot.send_message(call.message.chat.id, "🔄 Reiniciando...", parse_mode="HTML")
        global ULTIMO_REINICIO
        ULTIMO_REINICIO = datetime.now()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # ✅ CONFIRMAR CERRAR
    elif data == "confirmar_cerrar":
        bot.send_message(call.message.chat.id, "⛔ Cerrando bot... Hasta luego!", parse_mode="HTML")
        os._exit(0)

    # 🔙 VOLVER
    elif data == "volver_admin":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        panel_admin(bot, call.message)

# ==============================================
# 🎛️ MENÚS AUXILIARES CON BOTONES
# ==============================================
def menu_volver_admin():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 Volver al Panel", callback_data="volver_admin"))
    return markup

def esta_en_mantenimiento():
    return MODO_MANTENIMIENTO

# ==============================================
# 📊 FUNCIONES DE CÁLCULO
# ==============================================
def contar_ventas_hoy():
    hoy = datetime.now().strftime("%d/%m/%Y")
    ventas = obtener_historial_premium()
    return len([x for x in ventas if x.get("fecha", "") == hoy])

def sumar_ventas_totales():
    ventas = obtener_historial_premium()
    return sum([x.get("monto", 0) for x in ventas])

def sumar_ganancias_totales():
    ventas = obtener_historial_premium()
    return sum([x.get("ganancia", 0) for x in ventas])

def contar_usuarios_hoy():
    hoy = datetime.now().strftime("%d/%m/%Y")
    usuarios = obtener_todos_usuarios_db()
    return len([u for u in usuarios if u.get("registro", "").startswith(hoy)])
