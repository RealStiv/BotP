# ==============================================
# 🏦 GESTOR DE MÉTODOS DE PAGO - v6.0
# ==============================================
# ✅ Gestión completa de métodos
# ✅ Logs en canal
# ✅ Compatible MongoDB
# ==============================================

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from logger import *  # 📝 Sistema de registros

# ==============================================
# 🏦 BASE DE DATOS DE MÉTODOS
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
# 🎛️ PANEL PRINCIPAL
# ==============================================
def menu_gestion_pagos():
    """Genera el menú principal de administración"""
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
    for clave, metodo in PAYMENT_METHODS.items():
        estado = "✅" if metodo['activo'] else "❌"
        btn = InlineKeyboardButton(f"{estado} {metodo['nombre']}", callback_data=f"edit_pay_{clave}")
        markup.add(btn)
    
    # Botones generales
    btn_add = InlineKeyboardButton("➕ AGREGAR NUEVO", callback_data="add_new_pay")
    btn_back = InlineKeyboardButton("🔙 VOLVER AL PANEL", callback_data="admin_menu")
    markup.add(btn_add, btn_back)
    
    return texto, markup

# ==============================================
# 📝 EDITAR MÉTODO ESPECÍFICO
# ==============================================
def editar_metodo(clave):
    """Muestra opciones para un método específico"""
    if clave not in PAYMENT_METHODS:
        return "❌ Método no encontrado.", None
    
    metodo = PAYMENT_METHODS[clave]
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
    btn1 = InlineKeyboardButton("🔄 ACTIVAR / DESACTIVAR", callback_data=f"toggle_{clave}")
    btn2 = InlineKeyboardButton("✏️ EDITAR TEXTO / DATOS", callback_data=f"change_text_{clave}")
    btn3 = InlineKeyboardButton("💲 EDITAR COMISIÓN", callback_data=f"change_fee_{clave}")
    btn4 = InlineKeyboardButton("🗑️ ELIMINAR MÉTODO", callback_data=f"delete_pay_{clave}")
    btn5 = InlineKeyboardButton("🔙 VOLVER", callback_data="manage_payments")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    return texto, markup

# ==============================================
# 🔄 CAMBIAR ESTADO
# ==============================================
def toggle_estado(clave, id_admin="Admin"):
    """Activa o desactiva el método"""
    if clave in PAYMENT_METHODS:
        PAYMENT_METHODS[clave]['activo'] = not PAYMENT_METHODS[clave]['activo']
        nuevo_estado = "✅ ACTIVADO" if PAYMENT_METHODS[clave]['activo'] else "❌ DESACTIVADO"
        
        # 📝 Registro
        log_info(f"PAGO: {PAYMENT_METHODS[clave]['nombre']} -> {nuevo_estado} | Por: {id_admin}")
        
        return f"✅ <b>ESTADO CAMBIADO!</b>\n\n{PAYMENT_METHODS[clave]['nombre']}\nEstado: {nuevo_estado}"
    return "❌ Error"

# ==============================================
# ✏️ ACTUALIZAR DATOS
# ==============================================
def actualizar_datos(clave, nuevo_texto, id_admin="Admin"):
    """Cambia los datos de pago"""
    if clave in PAYMENT_METHODS:
        PAYMENT_METHODS[clave]['datos'] = nuevo_texto
        
        log_info(f"PAGO: Datos editados en {PAYMENT_METHODS[clave]['nombre']} | Por: {id_admin}")
        
        return f"✅ <b>DATOS ACTUALIZADOS!</b>\n\nLos cambios se ven al instante."
    return "❌ Error"

# ==============================================
# 💲 ACTUALIZAR COMISIÓN
# ==============================================
def actualizar_comision(clave, valor, id_admin="Admin"):
    """Cambia el porcentaje de comisión"""
    try:
        valor = float(valor)
        PAYMENT_METHODS[clave]['comision'] = valor
        
        log_info(f"PAGO: Comisión cambiada en {PAYMENT_METHODS[clave]['nombre']} a {valor}% | Por: {id_admin}")
        
        return f"✅ Comisión actualizada a: {valor}%"
    except:
        return "❌ Valor inválido"

# ==============================================
# ➕ AGREGAR NUEVO MÉTODO
# ==============================================
def agregar_nuevo(nombre, datos, comision=0.0, id_admin="Admin"):
    """Crea una nueva opción de pago"""
    nueva_clave = f"custom_{len(PAYMENT_METHODS)+1}"
    PAYMENT_METHODS[nueva_clave] = {
        "nombre": nombre,
        "estado": "activo",
        "monedas": ["USD", "BOB"],
        "datos": datos,
        "comision": comision,
        "activo": True
    }
    
    log_info(f"PAGO: Nuevo método '{nombre}' creado | Por: {id_admin}")
    
    return f"✅ <b>MÉTODO CREADO!</b>\n\n{nombre} ✅ Activado y listo."

# ==============================================
# 🗑️ ELIMINAR MÉTODO
# ==============================================
def eliminar_metodo(clave, id_admin="Admin"):
    """Elimina el método del sistema"""
    if clave in PAYMENT_METHODS:
        nombre = PAYMENT_METHODS[clave]['nombre']
        del PAYMENT_METHODS[clave]
        
        log_info(f"PAGO: Método eliminado '{nombre}' | Por: {id_admin}")
        
        return f"🗑️ <b>MÉTODO ELIMINADO</b>\n{nombre} ha sido borrado correctamente."
    return "❌ Error"

# ==============================================
# 📋 VISTA PARA USUARIOS
# ==============================================
def obtener_metodos_pago():
    """Muestra solo métodos activos al público"""
    texto = "💳 <b>MÉTODOS DE PAGO DISPONIBLES</b>\n\n"
    
    for clave, metodo in PAYMENT_METHODS.items():
        if metodo['activo']:
            texto += f"{metodo['nombre']}\n"
            texto += f"{metodo['datos']}\n"
            if metodo['comision'] > 0:
                texto += f"💸 Comisión: {metodo['comision']}%\n"
            texto += "\n"
    
    texto += "💰 <i>Recargas procesadas manualmente por el administrador</i>"
    return texto

def obtener_metodos_activos():
    """Devuelve diccionario con solo activos"""
    return {k: v for k, v in PAYMENT_METHODS.items() if v['activo']}

# ==============================================
# 💰 CÁLCULO DE PRECIO FINAL
# ==============================================
def aplicar_comision(monto, clave_metodo):
    """Suma la comisión del método al monto base"""
    if clave_metodo in PAYMENT_METHODS:
        comision = PAYMENT_METHODS[clave_metodo]['comision']
        monto_final = monto + (monto * comision / 100)
        return round(monto_final, 2)
    return round(monto, 2)
