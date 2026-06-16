# =============================================================================
# paises.py
# Módulo principal con toda la lógica de operaciones sobre países.
# Funciones: mostrar_menu, agregar, actualizar, buscar, filtrar, ordenar, estadísticas.
# =============================================================================

import unicodedata
import os
import questionary
from questionary import Choice

# =============================================================================
# FUNCIONES AUXILIARES DE CONSOLA
# =============================================================================

def limpiar_consola():
    """Limpia la pantalla según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def continuar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\n  Presioná Enter para continuar...")

# =============================================================================
# FUNCIONES AUXILIARES DE VALIDACIÓN
# =============================================================================

def pedir_entero_positivo(mensaje):
    """
    Solicita al usuario un número entero mayor a cero.
    Repite la solicitud hasta recibir un valor válido.
    Retorna el entero ingresado.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor <= 0:
                print("   ⚠ El valor debe ser mayor a 0. Intentá de nuevo.")
            else:
                return valor
        except ValueError:
            print("   ⚠ Ingresá solo números enteros positivos. Intentá de nuevo.")


def pedir_entero_no_negativo(mensaje):
    """
    Solicita al usuario un número entero mayor o igual a cero.
    Se utiliza para casos donde 0 representa "sin cambio".
    Retorna el entero ingresado.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor < 0:
                print("   ⚠ El valor no puede ser negativo. Intentá de nuevo.")
            else:
                return valor
        except ValueError:
            print("   ⚠ Ingresá solo números enteros. Intentá de nuevo.")


def pedir_texto_no_vacio(mensaje):
    while True:
        entrada = input(mensaje).strip()

        if not entrada:
            print("⚠ Este campo no puede estar vacío.")
            continue

        if not all(caracter.isalpha() or caracter.isspace() for caracter in entrada):
            print("⚠ Solo se permiten letras y espacios.")
            continue

        return entrada
    
def normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto.lower().strip())
        if unicodedata.category(c) != 'Mn'
    )

# =============================================================================
# FUNCIONES AUXILIARES DE VISUALIZACIÓN
# =============================================================================

def mostrar_pais(pais):
    """Muestra los datos de un único país en formato legible."""
    print(f"  • {pais['nombre']:<25} "
            f"Población: {pais['poblacion']:>15,}  "
            f"Superficie: {pais['superficie']:>12,} km²  "
            f"Continente: {pais['continente']}")


def mostrar_lista(paises):
    """
    Muestra una lista de países en formato de tabla.
    Si la lista está vacía, informa al usuario.
    """
    if not paises:
        print("  (No hay países para mostrar)")
        return

    print()
    print(f"  {'NOMBRE':<25} {'POBLACIÓN':>15}  {'SUPERFICIE (km²)':>16}  {'CONTINENTE'}")
    print("  " + "-" * 72)
    for pais in paises:
        print(f"  {pais['nombre']:<25} "
                f"{pais['poblacion']:>15,}  "
                f"{pais['superficie']:>16,}  "
                f"{pais['continente']}")
    print("  " + "-" * 72)
    print(f"  Total: {len(paises)} país/es encontrado/s")




# =============================================================================
# AGREGAR PAÍS
# =============================================================================

def agregar_pais(paises):
    """
    Solicita los datos de un nuevo país y lo agrega a la lista.

    Validaciones aplicadas:
    - Ningún campo puede estar vacío.
    - Población y superficie deben ser enteros positivos.
    - No se permiten países duplicados (comparación sin distinción de mayúsculas).
    """
    print("\n  ── Agregar nuevo país ──")

    nombre = pedir_texto_no_vacio("  Nombre del país: ")

    # Verificar duplicado (ignorar mayúsculas/minúsculas/acentos)
    if any(normalizar(p["nombre"]) == normalizar(nombre) for p in paises):
        print(f"  ⚠ Ya existe un país llamado '{nombre}'. No se puede duplicar.")
        return

    poblacion  = pedir_entero_positivo("  Población: ")
    superficie = pedir_entero_positivo("  Superficie (km²): ")
    continente = pedir_texto_no_vacio("  Continente: ")

    paises.append({
        "nombre":     nombre,
        "poblacion":  poblacion,
        "superficie": superficie,
        "continente": continente
    })
    print(f"\n  ✔ País '{nombre}' agregado correctamente.")


# =============================================================================
# ACTUALIZAR PAÍS
# =============================================================================

def actualizar_pais(paises):
    """
    Busca un país por nombre exacto (sin distinción de mayúsculas) y permite
    modificar su población y/o superficie.

    Reglas:
    - Ingresar 0 conserva el valor actual del campo.
    - El nombre y el continente no son modificables desde esta función.
    """
    print("\n  ── Actualizar país ──")

    if not paises:
        print("  ⚠ No hay países cargados.")
        return

    nombre = normalizar(pedir_texto_no_vacio("  Nombre del país a actualizar: "))

    for pais in paises:
        if normalizar(pais["nombre"]).lower() == nombre.lower():
            print(f"\n  País encontrado: {pais['nombre']}")
            print(f"    Población actual : {pais['poblacion']:,}")
            print(f"    Superficie actual: {pais['superficie']:,} km²\n")

            nueva_poblacion = pedir_entero_no_negativo(
                "  Nueva población (0 para mantener actual): "
            )
            if nueva_poblacion != 0:
                pais["poblacion"] = nueva_poblacion

            nueva_superficie = pedir_entero_no_negativo(
                "  Nueva superficie en km² (0 para mantener actual): "
            )
            if nueva_superficie != 0:
                pais["superficie"] = nueva_superficie

            print(f"\n  ✔ País '{pais['nombre']}' actualizado correctamente.")
            return

    print(f"  ⚠ No se encontró ningún país con el nombre '{nombre}'.")


# =============================================================================
# BUSCAR PAÍS
# =============================================================================

def buscar_pais(paises):
    """
    Busca países cuyo nombre contenga el texto ingresado.
    La búsqueda es parcial y no distingue mayúsculas de minúsculas.
    Muestra todos los resultados encontrados en formato de tabla.
    """
    print("\n  ── Buscar país por nombre ──")

    if not paises:
        print("  ⚠ No hay países cargados.")
        return

    termino = normalizar(pedir_texto_no_vacio("  Ingresá nombre (parcial o completo): ")).lower()

    resultados = [p for p in paises if termino in normalizar(p["nombre"].lower())]

    if resultados:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):")
        mostrar_lista(resultados)
    else:
        print(f"  ⚠ No se encontraron países que contengan '{termino}'.")


# =============================================================================
# FILTROS
# =============================================================================

def filtrar_por_continente(paises):
    """
    Filtra y muestra los países pertenecientes al continente indicado.
    Muestra previamente los continentes disponibles en el dataset.
    La comparación ignora mayúsculas y minúsculas.
    """
    print("\n  ── Filtrar por continente ──")

    if not paises:
        print("  ⚠ No hay países cargados.")
        return

    continentes_disponibles = sorted(set(p["continente"] for p in paises))
    print(f"  Continentes disponibles: {', '.join(continentes_disponibles)}\n")

    continente = pedir_texto_no_vacio("  Continente a filtrar: ")
    resultados = [p for p in paises if normalizar(p["continente"]).lower() == normalizar(continente).lower()]

    if resultados:
        print(f"\n  Países en '{continente.title()}':")
        mostrar_lista(resultados)
    else:
        print(f"  ⚠ No se encontraron países en el continente '{continente}'.")


def filtrar_por_poblacion(paises):
    """
    Filtra países cuya población esté dentro del rango [mínimo, máximo].
    Valida que el mínimo no supere al máximo antes de filtrar.
    """
    print("\n  ── Filtrar por rango de población ──")

    if not paises:
        print("  ⚠ No hay países cargados.")
        return

    print("  Ingresá el rango de población:")
    minimo = pedir_entero_positivo("    Mínimo: ")
    maximo = pedir_entero_positivo("    Máximo: ")

    if minimo > maximo:
        print("  ⚠ El mínimo no puede ser mayor que el máximo.")
        return

    resultados = [p for p in paises if minimo <= p["poblacion"] <= maximo]

    if resultados:
        print(f"\n  Países con población entre {minimo:,} y {maximo:,}:")
        mostrar_lista(resultados)
    else:
        print(f"  ⚠ No hay países con población entre {minimo:,} y {maximo:,}.")


def filtrar_por_superficie(paises):
    """
    Filtra países cuya superficie esté dentro del rango [mínimo, máximo] en km².
    Valida que el mínimo no supere al máximo antes de filtrar.
    """
    print("\n  ── Filtrar por rango de superficie ──")

    if not paises:
        print("  ⚠ No hay países cargados.")
        return

    print("  Ingresá el rango de superficie en km²:")
    minimo = pedir_entero_positivo("    Mínimo (km²): ")
    maximo = pedir_entero_positivo("    Máximo (km²): ")

    if minimo > maximo:
        print("  ⚠ El mínimo no puede ser mayor que el máximo.")
        return

    resultados = [p for p in paises if minimo <= p["superficie"] <= maximo]

    if resultados:
        print(f"\n  Países con superficie entre {minimo:,} km² y {maximo:,} km²:")
        mostrar_lista(resultados)
    else:
        print(f"  ⚠ No hay países con superficie entre {minimo:,} y {maximo:,} km².")


def menu_filtros(paises):
    """
    Submenú de filtros. Permite al usuario elegir el tipo de filtro a aplicar
    y volver al menú principal cuando lo desee.
    """
    while True:
        opcion = questionary.select(
            "Filtrar países por:",
            choices=[
                Choice("Continente",          value="1"),
                Choice("Rango de población",   value="2"),
                Choice("Rango de superficie",  value="3"),
                Choice("⬅ Volver al menú principal", value="0"),
            ]
        ).ask()

        match opcion:
            case "1":
                filtrar_por_continente(paises)
                continuar()
            case "2":
                filtrar_por_poblacion(paises)
                continuar()
            case "3":
                filtrar_por_superficie(paises)
                continuar()
            case "0":
                break


# =============================================================================
# ORDENAMIENTO — BUBBLE SORT
# =============================================================================

def ordenar_burbuja(paises, criterio, reverso=False):
    """
    Ordena la lista de países usando el algoritmo de burbuja.
    Parámetros:
        - criterio: clave del diccionario por la que ordenar ("nombre", "poblacion", "superficie")
        - reverso: False = ascendente, True = descendente
    """
    # Hacemos una copia para no modificar la lista original
    resultado = paises[:]
    n = len(resultado)

    for i in range(n - 1):
        for j in range(n - 1 - i):

            valor_actual   = resultado[j][criterio]
            valor_siguiente = resultado[j + 1][criterio]
            # Normalizar si son strings
            try:
                valor_actual = valor_actual.lower()
                valor_siguiente = valor_siguiente.lower()
            except AttributeError:
                pass

            # Decidimos si hay que intercambiar según el orden deseado
            if reverso:
                # Descendente: si el actual es MENOR que el siguiente, intercambiamos
                hay_que_intercambiar = valor_actual < valor_siguiente
            else:
                # Ascendente: si el actual es MAYOR que el siguiente, intercambiamos
                hay_que_intercambiar = valor_actual > valor_siguiente

            if hay_que_intercambiar:
                resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]

    return resultado


def ordenar_paises(paises):
    """
    Muestra un submenú para que el usuario elija el criterio y el sentido del
    ordenamiento, aplica Bubble Sort y presenta el resultado en tabla.
    No modifica la lista original de países.
    """
    print("\n  ── Ordenar países ──")

    if not paises:
        print("  ⚠ No hay países cargados.")
        return

    criterio = questionary.select(
        "Elegí el criterio de ordenamiento:",
        choices=[
            Choice("Nombre",     value="nombre"),
            Choice("Población",  value="poblacion"),
            Choice("Superficie", value="superficie"),
            Choice("⬅ Volver",  value="volver"),
        ]
    ).ask()

    if criterio == "volver":
        return

    reverso = questionary.select(
        "Elegí el orden:",
        choices=[
            Choice("Ascendente  (A→Z / menor a mayor)", value=False),
            Choice("Descendente (Z→A / mayor a menor)", value=True),
        ]
    ).ask()

    etiqueta = "descendente" if reverso else "ascendente"
    resultado = ordenar_burbuja(paises, criterio, reverso)

    print(f"\n  Países ordenados por '{criterio}' ({etiqueta}):")
    mostrar_lista(resultado)


# =============================================================================
# ESTADÍSTICAS
# =============================================================================

def _calcular_promedio(paises, campo):
    """
    Calcula el promedio de un campo numérico sobre todos los países.
    Función auxiliar privada (prefijo _).
    """
    total = 0
    for pais in paises:
        total += pais[campo]
    return total / len(paises)


def _contar_por_continente(paises):
    """
    Retorna un diccionario {continente: cantidad} con el recuento de países
    por continente. Función auxiliar privada (prefijo _).
    """
    conteo = {}
    for pais in paises:
        continente = pais["continente"]
        conteo[continente] = conteo.get(continente, 0) + 1
    return conteo


def mostrar_estadisticas(paises):
    """
    Calcula y muestra indicadores estadísticos del dataset:
    - País con mayor y menor población
    - Promedio de población
    - Promedio de superficie
    - Cantidad de países por continente
    """
    print("\n  --- Estadísticas generales ---")

    if not paises:
        print("   No hay países cargados para calcular estadísticas.")
        return
# Ordenamos una vez por cada criterio
    por_poblacion  = ordenar_burbuja(paises, "poblacion", reverso=False)  # ascendente
    por_superficie = ordenar_burbuja(paises, "superficie", reverso=False) # ascendente

    # El menor queda en el índice 0, el mayor en el último índice
    pais_menor_pob = por_poblacion[0]
    pais_mayor_pob = por_poblacion[-1]

    pais_menor_sup = por_superficie[0]
    pais_mayor_sup = por_superficie[-1]

    # Promedios: recorremos la lista original con un for
    total_poblacion = 0
    for pais in paises:
        total_poblacion += pais["poblacion"]
    promedio_pob = total_poblacion / len(paises)

    total_superficie = 0
    for pais in paises:
        total_superficie += pais["superficie"]
    promedio_sup = total_superficie / len(paises)

    # Cantidad de países por continente
    por_continente = {}
    for pais in paises:
        continente = pais["continente"]
        por_continente[continente] = por_continente.get(continente, 0) + 1
    

    # Mostrar resultados
    print()
    print("    ┌───────────────────────────────────────────────────────────────────────────────┐")
    print("    │                               ESTADÍSTICAS                                    │")
    print("    ├───────────────────────────────────────────────────────────────────────────────┤")
    print(f"    │  Total de países cargados : {len(paises):<34}                │")
    print("    ├───────────────────────────────────────────────────────────────────────────────┤")
    print("    │  POBLACIÓN                                                                    │")
    print(f"    │    Mayor : {pais_mayor_pob['nombre']:<20} {pais_mayor_pob['poblacion']:>20,}                          │")
    print(f"    │    Menor : {pais_menor_pob['nombre']:<20} {pais_menor_pob['poblacion']:>20,}                          │")
    print(f"    │    Promedio                        {promedio_pob:>25,.0f}                  │")
    print("    ├───────────────────────────────────────────────────────────────────────────────┤")
    print("    │  SUPERFICIE (km²)                                                             │")
    print(f"    │    Mayor : {pais_mayor_sup['nombre']:<20} {pais_mayor_sup['superficie']:>20,}                          │")
    print(f"    │    Menor : {pais_menor_sup['nombre']:<20} {pais_menor_sup['superficie']:>20,}                          │")
    print(f"    │    Promedio:                       {promedio_sup:>25,.0f}                  │")
    print("    ├───────────────────────────────────────────────────────────────────────────────┤")
    print("    │  PAÍSES POR CONTINENTE                                                        │")
    for continente, cantidad in sorted(por_continente.items()):
        barra = "█" * cantidad
        print(f"    │    {continente:<15} {barra:<20} {cantidad:>4} países                           │")
    print("    └───────────────────────────────────────────────────────────────────────────────┘")
