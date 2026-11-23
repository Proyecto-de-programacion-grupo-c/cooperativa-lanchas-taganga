# Casos de verificación – Incremento 3

Requisitos: 6 (el día de más y el de menos pasajeros), 7 (los días en cada nivel de ocupación) y 8 (la racha más larga en nivel crítico). Todo se ve en el informe de la opción 4.
Cada caso se comprueba ejecutando `user_interface.py`: se crea la lancha con la opción 1 (con inicio el 2026-11-01, salvo que se diga otra cosa), se registran los días con la opción 2 y se pide el informe con la opción 4.

| Caso | Lancha (cupos): pasajeros | Salida esperada | Qué prueba |
|---|---|---|---|
| N01 | Gaviota (120): 96, 54, 48, 114, 120 | Más: `2026-11-05` · Menos: `2026-11-03` · Crítico 2, Bajo 0, Adecuado 1, Lleno 2 · Racha: `2 días, desde el 2026-11-02` | Ejemplo del enunciado; un nivel con 0 días también se muestra |
| N02 | Estrella de Mar (60): 27, 36, 45, 57 | Más: `2026-11-04` · Menos: `2026-11-01` · 1, 1, 1, 1 · Racha: `1 día, el 2026-11-01` | Ejemplo del enunciado; una racha de un solo día |
| N03 | (120): 60, 120, 120, 24, 24 | Más: `2026-11-02` · Menos: `2026-11-04` | Empates: gana el primero (`>` y `<`, no `>=` ni `<=`) |
| N04 | (120): 59, 60, 83, 84, 107, 108 | Crítico 1, Bajo 2, Adecuado 2, Lleno 1 | Fronteras de los niveles: 49.2 %, 50 %, 69.2 %, 70 %, 89.2 % y 90 % |
| N05 | (120): 50, 40, 100, 55, 30, 45, 110 | Racha: `3 días, desde el 2026-11-04` | Ejemplo del enunciado: la racha más larga no es la primera |
| N06 | Caracola (40): 26 | Más y Menos: `2026-11-01` · 0, 1, 0, 0 · `La lancha no tuvo ningún día en nivel crítico` | Sin días críticos; un solo día es a la vez el de más y el de menos |
| N07 | (40): 0, 0, 0 | Más y Menos: `2026-11-01` · Crítico 3 · Racha: `3 días, desde el 2026-11-01` | Con el patrón `mayor = 0` y `>` del curso, el día de más pasajeros saldría `None`; por eso se empieza con el primer día |
| N08 | (120): 10, 10, 100, 10, 10 | Racha: `2 días, desde el 2026-11-01` | Empate de rachas: gana la que empezó primero |
| N09 | (120): 100, 10, 100, 10, 10, 10 | Racha: `3 días, desde el 2026-11-04` | La racha más larga llega hasta el último día (sin IndexError) |
| N10 | Inicio 2026-11-29 (120): 100, 100, 10, 120 | Más: `2026-12-02` · Menos: `2026-12-01` · Racha: `1 día, el 2026-12-01` | La fecha sale de la posición del día, con cambio de mes |
| N11 | Perla Negra (30), sin días | Solo `La lancha no tiene días registrados` | No muestra fechas, niveles ni racha |
| N12 | (120): 120, 100, 80, 60 | Más: `2026-11-01` · Menos: `2026-11-04` | El máximo en la primera posición y el mínimo en la última |

## Traza de `buscar_inicio_de_la_racha_crítica_más_larga()` (caso N05)

Cupos 120. Es crítico si el porcentaje es menor que 50 (menos de 60 pasajeros). Antes del for: `índice_de_inicio_más_larga = None`, `días_de_la_más_larga = 0`, `anterior_es_crítico = False`.

| Vuelta | `índice` | Pasajeros | `actual_es_crítico` | ¿Empieza racha? | `contar_días_críticos_seguidos(índice)` | `días_de_la_más_larga` | `índice_de_inicio_más_larga` |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 50 | True | Sí (el anterior no era crítico) | 2 | 2 | 0 |
| 2 | 1 | 40 | True | No (el anterior era crítico) | — | 2 | 0 |
| 3 | 2 | 100 | False | No | — | 2 | 0 |
| 4 | 3 | 55 | True | Sí | 3 | 3 | 3 |
| 5 | 4 | 30 | True | No | — | 3 | 3 |
| 6 | 5 | 45 | True | No | — | 3 | 3 |
| 7 | 6 | 110 | False | No | — | 3 | 3 |

El índice 3 corresponde a `fecha_de_inicio + 3 días` = **2026-11-04**, y la racha tiene **3 días**.

## Traza de `contar_días_críticos_seguidos(3)` (caso N05)

| Vuelta | `índice` | `índice < 7` | ¿Crítico? | `días_seguidos` al terminar | `racha_terminada` |
|---|---|---|---|---|---|
| 1 | 3 | True | Sí (55) | 1 | False |
| 2 | 4 | True | Sí (30) | 2 | False |
| 3 | 5 | True | Sí (45) | 3 | False |
| 4 | 6 | True | No (110) | 3 | True |
