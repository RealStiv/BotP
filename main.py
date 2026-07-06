# ==============================================
# 🤖 BOT SMM - VERSIÓN MAESTRA v6.0
# ==============================================
# ✅ Panel Admin Completo con Botones
# ✅ Modo Mantenimiento
# ✅ Reinicio Automático
# ✅ Sistema Sellers
# ✅ Tienda Premium
# ✅ BASE DE DATOS MONGODB 🍃
# ✅ SISTEMA DE LICENCIAS 🔑
# ✅ SISTEMA DE GIVEAWAYS 🎁
# ✅ LOGS EN CANAL TELEGRAM 📢
# ==============================================

# ==============================================
# 📦 IMPORTACIONES GENERALES
# ==============================================
import telebot
import requests
import time
import os
import sys
from datetime import datetime

# 🔌 CONEXIÓN A MÓDULOS PROPIOS
from users import *
from config import *
from security import *
from giveaway import *       # 🎁 SISTEMA DE GIVEAWAYS
from database import *       # 🍃 MONGODB
from keyboards import *
from admin import *          # 👑 PANEL MAESTRO
from services import *
from payment_manager import *
from stats import *
from logger import *         # 📝 SISTEMA DE LOGS
from premium import *
from sellers import *
from licencias import *      # 🔑 SISTEMA DE LICENCIAS

# ==============================================
# ⚙️ INICIALIZACIÓN DEL BOT
# ==============================================
bot = telebot.TeleBot(BOT_TOKEN)
ultima_conexion = time.time()

# ==============================================
# 🚀 INICIO DEL SISTEMA
# ==============================================
print("🍃 Conectando a MongoDB...")
print("📢 Iniciando sistema de logs...")
registrar_inicio_bot()  # 📢 AVISA AL CANAL

# ==============================================
# 🌐 FUNCIONES DE CONEXIÓN API
# ==============================================
def verificar_conexion():
    try:
        test = requests.get(f"{URL_PANEL}?key={API_KEY}&action=balance", timeout=10)
        return True, "✅ CONECTADO" if test.status_code == 200 else False, "❌ ERROR DE API"
    except:
        return False, "❌ SIN INTERNET"

def enviar_pedido(api_id, link, cantidad):
    global ultima_conexion
    ultima_conexion = time.time()
    try:
        datos = {
            "key": API_KEY,
            "action": "add",
            "service": api_id,
            "link": link,
            "quantity": cantidad
        }
        return requests.post(URL_PANEL, data=datos, timeout=15).json()
    except Exception as e:
        return {"error": f"Fallo: {str(e)}"}

# ==============================================
# ✨ MENSAJES DEL SISTEMA
# ==============================================
def bienvenida(nombre, uid):
    return f"""
╔══════════════════════════════╗
║       🚀 NOVABOT PREMIUM        ║
╚══════════════════════════════╝

👋 ¡Hola <b>{nombre}</b>! {obtener_nivel(uid)}
🆔 ID: <code>{uid}</code>

💎 <i>Servicios de alta calidad</i>
⚡ <i>Entrega rápida y segura</i>
🛡️ <i>Sistema protegido</i>
🎁 <i>¡Participa en nuestros sorteos!</i>

🔘 <b>Selecciona una opción:</b>
"""

# ==============================================
# 🔑 COMANDO DE ACTIVAR LICENCIA
# ==============================================
@bot.message_handler(commands=['activar', 'key', 'licencia'])
def cmd_activar(msg):
    uid = str(msg.from_user.id)
    nombre = msg.from_user.first_name
    
    registrar_comando(uid, nombre, "activar")
    
    partes = msg.text.split()
    if len(partes) < 2:
        bot.send_message(msg.chat.id, """
⚠️ <b>USO CORRECTO:</b>
<code>/activar TU_KEY_AQUI</code>

Ejemplo:
<code>/activar ABCD-1234-WXYZ-5678</code>
""", parse_mode="HTML")
        return
    
    key = partes[1].upper()
    ok, resp = activar_licencia(uid, nombre, key)
    bot.send_message(msg.chat.id, resp, parse_mode="HTML")

# ==============================================
# 🧑‍💼 PANEL DEL VENDEDOR
# ==============================================
@bot.message_handler(commands=['seller', 'panel', 'mipanel', 'vendedor'])
def panel_seller(msg):
    uid = str(msg.from_user.id)
    nombre = msg.from_user.first_name
    
    registrar_comando(uid, nombre, "panel_seller")
    
    # 🔒 VERIFICAR MANTENIMIENTO
    if esta_en_mantenimiento() and str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "🔧 <b>BOT EN MANTENIMIENTO</b>\nVolvemos pronto!", parse_mode="HTML")
        return
    
    if not es_seller(uid):
        bot.send_message(msg.chat.id, "❌ <b>ACCESO DENEGADO</b>\nNo tienes cuenta de vendedor.", parse_mode="HTML")
        return
    
    datos = obtener_datos(uid)
    
    if datos["estado"] != "activo":
        bot.send_message(msg.chat.id, "🔒 Tu cuenta está <b>SUSPENDIDA</b>", parse_mode="HTML")
        return
    
    texto = f"""
{datos['info_nivel']['color']} <b>PANEL DE VENDEDOR</b>
{datos['info_nivel']['nombre']}

👤 <b>Nombre:</b> {datos['nombre']}
🆔 <b>ID:</b> <code>{uid}</code>
📅 <b>Miembro desde:</b> {datos['fecha_registro']}

💰 <b>SALDO DISPONIBLE:</b>
💲 {datos['saldo_ganancias']:.2f} {MONEDA}

📊 <b>ESTADÍSTICAS:</b>
• Total vendido: <b>{datos['total_vendido']:.2f}</b>
• Ventas realizadas: <b>{datos['ventas_realizadas']}</b>
• Comisión: <b>{datos['info_nivel']['comision']}%</b>
• Descuento máx: <b>{datos['info_nivel']['descuento_max']}%</b>

⚡ Última venta: {datos['ultima_venta']}

🔘 <b>Selecciona una opción:</b>
"""
    bot.send_message(msg.chat.id, texto, reply_markup=menu_panel_seller(), parse_mode="HTML")

# ==============================================
# 📱 COMANDOS PRINCIPALES USUARIOS
# ==============================================
@bot.message_handler(commands=['start'])
def start(msg):
    uid = str(msg.from_user.id)
    nombre = sanitizar_texto(msg.from_user.first_name)
    
    registrar_comando(uid, nombre, "start")
    
    # 🛡️ Seguridad y Mantenimiento
    bloqueado, minutos = verificar_bloqueo(uid)
    if bloqueado:
        bot.send_message(msg.chat.id, f"🚫 <b>CUENTA BLOQUEADA</b>\n\nTiempo restante: {minutos} minutos", parse_mode="HTML")
        return
        
    if esta_en_mantenimiento() and str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "🔧 <b>BOT EN MANTENIMIENTO</b>\nVolvemos pronto!", parse_mode="HTML")
        return
        
    if not anti_spam(uid, "start"):
        return
    
    # 🔐 Registro en MongoDB
    es_nuevo = verificar_usuario(uid, nombre)
    
    if es_nuevo:
        registrar_usuario_nuevo(uid, nombre)  # 📢 LOG
    
    # 🔑 VERIFICAR LICENCIA
    tiene_licencia, plan = verificar_licencia_activa(uid)
    if not tiene_licencia:
        bot.send_message(msg.chat.id, f"""
🔒 <b>ACCESO RESTRINGIDO</b>

{plan}

Para activar escribe:
<code>/activar TU_KEY</code>
""", parse_mode="HTML")
        return
    
    # MENSAJE DE BIENVENIDA
    bot.send_message(msg.chat.id, bienvenida(nombre, uid), reply_markup=menu_principal(), parse_mode="HTML")

@bot.message_handler(commands=['admin', 'paneladmin', 'maestro'])
def panel_administracion(msg):
    uid = str(msg.from_user.id)
    nombre = msg.from_user.first_name
    registrar_comando(uid, nombre, "panel_admin")
    panel_admin(bot, msg)

@bot.message_handler(commands=['balance'])
def ver_saldo(msg):
    uid = str(msg.from_user.id)
    nombre = msg.from_user.first_name
    registrar_comando(uid, nombre, "balance")
    
    if esta_en_mantenimiento() and str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "🔧 <b>BOT EN MANTENIMIENTO</b>", parse_mode="HTML")
        return
        
    bot.send_message(msg.chat.id, f"💰 <b>SALDO ACTUAL</b>\n💵 {MONEDA} {obtener_saldo(uid):.2f}\n{obtener_nivel(uid)}", parse_mode="HTML")

# ==============================================
# 🎁 COMANDOS DE GIVEAWAYS
# ==============================================
@bot.message_handler(commands=['sorteos', 'giveaway', 'giveaways'])
def ver_sorteos_cmd(msg):
    uid = str(msg.from_user.id)
    nombre = msg.from_user.first_name
    registrar_comando(uid, nombre, "giveaways")
    
    if esta_en_mantenimiento() and str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "🔧 <b>BOT EN MANTENIMIENTO</b>", parse_mode="HTML")
        return
    bloqueado, _ = verificar_bloqueo(uid)
    if bloqueado: return
    txt = listar_sorteos()
    bot.send_message(msg.chat.id, txt, parse_mode="HTML")

@bot.message_handler(commands=['participar'])
def participar_cmd(msg):
    uid = str(msg.from_user.id)
    nombre = msg.from_user.first_name
    registrar_comando(uid, nombre, "participar")
    
    if esta_en_mantenimiento() and str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "🔧 <b>BOT EN MANTENIMIENTO</b>", parse_mode="HTML")
        return
    bloqueado, _ = verificar_bloqueo(uid)
    if bloqueado: return
    partes = msg.text.split()
    if len(partes) < 2:
        bot.send_message(msg.chat.id, "⚠️ <b>USO:</b>\n/participar [ID_SORTEO]", parse_mode="HTML")
        return
    ok, resp = participar(uid, partes[1])
    bot.send_message(msg.chat.id, f"<b>{resp}</b>", parse_mode="HTML")

# ==============================================
# 🎬 COMANDOS DE CUENTAS PREMIUM
# ==============================================
@bot.message_handler(commands=['premium', 'cuentas', 'streaming'])
def menu_premium(msg):
    uid = str(msg.from_user.id)
    nombre = msg.from_user.first_name
    registrar_comando(uid, nombre, "premium")
    
    if esta_en_mantenimiento() and str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "🔧 <b>BOT EN MANTENIMIENTO</b>\nVolvemos pronto!", parse_mode="HTML")
        return
        
    bloqueado, _ = verificar_bloqueo(uid)
    if bloqueado: return
    
    texto = """
🎬 <b>TIENDA DE CUENTAS PREMIUM</b>

⚡ <b>ENTREGA INSTANTÁNEA</b>
✅ 100% Garantizado
🔐 Privado y Seguro

Elige el servicio:
"""
    bot.send_message(msg.chat.id, texto, reply_markup=menu_premium_botones(), parse_mode="HTML")

# ==============================================
# 🎛️ MANEJADOR DE BOTONES PRINCIPALES
# ==============================================
@bot.callback_query_handler(func=lambda c: True)
def botones_avanzado(c):
    data = c.data
    uid = str(c.from_user.id)
    nombre = sanitizar_texto(c.from_user.first_name)
    
    # 📝 REGISTRAR BOTÓN PRESIONADO
    registrar_boton(uid, nombre, data)
    
    # 🛡️ Seguridad
    bloqueado, _ = verificar_bloqueo(uid)
    if bloqueado:
        bot.answer_callback_query(c.id, "🔒 Bloqueado temporalmente", show_alert=True)
        return

    # 🔒 VERIFICAR MANTENIMIENTO EN BOTONES
    if esta_en_mantenimiento() and str(uid) != str(ADMIN_ID):
        bot.answer_callback_query(c.id, "🔧 Bot en mantenimiento", show_alert=True)
        return

    # 🔙 VOLVER MENU
    if data == "volver_menu":
        bot.delete_message(c.message.chat.id, c.message.message_id)
        start(c.message)
        
    # 📋 MENU SERVICIOS
    elif data == "menu_servicios":
        estado, txt = verificar_conexion()
        bot.edit_message_text(f"📦 <b>CATÁLOGO</b>\n🔌 Estado: {txt}", 
                              c.message.chat.id, c.message.message_id,
                              reply_markup=menu_categorias(), parse_mode="HTML")
        
    # 👁️ VER CATEGORÍAS
    elif data.startswith("ver_"):
        cat = data.split("_")[1]
        emoji = {"tiktok":"🎵","insta":"📸","youtube":"📺","telegram":"✈️","facebook":"📘"}.get(cat,"📱")
        bot.edit_message_text(f"{emoji} <b>SERVICIOS DE {cat.upper()}</b>", 
                              c.message.chat.id, c.message.message_id,
                              reply_markup=lista_servicios(cat, SERVICIOS, MONEDA), parse_mode="HTML")
        
    # SELECCIONAR SERVICIO
    elif data.startswith("sel_"):
        sid = data.split("_")[1]
        info = SERVICIOS[sid]
        
        # 💰 PRECIO SEGÚN TIPO DE USUARIO
        precio_mostrar, ganancia = calcular_precio_y_comision(uid, info['precio_por_mil'])
        
        txt = f"""
📌 <b>{info['nombre']}</b>
💸 Precio: <b>{MONEDA} {precio_mostrar}/K</b>

ℹ️ <i>{info.get('descripcion','Servicio premium')}</i>

🔘 Usa ➕➖ para cambiar cantidad:
        """
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id,
                              reply_markup=selector_cant(sid, 100, MONEDA), parse_mode="HTML")
        
    # CONTROL DE CANTIDAD
    elif data.startswith("mas_") or data.startswith("menos_"):
        partes = data.split("_")
        acc, sid, cant = partes[0], partes[1], int(partes[2])
        nueva = cant + 100 if acc == "mas" else max(100, cant-100)
        total, precio_desc, porcentaje, ganancia = calcular_total(sid, nueva)
        
        if es_seller(uid):
            precio_base = total
            total, ganancia = calcular_precio_y_comision(uid, precio_base)
        
        txt = f"""
📌 <b>{SERVICIOS[sid]['nombre']}</b>

🔢 Cantidad: <b>{nueva:,}</b>
💰 Precio c/1K: <b>{MONEDA} {precio_desc}</b> {f'(-{porcentaje}%)' if porcentaje>0 else ''}

💳 <b>TOTAL: {MONEDA} {total}</b>

✅ Presiona confirmar para continuar.
        """
        bot.edit_message_text(txt, c.message.chat.id, c.message.message_id,
                              reply_markup=selector_cant(sid, nueva, MONEDA), parse_mode="HTML")
        
    # CONFIRMAR COMPRA
    elif data.startswith("ok_"):
        sid, cant = data.split("_")[1], int(data.split("_")[2])
        total, precio_desc, porcentaje, ganancia = calcular_total(sid, cant)
        
        if es_seller(uid):
            precio_real, ganancia = calcular_precio_y_comision(uid, total)
            if obtener_saldo(uid) < precio_real:
                bot.answer_callback_query(c.id, "❌ SALDO INSUFICIENTE", show_alert=True)
                return
            total_a_pagar = precio_real
        else:
            total_a_pagar = total
            ganancia = ganancia
        
        if obtener_saldo(uid) < total_a_pagar:
            bot.answer_callback_query(c.id, "❌ SALDO INSUFICIENTE", show_alert=True)
            return
            
        bot.send_message(c.message.chat.id, "🔗 <b>ENVÍA EL LINK</b>\nSolo enlaces oficiales:", parse_mode="HTML")
        bot.register_next_step_handler(c.message, proceso_final, sid=sid, cant=cant, total=total_a_pagar, ganancia=ganancia)
        
    # PERFIL
    elif data == "perfil":
        saldo = obtener_saldo(uid)
        nivel = obtener_nivel(uid)
        datos_user = obtener_datos_usuario(uid)
        registro = datos_user.get("registro", "Desconocido")
        ultimo = datos_user.get("ultimo_acceso", "Hoy")
        txt = f"""
👤 <b>MI PERFIL</b> {nivel}
🆔 ID: <code>{uid}</code>
💰 Saldo: <b>{MONEDA} {saldo:.2f}</b>
📅 Registrado: <code>{registro}</code>
🕒 Último acceso: <code>{ultimo}</code>

💎 <i>¡Disfruta de nuestros servicios!</i>
        """
        bot.send_message(c.message.chat.id, txt, parse_mode="HTML", reply_markup=boton_volver())
        
    # DEPOSITAR
    elif data == "depositar":
        txt = obtener_metodos_pago()
        bot.send_message(c.message.chat.id, txt, parse_mode="HTML", reply_markup=boton_volver())
        
    # ORDENES
    elif data == "ordenes":
        hist = obtener_historial_usuario(uid)
        bot.send_message(c.message.chat.id, hist, parse_mode="HTML", reply_markup=boton_volver())
        
    # 👑 OPCIONES DE ADMIN (CON BOTONES)
    elif data.startswith('admin_'):
        procesar_admin(bot, c)
        
    # 🎬 OPCIONES DE PREMIUM
    elif data.startswith('premium_'):
        procesar_premium(bot, c)
        
    # 🧑‍💼 OPCIONES DE SELLERS
    elif data.startswith('s_'):
        procesar_seller(bot, c)

# ==============================================
# 🚀 PROCESO FINAL DE COMPRA
# ==============================================
def proceso_final(msg, sid, cant, total, ganancia):
    uid = str(msg.from_user.id)
    nombre = msg.from_user.first_name
    link = msg.text
    info = SERVICIOS[sid]
    
    # 🔒 Seguridad
    if esta_en_mantenimiento() and str(uid) != str(ADMIN_ID):
        bot.send_message(msg.chat.id, "🔧 <b>BOT EN MANTENIMIENTO</b>", parse_mode="HTML")
        return
        
    if not validar_link_seguro(link):
        bot.send_message(msg.chat.id, "❌ <b>LINK NO PERMITIDO</b>", parse_mode="HTML")
        return
    link = sanitizar_texto(link)
    
    # 💰 Pago
    actualizar_saldo(uid, -total, f"Compra: {info['nombre']}")
    
    # 🧑‍💼 REGISTRAR GANANCIA SI ES SELLER
    if es_seller(uid):
        registrar_venta_reseller(uid, info['nombre'], total, ganancia)
        registrar_venta_seller(uid, nombre, info['nombre'], total, ganancia)  # 📢 LOG
    
    # 📤 Envío
    bot.send_message(msg.chat.id, "⏳ <b>PROCESANDO...</b>", parse_mode="HTML")
    res = enviar_pedido(info['api_id'], link, cant)
    
    # 📋 Registro
    orden_id = res.get('order','0000')
    registrar_compra(uid, sid, cant, total, link, orden_id)
    
    # 📢 LOG DE COMPRA
    registrar_compra(uid, nombre, info['nombre'], cant, total, ganancia, orden_id)
    
    # 🔔 Notificación Admin
    bot.send_message(ADMIN_ID, f"""
🛒 <b>¡NUEVA VENTA!</b>
👤 Usuario: {nombre}
🆔 ID: <code>{uid}</code>
📦 Servicio: {info['nombre']}
🔢 Cantidad: {cant:,}
💸 Monto: {MONEDA} {total}
💰 <b>GANANCIA: {MONEDA} {ganancia}</b>
🔗 Link: {link}
🆔 Orden: #{orden_id}
    """, parse_mode="HTML")
    
    # ✅ Respuesta
    if "order" in res:
        txt = f"""
✅ <b>¡ORDEN CREADA!</b>

📦 <b>{info['nombre']}</b>
🔢 Cantidad: <b>{cant:,}</b>
💸 Total: <b>{MONEDA} {total}</b>
🆔 ID: <code>#{orden_id}</code>

⏳ <i>Procesando...</i>
⌛ <i>Tiempo: {info.get('tiempo','Minutos')}</i>

💎 <b>¡Gracias por tu compra!</b>
        """
        bot.send_message(msg.chat.id, txt, parse_mode="HTML", reply_markup=menu_principal())
    else:
        actualizar_saldo(uid, total, "Reembolso por error")
        bot.send_message(msg.chat.id, f"❌ <b>ERROR</b>\n{res.get('error','Error desconocido')}", parse_mode="HTML")

# ==============================================
# ▶️ INICIO DEL SISTEMA
# ==============================================
if __name__ == "__main__":
    print("\033[92m")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    🤖 BOT SMM - VERSIÓN MAESTRA v6.0                ║")
    print("║ ✅ MONGODB | 🔑 LICENCIAS | 🎁 GIVEAWAYS | 👑 PANEL     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\033[94m[INFO]\033[0m 🍃 Base de Datos: MongoDB Conectada")
    print(f"\033[94m[INFO]\033[0m 📢 Sistema de Logs: ACTIVO")
    print(f"\033[94m[INFO]\033[0m 🔑 Sistema de Licencias: ACTIVO")
    print(f"\033[94m[INFO]\033[0m 🎁 Sistema de Giveaways: ACTIVO")
    print(f"\033[94m[INFO]\033[0m Servicios activos: {len(SERVICIOS)}")
    print(f"\033[94m[INFO]\033[0m Sistema Sellers: CONECTADO")
    print(f"\033[94m[INFO]\033[0m Sistema Premium: CONECTADO")
    print(f"\033[94m[INFO]\033[0m Panel Maestro: LISTO")
    print(f"\033[94m[INFO]\033[0m SISTEMA 100% OPERATIVO")
    print("\033[92m🚀 INICIANDO BOT...\033[0m")
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"\033[91m[ERROR]\033[0m {str(e)}")
        registrar_error("CRASH", str(e))
