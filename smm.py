# ==============================================
# 📈 SMM PANEL - INTEGRACIÓN COMPLETA
# ==============================================

import requests
from datetime import datetime
from config import URL_PANEL, API_KEY, MONEDA
from database import *
from logger import *

# ==============================================
# 🔌 CONECTAR A LA API
# ==============================================
def obtener_servicios_smm():
    """Obtiene lista de servicios disponibles"""
    try:
        datos = {
            "key": API_KEY,
            "action": "services"
        }
        respuesta = requests.post(URL_PANEL, data=datos, timeout=15)
        return respuesta.json() if respuesta.status_code == 200 else []
    except Exception as e:
        log_error(f"API SMM: Error al obtener servicios - {str(e)}")
        return []

def crear_pedido_smm(usuario_id, nombre_usuario, servicio_id, enlace, cantidad):
    """Crea un pedido en el panel SMM automáticamente"""
    try:
        # Obtener datos del servicio
        servicios = obtener_servicios_smm()
        servicio = next((s for s in servicios if s["service"] == str(servicio_id)), None)
        
        if not servicio:
            return False, "❌ Servicio no encontrado en el panel"
        
        # Calcular precio total
        precio_por_mil = float(servicio["price"])
        precio_total = precio_por_mil * (cantidad / 1000)
        precio_total = round(precio_total, 2)
        
        # Verificar saldo
        saldo_actual = obtener_saldo(usuario_id)
        if saldo_actual < precio_total:
            return False, f"""
❌ <b>SALDO INSUFICIENTE</b>

💰 Precio: {MONEDA} {precio_total:.2f}
💵 Tu saldo: {MONEDA} {saldo_actual:.2f}

🔹 Necesitas recargar para continuar.
"""
        
        # Enviar pedido a la API
        datos_pedido = {
            "key": API_KEY,
            "action": "add",
            "service": servicio_id,
            "link": enlace,
            "quantity": cantidad
        }
        
        respuesta = requests.post(URL_PANEL, data=datos_pedido, timeout=15)
        resultado = respuesta.json()
        
        if "order" in resultado:
            # Descontar saldo
            descontar_saldo(usuario_id, precio_total)
            
            # Registrar en base de datos
            insertar_movimiento_db({
                "uid": str(usuario_id),
                "nombre": nombre_usuario,
                "producto": servicio["name"],
                "monto": precio_total,
                "estado": "COMPLETADO",
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tipo": "COMPRA"
            })
            
            # LOG
            log_info(f"SMM: Pedido #{resultado['order']} creado por {nombre_usuario}")
            
            # Mensaje de éxito
            mensaje = f"""
╔════════════════════════════════════════╗
║       ✅  P E D I D O   C R E A D O      ║
╚════════════════════════════════════════╝

📦 <b>Servicio:</b> {servicio['name']}
🔗 <b>Enlace:</b> <code>{enlace}</code>
🔢 <b>Cantidad:</b> <code>{cantidad:,}</code>
💰 <b>Precio:</b> {MONEDA} {precio_total:.2f}
📉 <b>Saldo restante:</b> {MONEDA} {obtener_saldo(usuario_id):.2f}

🔢 <b>ID de Orden:</b> <code>#{resultado['order']}</code>

⏳ <b>Tiempo de entrega:</b> {servicio.get('delivery', 'Automático')}

✅ <b>¡Tu pedido está en proceso!</b>
"""
            return True, mensaje
            
        else:
            error_msg = resultado.get('error', 'Error desconocido')
            return False, f"❌ <b>Error en la API:</b>\n{error_msg}"
            
    except Exception as e:
        log_error(f"SMM: Error al crear pedido - {str(e)}")
        return False, "❌ Ocurrió un error al conectar con el panel"

def verificar_estado_pedido(order_id):
    """Consulta el estado de un pedido"""
    try:
        datos = {
            "key": API_KEY,
            "action": "status",
            "order": order_id
        }
        respuesta = requests.post(URL_PANEL, data=datos, timeout=10)
        return respuesta.json()
    except:
        return None

# ==============================================
# 📋 MENU VISUAL PARA USUARIOS
# ==============================================
def menu_smm():
    """Muestra los servicios disponibles"""
    servicios = obtener_servicios_smm()
    
    if not servicios:
        return "❌ No se pudieron cargar los servicios", None
    
    texto = """
📈 <b>PANEL SMM - SERVICIOS</b>

🔹 <b>Selecciona una categoría:</b>
"""
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Agrupar por categorías simples
    categorias = {}
    for s in servicios:
        nombre = s['name']
        if "Instagram" in nombre:
            cat = "📸 INSTAGRAM"
        elif "TikTok" in nombre:
            cat = "🎵 TIKTOK"
        elif "Facebook" in nombre:
            cat = "📘 FACEBOOK"
        elif "YouTube" in nombre:
            cat = "📺 YOUTUBE"
        elif "Telegram" in nombre:
            cat = "✈️ TELEGRAM"
        else:
            cat = "🌐 OTROS"
            
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(s)
    
    for cat, lista in categorias.items():
        btn = InlineKeyboardButton(f"{cat} ({len(lista)})", callback_data=f"ver_cat_{cat}")
        markup.add(btn)
    
    btn_back = InlineKeyboardButton("🔙 VOLVER", callback_data="volver_tienda")
    markup.add(btn_back)
    
    return texto, markup
