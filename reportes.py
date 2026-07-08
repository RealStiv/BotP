# ==============================================
# 📊 SISTEMA DE REPORTES ECONÓMICOS
# ==============================================
# Ganancias por día, semana y mes
# ==============================================

from datetime import datetime, timedelta
from config import *
from database import *

# ==============================================
# 📅 REPORTES POR PERIODO
# ==============================================
def reporte_hoy():
    """Reporte detallado del día actual"""
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    movimientos = obtener_movimientos_fecha_db(fecha_hoy)
    
    # Cálculos económicos
    total_ingresos = sum(
        m['monto'] for m in movimientos 
        if m['tipo'] in ["RECARGA", "COMPRA", "PREMIUM"]
    )
    total_gastos = sum(
        m['monto'] for m in movimientos 
        if m['tipo'] in ["RETIRO", "BONO"]
    )
    ganancia_neta = total_ingresos - total_gastos
    
    return f"""
📆 <b>REPORTE DEL DÍA DE HOY</b>
📅 {fecha_hoy}

💵 Ingresos totales: <b>{MONEDA} {total_ingresos:.2f}</b>
💸 Egresos: <b>{MONEDA} {total_gastos:.2f}</b>
💰 <b>GANANCIA NETA: {MONEDA} {ganancia_neta:.2f}</b>

📊 Operaciones: <code>{len(movimientos)}</code>
"""

def reporte_semana():
    """Reporte de los últimos 7 días"""
    fecha_inicio = datetime.now() - timedelta(days=7)
    fecha_fin = datetime.now()
    
    movimientos = obtener_movimientos_rango_db(fecha_inicio, fecha_fin)
    
    total_facturado = sum(
        m['monto'] for m in movimientos 
        if m['tipo'] in ["RECARGA", "COMPRA", "PREMIUM"]
    )
    
    return f"""
📅 <b>REPORTE ÚLTIMOS 7 DÍAS</b>

💸 Total facturado: <b>{MONEDA} {total_facturado:.2f}</b>
📦 Operaciones: <code>{len(movimientos)}</code>

🚀 ¡Sigue así!
"""

def grafico_ganancias():
    """Visualización simple del rendimiento"""
    return """
📈 <b>GRÁFICO DE RENDIMIENTO</b>

███░░░░░░░░░░░ 25%
██████░░░░░░░░ 50%
█████████░░░░░ 75%
██████████████ 100%

🟢 Sistema en crecimiento máximo
"""
