# ==============================================
# ⌨️ SISTEMA DE BOTONES Y MENÚS
# ==============================================
# Diseño profesional y organizado
# Compatible con Telebot
# ==============================================

import telebot

# ==============================================
# 🏠 MENÚ PRINCIPAL DEL USUARIO
# ==============================================
def menu_principal():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    b1 = telebot.types.InlineKeyboardButton("📦 Servicios SMM", callback_data="menu_servicios")
    b2 = telebot.types.InlineKeyboardButton("🎬 Cuentas Premium", callback_data="menu_premium")
    b3 = telebot.types.InlineKeyboardButton("💰 Mi Saldo", callback_data="balance")
    b4 = telebot.types.InlineKeyboardButton("👤 Mi Perfil", callback_data="perfil")
    b5 = telebot.types.InlineKeyboardButton("🎁 Sorteos", callback_data="ver_sorteos")
    b6 = telebot.types.InlineKeyboardButton("📜 Mis Órdenes", callback_data="ordenes")
    b7 = telebot.types.InlineKeyboardButton("💳 Depositar", callback_data="depositar")
    b8 = telebot.types.InlineKeyboardButton("🧑‍💼 Panel Vendedor", callback_data="panel_seller")
    
    markup.add(b1, b2, b3, b4, b5, b6, b7, b8)
    return markup

# ==============================================
# 📦 MENÚ DE CATEGORÍAS SMM
# ==============================================
def menu_categorias():
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    
    b1 = telebot.types.InlineKeyboardButton("🎵 TikTok", callback_data="ver_tiktok")
    b2 = telebot.types.InlineKeyboardButton("📸 Instagram", callback_data="ver_insta")
    b3 = telebot.types.InlineKeyboardButton("📺 YouTube", callback_data="ver_youtube")
    b4 = telebot.types.InlineKeyboardButton("✈️ Telegram", callback_data="ver_telegram")
    b5 = telebot.types.InlineKeyboardButton("📘 Facebook", callback_data="ver_facebook")
    b6 = telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_menu")
    
    markup.add(b1, b2, b3, b4, b5, b6)
    return markup

# ==============================================
# 🎬 MENÚ DE CUENTAS PREMIUM
# ==============================================
def menu_premium_botones():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    b1 = telebot.types.InlineKeyboardButton("🎬 Netflix", callback_data="premium_netflix")
    b2 = telebot.types.InlineKeyboardButton("🎵 Spotify", callback_data="premium_spotify")
    b3 = telebot.types.InlineKeyboardButton("Disney+", callback_data="premium_disney")
    b4 = telebot.types.InlineKeyboardButton("HBO Max", callback_data="premium_hbo")
    b5 = telebot.types.InlineKeyboardButton("Prime Video", callback_data="premium_prime")
    b6 = telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_menu")
    
    markup.add(b1, b2, b3, b4, b5, b6)
    return markup

# ==============================================
# 📋 LISTA DE SERVICIOS
# ==============================================
def lista_servicios(categoria, servicios, moneda):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    
    for sid, info in servicios.items():
        if info.get("categoria", "") == categoria or categoria == "todos":
            texto = f"{info['nombre']} | {moneda} {info['precio_por_mil']}/K"
            markup.add(telebot.types.InlineKeyboardButton(texto, callback_data=f"sel_{sid}"))
    
    markup.add(telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="menu_servicios"))
    return markup

# ==============================================
# 🔢 SELECTOR DE CANTIDAD
# ==============================================
def selector_cant(sid, cantidad, moneda):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    
    b_menos = telebot.types.InlineKeyboardButton("➖", callback_data=f"menos_{sid}_{cantidad}")
    b_num = telebot.types.InlineKeyboardButton(f"{cantidad:,}", callback_data="none")
    b_mas = telebot.types.InlineKeyboardButton("➕", callback_data=f"mas_{sid}_{cantidad}")
    b_ok = telebot.types.InlineKeyboardButton("✅ CONFIRMAR", callback_data=f"ok_{sid}_{cantidad}")
    
    # Detectar plataforma para volver al menú correcto
    plataforma = sid.split('_')[0] if '_' in sid else sid
    b_volver = telebot.types.InlineKeyboardButton("🔙 Volver", callback_data=f"ver_{plataforma}")
    
    markup.add(b_menos, b_num, b_mas)
    markup.add(b_ok)
    markup.add(b_volver)
    return markup

# ==============================================
# 🧑‍💼 PANEL DEL VENDEDOR
# ==============================================
def menu_panel_seller():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    b1 = telebot.types.InlineKeyboardButton("💰 Mis Ganancias", callback_data="s_ganancias")
    b2 = telebot.types.InlineKeyboardButton("📜 Historial", callback_data="s_historial")
    b3 = telebot.types.InlineKeyboardButton("🏧 Retirar Saldo", callback_data="s_retirar")
    b4 = telebot.types.InlineKeyboardButton("🏆 Ranking", callback_data="s_ranking")
    b5 = telebot.types.InlineKeyboardButton("🔙 Volver al Menú", callback_data="volver_menu")
    
    markup.add(b1, b2, b3, b4, b5)
    return markup

# ==============================================
# 👑 PANEL DE ADMIN - BOTONES AUXILIARES
# ==============================================
def boton_volver():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_menu"))
    return markup

def boton_volver_admin():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 Volver al Panel", callback_data="admin_volver"))
    return markup

# ==============================================
# 📂 MENÚS ESPECIALES
# ==============================================
def menu_confirmar():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("✅ Sí, confirmar", callback_data="confirmar_si"),
        telebot.types.InlineKeyboardButton("❌ No, cancelar", callback_data="confirmar_no")
    )
    return markup

def menu_pagos():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(telebot.types.InlineKeyboardButton("💳 Métodos de Pago", callback_data="metodos_pago"))
    markup.add(telebot.types.InlineKeyboardButton("📜 Historial de Pagos", callback_data="historial_pagos"))
    markup.add(telebot.types.InlineKeyboardButton("🔙 Volver", callback_data="volver_menu"))
    return markup
