import csv
import os

# ==========================================
# 1. MANEJO DE ARCHIVOS CSV
# ==========================================

def cargar_desde_csv(ruta_archivo):
    """
    Lee el archivo CSV y devuelve una lista de diccionarios.
    Controla errores de formato y existencia del archivo.
    """
    lista_paises = []
    if not os.path.exists(ruta_archivo):
        print(f"\n[!] Advertencia: El archivo '{ruta_archivo}' no existe. Se iniciará con una lista vacía.")
        return lista_paises

    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            
            columnas_requeridas = {"nombre", "poblacion", "superficie", "continente"}
            if not lector.fieldnames or not columnas_requeridas.issubset(set(lector.fieldnames)):
                print("Error: El formato del archivo CSV es incorrecto (faltan columnas).")
                return lista_paises

            for nro_linea, fila in enumerate(lector, start=2):
                try:
                    if not all(fila.values()):
                        raise ValueError("Contiene campos vacíos")

                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"].strip()
                    }
                    lista_paises.append(pais)
                except (ValueError, TypeError) as e:
                    print(f"[!] Ignorando línea {nro_linea} del CSV por error de formato: {e}")
                    
    except Exception as e:
        print(f"Error crítico al leer el archivo: {e}")
        
    return lista_paises

def guardar_en_csv(ruta_archivo, lista_paises):
    """Guarda la lista de países en el archivo CSV."""
    try:
        with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            for pais in lista_paises:
                escritor.writerow(pais)
        return True
    except Exception as e:
        print(f"Error al guardar los datos en el archivo: {e}")
        return False

# ==========================================
# 2. VALIDACIONES DE ENTRADA
# ==========================================

def leer_string_no_vacio(mensaje):
    """Solicita un string por consola y valida que no esté vacío."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("Error: Este campo no puede quedar vacío. Intente de nuevo.")

def leer_entero_positivo(mensaje):
    """Solicita un número entero por consola y valida que sea mayor que cero."""
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit():
            numero = int(entrada)
            if numero > 0:
                return numero
            print("Error: El número debe ser mayor a 0.")
        else:
            print("Error: Debe ingresar un número entero válido.")

def leer_opcion_menu(mensaje, opciones_validas):
    """Valida que la opción seleccionada esté dentro de la lista permitida."""
    while True:
        entrada = input(mensaje).strip()
        if entrada in opciones_validas:
            return entrada
        print(f"Error: Opción inválida. Seleccione una de las siguientes: {', '.join(opciones_validas)}")

# ==========================================
# 3. OPERACIONES LÓGICAS (FILTROS/ESTADÍSTICAS)
# ==========================================

def buscar_por_nombre(lista_paises, nombre_buscado, exacta=False):
    """Busca países por nombre. Permite coincidencia exacta o parcial."""
    resultados = []
    nombre_buscado = nombre_buscado.lower().strip()
    
    for pais in lista_paises:
        nombre_pais = pais["nombre"].lower()
        if exacta and nombre_pais == nombre_buscado:
            resultados.append(pais)
        elif not exacta and nombre_buscado in nombre_pais:
            resultados.append(pais)
            
    return resultados

def filtrar_paises(lista_paises, criterio, valor_min=None, valor_max=None, continente=None):
    """Filtra la lista de países según el criterio seleccionado."""
    resultados = []
    for pais in lista_paises:
        if criterio == "continente" and continente:
            if pais["continente"].lower() == continente.lower().strip():
                resultados.append(pais)
        elif criterio == "poblacion" and valor_min is not None and valor_max is not None:
            if valor_min <= pais["poblacion"] <= valor_max:
                resultados.append(pais)
        elif criterio == "superficie" and valor_min is not None and valor_max is not None:
            if valor_min <= pais["superficie"] <= valor_max:
                resultados.append(pais)
    return resultados

def ordenar_paises(lista_paises, clave, descendente=False):
    """Ordena y devuelve una nueva lista según la clave y el orden indicados."""
    return sorted(lista_paises, key=lambda x: x[clave], reverse=descendente)

def calcular_estadisticas(lista_paises):
    """Calcula indicadores estadísticos sobre el dataset."""
    if not lista_paises:
        return None
        
    pais_mayor_pob = max(lista_paises, key=lambda x: x["poblacion"])
    pais_menor_pob = min(lista_paises, key=lambda x: x["poblacion"])
    
    total_pob = sum(p["poblacion"] for p in lista_paises)
    total_sup = sum(p["superficie"] for p in lista_paises)
    cantidad = len(lista_paises)
    
    frecuencia_continentes = {}
    for p in lista_paises:
        cont = p["continente"]
        frecuencia_continentes[cont] = frecuencia_continentes.get(cont, 0) + 1
        
    return {
        "mayor_poblacion": pais_mayor_pob,
        "menor_poblacion": pais_menor_pob,
        "promedio_poblacion": total_pob / cantidad,
        "promedio_superficie": total_sup / cantidad,
        "frecuencia_continentes": frecuencia_continentes
    }

# ==========================================
# 4. FUNCIONES DE INTERFAZ (VISTAS DE MENÚ)
# ==========================================

def mostrar_tabla_paises(lista):
    """Muestra de forma bonita y tabulada una lista de países."""
    if not lista:
        print("\n--> No se encontraron registros para mostrar.")
        return
    
    print("\n" + "-" * 75)
    print(f"{'Nombre':<20} | {'Población':<15} | {'Superficie (km²)':<18} | {'Continente':<15}")
    print("-" * 75)
    for p in lista:
        print(f"{p['nombre']:<20} | {p['poblacion']:<15,} | {p['superficie']:<18,} | {p['continente']:<15}")
    print("-" * 75)

def opcion_agregar_pais(paises):
    """Maneja el flujo completo para dar de alta un nuevo país."""
    print("\n--- AGREGAR PAÍS ---")
    nombre = leer_string_no_vacio("Nombre del país: ")
    
    if buscar_por_nombre(paises, nombre, exacta=True):
        print("Error: Ya existe un país registrado con ese nombre.")
        return
        
    poblacion = leer_entero_positivo("Cantidad de población: ")
    superficie = leer_entero_positivo("Superficie en km²: ")
    continente = leer_string_no_vacio("Continente: ")
    
    paises.append({
        "nombre": nombre, 
        "poblacion": poblacion, 
        "superficie": superficie, 
        "continente": continente
    })
    print(f"¡Éxito! '{nombre}' fue agregado correctamente en memoria.")

def opcion_actualizar_pais(paises):
    """Maneja el flujo para modificar la población y superficie de un país."""
    print("\n--- ACTUALIZAR DATOS ---")
    nombre = leer_string_no_vacio("Ingrese el nombre exacto del país a modificar: ")
    encontrados = buscar_por_nombre(paises, nombre, exacta=True)
    
    if not encontrados:
        print("Error: No se encontró ningún país con ese nombre.")
    else:
        pais_a_modificar = encontrados[0]
        print(f"Datos actuales -> Población: {pais_a_modificar['poblacion']:,} | Superficie: {pais_a_modificar['superficie']:,}")
        
        pais_a_modificar["poblacion"] = leer_entero_positivo("Nueva población: ")
        pais_a_modificar["superficie"] = leer_entero_positivo("Nueva superficie en km²: ")
        print(f"¡Datos de '{pais_a_modificar['nombre']}' actualizados con éxito!")

def opcion_buscar_pais(paises):
    """Pide el término de búsqueda y muestra los resultados."""
    print("\n--- BUSCAR PAÍS ---")
    nombre = leer_string_no_vacio("Ingrese el nombre (o parte de él): ")
    resultados = buscar_por_nombre(paises, nombre, exacta=False)
    mostrar_tabla_paises(resultados)

def ejecutar_submenue_filtros(paises):
    """Maneja la interfaz visual y lógica para la opción de filtrado."""
    print("\n--- FILTRAR PAÍSES ---")
    print("1. Por Continente\n2. Por Rango de Población\n3. Por Rango de Superficie")
    sub_op = leer_opcion_menu("Seleccione criterio (1-3): ", ["1", "2", "3"])
    
    if sub_op == "1":
        cont = leer_string_no_vacio("Ingrese el continente: ")
        res = filtrar_paises(paises, "continente", continente=cont)
    elif sub_op == "2":
        min_p = leer_entero_positivo("Población mínima: ")
        max_p = leer_entero_positivo("Población máxima: ")
        res = filtrar_paises(paises, "poblacion", valor_min=min_p, valor_max=max_p)
    else:
        min_s = leer_entero_positivo("Superficie mínima: ")
        max_s = leer_entero_positivo("Superficie máxima: ")
        res = filtrar_paises(paises, "superficie", valor_min=min_s, valor_max=max_s)
        
    mostrar_tabla_paises(res)

def ejecutar_submenue_ordenamientos(paises):
    """Maneja la interfaz visual y lógica para la opción de ordenamiento."""
    print("\n--- ORDENAR PAÍSES ---")
    print("Criterio:\n1. Nombre\n2. Población\n3. Superficie")
    crit_op = leer_opcion_menu("Seleccione (1-3): ", ["1", "2", "3"])
    
    print("Sentido:\n1. Ascendente\n2. Descendente")
    sent_op = leer_opcion_menu("Seleccione (1-2): ", ["1", "2"])
    
    claves = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    descendente = True if sent_op == "2" else False
    
    lista_ordenada = ordenar_paises(paises, claves[crit_op], descendente)
    mostrar_tabla_paises(lista_ordenada)

def mostrar_estadisticas_generales(paises):
    """Muestra los indicadores estadísticos formateados en consola."""
    print("\n--- ESTADÍSTICAS GENERALES ---")
    est = calcular_estadisticas(paises)
    if not est:
        print("No hay suficientes datos para generar estadísticas.")
    else:
        print(f"• País con MAYOR población: {est['mayor_poblacion']['nombre']} ({est['mayor_poblacion']['poblacion']:,} hab.)")
        print(f"• País con MENOR población: {est['menor_poblacion']['nombre']} ({est['menor_poblacion']['poblacion']:,} hab.)")
        print(f"• Promedio de población global: {est['promedio_poblacion']:,.2f} habitantes")
        print(f"• Promedio de superficie global: {est['promedio_superficie']:,.2f} km²")
        print("\n• Cantidad de países por continente:")
        for cont, cant in est["frecuencia_continentes"].items():
            print(f"  - {cont}: {cant}")
