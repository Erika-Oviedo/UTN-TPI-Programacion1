# =============================================================================
# archivo_csv.py
# Módulo para lectura y escritura del archivo CSV de países.
# =============================================================================

import csv
import os

RUTA_CSV = "datos.csv"


def cargar_paises(ruta=RUTA_CSV):
    """
    Lee el archivo CSV y retorna una lista de diccionarios.
    Cada diccionario representa un país con sus 4 campos.
    Ignora filas con formato inválido e informa al usuario.
    """
    paises = []

    if not os.path.exists(ruta):
        print(f"  No se encontró el archivo '{ruta}'. Se iniciará con lista vacía.")
        return paises

    try:
        with open(ruta, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)

            # Verificar que el CSV tenga las columnas correctas
            columnas_requeridas = {"nombre", "poblacion", "superficie", "continente"}
            if lector.fieldnames is None or not columnas_requeridas.issubset(set(lector.fieldnames)):
                print("Error: El archivo CSV no tiene el formato correcto.")
                print(f"   Columnas requeridas: {columnas_requeridas}")
                return paises

            filas_invalidas = 0
            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    nombre = fila["nombre"].strip()
                    continente = fila["continente"].strip()
                    poblacion = int(fila["poblacion"].strip())
                    superficie = int(fila["superficie"].strip())

                    # Validar que no haya campos vacíos ni valores negativos
                    if not nombre or not continente:
                        raise ValueError("Campo de texto vacío")
                    if poblacion <= 0 or superficie <= 0:
                        raise ValueError("Valor numérico debe ser mayor a 0")

                    paises.append({
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente
                    })

                except (ValueError, KeyError) as error:
                    filas_invalidas += 1
                    print(f"  Fila {numero_fila} ignorada por formato inválido → {error}")

            if filas_invalidas > 0:
                print(f"  Se ignoraron {filas_invalidas} fila(s) con errores.")

    except Exception as error:
        print(f" Error inesperado al leer el archivo: {error}")

    return paises


def guardar_paises(paises, ruta=RUTA_CSV):
    """
    Guarda la lista de diccionarios de países en el archivo CSV.
    Sobreescribe el archivo existente con los datos actualizados.
    """
    try:
        with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(paises)

    except Exception as error:
        print(f" Error al guardar el archivo: {error}")