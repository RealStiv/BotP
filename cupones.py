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
    """Crea un nuevo cupón en la base de datos"""
    
    nuevo_cupon = {
        "codigo": codigo.upper(),
        "monto": float(monto),
        "usos_max": int(usos_max),
        "usados": 0,
        "fecha_creacion": datetime.now().strftime("%d/%m/%Y")
    }
    
    insertar_cupon_db(nuevo_cupon)
    log_info(f"CUPÓN CREADO: {codigo} | MONTO: {monto}")
    return True

# ==============================================
# ✅ CANJEAR CUPÓN
# ==============================================
def canjear_cupon(id_usuario, nombre_usuario, codigo):
    """Procesa el canje y acredita el saldo"""
    
    codigo = codigo.upper().strip()
    
    # Buscar cupón
    cupon = buscar_cupon_db(codigo)
    
    if not cupon:
        return False, "❌ <b>Cupón inválido o expirado</b>"
    
    if cupon['usados'] >= cupon['usos_max']:
        return False, "⚠️ <b>Este cupón ya se agotó</b>"
    
    # Verificar uso previo
    if usuario_uso_cupon_db(id_usuario, codigo):
        return False, "🔒 <b>Ya utilizaste este código</b>"
    
    # Acreditar saldo
    agregar_saldo_db(id_usuario, cupon['monto'])
    
    # Registrar uso
    registrar_uso_cupon_db(id_usuario, codigo, nombre_usuario)
    
    # Actualizar contador
    actualizar_usos_cupon_db(codigo)
    
    # LOG
    log_info(f"CANJEO: {nombre_usuario} usó {codigo} | +{cupon['monto']}")
    
    return True, f"""
🎉 <b>¡CUPÓN CANJEADO CON ÉXITO!</b>

✅ Código: <code>{codigo}</code>
💰 Saldo acreditado: <b>{MONEDA} {cupon['monto']:.2f}</b>

¡Disfruta tu saldo! 🚀
"""

# ==============================================
# 📋 LISTAR PARA ADMINISTRADOR
# ==============================================
def listar_cupones_admin():
    """Muestra estado de todos los cupones"""
    
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
