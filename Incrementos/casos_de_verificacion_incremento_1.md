# Casos de verificación – Incremento 1

Requisitos: 1 (crear una lancha), 2 (registrar los pasajeros del día siguiente), 10 (buscar por nombre) y 14 parcial (menú con las opciones 1, 2 y 7).
Cada caso se comprueba ejecutando `user_interface.py` y tecleando los datos en orden. Después de cada opción se pulsa Enter para volver al menú, y al final se teclea `7` para salir.

## Requisito 1. Crear una lancha

| Caso | Se teclea (opción 1) | Salida esperada | Qué prueba |
|---|---|---|---|
| C01 | Caracola · 40 · 2026 · 11 · 1 | `Lancha Caracola creada, sin días registrados` | Camino válido |
| C02 | *(vacío)* · 40 · 2026 · 11 · 1 | `El nombre no puede estar vacío` | Nombre vacío |
| C03 | `   ` · 40 · 2026 · 11 · 1 | `El nombre no puede estar vacío` | Solo espacios = vacío (`strip`) |
| C04 | Caracola · cuarenta · 2026 · 11 · 1 | `Los cupos por día deben ser un número entero` | Cupos no enteros, mensaje en español |
| C05 | Caracola · 40.5 · 2026 · 11 · 1 | `Los cupos por día deben ser un número entero` | Un decimal no es entero |
| C06 | Caracola · 0 · 2026 · 11 · 1 | `La lancha debe ofrecer al menos un cupo por día` | Frontera inferior que falla |
| C07 | Caracola · -5 · 2026 · 11 · 1 | `La lancha debe ofrecer al menos un cupo por día` | −5 sí es entero: separa la condición 2 de la 3 |
| C08 | Bote · 1 · 2026 · 11 · 1 | `Lancha Bote creada, sin días registrados` | Frontera inferior que pasa (`<` y no `<=`) |
| C09 | Caracola · 40 · 2026 · 11 · 31 | `La fecha no es válida` | Día que no existe |
| C10 | Caracola · 40 · 2026 · noviembre · 1 | `La fecha no es válida` | Mes no entero (no sale el mensaje de Python) |
| C11 | Caracola · 40 · 99999999999999999999 · 11 · 1 | `La fecha no es válida` | Año fuera de rango: sin la revisión de MINYEAR y MAXYEAR, el programa se cerraba con OverflowError |
| C12 | Caracola · 40 · 2027 · 2 · 29 | `La fecha no es válida` | 2027 no es bisiesto |
| C13 | Caracola · 40 · 2028 · 2 · 29 | `Lancha Caracola creada, sin días registrados` | 2028 sí es bisiesto |
| C14 | Caracola · 0 · 2026 · 11 · 31 | Solo `La lancha debe ofrecer al menos un cupo por día` | Orden: solo el primer error |
| C15 | *(vacío)* · cuarenta · 2026 · 13 · 1 | Solo `El nombre no puede estar vacío` | Orden: el nombre va antes que todo |
| C16 | Estrella de Mar · 60 · 2026 · 11 · 1, otra vez con 70, y después opción 2 con 61 | `Ya existe una lancha con ese nombre` y luego `Los pasajeros van de 0 a 60` | El duplicado no se crea y la original conserva sus 60 cupos |
| C17 | Gaviota · 120 …, después `  Gaviota ` · 50 … | `Ya existe una lancha con ese nombre` | Duplicado aunque tenga espacios alrededor |

## Requisito 2. Registrar los pasajeros del día siguiente

| Caso | Se teclea (opción 2) | Salida esperada | Qué prueba |
|---|---|---|---|
| C18 | Caracola (40 cupos, desde el 2026-11-01) · x · 41 · -1 · 26.5 · *(vacío)* · 26 | `Pasajeros del 2026-11-01:`; luego `Los pasajeros deben ser un número entero` (con x, 26.5 y vacío), `Los pasajeros van de 0 a 40` (con 41 y -1) y por último `Día registrado` | Reintento del mismo día sin cerrar el programa |
| C19 | Caracola · 0, después Caracola · 40 | Los dos se aceptan; el siguiente día pedido es `2026-11-03` | Fronteras incluidas (0 y cupos) |
| C20 | Delfín (30 cupos, desde el 2026-12-30), cuatro registros de 10 | Pide los días `2026-12-30`, `2026-12-31`, `2027-01-01` y `2027-01-02` | Fecha = inicio + días registrados, con cambio de año |
| C25 | Gaviota (120) y Caracola (40, desde el 2026-11-05); Gaviota · 96; Caracola · 120 · 26 | Caracola pide el `2026-11-05` y rechaza 120 con `Los pasajeros van de 0 a 40` | Cada lancha tiene su propio registro y sus propios cupos |

## Requisito 10. Buscar por nombre

| Caso | Se teclea | Salida esperada | Qué prueba |
|---|---|---|---|
| C21 | opción 2 · Medusa | `No hay una lancha con ese nombre` (no pide pasajeros) | La lancha no existe |
| C22 | existe Gaviota; opción 2 · gaviota | `No hay una lancha con ese nombre` | Distingue mayúsculas |
| C23 | existe Gaviota; opción 2 · `  Gaviota  ` · 96 | `Pasajeros del 2026-11-01:` y `Día registrado` | Ignora los espacios alrededor |
| C24 | existe Delfín; opción 2 · Delfin | `No hay una lancha con ese nombre` | Distingue tildes |

## Requisito 14. Menú (parcial)

| Caso | Se teclea | Salida esperada | Qué prueba |
|---|---|---|---|
| C26 | 8 | `La opción no es válida` y vuelve el menú | Número fuera de rango |
| C27 | dos | `La opción no es válida` | Texto |
| C28 | *(vacío)* | `La opción no es válida` | Entrada vacía |
| C29 | 4 | `Opción en construcción` (solo durante el incremento 1; en la versión final la opción 4 muestra el informe y C29 se cambió por la opción `0`, ver el incremento 6) | Opciones de los incrementos siguientes |
| — | 7 | El programa termina | Salir |

## Traza de `buscar_lancha("Estrella de Mar")`

Lanchas en la cooperativa: Gaviota, Estrella de Mar, Caracola.

| Vuelta | `lancha.nombre` | `lancha_encontrada is None` | `lancha.nombre == nombre_limpio` | `lancha_encontrada` al terminar |
|---|---|---|---|---|
| antes del for | — | — | — | `None` |
| 1 | Gaviota | True | False | `None` |
| 2 | Estrella de Mar | True | True | la Estrella de Mar |
| 3 | Caracola | False | False | la Estrella de Mar |

Con `"Medusa"`, ninguna vuelta cumple la condición y el método retorna `None`.
