# UTN-TPI-Programacion1
#  Sistema de Gestión de Países

Trabajo Práctico Integrador — Programación 1  
Aplicación de consola en Python para gestionar información sobre países del mundo.

---

##  Estructura del proyecto

```
tp-paises/
├── main.py          # Punto de entrada y menú principal
├── paises.py        # Lógica de negocio (agregar, buscar, filtrar, etc.)
├── archivo_csv.py   # Lectura y escritura del CSV
├── datos.csv        # Dataset con 30 países de ejemplo
└── README.md        # Este archivo
```

---

## ▶ Cómo ejecutar el programa

**Requisitos:** Python 3.x instalado.

```bash
# Clonar el repositorio
git clone https://github.com/usuario/tp-paises.git
cd tp-paises

# Ejecutar el programa
python main.py
```

No se requieren librerías externas. Solo se usa la librería estándar de Python (`csv`, `os`).

---

##  Funcionalidades

| Opción | Descripción |
|--------|-------------|
| 1 | Agregar un país (con validaciones) |
| 2 | Actualizar población y superficie |
| 3 | Buscar país por nombre (parcial o exacto) |
| 4 | Filtrar por continente / población / superficie |
| 5 | Ordenar por nombre, población o superficie (asc/desc) |
| 6 | Ver estadísticas del dataset |
| 7 | Mostrar todos los países |
| 0 | Salir |

---

##  Ejemplos de uso

### Agregar un país
```
Seleccioná una opción: 1

  --- Agregar nuevo país ---
  Nombre del país: Venezuela
  Población: 28200000
  Superficie (km²): 916445
  Continente: América

   País 'Venezuela' agregado correctamente.
```

### Buscar por nombre
```
Seleccioná una opción: 3

  --- Buscar país por nombre ---
  Ingresá nombre (parcial o completo): arg

  NOMBRE                     POBLACIÓN     SUPERFICIE (km²)  CONTINENTE
  ────────────────────────────────────────────────────────────────────────
  Argentina               45,376,763        2,780,400  América
  Total: 1 país/es encontrado/s
```

### Filtrar por continente
```
Seleccioná una opción: 4 → 1

  Continentes disponibles: África, América, Asia, Europa, Oceanía
  Continente a filtrar: Europa

  Países en 'Europa':
  NOMBRE                     POBLACIÓN     SUPERFICIE (km²)  CONTINENTE
  ────────────────────────────────────────────────────────────────────────
  Alemania                83,149,300          357,022  Europa
  España                  47,431,256          505,990  Europa
  ...
```

### Estadísticas
```
Seleccioná una opción: 6

  ┌──────────────────────────────────────────────────────────┐
  │                    ESTADÍSTICAS                          │
  ├──────────────────────────────────────────────────────────┤
  │  Total de países cargados : 30                           │
  │  POBLACIÓN                                               │
  │    Mayor : China                    1,412,600,000        │
  │    Menor : Nueva Zelanda                5,084,300        │
  │    Promedio                           159,624,000        │
  ...
```

---

##  Formato del CSV

```csv
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
```

- `nombre`: string, no vacío
- `poblacion`: entero positivo
- `superficie`: entero positivo (km²)
- `continente`: string, no vacío

---

##  Integrantes

| Nombre | Responsabilidades |
|--------|-------------------|
| [Fabiana           1] | archivo_csv.py · agregar · actualizar · ordenar · README |
| [Erika Oviedo      2] | main.py · buscar · filtros · estadísticas · informe PDF |

---

##  Links

- 📹 **Video demostrativo:** [insertar link]
- 📄 **Informe PDF:** [insertar link o adjuntar en el repositorio]