# ==============================================
# 📝 SISTEMA DE LOGS - VERSIÓN DIOS
# ==============================================
# ✅ REGISTRA TODO LO QUE PASA EN EL BOT
# ✅ ARCHIVO + CONSOLA + CANAL TELEGRAM
# ✅ COMPRAS, COMANDOS, SELLERS, ACCIONES
# ==============================================

import logging
import os
import requests
from logging.handlers import RotatingFileHandler
from datetime import datetime
from config import *

# ==============================================
# 📂 CREAR CARPETA SI NO EXISTE
# ==============================================
if not os.path.exists('logs'):
    os.makedirs('logs')

# ==============================================
# ⚙️ CONFIGURACIÓN MAESTRA
# ==============================================
def setup_logger():
    logger = logging.getLogger("BOT_SMM_DIOS")
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger
    
    # 🎨 FORMATO ULTRA DETALLADO
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )
    
    # 📄 LOGS GENERALES
    file_handler = RotatingFileHandler(
        "logs/bot.log",
        maxBytes=50*1024*1024,
        backupCount=20,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    
    # ❌ LOGS DE ERRORES
    error_handler = RotatingFileHandler(
        "logs/errores.log",
        maxBytes=20*1024*1024,
        backupCount=10,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # 🖥️ CONSOLA
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger

# ==============================================
# 🚀 INICIALIZAR SISTEMA
# ==============================================
logger = setup_logger()

# ==============================================
# 📢 FUNCIÓN PARA ENVIAR A CANAL TELEGRAM
# ==============================================
def enviar_a_canal(texto):
    try:
        URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        datos = {
            "chat_id": CHANNEL_LOGS,
            "text": texto,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        requests.post(URL, data=datos, timeout=5)
    except Exception as e:
        logger.error(f"Fallo al enviar al canal: {str(e)}")

# ==============================================
# 📝 FUNCIONES BÁSICAS
# ==============================================
def log_info(mensaje):
    logger.info(mensaje)

def log_error(mensaje):
    logger.error(mensaje)

def log_warning(mensaje):
    logger.warning(mensaje)

# ==============================================
# 📊 REGISTRO TOTAL DE ACCIONES
# ==============================================

# 🔻 SISTEMA GENERAL
def registrar_inicio_bot():
    txt = f"""
🚀 <b>🔴 BOT ENCENDIDO - SISTEMA ACTIVO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Versión: MAESTRA v6.0 (DIOS MODE)
📅 Fecha: <code>{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</code>
🔄 Estado: LISTO PARA RECIBIR ACCIONES
"""
    log_info("=== BOT INICIADO CORRECTAMENTE ===")
    enviar_a_canal(txt)

def registrar_reinicio():
    txt = f"""
🔄 <b>♻️ REINICIO DE SISTEMA</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""
    log_info("=== SISTEMA REINICIADO ===")
    enviar_a_canal(txt)

def registrar_mantenimiento(estado):
    txt = f"""
🔧 <b>🛠️ MODO MANTENIMIENTO {estado.upper()}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
    log_info(f"MANTENIMIENTO {estado}")
    enviar_a_canal(txt)

# 🔻 USUARIOS
def registrar_usuario_nuevo(uid, nombre):
    txt = f"""
🆕 <b>✨ NUEVO USUARIO REGISTRADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Nombre: <code>{nombre}</code>
🆔 ID: <code>{uid}</code>
📅 Fecha: <code>{datetime.now().strftime("%d/%m/%Y %H:%M")}</code>
"""
    log_info(f"NUEVO USUARIO | ID: {uid} | NOMBRE: {nombre}")
    enviar_a_canal(txt)

def registrar_acceso(uid, nombre):
    log_info(f"ACCESO | USUARIO: {uid} | NOMBRE: {nombre}")

def registrar_baneo(uid, nombre, motivo=""):
    txt = f"""
🚫 <b>⛔ USUARIO BANEADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <code>{nombre}</code> | ID: <code>{uid}</code>
📝 Motivo: <code>{motivo}</code>
"""
    log_warning(f"BANEO | USUARIO: {uid} | MOTIVO: {motivo}")
    enviar_a_canal(txt)

# 🔻 COMPRAS SMM
def registrar_compra(uid, nombre, servicio, cantidad, monto, ganancia, orden_id):
    txt = f"""
🛒 <b>💸 COMPRA REALIZADA</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Cliente: <code>{nombre}</code>
🆔 ID: <code>{uid}</code>
📦 Servicio: <b>{servicio}</b>
🔢 Cantidad: <code>{cantidad:,}</code>
🔢 Orden: <code>#{orden_id}</code>
💸 Monto: <b>{MONEDA} {monto:.2f}</b>
💰 Ganancia Neta: <b>{MONEDA} {ganancia:.2f}</b>
📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
    log_info(f"COMPRA | USUARIO: {uid} | SERV: {servicio} | CANT: {cantidad} | MONTO: ${monto} | GAN: ${ganancia} | ORDEN: #{orden_id}")
    enviar_a_canal(txt)

# 🔻 COMPRAS PREMIUM
def registrar_compra_premium(uid, nombre, servicio, cuenta, precio):
    txt = f"""
🎬 <b>🎟️ VENTA CUENTA PREMIUM</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <code>{nombre}</code> | ID: <code>{uid}</code>
📦 Servicio: <b>{servicio}</b>
🔑 Cuenta entregada: <code>{cuenta}</code>
💸 Precio: <b>{MONEDA} {precio:.2f}</b>
"""
    log_info(f"VENTA PREMIUM | USUARIO: {uid} | SERV: {servicio} | PRECIO: ${precio}")
    enviar_a_canal(txt)

# 🔻 PAGOS Y SALDO
def registrar_pago(uid, nombre, metodo, monto):
    txt = f"""
💳 <b>💰 DEPÓSITO RECIBIDO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <code>{nombre}</code> | ID: <code>{uid}</code>
💰 Monto: <b>{MONEDA} {monto:.2f}</b>
🏦 Método: <b>{metodo}</b>
📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
    log_info(f"PAGO | USUARIO: {uid} | METODO: {metodo} | MONTO: ${monto}")
    enviar_a_canal(txt)

def registrar_add_saldo(uid, nombre, monto, admin_nombre):
    txt = f"""
💰 <b>➕ SALDO AGREGADO MANUAL</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Usuario: <code>{nombre}</code> | ID: <code>{uid}</code>
💵 Monto: <b>{MONEDA} {monto:.2f}</b>
👑 Por Admin: <code>{admin_nombre}</code>
"""
    log_info(f"SALDO + | USUARIO: {uid} | MONTO: ${monto} | ADMIN: {admin_nombre}")
    enviar_a_canal(txt)

def registrar_sub_saldo(uid, nombre, monto, admin_nombre):
    txt = f"""
💰 <b>➖ SALDO RETIRADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Usuario: <code>{nombre}</code> | ID: <code>{uid}</code>
💵 Monto: <b>{MONEDA} {monto:.2f}</b>
👑 Por Admin: <code>{admin_nombre}</code>
"""
    log_info(f"SALDO - | USUARIO: {uid} | MONTO: ${monto} | ADMIN: {admin_nombre}")
    enviar_a_canal(txt)

# 🔻 COMANDOS Y BOTONES
def registrar_comando(uid, nombre, comando, texto=""):
    txt = f"""
⌨️ <b>⌨️ COMANDO EJECUTADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <code>{nombre}</code> | ID: <code>{uid}</code>
🔘 Comando: <code>/{comando}</code>
📄 Texto: <code>{texto}</code>
"""
    log_info(f"COMANDO | USUARIO: {uid} | /{comando} | TEXTO: {texto}")
    enviar_a_canal(txt)

def registrar_boton(uid, nombre, accion):
    txt = f"""
🔘 <b>🔵 BOTÓN PRESIONADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <code>{nombre}</code> | ID: <code>{uid}</code>
⚡ Acción: <code>{accion}</code>
"""
    log_info(f"BOTON | USUARIO: {uid} | ACCION: {accion}")
    enviar_a_canal(txt)

# ==============================================
# 🤝 SECCION SELLERS - TODO REGISTRADO
# ==============================================

def registrar_seller_creado(uid, nombre, nivel, admin):
    txt = f"""
🤝 <b>👔 NUEVO VENDEDOR CREADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Nombre: <code>{nombre}</code> | ID: <code>{uid}</code>
🏅 Nivel asignado: <b>{nivel}</b>
👑 Creado por: <code>{admin}</code>
"""
    log_info(f"SELLER CREADO | ID: {uid} | NIVEL: {nivel}")
    enviar_a_canal(txt)

def registrar_venta_seller(uid, nombre, servicio, monto_total, ganancia_seller):
    txt = f"""
🤝 <b>💼 VENTA POR RESELLER</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Vendedor: <code>{nombre}</code> | ID: <code>{uid}</code>
📦 Servicio: <b>{servicio}</b>
💸 Monto total: <b>{MONEDA} {monto_total:.2f}</b>
💎 Ganancia del vendedor: <b>{MONEDA} {ganancia_seller:.2f}</b>
"""
    log_info(f"VENTA SELLER | ID: {uid} | SERV: {servicio} | GANANCIA: ${ganancia_seller}")
    enviar_a_canal(txt)

def registrar_retiro_seller(uid, nombre, monto):
    txt = f"""
💸 <b>🏧 RETIRO DE SALDO SOLICITADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Vendedor: <code>{nombre}</code> | ID: <code>{uid}</code>
💰 Monto a retirar: <b>{MONEDA} {monto:.2f}</b>
📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
    log_info(f"RETIRO SELLER | ID: {uid} | MONTO: ${monto}")
    enviar_a_canal(txt)

def registrar_cambio_nivel(uid, nombre, nivel_anterior, nivel_nuevo):
    txt = f"""
📈 <b>⭐ CAMBIO DE NIVEL SELLER</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Usuario: <code>{nombre}</code> | ID: <code>{uid}</code>
📉 Anterior: <b>{nivel_anterior}</b>
📈 Nuevo: <b>{nivel_nuevo}</b>
"""
    log_info(f"NIVEL CAMBIADO | ID: {uid} | DE: {nivel_anterior} A: {nivel_nuevo}")
    enviar_a_canal(txt)

def registrar_estado_seller(uid, nombre, estado):
    txt = f"""
🔒 <b>🚫 ESTADO DE CUENTA CAMBIADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 <code>{nombre}</code> | ID: <code>{uid}</code>
🔄 Nuevo estado: <b>{estado.upper()}</b>
"""
    log_info(f"ESTADO SELLER | ID: {uid} | ESTADO: {estado}")
    enviar_a_canal(txt)

# 🔻 API Y CONEXIONES
def registrar_api(accion, estado, detalles=""):
    txt = f"""
🌐 <b>🔌 CONEXIÓN API</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Acción: <code>{accion}</code>
📊 Estado: <b>{estado}</b>
📝 Detalles: <code>{detalles}</code>
"""
    log_info(f"API | {accion} | {estado} | {detalles}")
    enviar_a_canal(txt)

# 🔻 ERRORES
def registrar_error(tipo, descripcion, uid="None", nombre="Desconocido"):
    txt = f"""
⚠️ <b>🔴 ERROR CRÍTICO EN SISTEMA</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Tipo: <code>{tipo}</code>
👤 Usuario: <code>{nombre}</code> | ID: <code>{uid}</code>
📝 Descripción: <code>{descripcion}</code>
📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""
    log_error(f"ERROR | {tipo} | USUARIO: {uid} | DESC: {descripcion}")
    enviar_a_canal(txt)

# 🔻 ADMINISTRACIÓN
def registrar_agregar_cuentas(servicio, cantidad, admin):
    txt = f"""
📦 <b>📥 STOCK ACTUALIZADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Servicio: <b>{servicio}</b>
➕ Cantidad agregada: <code>{cantidad}</code>
👑 Por Admin: <code>{admin}</code>
"""
    log_info(f"STOCK + | SERV: {servicio} | CANT: +{cantidad} | ADMIN: {admin}")
    enviar_a_canal(txt)

def registrar_cambio_precio(servicio, anterior, nuevo, admin):
    txt = f"""
🏷️ <b>💱 PRECIO MODIFICADO</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Servicio: <b>{servicio}</b>
💱 Anterior: <b>{MONEDA} {anterior:.2f}</b>
✅ Nuevo: <b>{MONEDA} {nuevo:.2f}</b>
👑 Por Admin: <code>{admin}</code>
"""
    log_info(f"PRECIO | SERV: {servicio} | ${anterior} -> ${nuevo}")
    enviar_a_canal(txt)

# ==============================================
# 📜 VER LOGS DESDE EL PANEL
# ==============================================
def obtener_ultimos_registros(cantidad=50):
    try:
        with open("logs/bot.log", "r", encoding="utf-8") as f:
            lineas = f.readlines()
        return "\n".join(lineas[-cantidad:]) if lineas else "📝 No hay registros aún."
    except:
        return "❌ Error al leer archivo de logs"

def obtener_errores_recientes(cantidad=20):
    try:
        with open("logs/errores.log", "r", encoding="utf-8") as f:
            lineas = f.readlines()
        return "\n".join(lineas[-cantidad:]) if lineas else "✅ Sistema sin errores recientes."
    except:
        return "📝 Archivo de errores vacío."
