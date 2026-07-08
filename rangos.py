# ==============================================
# 🏅 SISTEMA DE RANGOS Y NIVELES VIP
# ==============================================
# Más compras = Mejores beneficios
# ==============================================

from config import *
from database import *

# ==============================================
# 🎖️ DEFINICIÓN DE NIVELES
# ==============================================
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
# 📈 CALCULAR NIVEL SEGÚN MONTO
# ==============================================
def calcular_nivel(total_gastado):
    """Calcula qué nivel le corresponde"""
    for nivel in reversed(NIVELES):
        if total_gastado >= nivel['minimo']:
            return nivel
    return NIVELES[0]

# ==============================================
# ✅ VERIFICAR Y ACTUALIZAR RANGO
# ==============================================
def verificar_rango(id_usuario, nombre_usuario, monto_compra=0):
    """Verifica si el usuario sube de nivel tras una compra"""
    
    datos_usuario = obtener_usuario_db(id_usuario)
    if not datos_usuario:
        return None, None
    
    # Calcular nuevos totales
    total_actual = datos_usuario.get('total_gastado', 0) + monto_compra
    nivel_anterior = datos_usuario.get('nivel', 'BRONCE 🪙')
    nuevo_nivel = calcular_nivel(total_actual)
    
    # Actualizar en base de datos
    datos_actualizar = {
        "total_gastado": total_actual,
        "nivel": nuevo_nivel['nombre'],
        "descuento": nuevo_nivel['descuento']
    }
    actualizar_usuario_db(id_usuario, datos_actualizar)
    
    # ¿Subió de nivel?
    if nivel_anterior != nuevo_nivel['nombre']:
        mensaje = f"""
🎉 <b>¡FELICIDADES {nombre_usuario}!</b>

🔺 Has subido de nivel:
{nivel_anterior} ➡️ {nuevo_nivel['nombre']}

🎁 Beneficio desbloqueado:
✅ Descuento del <b>{nuevo_nivel['descuento']}%</b> en todas tus compras

¡Sigue comprando para subir más! 🚀
"""
        return True, mensaje
    
    return False, None

# ==============================================
# 📋 VER INFORMACIÓN DE MI PERFIL
# ==============================================
def ver_mi_nivel(id_usuario):
    """Muestra nivel actual y progreso"""
    datos_usuario = obtener_usuario_db(id_usuario)
    if not datos_usuario:
        return "❌ Error al obtener datos"
    
    total = datos_usuario.get('total_gastado', 0)
    nivel_actual = datos_usuario.get('nivel', 'BRONCE 🪙')
    descuento = datos_usuario.get('descuento', 0)
    
    # Calcular siguiente nivel
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
