# Casos de verificación – Incremento 2

Requisitos: 4 (el informe de una lancha) y 5 (la desviación estándar), en la opción 4 del menú.
Cada caso se comprueba ejecutando `user_interface.py`. Las lanchas se crean con la opción 1 (fecha de inicio 2026-11-01) y los días se registran con la opción 2, en el orden indicado.

| Caso | Datos | Salida esperada del informe | Qué prueba |
|---|---|---|---|
| I01 | Gaviota, 120 cupos: 96, 54, 48, 114, 120 | `Días registrados: 5` · `Pasajeros totales: 432` · `Promedio de pasajeros por día: 86.4` · `Factor de ocupación: 72.0 %` · `Desviación estándar de los pasajeros: 30.02` | Ejemplo del enunciado |
| I02 | Estrella de Mar, 60 cupos: 27, 36, 45, 57 | `4` · `165` · `41.25` · `68.75 %` · `11.1` | Ejemplo del enunciado. La desviación **muestral** daría 12.82, así que este caso separa la regla real (dividir entre n) de la parecida (dividir entre n − 1) |
| I03 | Perla Negra, 30 cupos, sin días | `Lancha: Perla Negra` · `Cupos por día: 30` · `La lancha no tiene días registrados` y **nada más** | Lista vacía (evita la división entre cero) |
| I04 | Caracola, 40 cupos: 26 | `1` · `26` · `26.0` · `65.0 %` · `0.0` | Un solo día: la desviación es 0.0 |
| I05 | 120 cupos: 100, 80 | `180` · `90.0` · `75.0 %` · `10.0` | Ejemplo del contexto del enunciado |
| I06 | 40 cupos: 0, 0 | `2` · `0` · `0.0` · `0.0 %` · `0.0` | Días con 0 pasajeros ≠ sin días registrados |
| I07 | 1 cupo: 1, 1, 1 | `Factor de ocupación: 100.0 %` · `0.0` | Ocupación completa, frontera superior |
| I08 | 3 cupos: 1, 2, 2 | `1.67` · `55.56 %` · `0.47` | El redondeo a dos decimales con `round` |
| I09 | 100 cupos: 64 | `Factor de ocupación: 64.0 %` | `round` muestra 64.0 y no 64.00 |
| I10 | Opción 4 con Medusa | `No hay una lancha con ese nombre` (no muestra cupos) | Lancha inexistente |
| I11 | Gaviota y Estrella de Mar en el mismo programa | Cada informe con sus propios datos: 72.0 % y 68.75 % | Varias lanchas (requisito 10) |

## Traza de `calcular_desviación_estándar()` con la Estrella de Mar

Promedio = 165 / 4 = 41.25. `suma_de_cuadrados` empieza en 0.

| Vuelta | `pasajeros` | `diferencia` | `diferencia * diferencia` | `suma_de_cuadrados` al terminar |
|---|---|---|---|---|
| 1 | 27 | −14.25 | 203.0625 | 203.0625 |
| 2 | 36 | −5.25 | 27.5625 | 230.625 |
| 3 | 45 | 3.75 | 14.0625 | 244.6875 |
| 4 | 57 | 15.75 | 248.0625 | 492.75 |

`varianza` = 492.75 / 4 = 123.1875 → `sqrt(123.1875)` = 11.0990… → `round(…, 2)` = **11.1**
