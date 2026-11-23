# Casos de verificación – Incremento 4

Requisitos: 3 (simular días, en la opción 3) y 9 (los días sin registrar, en el informe de la opción 4).
Cada caso se comprueba ejecutando `user_interface.py`. La Caracola se crea con 40 cupos y la Gaviota con 120, las dos con inicio el 2026-11-01.

## Requisito 3. Simular días

Datos en este orden: nombre · número de días · pasajeros mínimos · pasajeros máximos.

| Caso | Se teclea | Salida esperada | Qué prueba |
|---|---|---|---|
| S01 | Caracola · 3 · 20 · 40 | `Días simulados: 3, del 2026-11-01 al 2026-11-03`; el informe muestra 3 días, todos entre 20 y 40 | Camino válido |
| S02 | Caracola · 4 · 30 · 30 | Informe: `Pasajeros totales: 120` y `Desviación estándar de los pasajeros: 0.0` | Con mínimo = máximo el azar da siempre el mismo valor, así que el caso se puede repetir con resultado exacto |
| S03 | Caracola · tres | `El número de días debe ser un número entero`; **no** pide los mínimos | Revisión inmediata y vuelta al menú |
| S04 | Caracola · 0 | `Se debe simular al menos un día`; no pide los mínimos; el informe sigue sin días | Frontera inferior que falla |
| S05 | Caracola · -2 | `Se debe simular al menos un día` | Número negativo (sí es entero) |
| S06 | Caracola · 3 · x | `Los pasajeros deben ser un número entero`; **no** pide el máximo | El mínimo se revisa apenas se lee |
| S07 | Caracola · 3 · -1 | `Los pasajeros van de 0 a 40`; no pide el máximo | Mínimo fuera de rango |
| S08 | Caracola · 3 · 30 · 20 | `El mínimo no puede ser mayor que el máximo`; el informe sigue sin días | Ningún día se agrega si falla la última condición |
| S09 | Caracola · 3 · 20 · 41 | `Los pasajeros van de 0 a 40`; sin días agregados | Máximo fuera de rango |
| S10 | Caracola · 5 · 0 · 40 | `Días simulados: 5` | Fronteras incluidas: 0 y los cupos |
| S11 | Caracola · 1 · 0 · 0 | `Días simulados: 1, del 2026-11-01 al 2026-11-01`; total 0 | Frontera: simular exactamente un día |
| S12 | Caracola con el día 1 registrado (26) · 2 · 10 · 10; después la opción 2 | `Días simulados: 2, del 2026-11-02 al 2026-11-03`; después la opción 2 pide los `Pasajeros del 2026-11-04` | Los días simulados siguen el registro sin saltarse días |
| S13 | Medusa | `No hay una lancha con ese nombre`; no pide el número de días | Lancha inexistente |
| S14 | 40 ejecuciones de `simular_días(50, 20, 25)` | Aparecen todos los valores del 20 al 25 y ninguno queda fuera | `randint` incluye los dos extremos |

## Requisito 9. Los días sin registrar

La fecha actual sale del computador (`date.today()` en la interfaz). Para comprobar estos casos con resultados fijos, el programa se ejecutó con la fecha indicada en la columna "Hoy". Para comprobarlos a mano, se puede cambiar la fecha del computador, o adaptar los datos para que el último día registrado sea ayer (al día), anteayer (falta 1), etc.

| Caso | Hoy | Datos | Salida esperada | Qué prueba |
|---|---|---|---|---|
| F01 | 2026-11-20 | Gaviota, 5 días | `Último día registrado: 2026-11-05` · `Días por registrar: 14, del 2026-11-06 al 2026-11-19` | Ejemplo del enunciado |
| F02 | 2026-11-02 | Caracola, 1 día | `Último día registrado: 2026-11-01` · `El registro está al día` | Ejemplo del enunciado: el último día es ayer |
| F03 | 2026-11-03 | Caracola, 1 día | `Días por registrar: 1, del 2026-11-02 al 2026-11-02` | Frontera: falta exactamente un día |
| F04 | 2026-11-10 | Caracola con 30 días simulados | `Último día registrado: 2026-11-30` · `El registro está al día` | Días en el futuro: la resta es negativa, no se muestra un número negativo |
| F05 | 2026-11-01 | Caracola con el día de hoy registrado | `El registro está al día` | El último día registrado es posterior a ayer |
| F06 | 2027-01-03 | Inicio 2026-12-30, 1 día | `Días por registrar: 3, del 2026-12-31 al 2027-01-02` | Resta de fechas con cambio de año |

## Traza de `contar_días_sin_registrar(fecha_actual)`

| Caso | `fecha_siguiente` | `fecha_actual` | `(fecha_actual - fecha_siguiente).days` | ¿Es menor que 0? | Resultado |
|---|---|---|---|---|---|
| F01 | 2026-11-06 | 2026-11-20 | 14 | No | 14 |
| F02 | 2026-11-02 | 2026-11-02 | 0 | No | 0 → al día |
| F03 | 2026-11-02 | 2026-11-03 | 1 | No | 1 |
| F04 | 2026-12-01 | 2026-11-10 | −21 | Sí | 0 → al día |
