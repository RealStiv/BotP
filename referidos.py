# ==============================================
# 👥 SISTEMA DE REFERIDOS
# ==============================================
# Invita amigos y gana saldo
# ==============================================

from config import *
from database import *
from logger import *

# ==============================================
# ⚙️ CONFIGURACIÓN DE BONOS
# ==============================================
BONO_INVITADOR = 5.00   # Ganancia para quien invita
BONO_INVITADO = 2.00    # Ganancia para el nuevo usuario

# ==============================================
# 🔗 GENERAR ENLACE DE INVITACIÓN
# ==============================================
def obtener_enlace_referido(id_usuario):
    """Genera el enlace personalizado del usuario"""
    return f"https://t.me/{BOT_USERNAME}?start={id_usuario}"

# ==============================================
# ✅ VERIFICAR Y REGISTRAR REFERIDO
# ==============================================
def registrar_referido(id_nuevo_usuario, nombre_nuevo, id_referidor):
    """
    Registra la relación y entrega bonos si es válido.
    Evita auto-referidos y duplicados.
    """
    
    id_nuevo_usuario = str(id_nuevo_usuario)
    id_referidor = str(id_referidor)
    
    # 🚫 Evitar que se refericien a sí mismos
    if id_nuevo_usuario == id_referidor:
        return False
    
    # 📋 Verificar que no tenga referidor ya
    usuario_existente = obtener_usuario_db(id_nuevo_usuario)
    if usuario_existente and usuario_existente.get('referido_por'):
        return False
    
    # 💾 Guardar referencia en la base de datos
    actualizar_usuario_db(id_nuevo_usuario, {
        "referido_por": id_referidor,
        "referido_nombre": nombre_nuevo
    })
    
    # 💰 Entregar bonificaciones
    agregar_saldo_db(id_referidor, BONO_INVITADOR)
    agregar_saldo_db(id_nuevo_usuario, BONO_INVITADO)
    
    # 📝 Registro en sistema
    log_info(f"👥 REFERIDO: {nombre_nuevo} fue invitado por {id_referidor} | +{BONO_INVITADOR}")
    
    return True
