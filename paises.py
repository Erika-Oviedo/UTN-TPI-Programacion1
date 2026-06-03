# =============================================================================
# paises.py
# Módulo principal con toda la lógica de operaciones sobre países.
# Funciones: mostrar_menu, agregar, actualizar, buscar, filtrar, ordenar, estadísticas.
# =============================================================================
# =============================================================================
# FUNCIONES AUXILIARES DE VISUALIZACIÓN
# =============================================================================
def mostrar_menu():
    """Imprime el menú principal de opciones en consola."""
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║      SISTEMA DE GESTIÓN DE PAÍSES        ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║  1. Agregar un país                      ║")
    print("  ║  2. Actualizar población / superficie    ║")
    print("  ║  3. Buscar país por nombre               ║")
    print("  ║  4. Filtrar países                       ║")
    print("  ║  5. Ordenar países                       ║")
    print("  ║  6. Ver estadísticas                     ║")
    print("  ║  7. Mostrar todos los países             ║")
    print("  ║  8. Salir                                ║")
    print("  ╚══════════════════════════════════════════╝")


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


def pedir_entero_positivo(mensaje):
    """
    Pide al usuario un número entero positivo.
    Repite la solicitud hasta recibir un valor válido.
    Retorna el entero ingresado.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor < 0:
                print("   El valor debe ser mayor a 0. Intentá de nuevo.")
            else:
                return valor
        except ValueError:
            print("   Ingresá solo números enteros. Intentá de nuevo.")


def pedir_texto_no_vacio(mensaje):
    """
    Pide al usuario un texto no vacío.
    Repite la solicitud hasta recibir algo.
    Retorna el texto en formato limpio (strip).
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("   Este campo no puede estar vacío. Intentá de nuevo.")


# =============================================================================
# AGREGAR PAÍS
# =============================================================================

def agregar_pais(paises):
    """
    Solicita los datos de un nuevo país al usuario y lo agrega a la lista.
    Valida que no haya campos vacíos, que los números sean positivos
    y que no exista un país con el mismo nombre (sin distinguir mayúsculas).
    """
    print("\n  --- Agregar nuevo país ---")

    # Pedir y validar nombre
    nombre = pedir_texto_no_vacio("  Nombre del país: ")

    # Verificar si ya existe
    if any(p["nombre"].lower() == nombre.lower() for p in paises):
        print(f"   Ya existe un país llamado '{nombre}'. No se puede duplicar.")
        return

    # Pedir y validar resto de datos
    poblacion  = pedir_entero_positivo("  Población: ")
    superficie = pedir_entero_positivo("  Superficie (km²): ")
    continente = pedir_texto_no_vacio("  Continente: ")

    # Crear el diccionario y agregarlo
    nuevo_pais = {
        "nombre":     nombre,
        "poblacion":  poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(nuevo_pais)
    print(f"\n   País '{nombre}' agregado correctamente.")


# =============================================================================
# ACTUALIZAR PAÍS
# =============================================================================

def actualizar_pais(paises):
    """
    Busca un país por nombre exacto (sin distinguir mayúsculas)
    y permite actualizar su población y superficie.
    No modifica nombre ni continente.
    """
    print("\n  --- Actualizar país ---")

    if not paises:
        print("   No hay países cargados.")
        return

    nombre = pedir_texto_no_vacio("  Nombre del país a actualizar: ")

    # Buscar coincidencia exacta (ignorando mayúsculas)
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            print(f"\n  País encontrado: {pais['nombre']}")
            print(f"    Población actual : {pais['poblacion']:,}")
            print(f"    Superficie actual: {pais['superficie']:,} km²")
            print()

            nueva_poblacion  = pedir_entero_positivo("  Nueva población (0 cero para mantener actual): ")
            if nueva_poblacion != 0:
                pais["poblacion"] = nueva_poblacion
                
            nueva_superficie = pedir_entero_positivo("  Nueva superficie en km² (0 cero para mantener actual): ")
            if nueva_superficie != 0:
                pais["superficie"] = nueva_superficie


            print(f"\n   País '{pais['nombre']}' actualizado correctamente.")
            return

    print(f"   No se encontró ningún país con el nombre '{nombre}'.")


# =============================================================================
# BUSCAR PAÍS
# =============================================================================

def buscar_pais(paises):
    """
    Busca países cuyo nombre contenga el texto ingresado
    (búsqueda parcial, sin distinguir mayúsculas ni minúsculas).
    Muestra todos los resultados encontrados.
    """
    print("\n  --- Buscar país por nombre ---")

    if not paises:
        print("   No hay países cargados.")
        return

    termino = pedir_texto_no_vacio("  Ingresá nombre (parcial o completo): ").lower()

    resultados = [p for p in paises if termino in p["nombre"].lower()]

    if resultados:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):")
        mostrar_lista(resultados)
    else:
        print(f"   No se encontraron países que contengan '{termino}'.")


# =============================================================================
# FILTROS
# =============================================================================

def filtrar_por_continente(paises):
    """
    Filtra y muestra todos los países que pertenecen al continente ingresado.
    La comparación ignora mayúsculas/minúsculas.
    """
    print("\n  --- Filtrar por continente ---")

    if not paises:
        print("   No hay países cargados.")
        return

    # Mostrar continentes disponibles
    continentes_disponibles = sorted(set(p["continente"] for p in paises))
    print(f"  Continentes disponibles: {', '.join(continentes_disponibles)}")

    continente = pedir_texto_no_vacio("  Continente a filtrar: ")

    resultados = [p for p in paises if p["continente"].lower() == continente.lower()]

    if resultados:
        print(f"\n  Países en '{continente.title()}':")
        mostrar_lista(resultados)
    else:
        print(f"  No se encontraron países en el continente '{continente}'.")


def filtrar_por_poblacion(paises):
    """
    Filtra países cuya población esté dentro de un rango [mínimo, máximo].
    Valida que el mínimo no sea mayor que el máximo.
    """
    print("\n  --- Filtrar por rango de población ---")

    if not paises:
        print("  No hay países cargados.")
        return

    print("  Ingresá el rango de población:")
    minimo = pedir_entero_positivo("    Mínimo: ")
    maximo = pedir_entero_positivo("    Máximo: ")

    if minimo > maximo:
        print("  El mínimo no puede ser mayor que el máximo.")
        return

    resultados = [p for p in paises if minimo <= p["poblacion"] <= maximo]

    if resultados:
        print(f"\n  Países con población entre {minimo:,} y {maximo:,}:")
        mostrar_lista(resultados)
    else:
        print(f"  No hay países con población entre {minimo:,} y {maximo:,}.")


def filtrar_por_superficie(paises):
    """
    Filtra países cuya superficie esté dentro de un rango [mínimo, máximo] en km².
    Valida que el mínimo no sea mayor que el máximo.
    """
    print("\n  --- Filtrar por rango de superficie ---")

    if not paises:
        print("   No hay países cargados.")
        return

    print("  Ingresá el rango de superficie en km²:")
    minimo = pedir_entero_positivo("    Mínimo: ")
    maximo = pedir_entero_positivo("    Máximo: ")

    if minimo > maximo:
        print("   El mínimo no puede ser mayor que el máximo.")
        return

    resultados = [p for p in paises if minimo <= p["superficie"] <= maximo]

    if resultados:
        print(f"\n  Países con superficie entre {minimo:,} km² y {maximo:,} km²:")
        mostrar_lista(resultados)
    else:
        print(f"   No hay países con superficie entre {minimo:,} y {maximo:,} km².")


def menu_filtros(paises):
    """
    Submenú que agrupa todas las opciones de filtrado disponibles.
    """
    print("\n  ╔══════════════════════════════╗")
    print("    ║       FILTRAR PAÍSES         ║")
    print("    ╠══════════════════════════════╣")
    print("    ║  1. Por continente           ║")
    print("    ║  2. Por rango de población   ║")
    print("    ║  3. Por rango de superficie  ║")
    print("    ║  0. Volver al menú principal ║")
    print("    ╚══════════════════════════════╝")

    opcion = input("  Elegí una opción: ").strip()

    if opcion == "1":
        filtrar_por_continente(paises)
    elif opcion == "2":
        filtrar_por_poblacion(paises)
    elif opcion == "3":
        filtrar_por_superficie(paises)
    elif opcion == "0":
        return
    else:
        print("   Opción inválida.")


# =============================================================================
# ORDENAMIENTO
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
    Ordena y muestra los países según el criterio elegido por el usuario
    (nombre, población o superficie) en orden ascendente o descendente.
    No modifica la lista original.
    """
    print("\n  --- Ordenar países ---")

    if not paises:
        print("   No hay países cargados.")
        return

    print("  Ordenar por:")
    print("    1. Nombre")
    print("    2. Población")
    print("    3. Superficie")
    criterio_input = input("  Elegí criterio: ").strip()

    criterios = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    if criterio_input not in criterios:
        print("   Criterio inválido.")
        return

    criterio = criterios[criterio_input]

    print("\n  Orden:")
    print("    1. Ascendente  (A→Z / menor a mayor)")
    print("    2. Descendente (Z→A / mayor a menor)")
    orden_input = input("  Elegí orden: ").strip()

    if orden_input == "1":
        reverso = False
        etiqueta_orden = "ascendente"
    elif orden_input == "2":
        reverso = True
        etiqueta_orden = "descendente"
    else:
        print("   Opción de orden inválida.")
        return

    resultado = ordenar_burbuja(paises, criterio, reverso)

    print(f"\n  Países ordenados por '{criterio}' ({etiqueta_orden}):")
    mostrar_lista(resultado)


# =============================================================================
# ESTADÍSTICAS
# =============================================================================

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
    print(f"    │    Promedio                        {promedio_sup:>25,.0f}                  │")
    print("    ├───────────────────────────────────────────────────────────────────────────────┤")
    print("    │  PAÍSES POR CONTINENTE                                                        │")
    for continente, cantidad in sorted(por_continente.items()):
        barra = "█" * cantidad
        print(f"    │    {continente:<15} {barra:<20} {cantidad:>4} países                           │")
    print("    └───────────────────────────────────────────────────────────────────────────────┘")
