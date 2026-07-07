# ==============================================
# 🛡️ PANEL DE ADMINISTRACIÓN MASTER
# ==============================================
# ✅ Control total del sistema
# ✅ Compatible con todos los módulos
# ==============================================

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from database import *
from logger import *

# Importar todos los módulos
from admin_premium import panel_configuracion as panel_premium
from comprobantes import ver_comprobantes_pendientes
from configuracion import panel_configuracion, toggle_mantenimiento, actualizar_texto
from cupones import listar_cupones_admin, crear_cupon
from ranking import top_mejores_clientes, top_referidores
from payment_manager import menu_gestion_pagos, editar_metodo, toggle_estado, actualizar_datos, actualizar_comision, agregar_nuevo, eliminar_metodo
from soporte import ver_tickets_abiertos
from stats import obtener_estadisticas_completas, obtener_ranking_usuarios, obtener_top_servicios, obtener_reporte_completo
from tarjetas import menu_tienda, obtener_bases, obtener_stock_total

# ==============================================
# 🏠 MENÚ PRINCIPAL ADMIN
# ==============================================
def menu_admin_principal(bot, msg):
    uid = msg.from_user.id
    if uid != ADMIN_ID:
        bot.send_message(msg.chat.id, "❌ Acceso denegado.")
        return
    
    texto = """
⚔️ <b>PANEL DE ADMINISTRADOR</b> ⚔️

🔧 <b>CONTROL TOTAL DEL SISTEMA</b>

🔘 <b>Selecciona una sección:</b>
"""
    
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("📊 DASHBOARD", callback_data="admin_dashboard")
    b2 = InlineKeyboardButton("💳 GESTIONAR PAGOS", callback_data="manage_payments")
    b3 = InlineKeyboardButton("📸 COMPROBANTES", callback_data="ver_comprobantes")
    b4 = InlineKeyboardButton("🎫 SOPORTE", callback_data="ver_tickets")
    b5 = InlineKeyboardButton("🏆 RANKINGS", callback_data="ver_rankings")
    b6 = InlineKeyboardButton("⚙️ CONFIGURACIÓN", callback_data="config_global")
    b7 = InlineKeyboardButton("🎬 SERVICIOS PREMIUM", callback_data="panel_premium")
    b8 = InlineKeyboardButton("💳 TARJETAS CC", callback_data="gestionar_tarjetas")
    
    markup.add(b1, b2, b3, b4, b5, b6, b7, b8)
    
    bot.send_message(msg.chat.id, texto, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 📊 DASHBOARD
# ==============================================
def mostrar_dashboard(bot, call):
    datos = obtener_estadisticas_completas()
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="admin_menu")
    markup.add(btn_back)
    bot.edit_message_text(datos, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 🎫 SOPORTE
# ==============================================
def mostrar_tickets(bot, call):
    texto = ver_tickets_abiertos()
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="admin_menu")
    markup.add(btn_back)
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 🏆 RANKINGS
# ==============================================
def mostrar_rankings(bot, call):
    texto = top_mejores_clientes() + "\n\n" + top_referidores()
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="admin_menu")
    markup.add(btn_back)
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 💳 GESTIÓN DE PAGOS
# ==============================================
def mostrar_gestion_pagos(bot, call):
    texto, markup = menu_gestion_pagos()
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 📸 COMPROBANTES
# ==============================================
def mostrar_comprobantes(bot, call):
    texto, compras = ver_comprobantes_pendientes()
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="admin_menu")
    markup.add(btn_back)
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# ⚙️ CONFIGURACIÓN GLOBAL
# ==============================================
def mostrar_configuracion(bot, call):
    from configuracion import panel_configuracion
    # Esta función usa send_message directamente
    bot.delete_message(call.message.chat.id, call.message.message_id)
    panel_configuracion(bot, call.message)

# ==============================================
# 🎬 PANEL PREMIUM
# ==============================================
def mostrar_panel_premium(bot, call):
    from admin_premium import panel_configuracion
    bot.delete_message(call.message.chat.id, call.message.message_id)
    panel_configuracion(bot, call.message)

# ==============================================
# 💳 GESTIÓN DE TARJETAS
# ==============================================
def mostrar_gestion_tarjetas(bot, call):
    texto = menu_tienda()
    bases = obtener_bases()
    markup = InlineKeyboardMarkup(row_width=2)
    
    for key, db_info in bases.items():
        btn = InlineKeyboardButton(f"{db_info['nombre']} ({len(db_info['tarjetas'])})", callback_data=f"vender_cc_{key}")
        markup.add(btn)
    
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="admin_menu")
    markup.add(btn_back)
    
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 🎛️ MANEJADOR DE CALLBACKS
# ==============================================
def handle_admin_callback(bot, call):
    data = call.data
    
    if data == "admin_menu":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        menu_admin_principal(bot, call.message)
    
    elif data == "admin_dashboard":
        mostrar_dashboard(bot, call)
    
    elif data == "manage_payments":
        mostrar_gestion_pagos(bot, call)
    
    elif data == "ver_comprobantes":
        mostrar_comprobantes(bot, call)
    
    elif data == "ver_tickets":
        mostrar_tickets(bot, call)
    
    elif data == "ver_rankings":
        mostrar_rankings(bot, call)
    
    elif data == "config_global":
        mostrar_configuracion(bot, call)
    
    elif data == "panel_premium":
        mostrar_panel_premium(bot, call)
    
    elif data == "gestionar_tarjetas":
        mostrar_gestion_tarjetas(bot, call)
    
    # Manejar pagos
    elif data.startswith("edit_pay_"):
        key = data.replace("edit_pay_", "")
        texto, markup = editar_metodo(key)
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
    
    elif data.startswith("toggle_"):
        key = data.replace("toggle_", "")
        resultado = toggle_estado(key, call.from_user.id)
        bot.answer_callback_query(call.id, resultado, show_alert=True)
        # Volver a mostrar la lista
        texto, markup = menu_gestion_pagos()
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 📝 COMANDOS DE ADMIN
# ==============================================
def registrar_comandos_admin(bot):
    # Comando /admin
    @bot.message_handler(commands=['admin'])
    def cmd_admin(msg):
        menu_admin_principal(bot, msg)
    
    # Comando /responder
    @bot.message_handler(commands=['responder'])
    def cmd_responder(msg):
        if msg.from_user.id != ADMIN_ID:
            return
        
        try:
            partes = msg.text.split(" ", 2)
            uid = partes[1]
            respuesta = partes[2]
            
            bot.send_message(uid, f"📩 <b>RESPUESTA DEL ADMINISTRADOR</b>\n\n{respuesta}", parse_mode="HTML")
            bot.send_message(msg.chat.id, "✅ Mensaje enviado correctamente.")
            log_info(f"SOPORTE: Respuesta enviada a {uid}")
        except:
            bot.send_message(msg.chat.id, "❌ Uso correcto: /responder [ID] [texto]")
