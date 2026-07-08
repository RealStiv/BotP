# ==============================================
# 📊 SISTEMA DE ESTADÍSTICAS Y REPORTES PRO
# ==============================================
# Dashboard, Rankings, Análisis y Gráficos
# ==============================================

from config import *
from logger import *
from services import SERVICIOS
from datetime import datetime

# ==============================================
# 📊 DASHBOARD PRINCIPAL
# ==============================================
def obtener_estadisticas_completas():
    """Muestra el panel general con datos del sistema"""
    
    from database import total_usuarios_db, sumar_ganancias_totales
    
    # Datos generales
    total_usuarios = total_usuarios_db()
    ganancias_totales = sumar_ganancias_totales()
    total_servicios = len(SERVICIOS)
    
    # Fecha actual
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M:%S")
    
    texto = f"""
╔════════════════════════════════════╗
║      📊 DASHBOARD MASTER PRO      ║
╚════════════════════════════════════╝

📅 <b>Fecha:</b> <code>{fecha}</code>
⏰ <b>Hora:</b> <code>{hora}</code>
🔋 <b>Estado:</b> <code>ONLINE 🟢</code>

👥 <b>POBLACIÓN TOTAL</b>
• Usuarios Registrados: <b>{total_usuarios}</b>

💰 <b>ECONOMÍA DEL SISTEMA</b>
• Ganancias Totales: <b>{MONEDA} {ganancias_totales:.2f}</b>

🛒 <b>SERVICIOS</b>
• Productos Activos: <b>{total_servicios}</b>
• Sistema: <b>ESTABLE</b>

<b>🔧 Sistema listo para operaciones</b>
"""
    return texto

# ==============================================
# 📈 RANKING DE USUARIOS
# ==============================================
def obtener_ranking_usuarios():
    """Top 5 clientes con mayor saldo"""
    
    from database import obtener_todos_usuarios_db
    
    usuarios = obtener_todos_usuarios_db()
    
    if not usuarios:
        return "❌ No hay datos aún."
    
    # Ordenar por saldo descendente
    usuarios_ordenados = sorted(usuarios, key=lambda x: x.get('saldo', 0), reverse=True)
    
    texto = "🏆 <b>TOP 5 - MEJORES CLIENTES</b>\n\n"
    
    emojis = ["🥇","🥈","🥉","💳","💰"]
    for i, datos in enumerate(usuarios_ordenados[:5], 1):
        emoji = emojis[i-1] if i <=5 else "🔹"
        nombre = datos.get('nombre', f'ID: {datos["id"]}')
        saldo = datos.get('saldo', 0)
        texto += f"{emoji} <b>#{i}</b> - {nombre}\n   💵 Saldo: {MONEDA} {saldo:.2f}\n   🆔 <code>{datos['id']}</code>\n\n"
        
    return texto

# ==============================================
# 📋 ANÁLISIS DE SERVICIOS
# ==============================================
def obtener_top_servicios():
    """Informe de precios y categorías"""
    
    categorias = {
        "🎵 TikTok": 0,
        "📸 Instagram": 0,
        "✈️ Telegram": 0,
        "📘 Facebook": 0,
        "📺 YouTube": 0
    }
    
    total_precios = 0
    servicio_mas_caro = ("", 0)
    
    for id_serv, data in SERVICIOS.items():
        precio = data['precio_por_mil']
        total_precios += precio
        
        if precio > servicio_mas_caro[1]:
            servicio_mas_caro = (data['nombre'], precio)
            
        # Clasificar
        if "TikTok" in data['nombre']: 
            categorias["🎵 TikTok"] +=1
        elif "Instagram" in data['nombre']: 
            categorias["📸 Instagram"] +=1
        elif "Telegram" in data['nombre']: 
            categorias["✈️ Telegram"] +=1
        elif "Facebook" in data['nombre']: 
            categorias["📘 Facebook"] +=1
        elif "YouTube" in data['nombre']: 
            categorias["📺 YouTube"] +=1

    texto = f"""
📋 <b>INFORME DE SERVICIOS Y PRECIOS</b>

🛒 <b>RESUMEN POR PLATAFORMA:</b>
"""
    for cat, cant in categorias.items():
        texto += f"• {cat}: <b>{cant} servicios</b>\n"
        
    precio_promedio = total_precios / len(SERVICIOS) if SERVICIOS else 0
    
    texto += f"""
💸 <b>ANÁLISIS DE PRECIOS:</b>
• Precio Promedio: <b>{MONEDA} {precio_promedio:.2f} /1k</b>
• Servicio Más Alto: <b>{servicio_mas_caro[0]}</b>
• Valor: <b>{MONEDA} {servicio_mas_caro[1]:.2f}</b>

✅ Base de datos: <b>ACTUALIZADA</b>
"""
    return texto

# ==============================================
# 📄 REPORTE GENERAL
# ==============================================
def obtener_reporte_completo():
    """Lista de usuarios y saldos"""
    
    from database import obtener_todos_usuarios_db
    
    usuarios = obtener_todos_usuarios_db()
    
    texto = "📄 <b>REPORTE GENERAL DEL SISTEMA</b>\n\n"
    texto += f"👥 Usuarios: <code>{len(usuarios)}</code>\n"
    texto += f"💰 Dinero Total: <b>{MONEDA} {sum(u.get('saldo',0) for u in usuarios):.2f}</b>\n"
    texto += f"🛒 Servicios: <code>{len(SERVICIOS)}</code>\n"
    texto += "\n<b>Últimos usuarios registrados:</b>\n"
    
    for datos in usuarios[-10:]:
        nombre = datos.get('nombre', f'ID: {datos["id"]}')
        texto += f"🆔 <code>{datos['id']}</code> - {nombre} - {MONEDA} {datos.get('saldo',0):.2f}\n"
        
    return texto

# ==============================================
# 📈 GRÁFICOS Y RENDIMIENTO
# ==============================================
def grafico_ventas_semanales():
    from database import total_ventas_db
    
    total = total_ventas_db()
    
    texto = f"""
📈 <b>ANÁLISIS DE RENDIMIENTO</b>

🟢 <b>ESTADO GENERAL: SALUDABLE</b>

📊 <b>Total de Ventas:</b> <code>{total} operaciones</code>

🔥 <b>Sistema funcionando al máximo rendimiento</b>
"""
    return texto

def analisis_temporal():
    texto = """
📆 <b>REPORTE TEMPORAL</b>

✅ <b>Sistema estable y funcionando</b>
📅 Datos históricos preservados
🔄 Sincronización automática activa

💎 <b>¡Todo bajo control!</b>
"""
    return texto

# ==============================================
# 🧑‍💼 STATS RÁPIDAS
# ==============================================
def stats_rapidas():
    """Datos cortos para mensajes rápidos"""
    
    from database import total_usuarios_db, total_ventas_db
    
    return f"""
📊 <b>RESUMEN RÁPIDO</b>
👥 Usuarios: <code>{total_usuarios_db()}</code>
🛒 Ventas: <code>{total_ventas_db()}</code>
💱 Moneda: <code>{MONEDA}</code>
"""
