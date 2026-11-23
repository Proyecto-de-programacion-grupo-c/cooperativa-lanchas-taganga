# Casos de verificación – Incremento 6

Requisitos: 12 (cargar las lanchas desde un archivo), 13 (cargar los pasajeros desde un archivo) y 14 (el menú completo).
Cada caso se comprueba ejecutando `user_interface.py` desde la carpeta del proyecto y eligiendo la opción 6. Los archivos están en la carpeta `datos/`.

## Archivos de datos

| Archivo | Contenido | Para qué sirve |
|---|---|---|
| `lanchas.csv` | El archivo de lanchas del enunciado: 2 líneas válidas y 5 inválidas | Las causas para descartar una lancha |
| `pasajeros.csv` | El archivo de pasajeros del enunciado: 9 líneas válidas y 5 inválidas | Las causas para descartar un día |
| `lanchas_completas.csv` y `pasajeros_completos.csv` | Gaviota, Estrella de Mar, Caracola y Perla Negra, con los pasajeros de los ejemplos del enunciado | Cargar todo y comprobar los informes y el requisito 11 sin teclear |
| `lanchas_excel.csv` y `pasajeros_excel.csv` | Con BOM y fin de línea de Windows (como los guarda Excel), espacios alrededor de los campos, líneas vacías, campos vacíos y campos de más | Los casos que no están en el enunciado |
| `lanchas_latin1.csv` | Un archivo guardado en Latin-1, no en UTF-8 | Archivo con otra codificación |
| `solo_encabezado.csv` y `vacio.csv` | Solo la línea del encabezado, y ninguna línea | Archivos sin datos |

## Requisito 12. Cargar las lanchas

| Caso | Se teclea | Salida esperada | Qué prueba |
|---|---|---|---|
| A01 | `datos/lanchas.csv` | `Línea 4 descartada. La lancha debe ofrecer al menos un cupo por día` · `Línea 5 descartada. La línea no tiene cinco campos` · `Línea 6 descartada. Los cupos por día deben ser un número entero` · `Línea 7 descartada. Ya existe una lancha con ese nombre` · `Línea 8 descartada. La fecha no es válida` · `Lanchas cargadas: 2` | Ejemplo del enunciado: cada causa, en el mismo orden que al crear desde el teclado; la carga sigue después de cada línea mala |
| A03 | `datos/no_existe.csv` | `El archivo no existe`; **no** pide la ruta del archivo de pasajeros | Archivo de lanchas inexistente |
| A05 | Con la Caracola creada desde el teclado, opción 6 | `La carga solo se hace con el programa sin lanchas`; **no** pide ninguna ruta | Programa con lanchas |
| A06 | Una carga completa y después la opción 6 otra vez | `La carga solo se hace con el programa sin lanchas`; la Gaviota sigue con 5 días | Una segunda carga no duplica los días |
| A09 | `datos/lanchas_latin1.csv` | `El archivo no está guardado en UTF-8`; ninguna lancha cargada | Codificación distinta (sin el mensaje en inglés de Python) |
| A13 | `datos` (una carpeta) | `El archivo no existe` | La ruta no es de un archivo |

## Requisito 13. Cargar los pasajeros

| Caso | Se teclea | Salida esperada | Qué prueba |
|---|---|---|---|
| A02 | `datos/lanchas.csv` y `datos/pasajeros.csv`; después el informe de la Gaviota y el de la Estrella de Mar | `Línea 10 descartada. Los pasajeros van de 0 a 60` · `Línea 12 descartada. No hay una lancha con ese nombre` · `Línea 13 descartada. Los pasajeros van de 0 a 120` · `Línea 14 descartada. Los pasajeros deben ser un número entero` · `Línea 15 descartada. La línea no tiene dos campos` · `Días cargados: 9`; la Gaviota con 432 pasajeros totales y desviación 30.02, y la Estrella de Mar con 165 y 68.75 % | Ejemplo del enunciado; cada línea agrega el día siguiente de su lancha, aunque las líneas de las dos lanchas vengan mezcladas |
| A04 | `datos/lanchas.csv` y `datos/no_existe.csv`; después el informe de la Gaviota | `Lanchas cargadas: 2` · `El archivo no existe` · `La lancha no tiene días registrados` | Las lanchas se quedan, sin días |
| A07 | `datos/lanchas_completas.csv` y `datos/pasajeros_completos.csv`; después la opción 5 | `Lanchas cargadas: 4` · `Días cargados: 10` · más alto `Gaviota, con 72.0 %` · más bajo `Caracola, con 65.0 %`; sin líneas descartadas | Carga completa que alimenta el requisito 11 |
| A14 | Carga completa; después la opción 2 con la Caracola | `Pasajeros del 2026-11-02` | Después de cargar, el registro sigue desde el teclado |
| A15 | Carga completa; después se crea una Gaviota desde el teclado | `Ya existe una lancha con ese nombre` | Las lanchas cargadas cuentan para los duplicados |

## Casos fuera del enunciado (archivos guardados desde Excel)

| Caso | Se teclea | Salida esperada | Qué prueba |
|---|---|---|---|
| A08 | `datos/lanchas_excel.csv` y `datos/pasajeros_excel.csv`; después el informe de la Gaviota | Lanchas: las líneas 3 y 4 (vacía y con espacios) se saltan sin aviso · `Línea 5 descartada. El nombre no puede estar vacío` · `Línea 6 descartada. La línea no tiene cinco campos` (tiene seis) · `Lanchas cargadas: 1`. Pasajeros: `Línea 4 descartada. La línea no tiene dos campos` (tres) · `Línea 5 descartada. No hay una lancha con ese nombre` (nombre vacío) · `Línea 6 descartada. Los pasajeros deben ser un número entero` (vacío) · `Días cargados: 1`; informe con `Lancha: Gaviota` y 96 pasajeros | BOM, fin de línea `\r\n`, espacios alrededor de los campos (`  Gaviota  ; 120 `), líneas vacías, campos vacíos y campos de más |
| A10 | `datos/solo_encabezado.csv` dos veces | `Lanchas cargadas: 0` · `Días cargados: 0` | Archivo sin datos |
| A11 | `datos/vacio.csv` dos veces | `Lanchas cargadas: 0` · `Días cargados: 0` | Archivo sin ninguna línea, ni siquiera el encabezado |
| A12 | `"datos/lanchas_completas.csv"` (entre comillas) y `  datos/pasajeros_completos.csv  ` | `Lanchas cargadas: 4` · `Días cargados: 10` | Ruta pegada con "Copiar como ruta de acceso" de Windows |

## Requisito 14. El menú completo

| Caso | Se teclea | Salida esperada | Qué prueba |
|---|---|---|---|
| C26 | 8 | `La opción no es válida` y vuelve el menú | Número fuera de rango |
| C27 | dos | `La opción no es válida` | Texto |
| C28 | *(vacío)* | `La opción no es válida` | Entrada vacía |
| C29 | 0 | `La opción no es válida` | Frontera inferior |
| — | Las opciones 1 a 6 | Cada una atiende su requisito y después vuelve el menú | Ver los incrementos 1 a 6 |
| A16 | 7 | El programa termina sin errores | Salir |

## Traza de `cargar_pasajeros("datos/pasajeros.csv")` (líneas 9 a 15)

Antes de la línea 9, la Gaviota tiene 3 días (96, 54, 48) y la Estrella de Mar 3 (27, 36, 45).

| `índice` | Línea | Contenido | Campos | ¿Hay lancha? | Resultado |
|---|---|---|---|---|---|
| 8 | 9 | `Gaviota;120` | 2 | Sí | La Gaviota pasa a 5 días (la línea 8 le dio el cuarto, 114) |
| 9 | 10 | `Estrella de Mar;-1` | 2 | Sí | Descartada: `Los pasajeros van de 0 a 60` (sigue con 3 días) |
| 10 | 11 | `Estrella de Mar;57` | 2 | Sí | La Estrella de Mar pasa a 4 días |
| 11 | 12 | `Sirena;30` | 2 | No (Sirena se descartó al cargar las lanchas) | Descartada: `No hay una lancha con ese nombre` |
| 12 | 13 | `Gaviota;121` | 2 | Sí | Descartada: `Los pasajeros van de 0 a 120` |
| 13 | 14 | `Gaviota;noventa` | 2 | Sí | Descartada: `Los pasajeros deben ser un número entero` |
| 14 | 15 | `Estrella de Mar` | 1 | — | Descartada: `La línea no tiene dos campos` |

Al final, `contar_días_registrados_en_total()` = 5 + 4 = **9**.
