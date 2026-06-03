# =============================================================================
# main.py
# Punto de entrada del programa. Gestiona el menú principal y coordina
# las llamadas a los módulos de lógica y manejo de archivos.
# =============================================================================

from archivo_csv import cargar_paises, guardar_paises
from paises import (mostrar_menu,
    mostrar_lista,
    agregar_pais,
    actualizar_pais,
    buscar_pais,
    menu_filtros,
    ordenar_paises,
    mostrar_estadisticas
)


# =============================================================================
# MENÚ PRINCIPAL
# =============================================================================


def main():
    """
    Función principal. Carga los datos al inicio, muestra el menú en bucle
    y guarda los cambios automáticamente tras operaciones de escritura.
    """
    print()
    print("  ══════════════════════════════════════════")
    print("      SISTEMA DE GESTIÓN DE PAÍSES          ")
    print("  ══════════════════════════════════════════")

    # Cargar datos desde el CSV al iniciar
    paises = cargar_paises()
    print(f"   {len(paises)} países cargados desde el archivo.")

    while True:
        mostrar_menu()
        opcion = input("\n  Seleccioná una opción: ").strip()

        match opcion: 
            case "1":
                agregar_pais(paises)
                guardar_paises(paises)

            case "2":
                actualizar_pais(paises)
                guardar_paises(paises)

            case "3":
                buscar_pais(paises)

            case "4":
                menu_filtros(paises)

            case "5":
                ordenar_paises(paises)

            case "6":
                mostrar_estadisticas(paises)

            case "7":
                print("\n  --- Todos los países ---")
                mostrar_lista(paises)

            case "8":
                print("\n ¡Hasta luego, Gracias por Visitarnos!\n")
                break

            case _:
                print("\n  Opción inválida. Ingresá un número del 0 al 7.")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    main()