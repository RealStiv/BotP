# ==============================================
# 💳 SISTEMA DE TARJETAS CC
# ==============================================

import os
from config import *  # ⬅️ IMPORTANTE: Esto trae los precios
from database import *
from logger import *

# ==============================================
# 📦 BASES DE DATOS DE TARJETAS
# ==============================================
BASES_CC = {
    "visa": {
        "nombre": "💳 VISA",
        "precio": PRECIO_VISA,
        "tarjetas": []
    },
    "mastercard": {
        "nombre": "💳 MASTERCARD",
        "precio": PRECIO_MASTERCARD,
        "tarjetas": []
    },
    "amex": {
        "nombre": "💳 AMERICAN EXPRESS",
        "precio": PRECIO_AMEX,
        "tarjetas": []
    },
    "discover": {
        "nombre": "💳 DISCOVER",
        "precio": PRECIO_DISCOVER,
        "tarjetas": []
    }
}

# ==============================================
# 📄 CARGAR TARJETAS DESDE ARCHIVOS .TXT
# ==============================================
def cargar_tarjetas():
    """Carga las tarjetas desde la carpeta ./bases/"""
    for key, data in BASES_CC.items():
        ruta_archivo = f"{RUTA_BASES_TXT}{key}.txt"
        
        if os.path.exists(ruta_archivo):
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                    data['tarjetas'] = [linea.strip() for linea in lineas if linea.strip()]
                log_info(f"TARJETAS: Cargadas {len(data['tarjetas'])} de {key}")
            except Exception as e:
                log_error(f"ERROR al leer {key}.txt: {e}")
                data['tarjetas'] = []
        else:
            data['tarjetas'] = []
            log_warning(f"TARJETAS: Archivo {key}.txt no encontrado")

# Cargar al iniciar
cargar_tarjetas()

# ==============================================
# 📋 MENU TIENDA
# ==============================================
def menu_tienda():
    texto = """
💳 <b>TARJETAS C R E D I T   C A R D S</b>

🔹 <b>Disponibles y Verificadas</b>
🔒 <b>Full Data • Alta Aprobación</b>

────────────────────────────────────────
"""
    for key, data in BASES_CC.items():
        estado = "✅ DISPONIBLE" if len(data['tarjetas']) > 0 else "❌ AGOTADO"
        texto += f"{data['nombre']}\n"
        texto += f"💲 Precio: <b>{MONEDA} {data['precio']:.2f}</b> | {estado}\n"
        texto += "────────────────────────────────────────\n"
    
    texto += "\n🔘 <b>Selecciona una opción para comprar</b>"
    return texto

# ==============================================
# 📦 OBTENER BASES
# ==============================================
def obtener_bases():
    return BASES_CC

# ==============================================
# 🔢 OBTENER STOCK TOTAL
# ==============================================
def obtener_stock_total():
    total = 0
    for data in BASES_CC.values():
        total += len(data['tarjetas'])
    return total

# ==============================================
# 💸 VENDER TARJETA
# ==============================================
def vender_tarjeta(uid, nombre, tipo):
    if tipo not in BASES_CC:
        return False, "❌ Tipo de tarjeta no válido"
    
    base = BASES_CC[tipo]
    
    if len(base['tarjetas']) == 0:
        return False, "❌ Lo sentimos, no hay stock disponible por ahora"
    
    # Verificar saldo
    saldo_usuario = obtener_saldo(uid)
    precio = base['precio']
    
    if saldo_usuario < precio:
        return False, f"""
❌ <b>SALDO INSUFICIENTE</b>

💰 Precio: {MONEDA} {precio:.2f}
💵 Tu saldo: {MONEDA} {saldo_usuario:.2f}

🔹 Recarga y vuelve a intentar.
"""
    
    # Tomar la primera tarjeta
    tarjeta = base['tarjetas'].pop(0)
    
    # Descontar saldo
    descontar_saldo(uid, precio)
    
    # Registrar compra
    registrar_compra_db(uid, nombre, f"Tarjeta {base['nombre']}", precio, "Activo")
    
    log_info(f"VENTA: {nombre} compró {tipo} por {precio}")
    
    mensaje_exito = f"""
╔════════════════════════════════════════╗
║       ✅  C O M P R A   R E A L I Z A D A      ║
╚════════════════════════════════════════╝

🎫 <b>Detalles de tu compra:</b>

💳 Producto: <b>{base['nombre']}</b>
💰 Precio: <b>{MONEDA} {precio:.2f}</b>
📉 Saldo restante: <b>{MONEDA} {obtener_saldo(uid):.2f}</b>

────────────────────────────────────────
🔐 <b>TU TARJETA:</b>
<code>{tarjeta}</code>

⚠️ <b>IMPORTANTE:</b>
• No compartas esta información
• Úsala solo para compras seguras
• Respeta los límites establecidos

────────────────────────────────────────
🙏 <b>¡Gracias por tu compra!</b>
"""
    
    return True, mensaje_exito
