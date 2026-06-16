# =============================================================================
# archivo_csv.py
# Módulo de persistencia: lectura y escritura del archivo CSV de países.
# =============================================================================

import csv
import os

RUTA_CSV = "datos.csv"

# Columnas obligatorias del archivo CSV
COLUMNAS_REQUERIDAS = {"nombre", "poblacion", "superficie", "continente"}


def _validar_fila(fila, numero_fila):
    """
    Valida que una fila del CSV tenga el formato correcto.

    Retorna el diccionario del país si la fila es válida, o None si no lo es.
    Lanza ValueError con un mensaje descriptivo cuando detecta un problema.
    """
    nombre     = fila["nombre"].strip()
    continente = fila["continente"].strip()
    poblacion  = int(fila["poblacion"].strip())
    superficie = int(fila["superficie"].strip())

    if not nombre or not continente:
        raise ValueError("campo de texto vacío")
    if poblacion <= 0:
        raise ValueError(f"población inválida ({poblacion}): debe ser mayor a 0")
    if superficie <= 0:
        raise ValueError(f"superficie inválida ({superficie}): debe ser mayor a 0")

    return {
        "nombre":     nombre,
        "poblacion":  poblacion,
        "superficie": superficie,
        "continente": continente,
    }


def cargar_paises(ruta=RUTA_CSV):
    """
    Lee el archivo CSV y retorna una lista de diccionarios de países.

    Comportamiento:
    - Si el archivo no existe, retorna lista vacía e informa al usuario.
    - Si las columnas no coinciden con las requeridas, retorna lista vacía.
    - Las filas con formato inválido se omiten y se reportan individualmente.
    - Cualquier error inesperado de I/O es capturado y reportado.

    Retorna: list[dict]
    """
    paises = []

    if not os.path.exists(ruta):
        print(f"  ⚠ No se encontró '{ruta}'. Se iniciará con lista vacía.")
        return paises

    try:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Verificar encabezados
            if lector.fieldnames is None or not COLUMNAS_REQUERIDAS.issubset(
                set(lector.fieldnames)
            ):
                print("  ⚠ El CSV no tiene el formato correcto.")
                print(f"     Columnas requeridas: {', '.join(sorted(COLUMNAS_REQUERIDAS))}")
                return paises

            filas_invalidas = 0

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    pais = _validar_fila(fila, numero_fila)
                    paises.append(pais)
                except (ValueError, KeyError) as error:
                    filas_invalidas += 1
                    print(f"  ⚠ Fila {numero_fila} ignorada → {error}")

            if filas_invalidas > 0:
                print(f"  Se ignoraron {filas_invalidas} fila(s) con errores.")

    except OSError as error:
        print(f"  ✘ Error al leer el archivo '{ruta}': {error}")

    return paises


def guardar_paises(paises, ruta=RUTA_CSV):
    """
    Guarda la lista de países en el archivo CSV, sobreescribiendo su contenido.

    Parámetros:
        paises : lista de diccionarios de países.
        ruta   : ruta del archivo destino (por defecto RUTA_CSV).

    En caso de error de escritura, informa al usuario sin interrumpir el programa.
    """
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(paises)
    except OSError as error:
        print(f"  ✘ Error al guardar el archivo '{ruta}': {error}")
