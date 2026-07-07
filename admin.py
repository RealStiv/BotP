# ==============================================
# 🛡️ PANEL DE ADMINISTRACIÓN MASTER
# ==============================================
# ✅ Control total del sistema
# ✅ Compatible con todos los módulos
# ==============================================

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from config import *
from database import *
from logger import *

# Importar módulos
from comprobantes import ver_comprobantes_pendientes
from cupones import listar_cupones_admin, crear_cupon
from ranking import top_mejores_clientes, top_ganancias
from payment_manager import menu_gestion_pagos, editar_metodo, toggle_estado, actualizar_datos, actualizar_comision, agregar_metodo, eliminar_metodo
from soporte import ver_tickets_abiertos
from stats import obtener_dashboard, obtener_ranking_usuarios, obtener_top_servicios, obtener_reporte_completo
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
⚔️ <b>PANEL DE ADMINISTRADOR</b>

🔧 <b>CONTROL TOTAL DEL SISTEMA</b>

🔘 <b>Selecciona una sección:</b>
"""
    
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("📊 DASHBOARD", callback_data="admin_dashboard")
    b2 = InlineKeyboardButton("💳 GESTIONAR PAGOS", callback_data="manage_payments")
    b3 = InlineKeyboardButton("📸 COMPROBANTES", callback_data="ver_comprobantes")
    b4 = InlineKeyboardButton("🎫 SOPORTE", callback_data="ver_tickets")
    b5 = InlineKeyboardButton("🏆 RANKINGS", callback_data="ver_rankings")
    b8 = InlineKeyboardButton("💳 TARJETAS CC", callback_data="gestionar_tarjetas")
    b9 = InlineKeyboardButton("💲 PRECIOS CC", callback_data="precios_cc")
    
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5, b8)
    markup.add(b9)
    
    bot.send_message(msg.chat.id, texto, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 📊 DASHBOARD
# ==============================================
def mostrar_dashboard(bot, call):
    datos = obtener_dashboard()
    
    texto = f"""
📊 <b>DASHBOARD DEL SISTEMA</b>

👥 Usuarios Totales: <b>{datos['usuarios']}</b>
🛒 Ventas Realizadas: <b>{datos['ventas']}</b>
💳 Stock Total: <b>{datos['stock_tarjetas']}</b>
💰 Ganancia Total: <b>{MONEDA} {datos['ganancias']:.2f}</b>

✅ Sistema estable y funcionando
"""
    
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="admin_menu")
    markup.add(btn_back)
    
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

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
    texto = top_mejores_clientes() + "\n\n" + top_ganancias()
    
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
# 💳 GESTIÓN DE TARJETAS
# ==============================================
def mostrar_gestion_tarjetas(bot, call):
    texto = menu_tienda()
    bases = obtener_bases()
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    for key, data in bases.items():
        btn = InlineKeyboardButton(f"{data['nombre']} ({len(data['tarjetas'])})", callback_data=f"ver_stock_{key}")
        markup.add(btn)
    
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="admin_menu")
    markup.add(btn_back)
    
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 💲 EDITOR DE PRECIOS
# ==============================================
def menu_precios_cc(bot, call):
    from config import PRECIOS_CC
    
    texto = "💲 <b>GESTIÓN DE PRECIOS</b>\n\n"
    texto += "🔘 Selecciona qué precio deseas cambiar:\n\n"
    
    for key, data in PRECIOS_CC.items():
        texto += f"{data['nombre']}: <b>{MONEDA} {data['precio']:.2f}</b>\n"
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    for key, data in PRECIOS_CC.items():
        btn = InlineKeyboardButton(f"✏️ {data['nombre']}", callback_data=f"cambiar_precio_{key}")
        markup.add(btn)
    
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="admin_menu")
    markup.add(btn_back)
    
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

def solicitar_nuevo_precio(bot, call):
    tipo = call.data.replace("cambiar_precio_", "")
    nombre_tipo = PRECIOS_CC[tipo]['nombre']
    
    markup = ForceReply()
    msg_pregunta = bot.send_message(call.message.chat.id, f"✍️ <b>Ingresa el nuevo precio para {nombre_tipo}:</b>\n\n(Escribe solo el número ejemplo: 15.50)", reply_markup=markup, parse_mode="HTML")
    
    bot.register_next_step_handler(msg_pregunta, lambda m: guardar_nuevo_precio(m, tipo, nombre_tipo))

def guardar_nuevo_precio(msg, tipo, nombre_tipo):
    try:
        nuevo_precio = float(msg.text.replace(",", "."))
        
        from config import PRECIOS_CC
        PRECIOS_CC[tipo]['precio'] = nuevo_precio
        
        bot.send_message(msg.chat.id, f"✅ <b>PRECIO ACTUALIZADO!</b>\n\n{nombre_tipo}: Ahora vale {MONEDA} {nuevo_precio:.2f}", parse_mode="HTML")
        
        log_info(f"ADMIN: Cambió precio de {tipo} a {nuevo_precio}")
        
    except:
        bot.send_message(msg.chat.id, "❌ Valor inválido. Escribe solo números.")

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
    
    elif data == "gestionar_tarjetas":
        mostrar_gestion_tarjetas(bot, call)
        
    elif data == "precios_cc":
        menu_precios_cc(bot, call)

    elif data.startswith("cambiar_precio_"):
        solicitar_nuevo_precio(bot, call)
    
    # Manejar pagos
    elif data.startswith("edit_pay_"):
        key = data.replace("edit_pay_", "")
        texto, markup = editar_metodo(key)
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
    
    elif data.startswith("toggle_"):
        key = data.replace("toggle_", "")
        resultado = toggle_estado(key)
        bot.answer_callback_query(call.id, resultado, show_alert=True)
        texto, markup = menu_gestion_pagos()
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 📝 REGISTRAR COMANDOS
# ==============================================
def registrar_comandos_admin(bot):
    @bot.message_handler(commands=['admin'])
    def cmd_admin(msg):
        menu_admin_principal(bot, msg)
    
    @bot.message_handler(commands=['responder'])
    def cmd_responder(msg):
        if msg.from_user.id != ADMIN_ID:
            return
        
        try:
            partes = msg.text.split(" ", 2)
            uid = partes[1]
            respuesta = partes[2]
            
            bot.send_message(uid, f"📩 <b>RESPUESTA DEL ADMIN:</b>\n\n{respuesta}", parse_mode="HTML")
            bot.send_message(msg.chat.id, "✅ Mensaje enviado correctamente.")
        except:
            bot.send_message(msg.chat.id, "❌ Uso: /responder [ID] [mensaje]")
