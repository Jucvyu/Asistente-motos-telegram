# motos.py - Catálogo de motos para el bot recomendador
#
# Valores APROXIMADOS de referencia (mercado colombiano). Los precios están en
# pesos colombianos (COP) y cambian según año, versión y concesionario.
# Para agregar o actualizar motos, edita esta lista: el bot la usa directamente.
#
# Campos:
#   cc      -> cilindraje (cm³)
#   hp      -> potencia máxima (caballos de fuerza)
#   nm      -> torque máximo (newton-metro)
#   peso    -> peso aproximado (kg)
#   precio  -> precio aproximado (COP)
#   usos    -> para qué sirve: ciudad, trabajo, carretera, trocha, deportiva

MOTOS = [
    # ── Trabajo / ciudad (bajo cilindraje) ─────────────────
    {"marca": "Bajaj", "modelo": "Boxer CT100", "tipo": "Urbana", "cc": 102, "hp": 7.7, "nm": 8.2, "peso": 110, "precio": 5_600_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "AKT", "modelo": "NKD 125", "tipo": "Urbana", "cc": 125, "hp": 9.5, "nm": 9.0, "peso": 113, "precio": 5_400_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Suzuki", "modelo": "GN 125", "tipo": "Urbana", "cc": 124, "hp": 11.0, "nm": 9.6, "peso": 112, "precio": 6_900_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Honda", "modelo": "CB 125F", "tipo": "Urbana", "cc": 125, "hp": 10.6, "nm": 10.9, "peso": 117, "precio": 7_600_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Yamaha", "modelo": "YBR 125", "tipo": "Urbana", "cc": 124, "hp": 10.0, "nm": 10.0, "peso": 118, "precio": 7_500_000, "usos": ["trabajo", "ciudad"]},

    # ── Scooters ───────────────────────────────────────────
    {"marca": "Yamaha", "modelo": "BWS 125", "tipo": "Scooter", "cc": 125, "hp": 9.0, "nm": 9.0, "peso": 115, "precio": 9_200_000, "usos": ["ciudad"]},
    {"marca": "Honda", "modelo": "PCX 160", "tipo": "Scooter", "cc": 157, "hp": 15.8, "nm": 14.7, "peso": 132, "precio": 14_300_000, "usos": ["ciudad", "carretera"]},
    {"marca": "Yamaha", "modelo": "NMAX 155", "tipo": "Scooter", "cc": 155, "hp": 15.0, "nm": 13.9, "peso": 131, "precio": 15_200_000, "usos": ["ciudad", "carretera"]},

    # ── Naked / street de 150 a 250 cc ─────────────────────
    {"marca": "Yamaha", "modelo": "FZ 150", "tipo": "Naked", "cc": 149, "hp": 12.4, "nm": 13.6, "peso": 135, "precio": 10_200_000, "usos": ["ciudad", "trabajo"]},
    {"marca": "Suzuki", "modelo": "Gixxer 150", "tipo": "Naked", "cc": 155, "hp": 14.0, "nm": 14.0, "peso": 141, "precio": 9_600_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "TVS", "modelo": "Apache RTR 160 4V", "tipo": "Naked", "cc": 160, "hp": 17.6, "nm": 14.7, "peso": 145, "precio": 9_500_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "Bajaj", "modelo": "Pulsar NS 160", "tipo": "Naked", "cc": 160, "hp": 17.0, "nm": 14.6, "peso": 142, "precio": 10_000_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "Honda", "modelo": "CB 190R", "tipo": "Naked", "cc": 184, "hp": 15.4, "nm": 15.7, "peso": 140, "precio": 11_200_000, "usos": ["ciudad", "carretera"]},
    {"marca": "Bajaj", "modelo": "Pulsar NS 200", "tipo": "Naked", "cc": 200, "hp": 24.0, "nm": 18.7, "peso": 156, "precio": 12_600_000, "usos": ["ciudad", "deportiva", "carretera"]},
    {"marca": "KTM", "modelo": "Duke 200", "tipo": "Naked", "cc": 200, "hp": 25.0, "nm": 19.3, "peso": 159, "precio": 15_500_000, "usos": ["ciudad", "deportiva"]},

    # ── Deportivas ─────────────────────────────────────────
    {"marca": "Yamaha", "modelo": "R15 V4", "tipo": "Deportiva", "cc": 155, "hp": 18.4, "nm": 14.2, "peso": 141, "precio": 15_400_000, "usos": ["deportiva"]},
    {"marca": "Yamaha", "modelo": "MT-03", "tipo": "Naked", "cc": 321, "hp": 42.0, "nm": 29.6, "peso": 168, "precio": 28_500_000, "usos": ["deportiva", "ciudad", "carretera"]},
    {"marca": "KTM", "modelo": "390 Duke", "tipo": "Naked", "cc": 373, "hp": 44.0, "nm": 37.0, "peso": 167, "precio": 27_000_000, "usos": ["deportiva", "ciudad"]},
    {"marca": "Kawasaki", "modelo": "Ninja 400", "tipo": "Deportiva", "cc": 399, "hp": 45.0, "nm": 37.0, "peso": 168, "precio": 33_000_000, "usos": ["deportiva", "carretera"]},
    {"marca": "Kawasaki", "modelo": "Z650", "tipo": "Naked", "cc": 649, "hp": 67.0, "nm": 64.0, "peso": 187, "precio": 45_000_000, "usos": ["deportiva", "carretera", "ciudad"]},
    {"marca": "Yamaha", "modelo": "MT-07", "tipo": "Naked", "cc": 689, "hp": 73.0, "nm": 67.0, "peso": 184, "precio": 48_000_000, "usos": ["deportiva", "carretera"]},

    # ── Doble propósito / trocha ───────────────────────────
    {"marca": "Honda", "modelo": "XR 150L", "tipo": "Doble propósito", "cc": 149, "hp": 12.5, "nm": 12.5, "peso": 129, "precio": 9_600_000, "usos": ["trocha", "trabajo"]},
    {"marca": "Yamaha", "modelo": "XTZ 150", "tipo": "Doble propósito", "cc": 149, "hp": 12.2, "nm": 12.8, "peso": 128, "precio": 11_000_000, "usos": ["trocha", "trabajo"]},
    {"marca": "Honda", "modelo": "XR 190L", "tipo": "Doble propósito", "cc": 184, "hp": 16.0, "nm": 16.0, "peso": 138, "precio": 12_300_000, "usos": ["trocha", "trabajo", "carretera"]},
    {"marca": "Yamaha", "modelo": "XTZ 250", "tipo": "Doble propósito", "cc": 249, "hp": 21.0, "nm": 20.6, "peso": 140, "precio": 17_000_000, "usos": ["trocha", "carretera"]},
    {"marca": "Honda", "modelo": "XRE 300", "tipo": "Doble propósito", "cc": 291, "hp": 25.0, "nm": 27.0, "peso": 148, "precio": 21_000_000, "usos": ["trocha", "carretera"]},

    # ── Touring / aventura / clásicas ──────────────────────
    {"marca": "Suzuki", "modelo": "V-Strom 250 SX", "tipo": "Aventura", "cc": 249, "hp": 26.0, "nm": 22.2, "peso": 167, "precio": 20_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Royal Enfield", "modelo": "Classic 350", "tipo": "Clásica", "cc": 349, "hp": 20.2, "nm": 27.0, "peso": 195, "precio": 18_500_000, "usos": ["carretera", "ciudad"]},
    {"marca": "Royal Enfield", "modelo": "Himalayan 411", "tipo": "Aventura", "cc": 411, "hp": 24.3, "nm": 32.0, "peso": 199, "precio": 22_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Kawasaki", "modelo": "Versys-X 300", "tipo": "Aventura", "cc": 296, "hp": 39.0, "nm": 26.0, "peso": 175, "precio": 27_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "BMW", "modelo": "G 310 GS", "tipo": "Aventura", "cc": 313, "hp": 34.0, "nm": 28.0, "peso": 175, "precio": 30_000_000, "usos": ["carretera", "trocha"]},

    # ── Más urbanas y de trabajo (100 a 125 cc) ─────────────
    {"marca": "Hero", "modelo": "Eco Deluxe 100", "tipo": "Urbana", "cc": 97, "hp": 8.0, "nm": 8.0, "peso": 112, "precio": 4_500_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "TVS", "modelo": "Sport 100", "tipo": "Urbana", "cc": 110, "hp": 8.3, "nm": 8.7, "peso": 112, "precio": 4_900_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Honda", "modelo": "Wave 110S", "tipo": "Semiautomática", "cc": 109, "hp": 8.3, "nm": 8.6, "peso": 100, "precio": 5_300_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Suzuki", "modelo": "Viva R 115", "tipo": "Semiautomática", "cc": 113, "hp": 8.3, "nm": 8.4, "peso": 98, "precio": 5_900_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Yamaha", "modelo": "Crypton FI", "tipo": "Semiautomática", "cc": 113, "hp": 8.9, "nm": 9.4, "peso": 99, "precio": 6_000_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Bajaj", "modelo": "Platino 125", "tipo": "Urbana", "cc": 125, "hp": 10.8, "nm": 11.0, "peso": 122, "precio": 6_300_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Bajaj", "modelo": "Discover 125", "tipo": "Urbana", "cc": 125, "hp": 11.0, "nm": 11.0, "peso": 122, "precio": 6_600_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "TVS", "modelo": "Raider 125", "tipo": "Urbana", "cc": 125, "hp": 11.4, "nm": 11.2, "peso": 123, "precio": 7_200_000, "usos": ["ciudad", "trabajo"]},

    # ── Más scooters ───────────────────────────────────────
    {"marca": "Honda", "modelo": "Navi", "tipo": "Scooter", "cc": 109, "hp": 8.0, "nm": 9.0, "peso": 107, "precio": 5_900_000, "usos": ["ciudad"]},
    {"marca": "Kymco", "modelo": "Agility 125", "tipo": "Scooter", "cc": 125, "hp": 9.5, "nm": 9.5, "peso": 112, "precio": 7_000_000, "usos": ["ciudad"]},
    {"marca": "Suzuki", "modelo": "Burgman Street 125", "tipo": "Scooter", "cc": 124, "hp": 8.6, "nm": 10.0, "peso": 110, "precio": 8_500_000, "usos": ["ciudad"]},
    {"marca": "Honda", "modelo": "ADV 160", "tipo": "Scooter", "cc": 157, "hp": 15.8, "nm": 14.7, "peso": 133, "precio": 15_500_000, "usos": ["ciudad", "carretera"]},
    {"marca": "Yamaha", "modelo": "XMAX 300", "tipo": "Scooter", "cc": 292, "hp": 28.0, "nm": 29.0, "peso": 179, "precio": 28_000_000, "usos": ["ciudad", "carretera"]},

    # ── Más naked y street (150 a 400 cc) ──────────────────
    {"marca": "Hero", "modelo": "Hunk 160R", "tipo": "Naked", "cc": 163, "hp": 15.0, "nm": 14.0, "peso": 142, "precio": 8_500_000, "usos": ["ciudad", "trabajo"]},
    {"marca": "Honda", "modelo": "CB 160F", "tipo": "Naked", "cc": 162, "hp": 15.0, "nm": 14.0, "peso": 139, "precio": 9_900_000, "usos": ["ciudad", "trabajo"]},
    {"marca": "Bajaj", "modelo": "Pulsar N250", "tipo": "Naked", "cc": 249, "hp": 24.5, "nm": 21.5, "peso": 162, "precio": 13_500_000, "usos": ["ciudad", "carretera", "deportiva"]},
    {"marca": "Yamaha", "modelo": "FZ 25", "tipo": "Naked", "cc": 249, "hp": 20.8, "nm": 20.1, "peso": 153, "precio": 14_500_000, "usos": ["ciudad", "carretera"]},
    {"marca": "Suzuki", "modelo": "Gixxer 250", "tipo": "Naked", "cc": 249, "hp": 26.0, "nm": 22.2, "peso": 156, "precio": 15_500_000, "usos": ["ciudad", "deportiva", "carretera"]},
    {"marca": "Royal Enfield", "modelo": "Hunter 350", "tipo": "Clásica", "cc": 349, "hp": 20.2, "nm": 27.0, "peso": 181, "precio": 15_500_000, "usos": ["ciudad", "carretera"]},
    {"marca": "Honda", "modelo": "CB 300F", "tipo": "Naked", "cc": 293, "hp": 24.0, "nm": 25.6, "peso": 153, "precio": 17_000_000, "usos": ["ciudad", "carretera"]},
    {"marca": "KTM", "modelo": "250 Duke", "tipo": "Naked", "cc": 249, "hp": 30.0, "nm": 24.0, "peso": 162, "precio": 19_000_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "BMW", "modelo": "G 310 R", "tipo": "Naked", "cc": 313, "hp": 34.0, "nm": 28.0, "peso": 164, "precio": 25_000_000, "usos": ["ciudad", "deportiva"]},

    # ── Más deportivas ─────────────────────────────────────
    {"marca": "Bajaj", "modelo": "Pulsar RS 200", "tipo": "Deportiva", "cc": 200, "hp": 24.5, "nm": 18.7, "peso": 166, "precio": 14_000_000, "usos": ["deportiva", "carretera"]},
    {"marca": "KTM", "modelo": "RC 200", "tipo": "Deportiva", "cc": 200, "hp": 25.0, "nm": 19.2, "peso": 160, "precio": 17_000_000, "usos": ["deportiva"]},
    {"marca": "Yamaha", "modelo": "R3", "tipo": "Deportiva", "cc": 321, "hp": 42.0, "nm": 29.6, "peso": 169, "precio": 30_500_000, "usos": ["deportiva", "carretera"]},
    {"marca": "Honda", "modelo": "CB 650R", "tipo": "Naked", "cc": 649, "hp": 94.0, "nm": 63.0, "peso": 203, "precio": 52_000_000, "usos": ["deportiva", "carretera", "ciudad"]},
    {"marca": "Kawasaki", "modelo": "Z900", "tipo": "Naked", "cc": 948, "hp": 123.0, "nm": 98.6, "peso": 212, "precio": 62_000_000, "usos": ["deportiva", "carretera"]},
    {"marca": "Yamaha", "modelo": "MT-09", "tipo": "Naked", "cc": 890, "hp": 117.0, "nm": 93.0, "peso": 193, "precio": 65_000_000, "usos": ["deportiva", "carretera"]},
    {"marca": "Kawasaki", "modelo": "Ninja ZX-6R", "tipo": "Deportiva", "cc": 636, "hp": 127.0, "nm": 70.0, "peso": 198, "precio": 72_000_000, "usos": ["deportiva"]},
    {"marca": "Ducati", "modelo": "Monster", "tipo": "Naked", "cc": 937, "hp": 111.0, "nm": 93.0, "peso": 188, "precio": 80_000_000, "usos": ["deportiva", "ciudad"]},

    # ── Más doble propósito / trocha ───────────────────────
    {"marca": "AKT", "modelo": "TT DS 200", "tipo": "Doble propósito", "cc": 197, "hp": 15.5, "nm": 15.0, "peso": 131, "precio": 9_500_000, "usos": ["trocha", "trabajo"]},
    {"marca": "Hero", "modelo": "XPulse 200 4V", "tipo": "Doble propósito", "cc": 200, "hp": 19.0, "nm": 17.4, "peso": 159, "precio": 11_500_000, "usos": ["trocha", "carretera"]},
    {"marca": "Honda", "modelo": "XR 300L Tornado", "tipo": "Doble propósito", "cc": 293, "hp": 25.0, "nm": 26.0, "peso": 144, "precio": 21_000_000, "usos": ["trocha", "carretera"]},

    # ── Más touring / aventura / clásicas ──────────────────
    {"marca": "Bajaj", "modelo": "Dominar 250", "tipo": "Touring", "cc": 249, "hp": 27.0, "nm": 23.5, "peso": 180, "precio": 15_900_000, "usos": ["carretera", "ciudad"]},
    {"marca": "Royal Enfield", "modelo": "Meteor 350", "tipo": "Crucero", "cc": 349, "hp": 20.2, "nm": 27.0, "peso": 191, "precio": 19_000_000, "usos": ["carretera"]},
    {"marca": "Bajaj", "modelo": "Dominar 400", "tipo": "Touring", "cc": 373, "hp": 40.0, "nm": 35.0, "peso": 193, "precio": 20_500_000, "usos": ["carretera", "deportiva"]},
    {"marca": "Royal Enfield", "modelo": "Himalayan 450", "tipo": "Aventura", "cc": 452, "hp": 39.5, "nm": 40.0, "peso": 196, "precio": 28_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "CFMoto", "modelo": "450MT", "tipo": "Aventura", "cc": 449, "hp": 44.0, "nm": 44.0, "peso": 175, "precio": 29_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "KTM", "modelo": "390 Adventure", "tipo": "Aventura", "cc": 373, "hp": 43.0, "nm": 37.0, "peso": 172, "precio": 30_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Royal Enfield", "modelo": "Interceptor 650", "tipo": "Clásica", "cc": 648, "hp": 47.0, "nm": 52.0, "peso": 202, "precio": 30_000_000, "usos": ["carretera", "ciudad"]},
    {"marca": "Benelli", "modelo": "TRK 502", "tipo": "Aventura", "cc": 500, "hp": 47.0, "nm": 46.0, "peso": 235, "precio": 30_000_000, "usos": ["carretera"]},
    {"marca": "Honda", "modelo": "NX 500", "tipo": "Aventura", "cc": 471, "hp": 47.0, "nm": 43.0, "peso": 196, "precio": 39_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Kawasaki", "modelo": "KLR 650", "tipo": "Aventura", "cc": 652, "hp": 40.0, "nm": 52.0, "peso": 209, "precio": 42_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Suzuki", "modelo": "V-Strom 650", "tipo": "Aventura", "cc": 645, "hp": 70.0, "nm": 62.0, "peso": 216, "precio": 50_000_000, "usos": ["carretera"]},
    {"marca": "Yamaha", "modelo": "Ténéré 700", "tipo": "Aventura", "cc": 689, "hp": 72.0, "nm": 68.0, "peso": 204, "precio": 58_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Harley-Davidson", "modelo": "Nightster", "tipo": "Crucero", "cc": 975, "hp": 89.0, "nm": 95.0, "peso": 221, "precio": 85_000_000, "usos": ["carretera", "ciudad"]},
    {"marca": "Honda", "modelo": "Africa Twin", "tipo": "Aventura", "cc": 1084, "hp": 100.0, "nm": 105.0, "peso": 226, "precio": 95_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "BMW", "modelo": "R 1250 GS", "tipo": "Aventura", "cc": 1254, "hp": 136.0, "nm": 143.0, "peso": 249, "precio": 110_000_000, "usos": ["carretera", "trocha"]},

    # ── Tercera ampliación: urbanas y de trabajo ───────────
    {"marca": "Bajaj", "modelo": "Boxer CT 125", "tipo": "Urbana", "cc": 125, "hp": 10.0, "nm": 10.8, "peso": 122, "precio": 6_200_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "AKT", "modelo": "CR4 125", "tipo": "Urbana", "cc": 125, "hp": 10.4, "nm": 9.8, "peso": 125, "precio": 6_000_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Hero", "modelo": "Ignitor 125", "tipo": "Urbana", "cc": 125, "hp": 11.2, "nm": 11.0, "peso": 130, "precio": 6_800_000, "usos": ["ciudad", "trabajo"]},
    {"marca": "Bajaj", "modelo": "Pulsar NS 125", "tipo": "Naked", "cc": 124, "hp": 12.0, "nm": 11.0, "peso": 144, "precio": 8_000_000, "usos": ["ciudad", "trabajo"]},
    {"marca": "Yamaha", "modelo": "SZ15RR", "tipo": "Urbana", "cc": 149, "hp": 12.2, "nm": 12.8, "peso": 136, "precio": 8_300_000, "usos": ["trabajo", "ciudad"]},
    {"marca": "Honda", "modelo": "XBlade 160", "tipo": "Naked", "cc": 163, "hp": 13.8, "nm": 14.7, "peso": 140, "precio": 9_400_000, "usos": ["ciudad", "trabajo"]},
    {"marca": "Hero", "modelo": "Xtreme 160R 4V", "tipo": "Naked", "cc": 163, "hp": 16.6, "nm": 14.6, "peso": 144, "precio": 9_000_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "Bajaj", "modelo": "Pulsar N160", "tipo": "Naked", "cc": 165, "hp": 16.0, "nm": 14.7, "peso": 152, "precio": 10_500_000, "usos": ["ciudad", "carretera"]},
    {"marca": "TVS", "modelo": "Apache RTR 200 4V", "tipo": "Naked", "cc": 198, "hp": 20.5, "nm": 17.3, "peso": 152, "precio": 11_300_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "Bajaj", "modelo": "Pulsar 220F", "tipo": "Semicarenada", "cc": 220, "hp": 20.4, "nm": 18.6, "peso": 160, "precio": 11_900_000, "usos": ["carretera", "ciudad"]},
    {"marca": "Bajaj", "modelo": "Avenger 220 Street", "tipo": "Crucero", "cc": 220, "hp": 19.0, "nm": 17.5, "peso": 154, "precio": 11_500_000, "usos": ["carretera", "ciudad"]},

    # ── Tercera ampliación: scooters ───────────────────────
    {"marca": "Honda", "modelo": "Dio", "tipo": "Scooter", "cc": 110, "hp": 7.8, "nm": 9.0, "peso": 103, "precio": 6_400_000, "usos": ["ciudad"]},
    {"marca": "TVS", "modelo": "Ntorq 125", "tipo": "Scooter", "cc": 125, "hp": 9.4, "nm": 10.5, "peso": 116, "precio": 8_400_000, "usos": ["ciudad"]},
    {"marca": "Honda", "modelo": "Click 160", "tipo": "Scooter", "cc": 157, "hp": 15.4, "nm": 13.8, "peso": 114, "precio": 10_500_000, "usos": ["ciudad"]},
    {"marca": "Yamaha", "modelo": "Aerox 155", "tipo": "Scooter", "cc": 155, "hp": 15.0, "nm": 13.9, "peso": 125, "precio": 13_000_000, "usos": ["ciudad"]},

    # ── Tercera ampliación: naked y deportivas ─────────────
    {"marca": "Suzuki", "modelo": "Gixxer SF 150", "tipo": "Deportiva", "cc": 155, "hp": 13.6, "nm": 13.8, "peso": 148, "precio": 10_800_000, "usos": ["deportiva", "ciudad"]},
    {"marca": "Yamaha", "modelo": "MT-15", "tipo": "Naked", "cc": 155, "hp": 18.4, "nm": 14.1, "peso": 138, "precio": 14_500_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "Yamaha", "modelo": "XSR 155", "tipo": "Clásica", "cc": 155, "hp": 18.4, "nm": 14.2, "peso": 134, "precio": 15_800_000, "usos": ["ciudad"]},
    {"marca": "Benelli", "modelo": "302S", "tipo": "Naked", "cc": 300, "hp": 38.0, "nm": 26.5, "peso": 189, "precio": 21_000_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "TVS", "modelo": "Apache RR 310", "tipo": "Deportiva", "cc": 312, "hp": 34.0, "nm": 27.3, "peso": 174, "precio": 22_000_000, "usos": ["deportiva", "carretera"]},
    {"marca": "CFMoto", "modelo": "450NK", "tipo": "Naked", "cc": 449, "hp": 46.0, "nm": 39.0, "peso": 165, "precio": 22_000_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "Kawasaki", "modelo": "Z400", "tipo": "Naked", "cc": 399, "hp": 45.0, "nm": 37.0, "peso": 167, "precio": 29_000_000, "usos": ["ciudad", "deportiva"]},
    {"marca": "Honda", "modelo": "CB 500 Hornet", "tipo": "Naked", "cc": 471, "hp": 47.0, "nm": 43.0, "peso": 189, "precio": 34_000_000, "usos": ["ciudad", "carretera"]},
    {"marca": "Kawasaki", "modelo": "Ninja 650", "tipo": "Deportiva", "cc": 649, "hp": 67.0, "nm": 64.0, "peso": 193, "precio": 46_000_000, "usos": ["deportiva", "carretera"]},
    {"marca": "Triumph", "modelo": "Trident 660", "tipo": "Naked", "cc": 660, "hp": 81.0, "nm": 64.0, "peso": 189, "precio": 48_000_000, "usos": ["ciudad", "deportiva", "carretera"]},
    {"marca": "Suzuki", "modelo": "GSX-8S", "tipo": "Naked", "cc": 776, "hp": 82.0, "nm": 78.0, "peso": 202, "precio": 52_000_000, "usos": ["deportiva", "ciudad", "carretera"]},
    {"marca": "KTM", "modelo": "790 Duke", "tipo": "Naked", "cc": 799, "hp": 105.0, "nm": 87.0, "peso": 174, "precio": 52_000_000, "usos": ["deportiva", "ciudad"]},
    {"marca": "Honda", "modelo": "CBR 650R", "tipo": "Deportiva", "cc": 649, "hp": 94.0, "nm": 63.0, "peso": 208, "precio": 55_000_000, "usos": ["deportiva", "carretera"]},
    {"marca": "Yamaha", "modelo": "YZF-R7", "tipo": "Deportiva", "cc": 689, "hp": 73.0, "nm": 67.0, "peso": 188, "precio": 55_000_000, "usos": ["deportiva"]},
    {"marca": "Ducati", "modelo": "Scrambler Icon", "tipo": "Clásica", "cc": 803, "hp": 73.0, "nm": 65.0, "peso": 185, "precio": 55_000_000, "usos": ["ciudad", "carretera"]},
    {"marca": "BMW", "modelo": "S 1000 RR", "tipo": "Deportiva", "cc": 999, "hp": 207.0, "nm": 113.0, "peso": 197, "precio": 120_000_000, "usos": ["deportiva"]},
    {"marca": "Suzuki", "modelo": "Hayabusa", "tipo": "Deportiva", "cc": 1340, "hp": 187.0, "nm": 150.0, "peso": 264, "precio": 125_000_000, "usos": ["deportiva", "carretera"]},

    # ── Tercera ampliación: doble propósito / trocha ───────
    {"marca": "Kawasaki", "modelo": "KLX 230", "tipo": "Doble propósito", "cc": 233, "hp": 18.0, "nm": 18.3, "peso": 134, "precio": 18_000_000, "usos": ["trocha"]},
    {"marca": "Royal Enfield", "modelo": "Scram 411", "tipo": "Doble propósito", "cc": 411, "hp": 24.3, "nm": 32.0, "peso": 185, "precio": 20_000_000, "usos": ["trocha", "ciudad", "carretera"]},
    {"marca": "Honda", "modelo": "CRF 300L", "tipo": "Doble propósito", "cc": 286, "hp": 27.0, "nm": 26.6, "peso": 142, "precio": 25_000_000, "usos": ["trocha", "carretera"]},
    {"marca": "Suzuki", "modelo": "DR 650", "tipo": "Doble propósito", "cc": 644, "hp": 43.0, "nm": 54.0, "peso": 166, "precio": 35_000_000, "usos": ["trocha", "carretera"]},

    # ── Tercera ampliación: touring, aventura y crucero ────
    {"marca": "Royal Enfield", "modelo": "Bullet 350", "tipo": "Clásica", "cc": 349, "hp": 20.2, "nm": 27.0, "peso": 195, "precio": 17_000_000, "usos": ["carretera", "ciudad"]},
    {"marca": "Honda", "modelo": "Rebel 500", "tipo": "Crucero", "cc": 471, "hp": 46.0, "nm": 43.0, "peso": 191, "precio": 35_000_000, "usos": ["carretera", "ciudad"]},
    {"marca": "Royal Enfield", "modelo": "Super Meteor 650", "tipo": "Crucero", "cc": 648, "hp": 47.0, "nm": 52.3, "peso": 241, "precio": 36_000_000, "usos": ["carretera"]},
    {"marca": "Kawasaki", "modelo": "Vulcan S", "tipo": "Crucero", "cc": 649, "hp": 60.0, "nm": 63.0, "peso": 229, "precio": 48_000_000, "usos": ["carretera", "ciudad"]},
    {"marca": "Kawasaki", "modelo": "Versys 650", "tipo": "Touring", "cc": 649, "hp": 66.0, "nm": 61.0, "peso": 219, "precio": 50_000_000, "usos": ["carretera"]},
    {"marca": "Honda", "modelo": "XL750 Transalp", "tipo": "Aventura", "cc": 755, "hp": 91.0, "nm": 75.0, "peso": 208, "precio": 58_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "CFMoto", "modelo": "800MT", "tipo": "Aventura", "cc": 799, "hp": 95.0, "nm": 77.0, "peso": 231, "precio": 60_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Suzuki", "modelo": "V-Strom 800DE", "tipo": "Aventura", "cc": 776, "hp": 84.0, "nm": 78.0, "peso": 230, "precio": 62_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "BMW", "modelo": "F 900 GS", "tipo": "Aventura", "cc": 895, "hp": 105.0, "nm": 93.0, "peso": 219, "precio": 75_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Triumph", "modelo": "Tiger 900 GT", "tipo": "Aventura", "cc": 888, "hp": 108.0, "nm": 90.0, "peso": 219, "precio": 80_000_000, "usos": ["carretera", "trocha"]},
    {"marca": "Yamaha", "modelo": "Tracer 9 GT", "tipo": "Touring", "cc": 890, "hp": 117.0, "nm": 93.0, "peso": 220, "precio": 85_000_000, "usos": ["carretera"]},
    {"marca": "Ducati", "modelo": "Multistrada V2", "tipo": "Aventura", "cc": 937, "hp": 113.0, "nm": 96.0, "peso": 225, "precio": 90_000_000, "usos": ["carretera"]},
    {"marca": "Harley-Davidson", "modelo": "Sportster S", "tipo": "Crucero", "cc": 1252, "hp": 121.0, "nm": 125.0, "peso": 228, "precio": 100_000_000, "usos": ["carretera", "ciudad"]},
]
