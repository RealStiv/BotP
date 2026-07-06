# ==============================================
# 🏦 GESTOR DE MÉTODOS DE PAGO - v6.0
# ==============================================
# ✅ Gestión completa de métodos
# ✅ Logs en canal
# ✅ Compatible MongoDB
# ==============================================

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from logger import *  # 📝 SISTEMA DE LOGS

# ==============================================
# 🏦 BASE DE DATOS DE MÉTODOS DE PAGO
# ==============================================
PAYMENT_METHODS = {
    "binance": {
        "nombre": "🪙 Binance Pay",
        "estado": "activo",
        "monedas": ["USDT", "BNB", "BTC"],
        "datos": "🔗 Enlace: tu_link\n📱 ID: 123456",
        "comision": 0.00,
        "activo": True
    },
    "tigo": {
        "nombre": "🔵 Tigo Money",
        "estado": "activo",
        "monedas": ["BOB", "USD"],
        "datos": "📱 Número: +591 7XXXXXXX\n👤 Nombre: Tu Nombre",
        "comision": 0.00,
        "activo": True
    },
    "whatsapp": {
        "nombre": "📱 WhatsApp / Transferencia",
        "estado": "activo",
        "monedas": ["BOB", "USD"],
        "datos": "💬 Enviar comprobante al +591 7XXXXXXX",
        "comision": 0.00,
        "activo": True
    },
    "banco": {
        "nombre": "🏦 Banco BNB",
        "estado": "inactivo",
        "monedas": ["BOB"],
        "datos": "🏦 Cuenta Corriente: 12345678\n👤 Nombre: Empresa SRL",
        "comision": 1.50,
        "activo": False
    }
}

# ==============================================
# 🎛️ MENÚ PRINCIPAL DE GESTIÓN
# ==============================================
def menu_gestion_pagos():
    markup = InlineKeyboardMarkup(row_width=2)
    
    texto = f"""
⚙️ <b>PANEL DE CONTROL DE PAGOS</b> 🎛️

<b>Estado del Sistema:</b> 🟢 ACTIVO
<b>Moneda Base:</b> {MONEDA}

📊 <b>Estadísticas:</b>
• ✅ Métodos Activados: {sum(1 for m in PAYMENT_METHODS.values() if m['activo'])}
• ❌ Métodos Desactivados: {sum(1 for m in PAYMENT_METHODS.values() if not m['activo'])}
• 🏦 Total Métodos: {len(PAYMENT_METHODS)}

<b>🔧 Selecciona una opción:</b>
"""
    # Botones de métodos
    for key, metodo in PAYMENT_METHODS.items():
        estado = "✅" if metodo['activo'] else "❌"
        btn = InlineKeyboardButton(f"{estado} {metodo['nombre']}", callback_data=f"edit_pay_{key}")
        markup.add(btn)
    
    # Botones de acción
    btn_add = InlineKeyboardButton("➕ AGREGAR NUEVO", callback_data="add_new_pay")
    btn_back = InlineKeyboardButton("🔙 VOLVER AL PANEL", callback_data="admin_menu")
    markup.add(btn_add, btn_back)
    
    return texto, markup

# ==============================================
# 📝 EDITAR MÉTODO ESPECÍFICO
# ==============================================
def editar_metodo(key):
    if key not in PAYMENT_METHODS:
        return "❌ Método no encontrado.", None
    
    metodo = PAYMENT_METHODS[key]
    estado_txt = "✅ ACTIVO" if metodo['activo'] else "❌ INACTIVO"
    
    texto = f"""
📌 <b>{metodo['nombre']}</b>

🚦 <b>Estado:</b> {estado_txt}
💰 <b>Comisión:</b> {metodo['comision']}%
💱 <b>Monedas:</b> {', '.join(metodo['monedas'])}

📝 <b>DATOS DE PAGO:</b>
<pre>{metodo['datos']}</pre>

<b>¿Qué deseas hacer con este método?</b>
"""
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("🔄 ACTIVAR / DESACTIVAR", callback_data=f"toggle_{key}")
    btn2 = InlineKeyboardButton("✏️ EDITAR TEXTO / DATOS", callback_data=f"change_text_{key}")
    btn3 = InlineKeyboardButton("💲 EDITAR COMISIÓN", callback_data=f"change_fee_{key}")
    btn4 = InlineKeyboardButton("🗑️ ELIMINAR MÉTODO", callback_data=f"delete_pay_{key}")
    btn5 = InlineKeyboardButton("🔙 VOLVER", callback_data="manage_payments")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    return texto, markup

# ==============================================
# 🔄 ACTIVAR / DESACTIVAR
# ==============================================
def toggle_estado(key, admin_id):
    if key in PAYMENT_METHODS:
        PAYMENT_METHODS[key]['activo'] = not PAYMENT_METHODS[key]['activo']
        nuevo_estado = "✅ ACTIVADO" if PAYMENT_METHODS[key]['activo'] else "❌ DESACTIVADO"
        
        # 📝 LOG
        log_info(f"PAGO: {PAYMENT_METHODS[key]['nombre']} -> {nuevo_estado} por Admin {admin_id}")
        
        return f"✅ <b>ESTADO CAMBIADO!</b>\n\n{PAYMENT_METHODS[key]['nombre']}\nEstado: {nuevo_estado}"
    return "❌ Error"

# ==============================================
# ✏️ EDITAR DATOS
# ==============================================
def actualizar_datos(key, nuevo_texto, admin_id):
    if key in PAYMENT_METHODS:
        PAYMENT_METHODS[key]['datos'] = nuevo_texto
        
        # 📝 LOG
        log_info(f"PAGO: Datos editados en {PAYMENT_METHODS[key]['nombre']} por Admin {admin_id}")
        
        return f"✅ <b>DATOS ACTUALIZADOS!</b>\n\nLos cambios se ven al instante."
    return "❌ Error"

# ==============================================
# 💲 EDITAR COMISIÓN
# ==============================================
def actualizar_comision(key, valor, admin_id):
    try:
        valor = float(valor)
        PAYMENT_METHODS[key]['comision'] = valor
        
        # 📝 LOG
        log_info(f"PAGO: Comisión cambiada en {PAYMENT_METHODS[key]['nombre']} a {valor}% por Admin {admin_id}")
        
        return f"✅ Comisión actualizada a: {valor}%"
    except:
        return "❌ Valor inválido"

# ==============================================
# ➕ AGREGAR NUEVO MÉTODO
# ==============================================
def agregar_nuevo(nombre, datos, comision=0.0, admin_id="Admin"):
    new_id = f"custom_{len(PAYMENT_METHODS)+1}"
    PAYMENT_METHODS[new_id] = {
        "nombre": nombre,
        "estado": "activo",
        "monedas": ["USD", "BOB"],
        "datos": datos,
        "comision": comision,
        "activo": True
    }
    
    # 📝 LOG
    log_info(f"PAGO: Nuevo método creado '{nombre}' por {admin_id}")
    
    return f"✅ <b>MÉTODO CREADO!</b>\n\n{nombre} ✅ Activado y listo."

# ==============================================
# 🗑️ ELIMINAR MÉTODO
# ==============================================
def eliminar_metodo(key, admin_id):
    if key in PAYMENT_METHODS:
        nombre = PAYMENT_METHODS[key]['nombre']
        del PAYMENT_METHODS[key]
        
        # 📝 LOG
        log_info(f"PAGO: Método eliminado '{nombre}' por Admin {admin_id}")
        
        return f"🗑️ <b>MÉTODO ELIMINADO</b>\n{nombre} ha sido borrado correctamente."
    return "❌ Error"

# ==============================================
# 📋 LISTAR PARA USUARIOS (Solo activos)
# ==============================================
def obtener_metodos_pago():
    """Devuelve el texto con los métodos visibles para usuarios"""
    texto = "💳 <b>MÉTODOS DE PAGO DISPONIBLES</b>\n\n"
    
    for key, metodo in PAYMENT_METHODS.items():
        if metodo['activo']:
            texto += f"{metodo['nombre']}\n"
            texto += f"{metodo['datos']}\n"
            if metodo['comision'] > 0:
                texto += f"💸 Comisión: {metodo['comision']}%\n"
            texto += "\n"
    
    texto += "💰 <i>Recargas procesadas manualmente por el administrador</i>"
    return texto

def obtener_metodos_activos():
    activos = {}
    for key, m in PAYMENT_METHODS.items():
        if m['activo']:
            activos[key] = m
    return activos

# ==============================================
# 💰 CALCULAR COMISIÓN
# ==============================================
def aplicar_comision(monto, metodo_key):
    """Aplica la comisión del método de pago al monto"""
    if metodo_key in PAYMENT_METHODS:
        comision = PAYMENT_METHODS[metodo_key]['comision']
        monto_final = monto + (monto * comision / 100)
        return round(monto_final, 2)
    return monto
