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
