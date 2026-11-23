# recomendador.py - Lógica para recomendar motos (sin dependencias de Telegram)
import math
import re
import statistics
import unicodedata

from motos import MOTOS

# ─── Opciones que se le muestran al usuario ─────────────

USOS = {
    "ciudad": "🏙️ Ciudad / uso diario",
    "trabajo": "📦 Trabajo / domicilios",
    "carretera": "🛣️ Carretera / viajes",
    "trocha": "⛰️ Trocha / off-road",
    "deportiva": "🏁 Deportiva / velocidad",
}

# Palabras con las que se reconoce el uso si el usuario lo escribe a mano
PALABRAS_USO = {
    "ciudad": ["ciudad", "diario", "urbano", "universidad", "estudio", "transporte"],
    "trabajo": ["trabajo", "domicilio", "mensajer", "reparto", "carga", "rappi"],
    "carretera": ["carretera", "viaje", "ruta", "paseo", "turismo", "touring"],
    "trocha": ["trocha", "off", "campo", "finca", "montaña", "barro", "destapado"],
    "deportiva": ["deport", "velocidad", "pista", "rapida", "adrenalina"],
}

NO_SE = "🤷 No sé / me da igual"

RANGOS_CC = {
    "100 - 150 cc": (100, 150),
    "150 - 250 cc": (150, 250),
    "250 - 400 cc": (250, 400),
    "Más de 400 cc": (400, None),
}

# Cuánto se aleja una moto por cada unidad fuera de rango (escala de cada dato)
ESCALA = {"cc": 100, "hp": 10, "nm": 10}
NOMBRE_DATO = {"cc": "Cilindraje", "hp": "Potencia", "nm": "Torque"}
UNIDAD = {"cc": "cc", "hp": "hp", "nm": "Nm"}

TOLERANCIA_PRESUPUESTO = 0.10  # se aceptan motos hasta 10 % por encima
FUERA_DE_RANGO = 0.25          # castigo fijo por no cumplir, aunque sea por poco

# ─── Utilidades de texto ────────────────────────────────

def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower().strip())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def formatear_pesos(valor: float) -> str:
    return "$" + f"{valor:,.0f}".replace(",", ".")

def es_no_se(texto: str) -> bool:
    t = normalizar(texto)
    return texto == NO_SE or any(p in t for p in ["no se", "da igual", "cualquiera", "ninguno", "no importa"])

# ─── Interpretar respuestas ─────────────────────────────

def parsear_uso(texto: str):
    for clave, etiqueta in USOS.items():
        if texto == etiqueta:
            return clave
    t = normalizar(texto)
    for clave, palabras in PALABRAS_USO.items():
        if any(normalizar(p) in t for p in palabras):
            return clave
    return None

def parsear_rango(texto: str, opciones: dict):
    """Devuelve (minimo, maximo), None si al usuario le da igual, o lanza ValueError."""
    if texto in opciones:
        return opciones[texto]
    if es_no_se(texto):
        return None
    numeros = [float(n.replace(",", ".")) for n in re.findall(r"\d+(?:[.,]\d+)?", texto)]
    if len(numeros) >= 2:
        return tuple(sorted(numeros[:2]))
    if len(numeros) == 1:
        n = numeros[0]
        t = normalizar(texto)
        if any(p in t for p in ["mas de", "minimo", "al menos", "mayor"]):
            return (n, None)
        if any(p in t for p in ["menos de", "maximo", "hasta", "menor"]):
            return (None, n)
        return (n * 0.9, n * 1.1)
    raise ValueError("No se encontró un número")

def parsear_presupuesto(texto: str) -> float:
    """Entiende '8000000', '8.000.000', '8 millones', '8,5M', '12 palos' o '12' (millones)."""
    t = normalizar(texto)
    m = re.search(r"(\d[\d.,]*)\s*(millones|millon|mill|palos|palo|m\b)?", t)
    if not m:
        raise ValueError("No se encontró un número")
    numero, sufijo = m.group(1).rstrip(".,"), m.group(2)

    if sufijo or re.fullmatch(r"\d{1,3}[.,]\d{1,2}", numero):
        if numero.count(".") + numero.count(",") > 1:
            numero = re.sub(r"[.,]", "", numero)
        valor = float(numero.replace(",", ".")) * 1_000_000
    else:
        valor = float(re.sub(r"[.,]", "", numero))
        if valor < 1000:  # "12" -> 12 millones
            valor *= 1_000_000

    if not 1_000_000 <= valor <= 500_000_000:
        raise ValueError("Presupuesto fuera de rango")
    return valor

# ─── Rangos de hp y Nm según lo ya elegido ──────────────

def distancia_rango(valor: float, rango, escala: float) -> float:
    if rango is None:
        return 0.0
    minimo, maximo = rango
    if minimo is not None and valor < minimo:
        return FUERA_DE_RANGO + (minimo - valor) / escala
    if maximo is not None and valor > maximo:
        return FUERA_DE_RANGO + (valor - maximo) / escala
    return 0.0

def en_rango(valor: float, rango) -> bool:
    return distancia_rango(valor, rango, 1) == 0

def filtrar(catalogo, filtros: dict):
    return [m for m in catalogo if all(en_rango(m[d], r) for d, r in filtros.items())]

def opciones_rango(dato: str, perfil: dict, catalogo=MOTOS):
    """Arma las opciones de hp o Nm a partir de las motos que cumplen lo ya elegido.

    Para la potencia se mira el cilindraje; para el torque, el cilindraje y la potencia.
    Así nunca se ofrece, por ejemplo, "más de 40 hp" a quien pidió 100 - 150 cc.
    Devuelve (opciones, (mínimo, máximo)).
    """
    previos = {"hp": ["cc"], "nm": ["cc", "hp"]}[dato]
    base = catalogo
    # Si con todos los filtros quedan muy pocas motos, se van soltando de atrás hacia adelante
    for n in range(len(previos), 0, -1):
        filtros = {d: perfil[d] for d in previos[:n] if perfil.get(d)}
        seleccion = filtrar(catalogo, filtros)
        if len(seleccion) >= 4:
            base = seleccion
            break

    valores = sorted(m[dato] for m in base)
    minimo, maximo = valores[0], valores[-1]
    cortes = sorted({round(c) for c in statistics.quantiles(valores, n=4)} if len(valores) > 1 else set())
    cortes = [c for c in cortes if minimo < c < maximo]
    u = UNIDAD[dato]

    if not cortes:
        return {f"Cerca de {round(minimo)} {u}": (minimo, maximo)}, (minimo, maximo)

    opciones = {f"Hasta {cortes[0]} {u}": (None, cortes[0])}
    for a, b in zip(cortes, cortes[1:]):
        opciones[f"{a} - {b} {u}"] = (a, b)
    opciones[f"Más de {cortes[-1]} {u}"] = (cortes[-1], None)
    return opciones, (minimo, maximo)

# ─── Motor de recomendación ─────────────────────────────

def puntaje(moto: dict, perfil: dict) -> float:
    """Entre más bajo, más se parece la moto a lo que pidió el usuario."""
    p = 0.0
    if perfil["uso"] not in moto["usos"]:
        p += 2.0
    for dato in ("cc", "hp", "nm"):
        p += distancia_rango(moto[dato], perfil.get(dato), ESCALA[dato])

    presupuesto = perfil["presupuesto"]
    if moto["precio"] > presupuesto:
        p += (moto["precio"] - presupuesto) / presupuesto * 8
    else:
        # Leve preferencia por aprovechar el presupuesto
        p += (presupuesto - moto["precio"]) / presupuesto * 0.6
    return p

def cumple_todo(moto: dict, perfil: dict) -> bool:
    return (
        perfil["uso"] in moto["usos"]
        and all(en_rango(moto[d], perfil.get(d)) for d in ("cc", "hp", "nm"))
        and moto["precio"] <= perfil["presupuesto"] * (1 + TOLERANCIA_PRESUPUESTO)
    )

def afinidad(p: float) -> int:
    return round(100 * math.exp(-p / 2.5))

def recomendar(perfil: dict, catalogo=MOTOS, cantidad: int = 3):
    """Devuelve un dict con:
    resultados      -> las `cantidad` mejores como (moto, afinidad, cumple_todo), siempre con algo
    lista_perfectas -> TODAS las motos que cumplen todo, de la mejor a la peor
    perfectas       -> cuántas son
    dentro          -> si hay motos dentro del presupuesto
    """
    limite = perfil["presupuesto"] * (1 + TOLERANCIA_PRESUPUESTO)
    candidatas = [m for m in catalogo if m["precio"] <= limite]
    dentro = bool(candidatas)
    if not dentro:
        candidatas = list(catalogo)

    # Primero las que cumplen todo; luego, las más cercanas aunque su afinidad sea baja
    ordenadas = sorted(candidatas, key=lambda m: (not cumple_todo(m, perfil), puntaje(m, perfil)))
    lista_perfectas = [m for m in ordenadas if cumple_todo(m, perfil)]
    return {
        "resultados": [ficha_resultado(m, perfil) for m in ordenadas[:cantidad]],
        "lista_perfectas": lista_perfectas,
        "perfectas": len(lista_perfectas),
        "dentro": dentro,
    }

def ficha_resultado(moto: dict, perfil: dict):
    return moto, afinidad(puntaje(moto, perfil)), cumple_todo(moto, perfil)

# ─── Razones a favor y en contra ────────────────────────

def describir_rango(rango, unidad: str) -> str:
    minimo, maximo = rango
    if minimo is None:
        return f"hasta {maximo:g} {unidad}"
    if maximo is None:
        return f"más de {minimo:g} {unidad}"
    return f"{minimo:g} - {maximo:g} {unidad}"

def pros_contras(moto: dict, perfil: dict):
    """Devuelve (por qué puede ser ideal, por qué puede no serlo) para esa persona."""
    pros, contras = [], []
    uso = perfil["uso"]
    nombre_uso = USOS[uso].split(" ", 1)[1].lower()
    tipo, cc, hp, nm, peso = moto["tipo"], moto["cc"], moto["hp"], moto["nm"], moto["peso"]
    aventurera = tipo in ("Doble propósito", "Aventura")

    # Lo que pidió el usuario
    if uso in moto["usos"]:
        pros.append(f"Está pensada para {nombre_uso}")
    else:
        contras.append(f"No está pensada para {nombre_uso}")

    for dato in ("cc", "hp", "nm"):
        rango = perfil.get(dato)
        if rango is None:
            continue
        texto = f"{NOMBRE_DATO[dato]} de {moto[dato]:g} {UNIDAD[dato]}"
        pedido = describir_rango(rango, UNIDAD[dato])
        if en_rango(moto[dato], rango):
            pros.append(f"{texto}, dentro de lo que pediste ({pedido})")
        else:
            contras.append(f"{texto}, fuera de lo que pediste ({pedido})")

    diferencia = perfil["presupuesto"] - moto["precio"]
    if diferencia < 0:
        contras.append(f"Supera tu presupuesto por {formatear_pesos(-diferencia)}")
    elif diferencia >= perfil["presupuesto"] * 0.15:
        pros.append(f"Te sobran {formatear_pesos(diferencia)} para casco, SOAT y accesorios")
    else:
        pros.append(f"Cabe en tu presupuesto (te sobran {formatear_pesos(diferencia)})")

    # Características de la moto
    if tipo == "Scooter":
        pros.append("Automática: sin cambios en el trancón y con espacio bajo el sillín")
    if tipo == "Semiautomática":
        pros.append("Semiautomática: sin clutch, fácil de aprender a manejar")
    if peso <= 125:
        pros.append(f"Liviana ({peso} kg): fácil de maniobrar y parquear")
    if cc <= 150:
        pros.append("Gasta poca gasolina y su mantenimiento es económico")
    if aventurera and uso in ("trocha", "carretera", "trabajo"):
        pros.append("Suspensión de recorrido largo, buena para huecos y destapados")
    if hp >= 35 and uso in ("carretera", "deportiva"):
        pros.append(f"Con {hp:g} hp tiene potencia de sobra para adelantar")
    if nm >= 25 and uso in ("carretera", "trocha", "trabajo"):
        pros.append(f"Buen torque ({nm:g} Nm) para subir lomas con parrillero o carga")
    if tipo in ("Touring", "Crucero", "Clásica") and uso == "carretera":
        pros.append("Posición de manejo cómoda para viajes largos")

    if peso >= 190:
        contras.append(f"Pesada ({peso} kg): cuesta maniobrarla despacio o empujarla")
    if cc <= 125 and uso in ("carretera", "trocha"):
        contras.append(f"Con {cc} cc se queda corta en viajes largos y subidas fuertes")
    if tipo == "Scooter" and uso == "trocha":
        contras.append("Ruedas pequeñas: no está hecha para trocha")
    if tipo == "Deportiva" and uso in ("ciudad", "trabajo"):
        contras.append("Posición inclinada: cansa en trayectos diarios largos")
    if aventurera and uso in ("ciudad", "trabajo"):
        contras.append("Sillín alto: puede costar apoyar los pies si no eres alto")
    if hp >= 70:
        contras.append("Mucha potencia: no es para principiantes y el seguro es más caro")
    if cc > 200:
        contras.append("Por tener más de 200 cc, el SOAT es más costoso")
    if cc >= 400:
        contras.append("Consume más gasolina que una moto pequeña")

    return pros, contras
