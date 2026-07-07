# ==============================================
# 👥 SISTEMA DE REFERIDOS
# ==============================================
# Invita amigos y gana saldo
# ==============================================

from config import *
from database import *
from logger import *

# CONFIGURACIÓN
BONO_INVITADOR = 5.00  # Lo que gana quien invita
BONO_INVITADO = 2.00   # Lo que gana el nuevo

# ==============================================
# 🔗 GENERAR ENLACE
# ==============================================
def obtener_enlace_referido(uid):
    return f"https://t.me/{BOT_USERNAME}?start={uid}"

# ==============================================
# ✅ VERIFICAR Y REGISTRAR
# ==============================================
def registrar_referido(nuevo_uid, nuevo_nombre, referidor_id):
    """Registra que el usuario nuevo vino de otro"""
    
    # Evitar que se refericien a sí mismos
    if str(nuevo_uid) == str(referidor_id):
        return False
    
    # Verificar que no esté ya registrado
    usuario = obtener_usuario_db(nuevo_uid)
    if usuario and usuario.get('referido_por'):
        return False
    
    # Guardar quién lo refirió
    actualizar_usuario_db(nuevo_uid, {
        "referido_por": str(referidor_id),
        "referido_nombre": nuevo_nombre
    })
    
    # Dar bonificación
    agregar_saldo_db(referidor_id, BONO_INVITADOR)
    agregar_saldo_db(nuevo_uid, BONO_INVITADO)
    
    # LOG
    log_info(f"REFERIDO: {nuevo_nombre} fue invitado por {referidor_id}")
    
    # Notificar al referidor
    return True
