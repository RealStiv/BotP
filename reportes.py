# ==============================================
# 📊 SISTEMA DE REPORTES ECONÓMICOS
# ==============================================
# Ganancias por día, semana y mes
# ==============================================

from datetime import datetime, timedelta
from config import *
from database import *

# ==============================================
# 📅 REPORTES POR TIEMPO
# ==============================================def reporte_hoy():
    hoy = datetime.now().strftime("%d/%m/%Y")
    movimientos = obtener_movimientos_fecha_db(hoy)
    
    total_ingresos = sum(m['monto'] for m in movimientos if m['tipo'] in ["RECARGA", "COMPRA", "PREMIUM"])
    total_gastos = sum(m['monto'] for m in movimientos if m['tipo'] in ["RETIRO", "BONO"])
    ganancia_neta = total_ingresos - total_gastos
    
    return f"""
📆 <b>REPORTE DEL DÍA DE HOY</b>
📅 {hoy}

💵 Ingresos totales: <b>{MONEDA} {total_ingresos:.2f}</b>
💸 Egresos: <b>{MONEDA} {total_gastos:.2f}</b>
💰 <b>GANANCIA NETA: {MONEDA} {ganancia_neta:.2f}</b>

📊 Operaciones: <code>{len(movimientos)}</code>
"""

def reporte_semana():
    hace_7dias = datetime.now() - timedelta(days=7)
    movimientos = obtener_movimientos_rango_db(hace_7dias, datetime.now())
    
    total = sum(m['monto'] for m in movimientos if m['tipo'] in ["RECARGA", "COMPRA", "PREMIUM"])
    
    return f"""
📅 <b>REPORTE ÚLTIMOS 7 DÍAS</b>

💸 Total facturado: <b>{MONEDA} {total:.2f}</b>
📦 Operaciones: <code>{len(movimientos)}</code>

🚀 ¡Sigue así!
"""

def grafico_ganancias():
    """Gráfico simple con emojis"""
    return """
📈 <b>GRÁFICO DE RENDIMIENTO</b>

███░░░░░░░░░░░ 25%
██████░░░░░░░░ 50%
█████████░░░░░ 75%
██████████████ 100%

🟢 Sistema en crecimiento máximo
"""
