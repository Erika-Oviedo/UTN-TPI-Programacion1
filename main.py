# =============================================================================
# main.py
# Punto de entrada del programa. Gestiona el menú principal y coordina
# las llamadas a los módulos de lógica (paises.py) y persistencia (archivo_csv.py).
# =============================================================================

import questionary

from archivo_csv import cargar_paises, guardar_paises
from paises import (
    limpiar_consola,
    continuar,
    mostrar_lista,
    agregar_pais,
    actualizar_pais,
    buscar_pais,
    menu_filtros,
    ordenar_paises,
    mostrar_estadisticas,
)

# =============================================================================
# CONSTANTES DEL MENÚ
# =============================================================================

OPCIONES_MENU = [
    questionary.Choice("Agregar país",           value="1"),
    questionary.Choice("Actualizar país",         value="2"),
    questionary.Choice("Buscar país",             value="3"),
    questionary.Choice("Filtrar países",          value="4"),
    questionary.Choice("Ordenar países",          value="5"),
    questionary.Choice("Ver estadísticas",        value="6"),
    questionary.Choice("Mostrar todos los países",value="7"),
    questionary.Choice("Salir",                   value="8"),
]


# =============================================================================
# MENÚ PRINCIPAL
# =============================================================================

def mostrar_bienvenida(cantidad_paises):
    """Muestra el encabezado del sistema al iniciar."""
    print()
    print("  ══════════════════════════════════════════════")
    print("       SISTEMA DE GESTIÓN DE PAÍSES             ")
    print("        Programación 1 — UTN FRM                  ")
    print("  ══════════════════════════════════════════════")
    print(f"   ✔ {cantidad_paises} países cargados desde el archivo.\n")


def main():
    """
    Función principal del programa.

    Flujo:
        1. Carga el dataset desde el CSV al iniciar.
        2. Presenta el menú interactivo en bucle.
        3. Guarda automáticamente los cambios después de cada operación de escritura.
        4. Termina cuando el usuario elige la opción 'Salir'.
    """
    paises = cargar_paises()

    while True:
        limpiar_consola()
        mostrar_bienvenida(len(paises))
        
        opcion = questionary.select(
            "Seleccioná una opción:",
            choices=OPCIONES_MENU,
        ).ask()

        match opcion:
            case "1":
                agregar_pais(paises)
                guardar_paises(paises)
                continuar()

            case "2":
                actualizar_pais(paises)
                guardar_paises(paises)
                continuar()

            case "3":
                buscar_pais(paises)
                continuar()

            case "4":
                menu_filtros(paises)

            case "5":
                ordenar_paises(paises)
                continuar()

            case "6":
                mostrar_estadisticas(paises)
                continuar()

            case "7":
                print("\n  ── Todos los países ──")
                mostrar_lista(paises)
                continuar()

            case "8":
                print("\n  ¡Hasta luego! Gracias por usar el sistema.\n")
                break

            case _:
                print("\n  ⚠ Opción inválida.")
                continuar()


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    main()
