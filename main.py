# Trabajo Practico Integrador
# Programación I
# Integrantes: Rodriguez Fabiana / Oviedo Erika

from funciones import *
# Importar funciones


RUTA_CSV = "paises.csv"

def menu_principal():
    # Cargar los datos al iniciar el programa
    paises = cargar_desde_csv(RUTA_CSV)
    
    while True:
        print("\n========================================")
        print("      SISTEMA DE GESTIÓN DE PAÍSES      ")
        print("========================================")
        print("1. Mostrar todos los países")
        print("2. Agregar un nuevo país")
        print("3. Actualizar población y superficie")
        print("4. Buscar país por nombre")
        print("5. Filtrar países")
        print("6. Ordenar países")
        print("7. Ver estadísticas generales")
        print("8. Guardar y Salir")
        print("========================================")
        
        opcion = leer_opcion_menu("Seleccione una opción (1-8): ", [str(i) for i in range(1, 9)])
        
        if opcion == "1":
            mostrar_tabla_paises(paises)
        elif opcion == "2":
            opcion_agregar_pais(paises)
        elif opcion == "3":
            opcion_actualizar_pais(paises)
        elif opcion == "4":
            opcion_buscar_pais(paises)
        elif opcion == "5":
            ejecutar_submenue_filtros(paises)
        elif opcion == "6":
            ejecutar_submenue_ordenamientos(paises)
        elif opcion == "7":
            mostrar_estadisticas_generales(paises)
        elif opcion == "8":
            print("\nGuardando cambios en el archivo CSV...")
            if guardar_en_csv(RUTA_CSV, paises):
                print("¡Datos guardados con éxito! Que tengas un excelente día.")
            else:
                print("Atención: No se pudieron salvar los cambios de esta sesión.")
            break

if __name__ == "__main__":
    menu_principal()
