# ==============================================
# 🧑‍💼 SISTEMA DE GESTIÓN DE SELLERS PRO
# ==============================================
# ✅ Niveles, Comisiones, Permisos y Control Total
# ✅ BASE DE DATOS MONGODB 🍃
# ✅ SISTEMA DE LOGS 📢
# ==============================================

from datetime import datetime
from config import *
from logger import *      # 📝 Sistema de registros
from database import *    # 🍃 Conexión MongoDB

# ==============================================
# 🏅 DEFINICIÓN DE NIVELES Y BENEFICIOS
# ==============================================
NIVELES = {
    "novato": {
        "nombre": "🥉 SELLER NOVATO",
        "comision": 10,       # % de ganancia sobre el precio
        "descuento_max": 5,   # % máximo que puede rebajar al cliente
        "limite_venta": 100,  # Límite de venta por día
        "color": "🟤"
    },
    "avanzado": {
        "nombre": "🥈 SELLER AVANZADO",
        "comision": 18,
        "descuento_max": 12,
        "limite_venta": 500,
        "color": "🪙"
    },
    "pro": {
        "nombre": "🥇 SELLER PROFESIONAL",
        "comision": 25,
        "descuento_max": 20,
        "limite_venta": 2000,
        "color": "🟡"
    },
    "elite": {
        "nombre": "💎 SELLER ELITE",
        "comision": 35,
        "descuento_max": 30,
        "limite_venta": 99999,
        "color": "🔵"
    }
}

# ==============================================
# 🔐 LISTADO DE PERMISOS DEL SISTEMA
# ==============================================
PERMISOS = {
    "ver_precios_reales": "Ver costo real de productos",
    "ver_stock_completo": "Ver todo el stock disponible",
    "aplicar_descuentos": "Puede dar precios especiales",
    "vender_smm": "Acceso a servicios SMM",
    "vender_premium": "Acceso a cuentas Streaming",
    "retirar_saldo": "Puede retirar sus ganancias",
    "ver_reportes": "Ver estadísticas y reportes",
    "crear_clientes": "Registrar clientes propios",
    "soporte_privado": "Acceso a soporte exclusivo"
}

# ==============================================
# ➕ FUNCIÓN PRINCIPAL - CREAR NUEVO SELLER
# ==============================================
def crear_seller(id_usuario, nombre_usuario, nivel="novato", id_admin="Admin"):
    """Crea un nuevo vendedor en la base de datos"""
    id_usuario = str(id_usuario)
    
    # Validar nivel
    if nivel not in NIVELES:
        nivel = "novato"
    
    datos_nuevo_seller = {
        "uid": id_usuario,
        "nombre": nombre_usuario,
        "nivel": nivel,
        "fecha_registro": datetime.now().strftime("%d/%m/%Y"),
        "saldo_ganancias": 0.00,
        "total_vendido": 0.00,
        "ventas_realizadas": 0,
        "estado": "activo",
        "permisos": list(PERMISOS.keys()),
        "metodo_pago": "",
        "ultima_venta": "Nunca"
    }
    
    # Guardar en DB
    if sellers is not None:
        sellers.insert_one(datos_nuevo_seller)
    
    # Registro en sistema
    log_info(f"✅ SELLER CREADO: {nombre_usuario} | Nivel: {nivel} | Por: {id_admin}")
    
    return True

# ==============================================
# 🔍 VERIFICACIONES Y CONSULTAS
# ==============================================
def es_seller(id_usuario):
    """Verifica si el usuario es un seller activo"""
    id_usuario = str(id_usuario)
    if sellers is None:
        return False
    return sellers.find_one({"uid": id_usuario, "estado": "activo"}) is not None

def obtener_datos(id_usuario):
    """Obtiene datos completos incluyendo información del nivel"""
    id_usuario = str(id_usuario)
    if sellers is None:
        return None
    
    datos = sellers.find_one({"uid": id_usuario})
    if datos:
        # Agregar datos del nivel automáticamente
        datos["info_nivel"] = NIVELES.get(datos["nivel"], NIVELES["novato"])
        return datos
    return None

# ==============================================
# 💰 CÁLCULOS ECONÓMICOS
# ==============================================
def calcular_precio_y_comision(id_usuario, precio_base):
    """Calcula precio final para cliente y ganancia para el seller"""
    datos = obtener_datos(id_usuario)
    if not datos:
        return round(precio_base, 2), 0
    
    porcentaje_ganancia = datos["info_nivel"]["comision"]
    ganancia = (precio_base * porcentaje_ganancia) / 100
    precio_final = precio_base - ganancia
    
    return round(precio_final, 2), round(ganancia, 2)

def registrar_venta_reseller(id_usuario, producto, precio_publico, ganancia):
    """Actualiza saldo y contadores del vendedor tras una venta"""
    id_usuario = str(id_usuario)
    
    if sellers is None:
        return False
    
    # Actualizar contadores y saldo
    sellers.update_one(
        {"uid": id_usuario},
        {
            "$inc": {
                "saldo_ganancias": ganancia,
                "total_vendido": precio_publico,
                "ventas_realizadas": 1
            },
            "$set": {"ultima_venta": datetime.now().strftime("%d/%m/%Y %H:%M")}
        }
    )
    
    # Guardar historial detallado
    registro_venta = {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "seller_id": id_usuario,
        "producto": producto,
        "precio_publico": precio_publico,
        "ganancia": ganancia
    }
    
    if "ventas_sellers" in db.list_collection_names():
        db["ventas_sellers"].insert_one(registro_venta)
    
    return True

# ==============================================
# 📢 NOTIFICACIONES Y LOGS
# ==============================================
def registrar_venta_seller(id_seller, nombre_cliente, producto, monto, ganancia):
    """Envía aviso al canal de ventas y registra en logs"""
    datos_seller = obtener_datos(id_seller)
    nombre_vendedor = datos_seller['nombre'] if datos_seller else "Desconocido"
    
    mensaje = f"""
🧑‍💼 <b>¡VENTA POR RESELLER!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👤 Vendedor: <b>{nombre_vendedor}</b>
🆔 ID Vendedor: <code>{id_seller}</code>
👥 Cliente: <b>{nombre_cliente}</b>
📦 Producto: <b>{producto}</b>
💸 Monto: <b>{MONEDA} {monto}</b>
💰 Ganancia: <b>{MONEDA} {ganancia}</b>
📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
    enviar_a_canal(mensaje)
    log_info(f"💸 VENTA RESELLER | Seller: {id_seller} | Ganancia: {MONEDA} {ganancia}")

# ==============================================
# ⚙️ ADMINISTRACIÓN DE CUENTAS
# ==============================================
def cambiar_nivel(id_usuario, nuevo_nivel, id_admin="Admin"):
    id_usuario = str(id_usuario)
    if nuevo_nivel in NIVELES and sellers is not None:
        sellers.update_one({"uid": id_usuario}, {"$set": {"nivel": nuevo_nivel}})
        log_info(f"🔄 NIVEL CAMBIADO: Usuario {id_usuario} -> {nuevo_nivel} | Por: {id_admin}")
        return True
    return False

def suspender_seller(id_usuario, id_admin="Admin"):
    id_usuario = str(id_usuario)
    if sellers is not None:
        sellers.update_one({"uid": id_usuario}, {"$set": {"estado": "suspendido"}})
        log_info(f"⛔ SUSPENDIDO: Seller {id_usuario} | Por: {id_admin}")
        return True
    return False

def activar_seller(id_usuario, id_admin="Admin"):
    id_usuario = str(id_usuario)
    if sellers is not None:
        sellers.update_one({"uid": id_usuario}, {"$set": {"estado": "activo"}})
        log_info(f"✅ ACTIVADO: Seller {id_usuario} | Por: {id_admin}")
        return True
    return False

# ==============================================
# 📊 ESTADÍSTICAS Y RANKING
# ==============================================
def obtener_ranking():
    """Retorna top 10 mejores vendedores"""
    if sellers is None:
        return []
    return list(sellers.find().sort("total_vendido", -1).limit(10))

def stats_sellers():
    """Resumen general de estadísticas"""
    if sellers is None:
        return "📊 Sin datos disponibles"
    
    total = sellers.count_documents({})
    activos = sellers.count_documents({"estado": "activo"})
    return f"📊 Total: {total} | Activos: {activos}"
