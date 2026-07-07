# ==============================================
# 🏅 SISTEMA DE RANGOS Y NIVELES VIP
# ==============================================
# Más compras = Mejores beneficios
# ==============================================

from config import *
from database import *

# 🎖️ DEFINICIÓN DE NIVELES
NIVELES = [
    {
        "nombre": "BRONCE 🪙",
        "minimo": 0,
        "descuento": 0,
        "color": "🟤"
    },
    {
        "nombre": "PLATA ✨",
        "minimo": 100,
        "descuento": 5,
        "color": "⬜"
    },
    {
        "nombre": "ORO 💛",
        "minimo": 300,
        "descuento": 10,
        "color": "🟡"
    },
    {
        "nombre": "DIAMANTE 💎",
        "minimo": 500,
        "descuento": 15,
        "color": "🔷"
    }
]

# ==============================================
# 📈 CALCULAR NIVEL
# ==============================================
def calcular_nivel(total_gastado):
    for nivel in reversed(NIVELES):
        if total_gastado >= nivel['minimo']:
            return nivel
    return NIVELES[0]

# ==============================================
# ✅ VERIFICAR Y ACTUALIZAR
# ==============================================
def verificar_rango(uid, nombre, monto_compra=0):
    """Verifica si el usuario sube de nivel después de comprar"""
    
    usuario = obtener_usuario_db(uid)
    if not usuario:
        return None
    
    # Sumar al total gastado
    total_actual = usuario.get('total_gastado', 0) + monto_compra
    nivel_anterior = usuario.get('nivel', 'BRONCE 🪙')
    nuevo_nivel = calcular_nivel(total_actual)
    
    # Actualizar en DB
    datos = {
        "total_gastado": total_actual,
        "nivel": nuevo_nivel['nombre'],
        "descuento": nuevo_nivel['descuento']
    }
    actualizar_usuario_db(uid, datos)
    
    # ¿Subió de nivel?
    if nivel_anterior != nuevo_nivel['nombre']:
        mensaje = f"""
🎉 <b>¡FELICIDADES {nombre}!</b>

🔺 Has subido de nivel:
{nivel_anterior} ➡️ {nuevo_nivel['nombre']}

🎁 Beneficio desbloqueado:
✅ Descuento del <b>{nuevo_nivel['descuento']}%</b> en todas tus compras

¡Sigue comprando para subir más! 🚀
"""
        return True, mensaje
    
    return False, None

# ==============================================
# 📋 VER MI NIVEL
# ==============================================
def ver_mi_nivel(uid):
    usuario = obtener_usuario_db(uid)
    if not usuario:
        return "❌ Error"
    
    total = usuario.get('total_gastado', 0)
    nivel_actual = usuario.get('nivel', 'BRONCE 🪙')
    descuento = usuario.get('descuento', 0)
    
    # Calcular cuánto falta para el siguiente
    info_nivel = calcular_nivel(total)
    siguiente = None
    for n in NIVELES:
        if n['minimo'] > total:
            siguiente = n
            break
    
    texto = f"""
🏅 <b>MI PERFIL VIP</b>

💎 Nivel actual: <b>{nivel_actual}</b>
💰 Total gastado: <b>{MONEDA} {total:.2f}</b>
📉 Descuento: <b>{descuento}%</b>
"""
    
    if siguiente:
        falta = siguiente['minimo'] - total
        texto += f"""
📈 <b>PROGRESO AL SIGUIENTE NIVEL:</b>
🔹 {siguiente['nombre']}
🔢 Te falta: <b>{MONEDA} {falta:.2f}</b>
"""
    
    return texto
