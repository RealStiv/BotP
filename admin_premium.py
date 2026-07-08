# ==============================================
# 👑 PANEL DE ADMINISTRADOR - CUENTAS PREMIUM
# ==============================================
# Control total del sistema Streaming
# Base de Datos MONGODB 🍃
# ==============================================

from datetime import datetime
import telebot
from config import *
from database import *
from logger import *
from keyboards import boton_volver_admin

# ==============================================
# 📊 ESTADÍSTICAS GENERALES
# ==============================================
def obtener_estadisticas():
    """Retorna datos globales del sistema"""
    
    ventas = obtener_historial_premium()
    total_ventas = len(ventas)
    ingresos_totales = sum(v.get('precio', 0) for v in ventas)
    
    stock_por_servicio = {}
    servicios = ["netflix", "disney", "hbo", "prime", "spotify", "crunchy"]
    
    for serv in servicios:
        stock = obtener_stock_premium_db(serv)
        stock_por_servicio[serv] = len(stock)
    
    return {
        "ventas_total": total_ventas,
        "ingresos_total": ingresos_totales,
        "stock": stock_por_servicio
    }

# ==============================================
# ➕ AGREGAR CUENTAS AL SISTEMA
# ==============================================
def agregar_cuentas_admin(id_servicio, cuentas_nuevas):
    """
    Agrega cuentas al stock disponible
    Formato: ["user|pass|dias", "user2|pass2|dias"]
    """
    return agregar_cuentas_premium_db(id_servicio, cuentas_nuevas)

# ==============================================
# 📋 MENÚ PRINCIPAL
# ==============================================
def panel_admin_premium(bot, mensaje):
    """Muestra el panel principal de control"""
    
    id_usuario = str(mensaje.from_user.id)
    
    # Verificar permisos
    if str(id_usuario) != str(ADMIN_ID):
        bot.send_message(mensaje.chat.id, "❌ Acceso denegado.", parse_mode="HTML")
        return
    
    stats = obtener_estadisticas()
    
    texto = """
🎬 <b>PANEL DE CONTROL - CUENTAS PREMIUM</b>

📊 <b>ESTADÍSTICAS RÁPIDAS:</b>
• Ventas totales: <code>{}</code>
• Ingresos: <code>{} {}</code>
• Cuentas en stock: <code>{}</code>

🔧 <b>HERRAMIENTAS:</b>
✅ Agregar cuentas nuevas
✏️ Editar precios
📦 Ver stock por servicio
📜 Historial de ventas
📊 Reportes económicos

🔘 <b>Selecciona una opción:</b>
""".format(
    stats['ventas_total'],
    MONEDA, stats['ingresos_total'],
    sum(stats['stock'].values())
)
    
    bot.send_message(mensaje.chat.id, texto, reply_markup=menu_admin_premium(), parse_mode="HTML")

def menu_admin_premium():
    """Genera los botones del menú"""
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    b1 = telebot.types.InlineKeyboardButton("➕ Agregar Cuentas", callback_data="admin_add_premium")
    b2 = telebot.types.InlineKeyboardButton("✏️ Editar Precios", callback_data="admin_edit_premium")
    b3 = telebot.types.InlineKeyboardButton("📦 Ver Stock", callback_data="admin_stock_premium")
    b4 = telebot.types.InlineKeyboardButton("📜 Historial", callback_data="admin_historial_premium")
    b5 = telebot.types.InlineKeyboardButton("📊 Reportes", callback_data="admin_reportes_premium")
    b6 = telebot.types.InlineKeyboardButton("🔙 Volver al Admin", callback_data="admin_volver")
    
    markup.add(b1, b2, b3, b4, b5, b6)
    return markup

# ==============================================
# 🎛️ PROCESAR OPCIONES
# ==============================================
def procesar_admin_premium(bot, llamada):
    """Controla las acciones de los botones"""
    
    data = llamada.data
    id_usuario = str(llamada.from_user.id)
    
    if str(id_usuario) != str(ADMIN_ID):
        bot.answer_callback_query(llamada.id, "❌ No permitido", show_alert=True)
        return

    # ➕ AGREGAR CUENTAS
    elif data == "admin_add_premium":
        texto = """
➕ <b>AGREGAR NUEVAS CUENTAS</b>

Formato correcto:
<code>/addcuenta SERVICIO usuario|contraseña|dias</code>

Ejemplo:
<code>/addcuenta netflix mio123|clave456|30</code>

📋 Servicios disponibles:
• netflix | disney | hbo | prime | spotify | crunchy
"""
        bot.edit_message_text(texto, llamada.message.chat.id, llamada.message.message_id,
                              reply_markup=boton_volver_premium(), parse_mode="HTML")

    # ✏️ EDITAR PRECIOS
    elif data == "admin_edit_premium":
        texto = """
✏️ <b>EDITAR PRECIOS DE CUENTAS</b>

Usa el comando:
<code>/setprecio SERVICIO PRECIO</code>

Ejemplo:
<code>/setprecio netflix 15.00</code>
"""
        bot.edit_message_text(texto, llamada.message.chat.id, llamada.message.message_id,
                              reply_markup=boton_volver_premium(), parse_mode="HTML")

    # 📦 VER STOCK
    elif data == "admin_stock_premium":
        stats = obtener_estadisticas()
        texto = "📦 <b>STOCK ACTUAL DE CUENTAS</b>\n\n"
        
        for servicio, cantidad in stats['stock'].items():
            precio = obtener_precio_premium_db(servicio)
            texto += f"• <b>{servicio.upper()}</b>: {cantidad} unidades | {MONEDA} {precio:.2f}\n"
        
        bot.edit_message_text(texto, llamada.message.chat.id, llamada.message.message_id,
                              reply_markup=boton_volver_premium(), parse_mode="HTML")

    # 📜 HISTORIAL
    elif data == "admin_historial_premium":
        texto = "📜 <b>ÚLTIMAS VENTAS REALIZADAS</b>\n\n"
        todas_ventas = obtener_historial_premium()
        ventas = todas_ventas[-10:] if len(todas_ventas) > 10 else todas_ventas
        
        if not ventas:
            texto += "❌ No hay ventas registradas."
        else:
            for venta in ventas:
                texto += f"""
📌 <b>{venta.get('servicio', 'Desconocido')}</b>
👤 Usuario: {venta.get('nombre', 'ID: '+venta.get('uid', '?'))}
💰 Precio: {MONEDA} {venta.get('precio', 0)}
📅 {venta.get('fecha', '')}
──────────────────────────
"""
        
        bot.edit_message_text(texto, llamada.message.chat.id, llamada.message.message_id,
                              reply_markup=boton_volver_premium(), parse_mode="HTML")

    # 📊 REPORTES
    elif data == "admin_reportes_premium":
        stats = obtener_estadisticas()
        ganancia = stats['ingresos_total'] * 0.7
        
        texto = f"""
📊 <b>REPORTE ECONÓMICO - PREMIUM</b>

💸 Total vendido: <b>{MONEDA} {stats['ingresos_total']:.2f}</b>
💰 Ganancia estimada: <b>{MONEDA} {ganancia:.2f}</b>
📦 Órdenes procesadas: <b>{stats['ventas_total']}</b>

📅 Actualizado: {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
        bot.edit_message_text(texto, llamada.message.chat.id, llamada.message.message_id,
                              reply_markup=boton_volver_premium(), parse_mode="HTML")

# ==============================================
# 🔘 BOTÓN VOLVER
# ==============================================
def boton_volver_premium():
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("🔙 Volver al Panel", callback_data="admin_premium_menu")
    markup.add(btn)
    return markup
