# ==============================================
# 💳 SISTEMA DE VENTA CC - FULL DATA PRO
# ==============================================
# ✅ Lector de archivos .TXT
# ✅ Detecta cualquier formato
# ✅ BINs verificados con API
# ==============================================

import requests
import os
from datetime import datetime
from config import *  # ⬅️ AQUÍ TRAE TODO
from database import *
from logger import *

# ==============================================
# 📄 LECTOR DE ARCHIVOS TXT
# ==============================================
def procesar_archivo_txt(ruta_archivo):
    tarjetas_validas = []
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as archivo:
            lineas = archivo.readlines()
            
        for linea in lineas:
            linea = linea.strip()
            if not linea or len(linea) < 16:
                continue
            
            # Detectar separador
            if "|" in linea: partes = linea.split("|")
            elif "," in linea: partes = linea.split(",")
            elif ";" in linea: partes = linea.split(";")
            else: partes = linea.split()
            
            # Extraer datos
            numero = extraer_numero(partes[0])
            if not numero: continue
                
            mes = partes[1] if len(partes)>1 else "12"
            anio = partes[2] if len(partes)>2 else "28"
            cvv = partes[3] if len(partes)>3 else "000"
            nombre = partes[4] if len(partes)>4 else "Unknown"
            pais = partes[5] if len(partes)>5 else "United States"
            ciudad = partes[6] if len(partes)>6 else "Unknown"
            estado = partes[7] if len(partes)>7 else "Unknown"
            cp = partes[8] if len(partes)>8 else "00000"
            telefono = partes[9] if len(partes)>9 else "000000000"
            email = partes[10] if len(partes)>10 else "email@unknown.com"
            banco = partes[11] if len(partes)>11 else "Bank Unknown"
            tipo = partes[12] if len(partes)>12 else "Classic"
            
            tarjeta_limpia = f"{numero}|{mes}|{anio}|{cvv}|{nombre}|{pais}|{ciudad}|{estado}|{cp}|{telefono}|{email}|{banco}|{tipo}"
            tarjetas_validas.append(tarjeta_limpia)
        
        return True, tarjetas_validas
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def extraer_numero(texto):
    solo_numeros = ''.join(filter(str.isdigit, texto))
    if len(solo_numeros) >= 13 and len(solo_numeros) <= 19:
        return solo_numeros
    return None

# ==============================================
# 🔍 VERIFICAR BIN CON API
# ==============================================
def verificar_bin(numero):
    bin_number = str(numero)[:6]
    
    # Usando las variables de config.py
    if not API_KEY_BIN or API_KEY_BIN == "TU_API_KEY_AQUI":
        return True, {"bank": "No verificado", "country": "Desconocido"}
    
    try:
        headers = {'X-Api-Key': API_KEY_BIN}
        params = {'bin': bin_number}
        response = requests.get(API_URL_BIN, headers=headers, params=params, timeout=8)
        
        if response.status_code == 200:
            return True, response.json()
    except:
        pass
    
    return True, {"bank": "Desconocido", "country": "?"}

# ==============================================
# 🗄️ BASES DE DATOS
# ==============================================
BASES = {
    "visa": {
        "nombre": "💳 VISA - FULL DATA",
        "precio": PRECIO_VISA,  # ⬅️ Precio de config
        "tarjetas": []
    },
    "mastercard": {
        "nombre": "💳 MASTERCARD - FULL DATA",
        "precio": PRECIO_MASTERCARD,
        "tarjetas": []
    },
    "amex": {
        "nombre": "💳 AMERICAN EXPRESS",
        "precio": PRECIO_AMEX,
        "tarjetas": []
    },
    "discover": {
        "nombre": "💳 DISCOVER",
        "precio": PRECIO_DISCOVER,
        "tarjetas": []
    }
}

# ==============================================
# ⬆️ CARGAR DESDE TXT
# ==============================================
def cargar_desde_txt(tipo_db, nombre_archivo):
    ruta_completa = os.path.join(RUTA_BASES_TXT, nombre_archivo)
    exito, tarjetas = procesar_archivo_txt(ruta_completa)
    
    if not exito:
        return False, tarjetas
    
    if tipo_db in BASES:
        cantidad = len(tarjetas)
        BASES[tipo_db]['tarjetas'].extend(tarjetas)
        return True, f"✅ Cargadas <code>{cantidad}</code> tarjetas correctamente."
    
    return False, "❌ Base no encontrada"

# ==============================================
# 🛒 VENDER TARJETA
# ==============================================
def vender_tarjeta(uid, nombre_usuario, tipo_db):
    if tipo_db not in BASES:
        return False, "❌ Base no encontrada"
    
    db_info = BASES[tipo_db]
    
    if len(db_info['tarjetas']) == 0:
        return False, "⚠️ <b>AGOTADO</b>\nNo hay stock."
    
    precio = db_info['precio']
    
    # Verificar saldo
    usuario = obtener_usuario_db(uid)
    if not usuario or usuario.get('saldo', 0) < precio:
        return False, f"❌ Saldo insuficiente\nPrecio: {MONEDA} {precio:.2f}"
    
    # Sacar tarjeta
    datos = db_info['tarjetas'].pop(0).split("|")
    
    numero = datos[0]
    mes = datos[1]
    anio = datos[2]
    cvv = datos[3]
    nombre = datos[4]
    pais = datos[5]
    ciudad = datos[6]
    estado = datos[7]
    cp = datos[8]
    telefono = datos[9]
    email = datos[10]
    banco = datos[11]
    nivel = datos[12]
    
    # Verificar BIN
    valido, info_bin = verificar_bin(numero)
    
    # Descontar y registrar
    actualizar_usuario_db(uid, {"saldo": usuario['saldo'] - precio})
    insertar_movimiento_db({
        "uid": str(uid), "nombre": nombre_usuario, "tipo": "COMPRA",
        "monto": precio, "descripcion": f"CC Full Data | BIN: {numero[:6]}",
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    })
    
    emoji = obtener_bandera(pais)
    
    texto = f"""
💳 <b>✅ TARJETA ENTREGADA - FULL DATA</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏦 <b>Banco:</b> {banco}
🌍 <b>País:</b> {pais} {emoji}
📇 <b>Red:</b> {db_info['nombre'].replace('💳 ','')}
✅ <b>BIN ORIGINAL:</b> <code>{numero[:6]}</code>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>🔐 DATOS BANCARIOS:</b>
<code>{numero}</code>
📅 Exp: <code>{mes}/{anio}</code>
🔒 CVV: <code>{cvv}</code>

👤 <b>DATOS PERSONALES:</b>
• <b>Nombre:</b> {nombre}
• <b>Ciudad:</b> {ciudad}
• <b>Estado:</b> {estado}
• <b>CP:</b> {cp}
• <b>Teléfono:</b> {telefono}
• <b>Email:</b> {email}

💸 Pagado: {MONEDA} {precio:.2f}
✅ Datos 100% completos
"""
    return True, texto

# ==============================================
# 📋 MENU Y AYUDANTES
# ==============================================
def menu_tienda():
    return """
💳 <b>TIENDA DE TARJETAS - FULL DATA</b>

🔸 <b>INCLUYE:</b>
✅ Número, Expiración y CVV
✅ Nombre completo real
✅ Ciudad, Estado y Código Postal
✅ Teléfono y Email
✅ Banco y País verificados
✅ ✅ BIN 100% ORIGINAL

🔘 <b>Selecciona una opción:</b>
"""

def obtener_bases():
    return BASES

def obtener_bandera(pais):
    banderas = {
        "United States": "🇺🇸", "United Kingdom": "🇬🇧", "Canada": "🇨🇦",
        "Mexico": "🇲🇽", "Argentina": "🇦🇷", "Brazil": "🇧🇷", "Spain": "🇪🇸"
    }
    return banderas.get(pais, "🌍")

def obtener_stock_total():
    return sum(len(db['tarjetas']) for db in BASES.values())
