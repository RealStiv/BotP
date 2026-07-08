# ==============================================
# 🎬 SISTEMA DE CUENTAS PREMIUM PRO - v6.0
# ==============================================
# ✅ Stock, Precios, Garantía, Logs
# ✅ Compatible MongoDB
# ✅ Sistema de Ganancias y Comisiones
# ==============================================

import time
from datetime import datetime, timedelta
from config import *
from logger import *      # 📝 Sistema de registros
from database import *    # 🍃 Conexión MongoDB

# ==============================================
# 🗄️ STOCK DE CUENTAS
# ==============================================
# Formato: "usuario|contraseña|dias_garantia"
# ==============================================
CUENTAS_DISPONIBLES = {
    "netflix": [
        "usuario1@gmail.com|PassSegura123|30",
        "usuario2@hotmail.com|NetflixSafe456|30",
        "usuario3@outlook.com|MiCuenta789|30",
        "cliente01|Password100|30"
    ],
    "disney": [
        "disney_user@test.com|DisneyPlus2024|30",
        "streaming@mail.com|ClaveSegura|30"
    ],
    "hbo": [
        "hbo_max_1|MaxPass123!|30",
        "max_stream|HBO_Safe_456|30"
    ],
    "prime": [
        "amazon_prime|PrimeVideo2024|30",
        "prime_video|AmazonPass!|30"
    ],
    "spotify": [
        "spotify_premium|MusicHighQuality|30",
        "music_lover|SoundBest|30"
    ],
    "crunchy": [
        "anime_fan|AnimePass123|30",
        "otaku_master|CrunchySafe|30"
    ]
}

# ==============================================
# 🏷️ CATÁLOGO DE SERVICIOS
# ==============================================
SERVICIOS_PREMIUM = {
    "netflix": {
        "nombre": "🎬 NETFLIX PREMIUM",
        "precio": 15.00,
        "moneda": "USD",
        "descripcion": "HD | Pantallas: 4 | Actualizado"
    },
    "disney": {
        "nombre": "📺 DISNEY+ STAR+",
        "precio": 10.00,
        "moneda": "USD",
        "descripcion": "Full HD | Incluye Star+"
    },
    "hbo": {
        "nombre": "⚡ HBO MAX",
        "precio": 12.00,
        "moneda": "USD",
        "descripcion": "4K Ultra HD | Estrenos Exclusivos"
    },
    "prime": {
        "nombre": "🎦 AMAZON PRIME",
        "precio": 9.00,
        "moneda": "USD",
        "descripcion": "Películas y Envíos Gratis"
    },
    "spotify": {
        "nombre": "🎵 SPOTIFY PREMIUM",
        "precio": 8.00,
        "moneda": "USD",
        "descripcion": "Sin Anuncios | Salta Canciones"
    },
    "crunchy": {
        "nombre": "🍙 CRUNCHYROLL",
        "precio": 7.00,
        "moneda": "USD",
        "descripcion": "Anime Sin Publicidad"
    }
}

# ==============================================
# 🎫 FUNCIÓN PRINCIPAL: ENTREGAR CUENTA
# ==============================================
def entregar_cuenta(id_servicio, id_usuario, nombre_usuario, metodo_pago="Manual"):
    """
    Saca una cuenta del stock, la entrega y registra la venta.
    Retorna: (datos_cuenta, informacion_servicio) o (None, mensaje_error)
    """
    if id_servicio not in CUENTAS_DISPONIBLES:
        return None, "❌ Servicio no encontrado"
    
    if len(CUENTAS_DISPONIBLES[id_servicio]) == 0:
        return None, "⚠️ <b>AGOTADO</b>\nNo hay stock disponible por el momento."
    
    # Extraer primera cuenta de la lista
    cuenta_completa = CUENTAS_DISPONIBLES[id_servicio].pop(0)
    usuario_cuenta, contraseña_cuenta, dias_garantia = cuenta_completa.split("|")
    
    # Obtener precio y calcular ganancia
    info_servicio = SERVICIOS_PREMIUM[id_servicio]
    precio_venta, ganancia = calcular_precio_y_comision(id_usuario, info_servicio['precio'])
    
    # 📝 Guardar en base de datos
    registro_venta = {
        "uid": str(id_usuario),
        "nombre": nombre_usuario,
        "servicio": info_servicio['nombre'],
        "precio": precio_venta,
        "ganancia": ganancia,
        "cuenta": usuario_cuenta,
        "metodo": metodo_pago,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "garantia_hasta": (datetime.now() + timedelta(days=int(dias_garantia))).strftime("%d/%m/%Y")
    }
    guardar_venta_premium(registro_venta)
    
    # 📢 Notificación al canal y Log
    mensaje_log = f"""
🎬 <b>¡VENTA PREMIUM!</b>
👤 Usuario: {nombre_usuario}
🆔 ID: <code>{id_usuario}</code>
📦 Producto: {info_servicio['nombre']}
💸 Precio: {MONEDA} {precio_venta}
💰 Ganancia: {MONEDA} {ganancia}
🔐 Cuenta: <code>{usuario_cuenta}</code>
"""
    enviar_a_canal(mensaje_log)
    log_info(f"VENTA PREMIUM | Usuario: {id_usuario} | {info_servicio['nombre']} | ${precio_venta}")
    
    return (usuario_cuenta, contraseña_cuenta, int(dias_garantia)), info_servicio

# ==============================================
# 📋 FUNCIONES AUXILIARES
# ==============================================
def obtener_info(id_servicio):
    """Obtiene datos de un servicio específico"""
    return SERVICIOS_PREMIUM.get(id_servicio, None)

def stock_total(id_servicio):
    """Cantidad de cuentas disponibles"""
    return len(CUENTAS_DISPONIBLES.get(id_servicio, []))

def listar_servicios():
    """Lista completa del catálogo"""
    return SERVICIOS_PREMIUM

def agregar_cuentas(id_servicio, lista_cuentas, id_admin="Admin"):
    """Agrega nuevas cuentas al stock"""
    if id_servicio in CUENTAS_DISPONIBLES:
        CUENTAS_DISPONIBLES[id_servicio].extend(lista_cuentas)
        
        log_info(f"STOCK: +{len(lista_cuentas)} cuentas en {id_servicio} | Por: {id_admin}")
        return True, f"✅ Agregadas {len(lista_cuentas)} cuentas correctamente."
    
    return False, "❌ Servicio no encontrado"

# ==============================================
# 💰 CÁLCULO DE PRECIOS Y COMISIONES
# ==============================================
def calcular_precio_y_comision(id_usuario, precio_base):
    """Aplica descuento si es Seller, sino precio normal"""
    from sellers import es_seller, obtener_datos
    
    if es_seller(id_usuario):
        datos_seller = obtener_datos(id_usuario)
        if datos_seller and "info_nivel" in datos_seller:
            porcentaje = datos_seller['info_nivel']['comision']
            ganancia = (precio_base * porcentaje) / 100
            precio_final = precio_base - ganancia
            return round(precio_final, 2), round(ganancia, 2)
    
    # Usuario normal
    return round(precio_base, 2), 0

# ==============================================
# 📊 PANEL DE CONTROL - STOCK
# ==============================================
def ver_stock_completo():
    """Muestra estado del stock para admin"""
    texto = "📦 <b>STOCK DE CUENTAS PREMIUM</b>\n\n"
    for clave, cuentas in CUENTAS_DISPONIBLES.items():
        nombre = SERVICIOS_PREMIUM[clave]['nombre']
        cantidad = len(cuentas)
        estado = "🟢" if cantidad > 0 else "🔴"
        texto += f"{estado} <b>{nombre}</b>: <code>{cantidad} unidades</code>\n"
    return texto
