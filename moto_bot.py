# moto_bot.py - Bot de Telegram que recomienda motos según la necesidad del usuario
import asyncio
import os
import re
from html import escape, unescape

from dotenv import load_dotenv
from telegram import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ChatAction
from telegram.error import TelegramError
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from recomendador import (
    NO_SE,
    RANGOS_CC,
    USOS,
    ficha_resultado,
    formatear_pesos,
    opciones_rango,
    parsear_presupuesto,
    parsear_rango,
    parsear_uso,
    pros_contras,
    recomendar,
)
from imagenes import obtener_imagen

# ─── Configuración ──────────────────────────────────────

load_dotenv()
# Usa un token propio si existe; si no, el mismo del otro bot
TOKEN = os.getenv("MOTO_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("❌ ERROR: Configura MOTO_BOT_TOKEN o TELEGRAM_TOKEN en el archivo .env")
    exit(1)

USO, CILINDRAJE, POTENCIA, TORQUE, PRESUPUESTO = range(5)
DATOS_PERFIL = ("uso", "cc", "hp", "nm", "presupuesto")

# ─── Teclados ───────────────────────────────────────────

def teclado(opciones) -> ReplyKeyboardMarkup:
    opciones = list(opciones)
    filas = [opciones[i:i + 2] for i in range(0, len(opciones), 2)]
    return ReplyKeyboardMarkup(filas, one_time_keyboard=True, resize_keyboard=True)

TECLADO_USO = teclado(USOS.values())
TECLADO_CC = teclado([*RANGOS_CC, NO_SE])

def preparar_opciones(context: ContextTypes.DEFAULT_TYPE, dato: str):
    """Calcula las opciones de hp o Nm que tienen sentido para lo ya elegido."""
    opciones, (minimo, maximo) = opciones_rango(dato, context.user_data)
    context.user_data["opciones"] = opciones
    return teclado([*opciones, NO_SE]), f"{minimo:g} y {maximo:g}"

# ─── Pasos de la conversación ───────────────────────────

async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🏍️ <b>¡Hola! Soy tu asesor de motos.</b>\n\n"
        "Te haré 5 preguntas rápidas y te diré cuáles motos se ajustan mejor a lo que necesitas.\n"
        "Puedes cancelar en cualquier momento con /cancelar.\n\n"
        "<b>1/5 · ¿Para qué la vas a usar principalmente?</b>",
        parse_mode="HTML",
        reply_markup=TECLADO_USO,
    )
    return USO

async def recibir_uso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uso = parsear_uso(update.message.text)
    if uso is None:
        await update.message.reply_text("🤔 No entendí. Elige una de las opciones:", reply_markup=TECLADO_USO)
        return USO

    context.user_data["uso"] = uso
    await update.message.reply_text(
        "<b>2/5 · ¿Qué cilindraje buscas?</b>\n"
        "Elige un rango o escribe un valor, por ejemplo <i>200</i> o <i>150 a 250</i>.",
        parse_mode="HTML",
        reply_markup=TECLADO_CC,
    )
    return CILINDRAJE

async def recibir_cilindraje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["cc"] = parsear_rango(update.message.text, RANGOS_CC)
    except ValueError:
        await update.message.reply_text("🤔 Escribe un número (ej. 200) o elige una opción:", reply_markup=TECLADO_CC)
        return CILINDRAJE

    teclado_hp, rango = preparar_opciones(context, "hp")
    await update.message.reply_text(
        "<b>3/5 · ¿Cuánta potencia necesitas?</b>\n"
        f"Con ese cilindraje, las motos tienen entre <b>{rango} hp</b>. "
        "Elige una opción o escribe un valor, por ejemplo <i>15</i> o <i>más de 20</i>.",
        parse_mode="HTML",
        reply_markup=teclado_hp,
    )
    return POTENCIA

async def recibir_potencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["hp"] = parsear_rango(update.message.text, context.user_data["opciones"])
    except ValueError:
        teclado_hp = teclado([*context.user_data["opciones"], NO_SE])
        await update.message.reply_text("🤔 Escribe un número (ej. 15) o elige una opción:", reply_markup=teclado_hp)
        return POTENCIA

    teclado_nm, rango = preparar_opciones(context, "nm")
    await update.message.reply_text(
        "<b>4/5 · ¿Qué torque buscas?</b>\n"
        "En newton-metro (Nm). Más torque = más fuerza para subir y cargar peso.\n"
        f"Con lo que elegiste, las motos tienen entre <b>{rango} Nm</b>.",
        parse_mode="HTML",
        reply_markup=teclado_nm,
    )
    return TORQUE

async def recibir_torque(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["nm"] = parsear_rango(update.message.text, context.user_data["opciones"])
    except ValueError:
        teclado_nm = teclado([*context.user_data["opciones"], NO_SE])
        await update.message.reply_text("🤔 Escribe un número (ej. 15) o elige una opción:", reply_markup=teclado_nm)
        return TORQUE

    await update.message.reply_text(
        "<b>5/5 · ¿Cuál es tu presupuesto?</b>\n"
        "Escríbelo en pesos, por ejemplo <i>12.000.000</i>, <i>12 millones</i> o <i>12</i>.",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PRESUPUESTO

async def recibir_presupuesto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["presupuesto"] = parsear_presupuesto(update.message.text)
    except ValueError:
        await update.message.reply_text(
            "🤔 No entendí el valor. Escribe algo como <i>12.000.000</i> o <i>12 millones</i>.",
            parse_mode="HTML",
        )
        return PRESUPUESTO

    perfil = {dato: context.user_data.get(dato) for dato in DATOS_PERFIL}
    context.user_data.clear()
    pendientes = await enviar_recomendacion(update.message.chat, perfil)
    if pendientes:
        # Para el botón "Ver más": qué motos faltan por mostrar y desde qué número
        context.user_data["ver_mas"] = {"perfil": perfil, "motos": pendientes, "desde": TARJETAS_INICIALES}
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Búsqueda cancelada. Escribe /start cuando quieras empezar de nuevo.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

async def sin_conversacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏍️ Escribe /start para que te recomiende una moto.")

# ─── Respuesta final ────────────────────────────────────

def ficha(moto: dict) -> str:
    return (
        f"⚙️ {moto['cc']} cc · {moto['hp']:g} hp · {moto['nm']:g} Nm · {moto['peso']} kg\n"
        f"💰 {formatear_pesos(moto['precio'])} aprox."
    )

def lista(titulo: str, razones: list[str], vacio: str) -> str:
    lineas = [f"   • {escape(r)}" for r in razones] or [f"   • {vacio}"]
    return titulo + "\n" + "\n".join(lineas)

TARJETAS_INICIALES = 3   # fichas con foto que se envían de una vez
TARJETAS_POR_BOTON = 5   # fichas que envía cada toque de "Ver más"
LIMITE_MENSAJE = 4000    # Telegram permite 4096 caracteres por mensaje; se deja margen

def lista_nombres(motos: list[dict]) -> str:
    """Lista numerada solo con marca y modelo, con todas las motos."""
    return "\n".join(f"{i}. {escape(m['marca'])} {escape(m['modelo'])}" for i, m in enumerate(motos, 1))

def dividir_mensaje(texto: str) -> list[str]:
    """Parte un texto largo en varios mensajes, cortando entre líneas."""
    mensajes, actual = [], ""
    for linea in texto.split("\n"):
        candidato = f"{actual}\n{linea}" if actual else linea
        if actual and largo_telegram(candidato) > LIMITE_MENSAJE:
            mensajes.append(actual)
            actual = linea
        else:
            actual = candidato
    return mensajes + [actual]

def encabezado(busqueda: dict) -> str:
    perfectas, dentro = busqueda["perfectas"], busqueda["dentro"]
    mostradas = len(busqueda["resultados"])
    baja = ", aunque su afinidad sea baja" if busqueda["resultados"][0][1] < 50 else ""
    if not dentro:
        return (
            "🔎 <b>No encontré motos con tus especificaciones</b> y ninguna cabe en tu presupuesto. "
            f"Te dejo las más cercanas a lo que puedes pagar{baja}:"
        )
    if perfectas == 0:
        return (
            "🔎 <b>No encontré motos con todas tus especificaciones.</b> "
            f"Te dejo las que más se acercan{baja}:"
        )

    motos = "moto que cumple" if perfectas == 1 else "motos que cumplen"
    texto = f"✅ Encontré <b>{perfectas} {motos} todo</b> lo que pediste:\n\n{lista_nombres(busqueda['lista_perfectas'])}\n\n"
    if perfectas < mostradas:
        texto += "Abajo va su ficha y las más cercanas que no cumplen todo:"
    elif perfectas > mostradas:
        texto += f"Abajo va la ficha de las {mostradas} mejores. Con el botón del final puedes ver las demás."
    else:
        texto += "Abajo va la ficha de cada una:"
    return texto

LIMITE_PIE_FOTO = 1024  # máximo de caracteres que Telegram permite debajo de una foto

def titulo_moto(i: int, moto: dict) -> str:
    medallas = ["🥇", "🥈", "🥉"]
    puesto = medallas[i] if i < len(medallas) else f"{i + 1}."
    return f"{puesto} <b>{escape(moto['marca'])} {escape(moto['modelo'])}</b> ({escape(moto['tipo'])})"

def bloque_moto(i: int, moto: dict, porcentaje: int, cumple: bool, perfil: dict) -> str:
    pros, contras = pros_contras(moto, perfil)
    sello = " · ✅ Cumple todo" if cumple else ""
    return (
        f"{titulo_moto(i, moto)}\nAfinidad {porcentaje}%{sello}\n"
        f"{ficha(moto)}\n\n"
        + lista("👍 <b>Por qué puede ser ideal para ti:</b>", pros, "Nada que destacar para tu caso") + "\n\n"
        + lista("👎 <b>Por qué puede no serlo:</b>", contras, "Nada importante para lo que buscas")
    )

def tarjetas(perfil: dict, motos: list[dict], desde: int = 0) -> list[tuple]:
    """(moto, título corto, bloque completo) para cada moto, numeradas desde `desde`."""
    lista_tarjetas = []
    for k, moto in enumerate(motos):
        _, porcentaje, cumple = ficha_resultado(moto, perfil)
        i = desde + k
        lista_tarjetas.append((moto, titulo_moto(i, moto), bloque_moto(i, moto, porcentaje, cumple, perfil)))
    return lista_tarjetas

def boton_ver_mas(quedan: int) -> InlineKeyboardMarkup:
    siguiente = min(quedan, TARJETAS_POR_BOTON)
    texto = f"📸 Ver {siguiente} más (quedan {quedan})" if quedan > siguiente else f"📸 Ver las {quedan} restantes"
    return InlineKeyboardMarkup([[InlineKeyboardButton(texto, callback_data="ver_mas")]])

def construir_partes(perfil: dict) -> dict:
    """Arma la respuesta por partes: encabezado, un bloque por moto, cierre y motos pendientes."""
    busqueda = recomendar(perfil, cantidad=TARJETAS_INICIALES)
    resultados = busqueda["resultados"]

    inicio = (
        "🏍️ <b>Tus motos recomendadas</b>\n"
        f"Uso: {USOS[perfil['uso']]} · Presupuesto: {formatear_pesos(perfil['presupuesto'])}\n\n"
        + encabezado(busqueda)
    )
    motos = tarjetas(perfil, [moto for moto, _, _ in resultados])
    # Las que cumplen todo pero no alcanzaron a mostrarse con foto
    pendientes = busqueda["lista_perfectas"][len(resultados):]

    mejor, _, cumple = resultados[0]
    nombre = f"{escape(mejor['marca'])} {escape(mejor['modelo'])}"
    recomendacion = (
        f"💡 <b>Mi recomendación:</b> la {nombre} es la que mejor encaja con lo que necesitas."
        if cumple else
        f"💡 <b>Mi recomendación:</b> la {nombre} es la más cercana. "
        "Prueba con un rango más amplio o con otro presupuesto para ver más opciones."
    )
    mas = (
        f"\n\n📋 Hay <b>{len(pendientes)} motos más</b> que cumplen todo. Toca el botón para ver su ficha."
        if pendientes else ""
    )
    cierre = (
        recomendacion + mas + "\n\n"
        "<i>Precios y fichas aproximados; confírmalos con el concesionario. "
        "Las fotos son de referencia y se buscan en internet.</i>\n"
        "🔁 Escribe /start para hacer otra búsqueda."
    )
    return {"inicio": inicio, "motos": motos, "cierre": cierre, "pendientes": pendientes}

def construir_respuesta(perfil: dict) -> str:
    """Toda la respuesta como un solo texto (sin fotos)."""
    partes = construir_partes(perfil)
    separador = "\n\n━━━━━━━━━━━━━━━━━━━━━━\n"
    return separador.join([partes["inicio"], *(bloque for _, _, bloque in partes["motos"]), partes["cierre"]])

def largo_telegram(html_texto: str) -> int:
    """Largo como lo cuenta Telegram: sin etiquetas y en unidades UTF-16 (un emoji cuenta 2)."""
    plano = unescape(re.sub(r"<[^>]+>", "", html_texto))
    return len(plano.encode("utf-16-le")) // 2

async def enviar_tarjetas(chat: Chat, lista_tarjetas: list[tuple]):
    """Envía cada moto como foto con su ficha debajo (o solo texto si no hay foto)."""
    await chat.send_action(ChatAction.UPLOAD_PHOTO)
    fotos = await asyncio.gather(
        *(obtener_imagen(moto) for moto, _, _ in lista_tarjetas),
        return_exceptions=True,
    )

    for (moto, titulo, bloque), foto in zip(lista_tarjetas, fotos):
        if isinstance(foto, bytes):
            try:
                if largo_telegram(bloque) <= LIMITE_PIE_FOTO:
                    await chat.send_photo(foto, caption=bloque, parse_mode="HTML")
                    continue
                await chat.send_photo(foto, caption=titulo, parse_mode="HTML")
            except TelegramError as e:
                print(f"⚠️ No se pudo enviar la foto de {moto['marca']} {moto['modelo']}: {e}")
        # Sin foto, o con un texto demasiado largo para ir debajo de la foto
        await chat.send_message(bloque, parse_mode="HTML")

async def enviar_recomendacion(chat: Chat, perfil: dict) -> list[dict]:
    """Envía la recomendación y devuelve las motos que quedaron para el botón "Ver más"."""
    partes = construir_partes(perfil)
    for texto in dividir_mensaje(partes["inicio"]):
        await chat.send_message(texto, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    await enviar_tarjetas(chat, partes["motos"])

    pendientes = partes["pendientes"]
    await chat.send_message(
        partes["cierre"],
        parse_mode="HTML",
        reply_markup=boton_ver_mas(len(pendientes)) if pendientes else None,
    )
    return pendientes

async def ver_mas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Botón "Ver más": envía las siguientes motos que cumplen todo."""
    consulta = update.callback_query
    await consulta.answer()
    try:
        await consulta.edit_message_reply_markup(None)  # quita el botón ya usado
    except TelegramError:
        pass

    chat = consulta.message.chat
    datos = context.user_data.get("ver_mas")
    if not datos or not datos["motos"]:
        await chat.send_message("⌛ Esa búsqueda ya terminó. Escribe /start para hacer otra.")
        return

    lote, datos["motos"] = datos["motos"][:TARJETAS_POR_BOTON], datos["motos"][TARJETAS_POR_BOTON:]
    desde = datos["desde"]
    datos["desde"] += len(lote)
    await enviar_tarjetas(chat, tarjetas(datos["perfil"], lote, desde))

    if datos["motos"]:
        await chat.send_message(
            f"📋 Quedan <b>{len(datos['motos'])} motos más</b> que cumplen todo.",
            parse_mode="HTML",
            reply_markup=boton_ver_mas(len(datos["motos"])),
        )
    else:
        context.user_data.pop("ver_mas", None)
        await chat.send_message("✅ Esas son todas las motos que cumplen lo que pediste.\n🔁 Escribe /start para hacer otra búsqueda.")

# ─── Inicialización ─────────────────────────────────────

def main():
    print("🏍️ Bot recomendador de motos activo...")
    app = ApplicationBuilder().token(TOKEN).build()

    texto = filters.TEXT & ~filters.COMMAND
    conversacion = ConversationHandler(
        entry_points=[CommandHandler("start", inicio)],
        states={
            USO: [MessageHandler(texto, recibir_uso)],
            CILINDRAJE: [MessageHandler(texto, recibir_cilindraje)],
            POTENCIA: [MessageHandler(texto, recibir_potencia)],
            TORQUE: [MessageHandler(texto, recibir_torque)],
            PRESUPUESTO: [MessageHandler(texto, recibir_presupuesto)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar), CommandHandler("start", inicio)],
    )
    app.add_handler(conversacion)
    app.add_handler(CallbackQueryHandler(ver_mas, pattern="^ver_mas$"))
    app.add_handler(MessageHandler(texto, sin_conversacion))

    print("🟢 Bot corriendo... Esperando mensajes")
    app.run_polling()

if __name__ == "__main__":
    main()
