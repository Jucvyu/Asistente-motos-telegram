# imagenes.py - Busca en la web (DuckDuckGo) la foto de cada moto y la guarda en caché
#
# El bot llama a obtener_imagen(moto) y recibe los bytes de la foto (o None).
# Los enlaces que funcionan se guardan en imagenes_motos.json para no buscar dos veces.
# Si una foto no corresponde a la moto, borra su entrada del JSON (o pon otro enlace en "url").
#
# Para buscar de una vez las fotos de todo el catálogo:
#     python imagenes.py
import asyncio
import io
import json
import re
import threading
import time
import unicodedata
from pathlib import Path

import httpx
from ddgs import DDGS
from PIL import Image, UnidentifiedImageError

ARCHIVO_CACHE = Path(__file__).with_name("imagenes_motos.json")
TIPOS_VALIDOS = ("image/jpeg", "image/png")
TAMANO_MAXIMO = 8 * 1024 * 1024  # Telegram acepta fotos de hasta 10 MB
CABECERAS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/130.0 Safari/537.36",
    "Accept": "image/jpeg,image/png,image/*;q=0.8",
}

_cache = None
_bloqueo = asyncio.Lock()

# Un solo cliente de búsqueda para todo el programa: crear uno por búsqueda agota
# las conexiones del sistema después de unas 25 búsquedas
_buscador = None
_bloqueo_buscador = threading.Lock()

# ─── Caché ──────────────────────────────────────────────

def nombre(moto: dict) -> str:
    return f"{moto['marca']} {moto['modelo']}"

def cargar_cache() -> dict:
    global _cache
    if _cache is None:
        try:
            _cache = json.loads(ARCHIVO_CACHE.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            _cache = {}
    return _cache

def guardar_cache():
    ARCHIVO_CACHE.write_text(json.dumps(cargar_cache(), ensure_ascii=False, indent=2), encoding="utf-8")

# ─── Búsqueda ───────────────────────────────────────────

def compacto(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", texto)

def buscar(consulta: str) -> list[dict]:
    global _buscador
    with _bloqueo_buscador:
        for intento in range(3):
            try:
                if _buscador is None:
                    _buscador = DDGS(timeout=10)
                return _buscador.images(consulta, max_results=10, safesearch="moderate")
            except Exception:
                if intento == 2:
                    raise
                _buscador = None  # se crea un cliente nuevo y se reintenta
                time.sleep(3 * (intento + 1))

def nombra_el_modelo(resultado: dict, moto: dict) -> bool:
    texto = compacto(resultado.get("title", "") + resultado.get("image", "") + resultado.get("url", ""))
    return compacto(moto["modelo"]) in texto

def buscar_candidatas(moto: dict) -> list[tuple[str, dict]]:
    """Devuelve los enlaces a probar, en orden: primero los que nombran el modelo exacto.

    Prueba varias consultas hasta encontrar resultados que mencionen el modelo, para no
    quedarse con la foto de otra moto de la misma marca.
    """
    resultados = []
    for consulta in (f"{nombre(moto)} moto", nombre(moto), f"{nombre(moto)} motocicleta"):
        resultados += buscar(consulta)
        if any(nombra_el_modelo(r, moto) for r in resultados):
            break

    buenas = [r for r in resultados if nombra_el_modelo(r, moto)]
    otras = [r for r in resultados if not nombra_el_modelo(r, moto)]
    buenas.sort(key=lambda r: int(r.get("width") or 0) < 500)  # primero las grandes

    intentos = []
    for r in buenas:  # foto original y, si no baja, su miniatura
        intentos += [(r["image"], r), (r["thumbnail"], r)]
    intentos += [(r["image"], r) for r in otras] + [(r["thumbnail"], r) for r in otras]
    return intentos

LADO_MAXIMO = 1280  # píxeles; Telegram reduce las fotos más grandes de todos modos

def preparar_foto(datos: bytes):
    """Convierte la foto a JPG con fondo blanco (los PNG transparentes salen negros en Telegram)."""
    try:
        img = Image.open(io.BytesIO(datos))
        img.load()
    except (UnidentifiedImageError, OSError):
        return None
    if img.width < 200 or img.height < 120:  # demasiado pequeña para verse bien
        return None
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        fondo = Image.new("RGB", img.size, "white")
        fondo.paste(img, mask=img.getchannel("A"))
        img = fondo
    else:
        img = img.convert("RGB")
    img.thumbnail((LADO_MAXIMO, LADO_MAXIMO))
    salida = io.BytesIO()
    img.save(salida, "JPEG", quality=88)
    return salida.getvalue()

async def descargar(cliente: httpx.AsyncClient, url: str):
    try:
        r = await cliente.get(url)
        tipo = r.headers.get("content-type", "").split(";")[0].strip().lower()
        if r.status_code == 200 and tipo in TIPOS_VALIDOS and 5_000 < len(r.content) < TAMANO_MAXIMO:
            return await asyncio.to_thread(preparar_foto, r.content)
    except httpx.HTTPError:
        pass
    return None

async def obtener_imagen(moto: dict):
    """Devuelve los bytes de la foto de la moto, o None si no se encontró ninguna."""
    cache = cargar_cache()
    clave = nombre(moto)
    async with httpx.AsyncClient(headers=CABECERAS, timeout=15, follow_redirects=True) as cliente:
        guardada = cache.get(clave)
        if guardada:
            datos = await descargar(cliente, guardada["url"])
            if datos:
                return datos

        try:
            intentos = await asyncio.to_thread(buscar_candidatas, moto)
        except Exception as e:  # DuckDuckGo puede limitar los pedidos
            print(f"⚠️ No se pudo buscar la imagen de {clave}: {e}")
            return None

        for url, c in intentos:
            datos = await descargar(cliente, url)
            if datos:
                async with _bloqueo:
                    cache[clave] = {"url": url, "titulo": c.get("title", ""), "pagina": c.get("url", "")}
                    guardar_cache()
                return datos
    return None

# ─── Precarga de todo el catálogo ───────────────────────

async def precargar():
    """Busca solo las motos que aún no tienen foto en la caché.

    Después de unas 25 búsquedas seguidas en el mismo proceso, las conexiones empiezan
    a fallar; por eso se detiene tras 3 fallos seguidos. Vuelve a correrlo y seguirá
    donde quedó.
    """
    from motos import MOTOS

    cache = cargar_cache()
    pendientes = [m for m in MOTOS if nombre(m) not in cache]
    print(f"{len(MOTOS) - len(pendientes)} de {len(MOTOS)} motos ya tienen foto. Faltan {len(pendientes)}.")

    fallos_seguidos = 0
    for i, moto in enumerate(pendientes, 1):
        try:
            datos = await asyncio.wait_for(obtener_imagen(moto), timeout=60)
        except asyncio.TimeoutError:
            datos = None
        print(f"[{i}/{len(pendientes)}] {nombre(moto)}: " + (f"✅ {len(datos) // 1024} KB" if datos else "❌ sin imagen"))
        fallos_seguidos = 0 if datos else fallos_seguidos + 1
        if fallos_seguidos >= 3:
            print("\n⏸️ Varias búsquedas seguidas fallaron. Vuelve a correr el script para continuar.")
            break
        await asyncio.sleep(1)  # pausa para no saturar el buscador

    faltan = [nombre(m) for m in MOTOS if nombre(m) not in cargar_cache()]
    print(f"\nListo: {len(MOTOS) - len(faltan)} de {len(MOTOS)} motos con foto.")
    if faltan:
        print("Sin foto todavía:", ", ".join(faltan))

if __name__ == "__main__":
    asyncio.run(precargar())
