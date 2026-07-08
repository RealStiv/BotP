# ==============================================
# 🛒 CATÁLOGO DE SERVICIOS SMM PRO
# ==============================================
# Precios en USD | API IDs | Ganancias | Compatible Sellers
# ==============================================

from config import *
from logger import *
from sellers import obtener_datos, es_seller

# ==============================================
# 🗄️ BASE DE DATOS DE SERVICIOS
# ==============================================
SERVICIOS = {

    # ==============================================
    # 🎵 TIKTOK - SEGUIDORES
    # ==============================================
    "tt_followers_hq": {
        "nombre": "👥 Seguidores TikTok [HQ] 💎",
        "api_id": 15395,
        "precio_por_mil": 8.50,
        "costo_real": 5.25,
        "ganancia_base": 3.25,
        "descripcion": "✅ Max 50K | Low Drop | No Refill | ⚡ 20K/Día",
        "tiempo": "Instantáneo"
    },
    "tt_followers_hq_30d": {
        "nombre": "👥 Seguidores TikTok [HQ] ♻️",
        "api_id": 16316,
        "precio_por_mil": 10.00,
        "costo_real": 6.00,
        "ganancia_base": 4.00,
        "descripcion": "✅ Max 50K | Garantía 30 Días | ⚡ 20K/Día",
        "tiempo": "Instantáneo"
    },
    "tt_followers_real": {
        "nombre": "👥 Seguidores Reales 100% 🚀",
        "api_id": 17776,
        "precio_por_mil": 5.50,
        "costo_real": 3.00,
        "ganancia_base": 2.50,
        "descripcion": "✅ Usuarios Reales | Max 50K | ⚡ 100K/Día",
        "tiempo": "Instantáneo"
    },
    "tt_followers_real_30d": {
        "nombre": "👥 Seguidores Reales ♻️ 30D",
        "api_id": 17777,
        "precio_por_mil": 6.50,
        "costo_real": 3.45,
        "ganancia_base": 3.05,
        "descripcion": "✅ 100% Reales | Garantía 30 Días | ⚡ Rápido",
        "tiempo": "Instantáneo"
    },
    "tt_followers_1m": {
        "nombre": "👥 Seguidores Max 1M 🚀",
        "api_id": 13083,
        "precio_por_mil": 2.50,
        "costo_real": 0.99,
        "ganancia_base": 1.51,
        "descripcion": "✅ Real People | 250K/Día | Cancel Enable",
        "tiempo": "Inicio Rápido"
    },
    "tt_followers_hq_100k": {
        "nombre": "👥 Seguidores HQ [Max 100K] 🌌",
        "api_id": 17804,
        "precio_por_mil": 5.00,
        "costo_real": 2.95,
        "ganancia_base": 2.05,
        "descripcion": "✅ Non Drop | Garantía 30D | ⚡ 50K/Día",
        "tiempo": "Instantáneo"
    },
    "tt_followers_10m": {
        "nombre": "👥 Seguidores Max 10M ⚡",
        "api_id": 10259,
        "precio_por_mil": 3.00,
        "costo_real": 1.45,
        "ganancia_base": 1.55,
        "descripcion": "✅ Con Foto | 100K/Día | Alta Calidad",
        "tiempo": "Inicio Rápido"
    },
    "tt_followers_lq": {
        "nombre": "👥 Seguidores Económicos 💸",
        "api_id": 16320,
        "precio_por_mil": 2.80,
        "costo_real": 1.75,
        "ganancia_base": 1.05,
        "descripcion": "✅ Precio Bajo | Rápidos | 100K/Día",
        "tiempo": "Instantáneo"
    },
    "tt_followers_old": {
        "nombre": "👥 Seguidores Cuentas Antiguas 📜",
        "api_id": 17572,
        "precio_por_mil": 3.50,
        "costo_real": 1.85,
        "ganancia_base": 1.65,
        "descripcion": "✅ Old Accounts | Max 1M | 100K/Día",
        "tiempo": "Instantáneo"
    },

    # ==============================================
    # ❤️ TIKTOK - LIKES
    # ==============================================
    "tt_likes_nodrop": {
        "nombre": "❤️ Likes [No Drop] 30D 🚀",
        "api_id": 18008,
        "precio_por_mil": 0.60,
        "costo_real": 0.19,
        "ganancia_base": 0.41,
        "descripcion": "✅ Max 500K | No Caen | 200 por Hora",
        "tiempo": "Rápido"
    },
    "tt_likes_30d": {
        "nombre": "❤️ Likes [Garantía 30D] ♻️",
        "api_id": 18009,
        "precio_por_mil": 0.70,
        "costo_real": 0.23,
        "ganancia_base": 0.47,
        "descripcion": "✅ Non Drop | Garantía 30 Días | 200/H",
        "tiempo": "Rápido"
    },
    "tt_likes_instant": {
        "nombre": "❤️ Likes [Instantáneos] ⚡",
        "api_id": 18010,
        "precio_por_mil": 0.70,
        "costo_real": 0.23,
        "ganancia_base": 0.47,
        "descripcion": "✅ 1K por Hora | No Refill | Instant",
        "tiempo": "Inmediato"
    },
    "tt_likes_premium": {
        "nombre": "❤️ Likes Premium ♻️ 30D",
        "api_id": 18011,
        "precio_por_mil": 0.85,
        "costo_real": 0.28,
        "ganancia_base": 0.57,
        "descripcion": "✅ Garantía 30D | Instantáneos | 1K/H",
        "tiempo": "Muy Rápido"
    },

    # ==============================================
    # 📸 INSTAGRAM - SERVICIOS
    # ==============================================
    "ig_likes_world": {
        "nombre": "❤️ Likes Instagram Mundo 🌍",
        "api_id": 17858,
        "precio_por_mil": 3.50,
        "costo_real": 1.65,
        "ganancia_base": 1.85,
        "descripcion": "✅ Reales | Max 30K | Garantía 30D",
        "tiempo": "30K/Día"
    },
    "ig_likes_world_big": {
        "nombre": "❤️ Likes Mundo [Max 100K] 💎",
        "api_id": 17859,
        "precio_por_mil": 3.50,
        "costo_real": 1.65,
        "ganancia_base": 1.85,
        "descripcion": "✅ HQ Real | Non Drop | 100K/Día",
        "tiempo": "Rápido"
    },
    "ig_views_story": {
        "nombre": "👁️ Vistas Historias 📖",
        "api_id": 17860,
        "precio_por_mil": 4.50,
        "costo_real": 2.20,
        "ganancia_base": 2.30,
        "descripcion": "✅ Max 200K | Garantía 30D | Reales",
        "tiempo": "200K/Día"
    },
    "ig_shares": {
        "nombre": "📤 Comparticiones Post 📨",
        "api_id": 17861,
        "precio_por_mil": 8.00,
        "costo_real": 4.95,
        "ganancia_base": 3.05,
        "descripcion": "✅ Max 200K | Reales | Garantía 30D",
        "tiempo": "Rápido"
    },
    "ig_views_video": {
        "nombre": "📹 Vistas Videos 🎬",
        "api_id": 17862,
        "precio_por_mil": 6.50,
        "costo_real": 3.85,
        "ganancia_base": 2.65,
        "descripcion": "✅ HQ Real | Non Drop | 200K/Día",
        "tiempo": "Estable"
    },
    "ig_likes_impressions": {
        "nombre": "❤️ Likes + Impresiones 🇷🇺",
        "api_id": 17863,
        "precio_por_mil": 5.50,
        "costo_real": 3.30,
        "ganancia_base": 2.20,
        "descripcion": "✅ Rusos | Max 200K | Reales",
        "tiempo": "200K/Día"
    },
    "ig_likes_impressions_30d": {
        "nombre": "❤️ Likes + Impresiones ♻️",
        "api_id": 17864,
        "precio_por_mil": 7.00,
        "costo_real": 4.40,
        "ganancia_base": 2.60,
        "descripcion": "✅ Garantía 30D | Reales | 200K/Día",
        "tiempo": "Rápido"
    },
    "ig_likes_male": {
        "nombre": "❤️ Likes Hombres 👨",
        "api_id": 17865,
        "precio_por_mil": 7.00,
        "costo_real": 4.40,
        "ganancia_base": 2.60,
        "descripcion": "✅ Solo Hombres | Max 130K | Garantía",
        "tiempo": "130K/Día"
    },
    "ig_followers_brazil": {
        "nombre": "👥 Seguidores Brasil 🇧🇷",
        "api_id": 8686,
        "precio_por_mil": 2.50,
        "costo_real": 0.90,
        "ganancia_base": 1.60,
        "descripcion": "✅ 100% Reales | Max 10K | Instant",
        "tiempo": "Rápido"
    },

    # ==============================================
    # 📘 YOUTUBE - LIKES
    # ==============================================
    "yt_likes_server": {
        "nombre": "👍 Likes YouTube [New Server] ⚡",
        "api_id": 17855,
        "precio_por_mil": 2.00,
        "costo_real": 0.828,
        "ganancia_base": 1.17,
        "descripcion": "✅ Almost No Drop | 5K/Día | Instant",
        "tiempo": "Rápido"
    },
    "yt_likes_server_30d": {
        "nombre": "👍 Likes [Garantía 30D] ♻️",
        "api_id": 17856,
        "precio_por_mil": 2.20,
        "costo_real": 0.85,
        "ganancia_base": 1.35,
        "descripcion": "✅ Non Drop | 10K/Día | Garantía",
        "tiempo": "Instantáneo"
    },
    "yt_likes_high_speed": {
        "nombre": "👍 Likes Alta Velocidad 🔥",
        "api_id": 15956,
        "precio_por_mil": 3.50,
        "costo_real": 1.80,
        "ganancia_base": 1.70,
        "descripcion": "✅ Super Instant | 1K/Min | No Refill",
        "tiempo": "Muy Rápido"
    },
    "yt_likes_high_speed_30d": {
        "nombre": "👍 Likes Velocidad ♻️ 30D",
        "api_id": 15957,
        "precio_por_mil": 3.80,
        "costo_real": 1.90,
        "ganancia_base": 1.90,
        "descripcion": "✅ Garantía 30D | 1K/Min | Rápidos",
        "tiempo": "Instantáneo"
    },
    "yt_likes_high_speed_60d": {
        "nombre": "👍 Likes Velocidad ♻️ 60D",
        "api_id": 15958,
        "precio_por_mil": 4.00,
        "costo_real": 2.00,
        "ganancia_base": 2.00,
        "descripcion": "✅ Garantía 60 Días | 1K/Min",
        "tiempo": "Instantáneo"
    },
    "yt_likes_high_speed_90d": {
        "nombre": "👍 Likes Velocidad ♻️ 90D",
        "api_id": 15959,
        "precio_por_mil": 4.20,
        "costo_real": 2.10,
        "ganancia_base": 2.10,
        "descripcion": "✅ Garantía 90 Días | Premium",
        "tiempo": "Instantáneo"
    },
    "yt_likes_high_speed_365d": {
        "nombre": "👍 Likes Velocidad ♻️ 1 AÑO",
        "api_id": 15960,
        "precio_por_mil": 4.50,
        "costo_real": 2.20,
        "ganancia_base": 2.30,
        "descripcion": "✅ Garantía 365 Días | Máxima Calidad",
        "tiempo": "Instantáneo"
    },
    "yt_likes_lifetime": {
        "nombre": "👍 Likes [GARANTÍA VIDA] 💎",
        "api_id": 15961,
        "precio_por_mil": 4.80,
        "costo_real": 2.30,
        "ganancia_base": 2.50,
        "descripcion": "✅ Garantía Permanente | El mejor servicio",
        "tiempo": "Instantáneo"
    },

    # ==============================================
    # 📘 FACEBOOK
    # ==============================================
    "fb_followers_hq": {
        "nombre": "👥 Seguidores Facebook HQ 📘",
        "api_id": 12238,
        "precio_por_mil": 1.20,
        "costo_real": 0.33,
        "ganancia_base": 0.87,
        "descripcion": "✅ Perfiles Reales | 0% Drop | 50K/Día",
        "tiempo": "Instant"
    },
    "fb_followers_nodrop": {
        "nombre": "👥 Seguidores [Non Drop] ♻️",
        "api_id": 8044,
        "precio_por_mil": 1.30,
        "costo_real": 0.34,
        "ganancia_base": 0.96,
        "descripcion": "✅ Garantía 30D | Rápidos | 50K/Día",
        "tiempo": "Instant"
    },
    "fb_reactions_like": {
        "nombre": "👍 Reacciones Like FB",
        "api_id": 1461,
        "precio_por_mil": 0.70,
        "costo_real": 0.22,
        "ganancia_base": 0.48,
        "descripcion": "✅ Likes Reales | Garantía 30D | 50K/Día",
        "tiempo": "Rápido"
    },
    "fb_reactions_love": {
        "nombre": "❤️ Reacciones Love",
        "api_id": 655,
        "precio_por_mil": 0.70,
        "costo_real": 0.22,
        "ganancia_base": 0.48,
        "descripcion": "✅ Corazones | Garantía 30D | Rápidas",
        "tiempo": "Rápido"
    },
    "fb_reactions_wow": {
        "nombre": "😮 Reacciones Wow",
        "api_id": 656,
        "precio_por_mil": 0.70,
        "costo_real": 0.22,
        "ganancia_base": 0.48,
        "descripcion": "✅ Sorpresa | Garantía 30D | 50K/Día",
        "tiempo": "Rápido"
    },
    "fb_reactions_care": {
        "nombre": "🥰 Reacciones Care",
        "api_id": 1459,
        "precio_por_mil": 0.70,
        "costo_real": 0.22,
        "ganancia_base": 0.48,
        "descripcion": "✅ Cariño | Garantía 30D | Reales",
        "tiempo": "Rápido"
    },
    "fb_reactions_haha": {
        "nombre": "😂 Reacciones Haha",
        "api_id": 657,
        "precio_por_mil": 0.70,
        "costo_real": 0.22,
        "ganancia_base": 0.48,
        "descripcion": "✅ Risas | Garantía 30D | Rápidas",
        "tiempo": "Rápido"
    },
    "fb_reactions_sad": {
        "nombre": "😢 Reacciones Sad",
        "api_id": 658,
        "precio_por_mil": 0.70,
        "costo_real": 0.22,
        "ganancia_base": 0.48,
        "descripcion": "✅ Tristeza | Garantía 30D | Reales",
        "tiempo": "Rápido"
    },
    "fb_reactions_angry": {
        "nombre": "😡 Reacciones Angry",
        "api_id": 659,
        "precio_por_mil": 0.70,
        "costo_real": 0.22,
        "ganancia_base": 0.48,
        "descripcion": "✅ Enojo | Garantía 30D | 50K/Día",
        "tiempo": "Rápido"
    },

    # ==============================================
    # ✈️ TELEGRAM
    # ==============================================
    "tg_members_nodrop": {
        "nombre": "👥 Miembros Telegram ♻️ 90D",
        "api_id": 9043,
        "precio_por_mil": 1.50,
        "costo_real": 0.25,
        "ganancia_base": 1.25,
        "descripcion": "✅ Zero Drop | Garantía 90 Días | Rápidos",
        "tiempo": "Estable"
    },
    "tg_premium_3d": {
        "nombre": "⭐ Premium Members + Views [3D]",
        "api_id": 17705,
        "precio_por_mil": 4.50,
        "costo_real": 1.45,
        "ganancia_base": 3.05,
        "descripcion": "✅ Cuentas Premium | 50K/Día | 3 Días",
        "tiempo": "Instant"
    },
    "tg_premium_7d": {
        "nombre": "⭐ Premium Members + Views [7D]",
        "api_id": 17706,
        "precio_por_mil": 6.50,
        "costo_real": 2.26,
        "ganancia_base": 4.24,
        "descripcion": "✅ Garantía 7 Días | Alta Calidad",
        "tiempo": "Instant"
    },
    "tg_premium_10d": {
        "nombre": "⭐ Premium Members + Views [10D]",
        "api_id": 17707,
        "precio_por_mil": 8.00,
        "costo_real": 2.85,
        "ganancia_base": 5.15,
        "descripcion": "✅ Garantía 10 Días | Exclusivo",
        "tiempo": "Instant"
    },
    "tg_premium_15d": {
        "nombre": "⭐ Premium Members + Views [15D]",
        "api_id": 17708,
        "precio_por_mil": 10.00,
        "costo_real": 3.85,
        "ganancia_base": 6.15,
        "descripcion": "✅ Garantía 15 Días | Top Quality",
        "tiempo": "Instant"
    },
    "tg_premium_20d": {
        "nombre": "⭐ Premium Members + Views [20D]",
        "api_id": 17709,
        "precio_por_mil": 13.00,
        "costo_real": 5.75,
        "ganancia_base": 7.25,
        "descripcion": "✅ Garantía 20 Días | Elite",
        "tiempo": "Instant"
    },
    "tg_premium_25d": {
        "nombre": "⭐ Premium Members + Views [25D]",
        "api_id": 17710,
        "precio_por_mil": 15.00,
        "costo_real": 6.25,
        "ganancia_base": 8.75,
        "descripcion": "✅ Garantía 25 Días | VIP",
        "tiempo": "Instant"
    },
    "tg_premium_30d": {
        "nombre": "⭐ Premium Members + Views [30D]",
        "api_id": 17711,
        "precio_por_mil": 16.50,
        "costo_real": 6.85,
        "ganancia_base": 9.65,
        "descripcion": "✅ Garantía 30 Días | MÁXIMO NIVEL",
        "tiempo": "Instant"
    },
    "tg_bot_start": {
        "nombre": "🤖 Bot Start Básico",
        "api_id": 17715,
        "precio_por_mil": 5.50,
        "costo_real": 2.45,
        "ganancia_base": 3.05,
        "descripcion": "✅ Instant Start | Max 200K | Non Drop",
        "tiempo": "Rápido"
    },
    "tg_bot_activity": {
        "nombre": "🤖 Bot Start + Actividad",
        "api_id": 17716,
        "precio_por_mil": 7.50,
        "costo_real": 3.35,
        "ganancia_base": 4.15,
        "descripcion": "✅ Con Actividad | Premium Accounts | Rápido",
        "tiempo": "Instant"
    }
}

# ==============================================
# 🧮 FUNCIÓN DE CÁLCULO
# ==============================================
def calcular_precio_total(servicio_id, cantidad, uid_usuario=None):
    """
    Calcula precio final, costo y ganancia.
    Si es Seller, aplica su comisión personalizada.
    """
    servicio = SERVICIOS.get(servicio_id)
    
    if not servicio:
        return 0, 0, 0
    
    precio_base = servicio['precio_por_mil']
    costo_real = servicio['costo_real']
    ganancia = servicio['ganancia_base']
    precio_final = precio_base

    # Aplicar descuento si es vendedor
    if uid_usuario and es_seller(uid_usuario):
        datos_seller = obtener_datos(uid_usuario)
        if datos_seller and "info_nivel" in datos_seller:
            comision = datos_seller['info_nivel'].get('comision', 0)
            descuento = (precio_base * comision) / 100
            precio_final = precio_base - descuento
            ganancia = descuento  # La ganancia del sistema se ajusta al descuento

    # Calcular montos finales
    total_cobrar = round((precio_final / 1000) * cantidad, 4)
    total_costo = round((costo_real / 1000) * cantidad, 4)
    total_ganancia = round((ganancia / 1000) * cantidad, 4)

    return total_cobrar, total_costo, total_ganancia

# ==============================================
# 📋 FUNCIONES DE CONSULTA
# ==============================================
def listar_servicios():
    """Retorna el catálogo completo de servicios"""
    return SERVICIOS

def obtener_servicio(servicio_id):
    """Obtiene datos de un servicio específico"""
    return SERVICIOS.get(servicio_id)

def buscar_por_api_id(api_id):
    """Busca servicio por su ID de API externa"""
    for clave, datos in SERVICIOS.items():
        if datos.get('api_id') == api_id:
            return clave, datos
    return None, None
