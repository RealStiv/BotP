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
from logger import *      # 📝 SISTEMA DE LOGS
from database import *    # 🍃 MONGODB

# ==============================================
# 🗄️ BASE DE DATOS DE CUENTAS
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
# 🏷️ PRECIOS Y NOMBRES
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
def entregar_cuenta(servicio_id, uid, nombre, metodo_pago="Manual"):
    """
    Saca una cuenta del stock, la entrega y registra la venta
    Retorna: (usuario, contraseña, dias_garantia) o None
    """
    if servicio_id not in CUENTAS_DISPONIBLES:
        return None, "❌ Servicio no encontrado"
    
    if len(CUENTAS_DISPONIBLES[servicio_id]) == 0:
        return None, "⚠️ <b>AGOTADO</b>\nNo hay stock disponible por el momento."
    
    # Sacar la primera cuenta de la lista
    cuenta_completa = CUENTAS_DISPONIBLES[servicio_id].pop(0)
    usuario_cuenta, contraseña_cuenta, dias = cuenta_completa.split("|")
    
    # Obtener precio y calcular ganancia
    info = SERVICIOS_PREMIUM[servicio_id]
    precio_venta, ganancia = calcular_precio_y_comision(uid, info['precio'])
    
    # 📝 REGISTRAR EN MONGODB
    venta_db = {
        "uid": str(uid),
        "nombre": nombre,
        "servicio": info['nombre'],
        "precio": precio_venta,
        "ganancia": ganancia,
        "cuenta": usuario_cuenta,
        "metodo": metodo_pago,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "garantia_hasta": (datetime.now() + timedelta(days=int(dias))).strftime("%d/%m/%Y")
    }
    guardar_venta_premium(venta_db)
    
    # 📢 LOG EN CANAL
    txt_log = f"""
🎬 <b>¡VENTA PREMIUM!</b>
👤 Usuario: {nombre}
🆔 ID: <code>{uid}</code>
📦 Producto: {info['nombre']}
💸 Precio: {MONEDA} {precio_venta}
💰 Ganancia: {MONEDA} {ganancia}
🔐 Cuenta: <code>{usuario_cuenta}</code>
"""
    enviar_a_canal(txt_log)
    log_info(f"VENTA PREMIUM | Usuario: {uid} | {info['nombre']} | ${precio_venta}")
    
    return (usuario_cuenta, contraseña_cuenta, int(dias)), info

# ==============================================
# 📋 FUNCIONES AUXILIARES
# ==============================================
def obtener_info(servicio_id):
    return SERVICIOS_PREMIUM.get(servicio_id, None)

def stock_total(servicio_id):
    return len(CUENTAS_DISPONIBLES.get(servicio_id, []))

def listar_servicios():
    return SERVICIOS_PREMIUM

def agregar_cuentas(servicio_id, lista_cuentas, admin_id="Admin"):
    """Agrega nuevas cuentas al stock"""
    if servicio_id in CUENTAS_DISPONIBLES:
        CUENTAS_DISPONIBLES[servicio_id].extend(lista_cuentas)
        
        # LOG
        log_info(f"STOCK: Agregadas {len(lista_cuentas)} cuentas a {servicio_id} por {admin_id}")
        return True, f"✅ Agregadas {len(lista_cuentas)} cuentas correctamente."
    return False, "❌ Servicio no encontrado"

def obtener_ventas_db():
    """Obtener historial de MongoDB"""
    return obtener_historial_premium()

# ==============================================
# 💰 PRECIOS Y COMISIONES
# ==============================================
def calcular_precio_y_comision(uid, precio_base):
    """Calcula precio final y ganancia según nivel del usuario"""
    from sellers import es_seller, obtener_datos
    
    if es_seller(uid):
        datos = obtener_datos(uid)
        if datos and "info_nivel" in datos:
            comision = datos['info_nivel']['comision']
            precio_final = precio_base * (1 - comision / 100)
            ganancia = precio_base - precio_final
            return round(precio_final, 2), round(ganancia, 2)
    
    # Si es usuario normal o no hay datos de seller
    return precio_base, precio_base

# ==============================================
# 📊 VER STOCK PARA PANEL ADMIN
# ==============================================
def ver_stock_completo():
    texto = "📦 <b>STOCK DE CUENTAS PREMIUM</b>\n\n"
    for key, cuentas in CUENTAS_DISPONIBLES.items():
        nombre = SERVICIOS_PREMIUM[key]['nombre']
        cantidad = len(cuentas)
        estado = "🟢" if cantidad > 0 else "🔴"
        texto += f"{estado} <b>{nombre}</b>: <code>{cantidad} unidades</code>\n"
    return texto
