# ==============================================
# 💳 SISTEMA DE TARJETAS CC
# ==============================================

import os
from config import *
from database import *
from logger import *

# ==============================================
# 💲 PRECIOS Y CONFIGURACIÓN
# ==============================================
PRECIOS = {
    "visa": 15.00,
    "mastercard": 12.00,
    "amex": 20.00,
    "discover": 10.00
}

BASES_CC = {
    "visa": {
        "nombre": "💳 VISA",
        "precio": PRECIOS["visa"],
        "tarjetas": []
    },
    "mastercard": {
        "nombre": "💳 MASTERCARD",
        "precio": PRECIOS["mastercard"],
        "tarjetas": []
    },
    "amex": {
        "nombre": "💳 AMERICAN EXPRESS",
        "precio": PRECIOS["amex"],
        "tarjetas": []
    },
    "discover": {
        "nombre": "💳 DISCOVER",
        "precio": PRECIOS["discover"],
        "tarjetas": []
    }
}

# ==============================================
# 📄 CARGA DESDE ARCHIVOS .TXT
# ==============================================
def cargar_tarjetas():
    """Lee los archivos y carga las tarjetas en memoria"""
    
    for tipo, datos in BASES_CC.items():
        ruta_archivo = os.path.join(RUTA_BASES_TXT, f"{tipo}.txt")
        
        if os.path.exists(ruta_archivo):
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                    lineas = archivo.readlines()
                    datos['tarjetas'] = [linea.strip() for linea in lineas if linea.strip()]
                
                log_info(f"✅ Cargadas {len(datos['tarjetas'])} tarjetas de {tipo.upper()}")
            
            except Exception as error:
                log_error(f"❌ Error al leer {tipo}.txt: {str(error)}")
                datos['tarjetas'] = []
        else:
            datos['tarjetas'] = []
            log_warning(f"⚠️ Archivo {tipo}.txt no encontrado en {ruta_archivo}")

# Ejecutar carga automática
cargar_tarjetas()

# ==============================================
# 📋 MENÚ VISUAL PARA USUARIO
# ==============================================
def menu_tienda():
    """Genera el texto con precios y disponibilidad"""
    
    texto = """
💳 <b>TARJETAS C R E D I T   C A R D S</b>

🔹 <b>Disponibles y Verificadas</b>
🔒 <b>Full Data • Alta Aprobación</b>

────────────────────────────────────────
"""
    for tipo, datos in BASES_CC.items():
        estado = "✅ DISPONIBLE" if len(datos['tarjetas']) > 0 else "❌ AGOTADO"
        texto += f"{datos['nombre']}\n"
        texto += f"💲 Precio: {MONEDA} {datos['precio']:.2f} | {estado}\n"
        texto += "────────────────────────────────────────\n"

    texto += "\n🔘 <b>Selecciona una opción para comprar</b>"
    return texto

# ==============================================
# 📦 OBTENER DATOS
# ==============================================
def obtener_bases():
    return BASES_CC

def obtener_stock_total():
    return sum(len(datos['tarjetas']) for datos in BASES_CC.values())

# ==============================================
# 💸 PROCESO DE VENTA
# ==============================================
def vender_tarjeta(id_usuario, nombre_usuario, tipo_tarjeta):
    """
    Valida, descuenta saldo y entrega la tarjeta
    """
    
    # Validar tipo
    if tipo_tarjeta not in BASES_CC:
        return False, "❌ <b>Tipo de tarjeta no válido o no disponible</b>"

    base = BASES_CC[tipo_tarjeta]

    # Verificar stock
    if not base['tarjetas']:
        return False, "❌ <b>Lo sentimos, actualmente no hay stock disponible</b>"
    
    # Datos económicos
    saldo_actual = obtener_saldo(id_usuario)
    precio = base['precio']

    # Verificar fondos
    if saldo_actual < precio:
        return False, f"""
❌ <b>SALDO INSUFICIENTE</b>

💰 Precio: {MONEDA} {precio:.2f}
💵 Tu saldo: {MONEDA} {saldo_actual:.2f}

🔹 Necesitas recargar para poder comprar.
"""

    # Ejecutar venta
    tarjeta_entregada = base['tarjetas'].pop(0)
    descontar_saldo(id_usuario, precio)
    registrar_compra_db(id_usuario, nombre_usuario, f"Tarjeta {base['nombre']}", precio, "Activo")

    # LOG
    log_info(f"💳 VENTA: {nombre_usuario} compró {tipo_tarjeta} por {MONEDA} {precio}")

    # Mensaje final
    mensaje_respuesta = f"""
╔════════════════════════════════════════╗
║       ✅  C O M P R A   R E A L I Z A D A      ║
╚════════════════════════════════════════╝

🎫 <b>Detalles de tu compra:</b>

💳 Producto: <b>{base['nombre']}</b>
💰 Precio: <b>{MONEDA} {precio:.2f}</b>
📉 Saldo restante: <b>{MONEDA} {obtener_saldo(id_usuario):.2f}</b>

────────────────────────────────────────
🔐 <b>TU TARJETA:</b>
<code>{tarjeta_entregada}</code>

⚠️ <b>IMPORTANTE:</b>
• No compartas esta información con nadie.
• Úsala solo en sitios seguros y confiables.
• Si falla, intenta en otro sitio o hora.

────────────────────────────────────────
🙏 <b>¡Gracias por tu compra!</b>
"""

    return True, mensaje_respuesta
