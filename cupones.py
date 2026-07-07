# ==============================================
# 🎫 SISTEMA DE CUPONES Y DESCUENTOS
# ==============================================
# Códigos promocionales y bonificaciones
# ==============================================

from datetime import datetime
from config import *
from database import *
from logger import *

# ==============================================
# 🎟️ CREAR NUEVO CUPÓN
# ==============================================
def crear_cupon(codigo, monto, usos_max=1):
    """Crea un cupón nuevo"""
    cupon = {
        "codigo": codigo.upper(),
        "monto": float(monto),
        "usos_max": int(usos_max),
        "usados": 0,
        "fecha_creacion": datetime.now().strftime("%d/%m/%Y")
    }
    
    insertar_cupon_db(cupon)
    log_info(f"CUPÓN CREADO: {codigo} | MONTO: {monto}")
    return True

# ==============================================
# ✅ CANJEAR CUPÓN
# ==============================================
def canjear_cupon(uid, nombre, codigo):
    """Procesa el canje de un cupón"""
    codigo = codigo.upper().strip()
    
    # Buscar cupón
    cupon = buscar_cupon_db(codigo)
    
    if not cupon:
        return False, "❌ <b>Cupón inválido o expirado</b>"
    
    if cupon['usados'] >= cupon['usos_max']:
        return False, "⚠️ <b>Este cupón ya se agotó</b>"
    
    # Verificar si ya lo usó este usuario
    if usuario_uso_cupon_db(uid, codigo):
        return False, "🔒 <b>Ya utilizaste este código</b>"
    
    # Acreditar saldo
    agregar_saldo_db(uid, cupon['monto'])
    
    # Registrar uso
    registrar_uso_cupon_db(uid, codigo, nombre)
    
    # Actualizar contador
    actualizar_usos_cupon_db(codigo)
    
    # LOG
    log_info(f"CANJEO: {nombre} usó {codigo} | +{cupon['monto']}")
    
    return True, f"""
🎉 <b>¡CUPÓN CANJEADO CON ÉXITO!</b>

✅ Código: <code>{codigo}</code>
💰 Saldo acreditado: <b>{MONEDA} {cupon['monto']:.2f}</b>

¡Disfruta tu saldo! 🚀
"""

# ==============================================
# 📋 LISTAR CUPONES ACTIVOS (ADMIN)
# ==============================================
def listar_cupones_admin():
    cupones = obtener_todos_cupones_db()
    
    if not cupones:
        return "❌ No hay cupones creados aún"
    
    texto = "🎫 <b>LISTA DE CUPONES ACTIVOS</b>\n\n"
    
    for c in cupones:
        estado = "🟢" if c['usados'] < c['usos_max'] else "🔴"
        texto += f"{estado} <b>{c['codigo']}</b>\n"
        texto += f"💵 Valor: {MONEDA} {c['monto']:.2f}\n"
        texto += f"🔢 Usos: {c['usados']}/{c['usos_max']}\n\n"
    
    return texto
