# ==============================================
# 📈 SMM PANEL - INTEGRACIÓN COMPLETA
# ==============================================

import requests
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
        respuesta = requests.post(URL_PANEL, data=datos)
        return respuesta.json() if respuesta.status_code == 200 else []
    except Exception as e:
        log_error(f"API SMM: Error al obtener servicios - {str(e)}")
        return []

def crear_pedido_smm(usuario_id, nombre_usuario, servicio_id, enlace, cantidad):
    """Crea un pedido en el panel SMM"""
    try:
        # Obtener precio del servicio
        servicios = obtener_servicios_smm()
        servicio = next((s for s in servicios if s["service"] == str(servicio_id)), None)
        
        if not servicio:
            return False, "❌ Servicio no encontrado"
        
        precio_total = float(servicio["price"]) * cantidad
        
        # Verificar saldo
        saldo_actual = obtener_saldo(usuario_id)
        if saldo_actual < precio_total:
            return False, f"❌ Saldo insuficiente\n\n💰 Precio: {MONEDA} {precio_total:.2f}\n💵 Tu saldo: {MONEDA} {saldo_actual:.2f}"
        
        # Crear pedido en API
        datos_pedido = {
            "key": API_KEY,
            "action": "add",
            "service": servicio_id,
            "link": enlace,
            "quantity": cantidad
        }
        
        respuesta = requests.post(URL_PANEL, data=datos_pedido)
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
            
            log_info(f"SMM: Pedido #{resultado['order']} creado por {nombre_usuario}")
            
            mensaje = f"""
✅ <b>PEDIDO CREADO EXITOSAMENTE</b>

📦 Servicio: <b>{servicio['name']}</b>
🔗 Enlace: <code>{enlace}</code>
🔢 Cantidad: <b>{cantidad:,}</b>
💰 Precio: <b>{MONEDA} {precio_total:.2f}</b>
📉 Saldo restante: <b>{MONEDA} {obtener_saldo(usuario_id):.2f}</b>

🔢 ID de Orden: <code>#{resultado['order']}</code>

⏳ Tiempo de entrega: {servicio.get('delivery', 'Inmediato')}
"""
            return True, mensaje
        else:
            return False, f"❌ Error: {resultado.get('error', 'Desconocido')}"
            
    except Exception as e:
        log_error(f"SMM: Error al crear pedido - {str(e)}")
        return False, "❌ Ocurrió un error al procesar tu pedido"

def verificar_estado_pedido(order_id):
    """Verifica el estado de un pedido"""
    try:
        datos = {
            "key": API_KEY,
            "action": "status",
            "order": order_id
        }
        respuesta = requests.post(URL_PANEL, data=datos)
        return respuesta.json()
    except:
        return None
