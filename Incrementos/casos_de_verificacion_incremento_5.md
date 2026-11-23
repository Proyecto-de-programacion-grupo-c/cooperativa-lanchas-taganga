# Casos de verificación – Incremento 5

Requisito 11: la lancha con el factor de ocupación más alto y la del más bajo, en la opción 5 del menú.
Cada caso se comprueba ejecutando `user_interface.py`: se crean las lanchas con la opción 1 **en el orden indicado**, se registran los días con la opción 2 y se elige la opción 5.

| Caso | Lanchas en orden de creación: cupos y pasajeros (factor sin redondear) | Salida esperada | Qué prueba |
|---|---|---|---|
| M01 | Gaviota 120: 96, 54, 48, 114, 120 (72.0) · Estrella de Mar 60: 27, 36, 45, 57 (68.75) · Caracola 40: 26 (65.0) · Perla Negra 30: sin días | Más alto: `Gaviota, con 72.0 %` · Más bajo: `Caracola, con 65.0 %` | Ejemplo del enunciado; la Perla Negra no se compara |
| M02 | Ninguna lancha | `Ninguna lancha tiene días registrados` | Lista vacía |
| M03 | Perla Negra 30 y Medusa 20, sin días | `Ninguna lancha tiene días registrados` | Hay lanchas, pero ninguna tiene días |
| M04 | Perla Negra sin días · Caracola 40: 26 | Más alto y más bajo: `Caracola, con 65.0 %` | Con una sola lancha comparable, es a la vez la más alta y la más baja |
| M05 | A 100: 80 (80.0) · B 50: 40 (80.0) · C 100: 50 (50.0) | Más alto: `A, con 80.0 %` · Más bajo: `C, con 50.0 %` | Empate en el más alto: gana la que se creó primero (`>`, no `>=`) |
| M06 | A 100: 80 · B 100: 50 (50.0) · C 10: 5 (50.0) | Más bajo: `B, con 50.0 %` | Empate en el más bajo: gana la que se creó primero (`<`, no `<=`) |
| M07 | A 3: 2 (66.666…) · B 10000: 6667 (66.67) | Más alto: `B, con 66.67 %` · Más bajo: `A, con 66.67 %` | Se compara **sin redondear**: redondeadas empatarían y saldría A en los dos |
| M08 | Ceros 40: 0, 0 (0.0) · Perla sin días | Más alto y más bajo: `Ceros, con 0.0 %` | Con el patrón `mayor = 0` y `>` no habría lancha más alta |
| M09 | Perla sin días · A 100: 30 · B 100: 90 | Más alto: `B, con 90.0 %` · Más bajo: `A, con 30.0 %` | La primera lancha de la lista no tiene días (no se puede empezar con ella) |
| M10 | B 100: 90 · A 100: 30 | Más alto: `B` · Más bajo: `A` | El resultado no depende del orden cuando no hay empate |
| M11 | A 100: 30 · B 100: 90; opción 5; después A registra cinco días con 100; opción 5 otra vez | Primero el más bajo es `A, con 30.0 %`; después, más alto `B, con 90.0 %` y más bajo `A, con 88.33 %` | Los factores se calculan en el momento de la consulta |

## Traza de `buscar_lancha_de_factor_más_alto()` (caso M09)

Antes del for: `lancha_de_factor_más_alto = None`, `factor_más_alto = 0.0`.

| Vuelta | `lancha.nombre` | `factor_de_ocupación` | ¿No es None? | `… is None or factor > factor_más_alto` | `factor_más_alto` | `lancha_de_factor_más_alto` |
|---|---|---|---|---|---|---|
| 1 | Perla | None | No | (no se evalúa) | 0.0 | None |
| 2 | A | 30.0 | Sí | True (todavía es None) | 30.0 | A |
| 3 | B | 90.0 | Sí | True (90.0 > 30.0) | 90.0 | B |

## Nota sobre la verificación

En el caso M11, la salida esperada que propuso la IA estaba mal: decía que, después de registrar los cinco días, A pasaba a ser la más alta con 88.33 %. El caso falló al ejecutarlo. Al revisar, el programa estaba bien: A queda con (30 + 5 × 100) / 6 = 88.33 %, que sigue siendo menor que el 90.0 % de B. Se corrigió la salida esperada, no el código.
