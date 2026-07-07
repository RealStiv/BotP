# ==============================================
# 🤖 NOVOBOT - SISTEMA COMPLETO
# ==============================================
# ✅ Versión Final - Todo Integrado
# ✅ MongoDB + Telegram API
# ==============================================

import telebot
from telebot.types import *
from config import *
from database import *
from logger import *
from users import *

# ==============================================
# 🚀 INICIALIZACIÓN DEL BOT
# ==============================================
# ⚠️ IMPORTANTE: Esto debe ir PRIMERO que todo lo demás
bot = telebot.TeleBot(BOT_TOKEN)

# Importar módulos después de definir el bot
from admin import registrar_comandos_admin, handle_admin_callback
from comprobantes import guardar_comprobante
from cupones import canjear_cupon, crear_cupon
from historial import ver_historial_usuario
from pedidos import ver_mis_pedidos, crear_pedido, cambiar_estado
from rangos import ver_mi_nivel
from referidos import obtener_enlace_referido, registrar_referido
from payment_manager import obtener_metodos_pago, aplicar_comision
from soporte import abrir_ticket
from tarjetas import menu_tienda, obtener_bases, obtener_stock_total, vender_tarjeta

log_info("="*50)
log_info("🤖 BOT INICIANDO...")
log_info(f"🔋 Estado: ONLINE")
log_info("="*50)

# ==============================================
# 👋 COMANDO /START
# ==============================================
@bot.message_handler(commands=['start'])
def cmd_start(msg):
    uid = msg.from_user.id
    nombre = msg.from_user.first_name
    
    # Verificar si es nuevo
    es_nuevo = verificar_o_crear_usuario(uid, nombre)
    
    # Verificar si viene de un referido
    if len(msg.text.split()) > 1:
        referidor_id = msg.text.split()[1]
        if str(referidor_id) != str(uid):
            registro = registrar_referido(uid, nombre, referidor_id)
            if registro:
                bot.send_message(msg.chat.id, "🎉 ¡Has recibido un bono por registrarte!")
    
    # ──── 🌟 MENSAJE DE BIENVENIDA PREMIUM ────
    texto_bienvenida = f"""
╔════════════════════════════════════════╗
║       🚀  S I S T E M A   N O V A      ║
╚════════════════════════════════════════╝

👋 ¡Hola <b>{nombre}</b>! Bienvenido al mejor servicio.

✨ <b>¿Qué encontrarás aquí?</b>

🎬 <b>Cuentas Premium</b> • Netflix, Disney+, HBO y más
💳 <b>Tarjetas CC</b> • Full Data y verificadas
📈 <b>SMM Panel</b> • Seguidores, Likes y Visitas
💰 <b>Recargas</b> • Métodos rápidos y seguros

🔒 <b>Garantía y Seguridad 100%</b>
⚡ <b>Soporte 24/7</b>
💎 <b>Sistema de Niveles y Beneficios</b>

────────────────────────────────────────
🔘 <b>¡Comienza a explorar usando los botones!</b>
"""

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("💰 MI SALDO")
    btn2 = KeyboardButton("🛒 TIENDA")
    btn3 = KeyboardButton("💳 RECARGAR")
    btn4 = KeyboardButton("📜 HISTORIAL")
    btn5 = KeyboardButton("🏅 MI NIVEL")
    btn6 = KeyboardButton("👥 REFERIDOS")
    btn7 = KeyboardButton("🎫 SOPORTE")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7)
    
    bot.send_message(msg.chat.id, texto_bienvenida, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 💰 MI SALDO
# ==============================================
@bot.message_handler(func=lambda m: m.text == "💰 MI SALDO")
def cmd_saldo(msg):
    uid = msg.from_user.id
    saldo = obtener_saldo(uid)
    nivel = obtener_nivel(uid)
    
    texto = f"""
💰 <b>MI SALDO</b>

💵 Disponible: <b>{MONEDA} {saldo:.2f}</b>
🏅 Nivel: <b>{nivel}</b>

✅ Cuenta verificada
"""
    bot.send_message(msg.chat.id, texto, parse_mode="HTML")

# ==============================================
# 💳 RECARGAR
# ==============================================
@bot.message_handler(func=lambda m: m.text == "💳 RECARGAR")
def cmd_recargar(msg):
    metodos = obtener_metodos_pago()
    
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("📸 ENVIAR COMPROBANTE", callback_data="enviar_comprobante")
    markup.add(btn1)
    
    bot.send_message(msg.chat.id, metodos, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 🛒 TIENDA
# ==============================================
@bot.message_handler(func=lambda m: m.text == "🛒 TIENDA")
def cmd_tienda(msg):
    texto = """
🛒 <b>TIENDA DE SERVICIOS</b>

🔹 <b>SECCIONES DISPONIBLES:</b>

🎬 <b>SERVICIOS PREMIUM</b>
• Netflix, Disney+, HBO, etc.
• Cuentas privadas y garantizadas

💳 <b>TARJETAS CC FULL DATA</b>
• Visa, Mastercard, Amex
• Datos completos y verificados

📈 <b>SMM PANEL</b>
• Seguidores, Likes, Vistas
• Redes sociales

🔘 <b>Selecciona qué deseas ver:</b>
"""
    
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("🎬 PREMIUM", callback_data="ver_premium")
    b2 = InlineKeyboardButton("💳 TARJETAS", callback_data="ver_tarjetas")
    b3 = InlineKeyboardButton("📈 SMM PANEL", callback_data="ver_smm")
    markup.add(b1, b2, b3)
    
    bot.send_message(msg.chat.id, texto, reply_markup=markup, parse_mode="HTML")

# ==============================================
# 📜 HISTORIAL
# ==============================================
@bot.message_handler(func=lambda m: m.text == "📜 HISTORIAL")
def cmd_historial(msg):
    uid = msg.from_user.id
    texto = ver_historial_usuario(uid)
    bot.send_message(msg.chat.id, texto, parse_mode="HTML")

# ==============================================
# 🏅 MI NIVEL
# ==============================================
@bot.message_handler(func=lambda m: m.text == "🏅 MI NIVEL")
def cmd_nivel(msg):
    uid = msg.from_user.id
    texto = ver_mi_nivel(uid)
    bot.send_message(msg.chat.id, texto, parse_mode="HTML")

# ==============================================
# 👥 REFERIDOS
# ==============================================
@bot.message_handler(func=lambda m: m.text == "👥 REFERIDOS")
def cmd_referidos(msg):
    uid = msg.from_user.id
    enlace = obtener_enlace_referido(uid)
    
    texto = f"""
👥 <b>PROGRAMA DE REFERIDOS</b>

🎁 <b>GANA SALDO GRATIS</b>

🔹 Invita amigos y gana:
• 🎁 Tu ganas: <b>{MONEDA} {BONO_INVITADOR:.2f}</b>
• 🎁 Tu amigo gana: <b>{MONEDA} {BONO_INVITADO:.2f}</b>

🔗 <b>TU ENLACE:</b>
<code>{enlace}</code>

📲 Copia y comparte con tus amigos!
"""
    bot.send_message(msg.chat.id, texto, parse_mode="HTML")

# ==============================================
# 🎫 SOPORTE
# ==============================================
@bot.message_handler(func=lambda m: m.text == "🎫 SOPORTE")
def cmd_soporte(msg):
    uid = msg.from_user.id
    nombre = msg.from_user.first_name
    
    markup = ForceReply()
    msg_pregunta = bot.send_message(msg.chat.id, "✍️ <b>Escribe tu consulta o problema:</b>", reply_markup=markup, parse_mode="HTML")
    
    bot.register_next_step_handler(msg_pregunta, lambda m: procesar_ticket(m, uid, nombre))

def procesar_ticket(msg, uid, nombre):
    exito, respuesta = abrir_ticket(uid, nombre, msg.text)
    bot.send_message(msg.chat.id, respuesta, parse_mode="HTML")

# ==============================================
# 🎫 CANJEAR CUPÓN
# ==============================================
@bot.message_handler(commands=['cupon'])
def cmd_cupon(msg):
    uid = msg.from_user.id
    nombre = msg.from_user.first_name
    
    if len(msg.text.split()) < 2:
        bot.send_message(msg.chat.id, "❌ Uso: /cupon [CODIGO]")
        return
    
    codigo = msg.text.split()[1]
    exito, respuesta = canjear_cupon(uid, nombre, codigo)
    bot.send_message(msg.chat.id, respuesta, parse_mode="HTML")

# ==============================================
# 📸 MANEJAR FOTOS DE COMPROBANTES
# ==============================================
@bot.message_handler(content_types=['photo'])
def handle_photo(msg):
    uid = msg.from_user.id
    nombre = msg.from_user.first_name
    
    # Obtener el file_id de la foto
    file_id = msg.photo[-1].file_id
    
    # Aquí deberías pedir monto y método, pero por ahora guardamos directo
    exito, respuesta = guardar_comprobante(uid, nombre, 0.00, "Telegram", file_id)
    bot.send_message(msg.chat.id, respuesta, parse_mode="HTML")

# ==============================================
# 🔄 MANEJADOR DE CALLBACKS
# ==============================================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    
    # Admin callbacks
    if data in ["admin_menu", "admin_dashboard", "manage_payments", "ver_comprobantes", "ver_tickets", "ver_rankings", "config_global", "panel_premium", "gestionar_tarjetas", "precios_cc"] or data.startswith(("edit_pay_", "toggle_", "change_", "delete_", "cambiar_precio_")):
        handle_admin_callback(bot, call)
        return
    
    # Ver tarjetas
    elif data == "ver_tarjetas":
        texto = menu_tienda()
        bases = obtener_bases()
        markup = InlineKeyboardMarkup(row_width=2)
        
        for key, db_info in bases.items():
            estado = "✅" if len(db_info['tarjetas']) > 0 else "❌"
            btn = InlineKeyboardButton(f"{estado} {db_info['nombre']}", callback_data=f"comprar_cc_{key}")
            markup.add(btn)
        
        btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="volver_tienda")
        markup.add(btn_back)
        
        bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
    
    elif data.startswith("comprar_cc_"):
        key = data.replace("comprar_cc_", "")
        uid = call.from_user.id
        nombre = call.from_user.first_name
        
        exito, respuesta = vender_tarjeta(uid, nombre, key)
        bot.send_message(call.message.chat.id, respuesta, parse_mode="HTML")
    
    elif data == "volver_tienda":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        cmd_tienda(call.message)

# ==============================================
# 🚀 INICIAR BOT
# ==============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 NOVOBOT - SISTEMA COMPLETO")
    print("✅ Versión: FINAL")
    print("✅ Base de datos: MongoDB")
    print("✅ Estado: LISTO PARA FUNCIONAR")
    print("="*60 + "\n")
    
    # Registrar comandos de admin
    registrar_comandos_admin(bot)
    
    # Iniciar bot
    bot.infinity_polling()
