# ==============================================
# 📊 SISTEMA DE RANKING Y TOPs
# ==============================================
# Los mejores clientes del mes y semana
# ==============================================

from config import *
from database import *

# ==============================================
# 🏆 TOP 10 GENERAL
# ==============================================
def top_mejores_clientes():
    """Ranking por total gastado"""
    usuarios = obtener_todos_usuarios_db()
    
    # Ordenar por total gastado
    usuarios_ordenados = sorted(usuarios, key=lambda x: x.get('total_gastado', 0), reverse=True)
    
    texto = "🏆 <b>TOP 10 - MEJORES CLIENTES</b>\n\n"
    
    medallas = ["🥇", "🥈", "🥉", "💠", "💠", "💠", "💠", "💠", "💠", "💠"]
    
    for i, usuario in enumerate(usuarios_ordenados[:10]):
        nombre = usuario.get('nombre', 'Usuario')
        total = usuario.get('total_gastado', 0)
        nivel = usuario.get('nivel', 'BRONCE')
        
        texto += f"{medallas[i]} <b>{nombre}</b>\n"
        texto += f"   💵 {MONEDA} {total:.2f} | {nivel}\n\n"
    
    texto += "📅 Actualizado hoy"
    return texto

# ==============================================
# 👥 TOP REFERIDORES
# ==============================================
def top_referidores():
    """Ranking por cantidad de invitados"""
    usuarios = obtener_todos_usuarios_db()
    ordenados = sorted(usuarios, key=lambda x: x.get('referidos', 0), reverse=True)
    
    texto = "👥 <b>TOP 5 - MAYORES INVITADORES</b>\n\n"
    
    for i, usuario in enumerate(ordenados[:5]):
        nombre = usuario.get('nombre', 'Usuario')
        cantidad = usuario.get('referidos', 0)
        
        texto += f"#{i+1} <b>{nombre}</b>\n"
        texto += f"   👤 {cantidad} amigos invitados\n\n"
    
    return texto
