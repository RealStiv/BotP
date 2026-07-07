# ==============================================
# 🧑‍💼 SISTEMA DE GESTIÓN DE SELLERS PRO
# ==============================================
# ✅ Niveles, Comisiones, Permisos y Control Total
# ✅ BASE DE DATOS MONGODB 🍃
# ✅ SISTEMA DE LOGS 📢
# ==============================================

from datetime import datetime
from config import *
from logger import *      # 📝 SISTEMA DE LOGS
from database import *    # 🍃 MONGODB

# ==============================================
# 🏅 NIVELES Y BENEFICIOS
# ==============================================
NIVELES = {
    "novato": {
        "nombre": "🥉 SELLER NOVATO",
        "comision": 10,       # % de ganancia
        "descuento_max": 5,   # % que puede bajar al cliente
        "limite_venta": 100,  # Límite máximo de venta por día
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
# 🔐 PERMISOS DISPONIBLES
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
# ➕ FUNCIÓN PRINCIPAL CREAR SELLER
# ==============================================
def crear_seller(uid, nombre, nivel="novato", admin_id="Admin"):
    """Crea un nuevo vendedor en el sistema"""
    uid = str(uid)
    
    if nivel not in NIVELES:
        nivel = "novato"
    
    datos = {
        "uid": uid,
        "nombre": nombre,
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
    
    # Guardar en MongoDB
    if sellers is not None:
        sellers.insert_one(datos)
    
    # 📝 LOG
    log_info(f"SELLER: Nuevo vendedor creado | {nombre} | Nivel: {nivel} | por Admin {admin_id}")
    
    return True

# ==============================================
# 🔍 VERIFICACIONES
# ==============================================
def es_seller(uid):
    """Verifica si el usuario es vendedor"""
    uid = str(uid)
    if sellers is None:
        return False
    return sellers.find_one({"uid": uid, "estado": "activo"}) is not None

def obtener_datos(uid):
    """Obtiene datos completos con información de nivel"""
    uid = str(uid)
    if sellers is None:
        return None
    
    datos = sellers.find_one({"uid": uid})
    if datos:
        datos["info_nivel"] = NIVELES.get(datos["nivel"], NIVELES["novato"])
        return datos
    return None

# ==============================================
# 💰 CALCULOS ECONÓMICOS
# ==============================================
def calcular_precio_y_comision(uid, precio_base):
    """Calcula precio para cliente y ganancia del seller"""
    datos = obtener_datos(uid)
    if not datos:
        return precio_base, 0
    
    porcentaje = datos["info_nivel"]["comision"]
    ganancia = (precio_base * porcentaje) / 100
    precio_final = precio_base - ganancia
    
    return round(precio_final, 2), round(ganancia, 2)

def registrar_venta_reseller(uid, producto, precio_publico, ganancia):
    """Registra una venta y actualiza saldo en MongoDB"""
    uid = str(uid)
    
    if sellers is None:
        return False
    
    # Actualizar saldo y contadores
    sellers.update_one(
        {"uid": uid},
        {
            "$inc": {
                "saldo_ganancias": ganancia,
                "total_vendido": precio_publico,
                "ventas_realizadas": 1
            },
            "$set": {"ultima_venta": datetime.now().strftime("%d/%m/%Y %H:%M")}
        }
    )
    
    # Historial
    venta = {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "seller_id": uid,
        "producto": producto,
        "precio_publico": precio_publico,
        "ganancia": ganancia
    }
    
    if "ventas_sellers" in db.list_collection_names():
        db["ventas_sellers"].insert_one(venta)
    
    return True

# ==============================================
# 📝 LOGS DE ACCIONES
# ==============================================
def registrar_venta_seller(uid, nombre_usuario, producto, monto, ganancia):
    """Log para el canal principal"""
    datos_seller = obtener_datos(uid)
    nombre_vendedor = datos_seller['nombre'] if datos_seller else "Desconocido"
    
    txt = f"""
🧑‍💼 <b>¡VENTA POR RESELLER!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👤 Vendedor: <b>{nombre_vendedor}</b>
🆔 ID Vendedor: <code>{uid}</code>
👥 Cliente: <b>{nombre_usuario}</b>
📦 Producto: <b>{producto}</b>
💸 Monto: <b>{MONEDA} {monto}</b>
💰 Ganancia: <b>{MONEDA} {ganancia}</b>
📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
    enviar_a_canal(txt)
    log_info(f"VENTA RESELLER | Vendedor: {uid} | Ganancia: {MONEDA} {ganancia}")

# ==============================================
# ⚙️ CONTROL DE NIVELES Y PERMISOS
# ==============================================
def cambiar_nivel(uid, nuevo_nivel, admin_id="Admin"):
    uid = str(uid)
    if nuevo_nivel in NIVELES and sellers is not None:
        sellers.update_one({"uid": uid}, {"$set": {"nivel": nuevo_nivel}})
        
        # LOG
        log_info(f"SELLER: Nivel cambiado | {uid} -> {nuevo_nivel} por {admin_id}")
        return True
    return False

def suspender_seller(uid, admin_id="Admin"):
    uid = str(uid)
    if sellers is not None:
        sellers.update_one({"uid": uid}, {"$set": {"estado": "suspendido"}})
        
        # LOG
        log_info(f"SELLER: SUSPENDIDO | {uid} por {admin_id}")
        return True
    return False

def activar_seller(uid, admin_id="Admin"):
    uid = str(uid)
    if sellers is not None:
        sellers.update_one({"uid": uid}, {"$set": {"estado": "activo"}})
        
        # LOG
        log_info(f"SELLER: ACTIVADO | {uid} por {admin_id}")
        return True
    return False

# ==============================================
# 📊 ESTADÍSTICAS
# ==============================================
def obtener_ranking():
    """Retorna top sellers"""
    if sellers is None:
        return []
    return list(sellers.find().sort("total_vendido", -1).limit(10))

def stats_sellers():
    """Estadísticas generales"""
    if sellers is None:
        return "📊 Sin datos"
    
    total = sellers.count_documents({})
    activos = sellers.count_documents({"estado": "activo"})
    return f"📊 Total: {total} | Activos: {activos}"
