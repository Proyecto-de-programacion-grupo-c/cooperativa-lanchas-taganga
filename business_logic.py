from datetime import MAXYEAR, MINYEAR, date, timedelta
from math import sqrt
from os.path import isfile
from random import randint

CUPOS_MÍNIMOS = 1
PASAJEROS_MÍNIMOS = 0
DÍAS_MÍNIMOS_A_SIMULAR = 1
PORCENTAJE = 100
LÍMITE_NIVEL_BAJO = 50
LÍMITE_NIVEL_ADECUADO = 70
LÍMITE_NIVEL_LLENO = 90
NIVEL_CRÍTICO = "Crítico"
NIVEL_BAJO = "Bajo"
NIVEL_ADECUADO = "Adecuado"
NIVEL_LLENO = "Lleno"
SEPARADOR_DE_CAMPOS = ";"
CAMPOS_DEL_ARCHIVO_DE_LANCHAS = 5
CAMPOS_DEL_ARCHIVO_DE_PASAJEROS = 2


def convertir_a_entero(texto: str, mensaje_de_error: str) -> int:
    # Decisión: int() lanza un ValueError con un mensaje de Python en inglés.
    # Se captura aquí y se lanza otro ValueError con el mensaje del dominio,
    # para que la interfaz muestre siempre un mensaje claro en español.
    try:
        número = int(texto)
    except ValueError:
        raise ValueError(mensaje_de_error)
    return número


def construir_fecha(texto_año: str, texto_mes: str, texto_día: str) -> date:
    MENSAJE_DE_FECHA = "La fecha no es válida"
    año = convertir_a_entero(texto_año, MENSAJE_DE_FECHA)
    mes = convertir_a_entero(texto_mes, MENSAJE_DE_FECHA)
    día = convertir_a_entero(texto_día, MENSAJE_DE_FECHA)
    # Decisión: con un año gigante, date() no lanza ValueError sino
    # OverflowError, y el programa se cerraría. Por eso el año se revisa
    # antes contra el rango que acepta date (de MINYEAR a MAXYEAR).
    if año < MINYEAR or año > MAXYEAR:
        raise ValueError(MENSAJE_DE_FECHA)
    try:
        fecha = date(año, mes, día)
    except ValueError:
        raise ValueError(MENSAJE_DE_FECHA)
    return fecha


def convertir_días_a_simular(texto_días: str) -> int:
    cantidad_de_días = convertir_a_entero(texto_días, "El número de días debe ser un número entero")
    if cantidad_de_días < DÍAS_MÍNIMOS_A_SIMULAR:
        raise ValueError("Se debe simular al menos un día")
    return cantidad_de_días


def calcular_día_anterior(fecha: date) -> date:
    día_anterior = fecha - timedelta(days=1)
    return día_anterior


def leer_líneas_de_archivo(ruta: str) -> list:
    # Decisión: se quitan los espacios y las comillas que rodean la ruta, porque
    # "Copiar como ruta de acceso" en Windows la copia entre comillas.
    ruta_limpia = ruta.strip().strip('"')
    if not isfile(ruta_limpia):
        raise ValueError("El archivo no existe")
    # Decisión: utf-8-sig lee igual un archivo UTF-8 normal y uno con la marca
    # BOM que agrega Excel al guardar "CSV UTF-8". Con utf-8, el BOM quedaría
    # pegado al primer campo de la primera línea; hoy esa línea es el encabezado,
    # que se salta, así que es una precaución por si el formato cambia.
    # Decisión: el archivo se lee completo antes de procesarlo; si no está en
    # UTF-8, el error ocurre antes de cargar cualquier línea, y su mensaje en
    # inglés (UnicodeDecodeError es un ValueError) se cambia por uno en español.
    try:
        with open(ruta_limpia, encoding="utf-8-sig") as archivo:
            contenido = archivo.read()
    except UnicodeDecodeError:
        raise ValueError("El archivo no está guardado en UTF-8")
    líneas = contenido.splitlines()
    return líneas


class Lancha:
    def __init__(self, nombre: str, cupos_por_día: int, fecha_de_inicio: date):
        self.nombre = nombre
        self.cupos_por_día = cupos_por_día
        self.fecha_de_inicio = fecha_de_inicio
        self.pasajeros_por_día = []

    def calcular_fecha_del_día_siguiente(self) -> date:
        # Decisión: el día siguiente es el que tendría la posición igual al número
        # de días registrados, así que se reutiliza calcular_fecha_de_un_día.
        fecha_siguiente = self.calcular_fecha_de_un_día(self.contar_días_registrados())
        return fecha_siguiente

    def agregar_pasajeros(self, pasajeros: int):
        # Decisión (incremento 4): el rango se revisa en revisar_pasajeros, que
        # también usa convertir_pasajeros al simular días, para no repetir la regla.
        self.revisar_pasajeros(pasajeros)
        self.pasajeros_por_día.append(pasajeros)

    def registrar_día(self, texto_pasajeros: str):
        pasajeros = convertir_a_entero(texto_pasajeros, "Los pasajeros deben ser un número entero")
        self.agregar_pasajeros(pasajeros)

    def contar_días_registrados(self) -> int:
        días_registrados = len(self.pasajeros_por_día)
        return días_registrados

    def calcular_pasajeros_totales(self) -> int:
        total = 0
        for pasajeros in self.pasajeros_por_día:
            total = total + pasajeros
        return total

    def calcular_promedio_de_pasajeros(self) -> float | None:
        días_registrados = self.contar_días_registrados()
        # Decisión: sin días registrados no hay promedio; se retorna None para
        # evitar la división entre cero, y la interfaz muestra el aviso.
        if días_registrados == 0:
            promedio = None
        else:
            promedio = self.calcular_pasajeros_totales() / días_registrados
        return promedio

    def calcular_factor_de_ocupación(self) -> float | None:
        promedio = self.calcular_promedio_de_pasajeros()
        if promedio is None:
            factor_de_ocupación = None
        else:
            factor_de_ocupación = promedio / self.cupos_por_día * PORCENTAJE
        return factor_de_ocupación

    def calcular_desviación_estándar(self) -> float | None:
        promedio = self.calcular_promedio_de_pasajeros()
        # Decisión: la desviación es la poblacional (se divide entre el número de
        # días, no entre el número de días menos uno), como dice el requisito 5.
        if promedio is None:
            desviación_estándar = None
        else:
            suma_de_cuadrados = 0
            for pasajeros in self.pasajeros_por_día:
                diferencia = pasajeros - promedio
                suma_de_cuadrados = suma_de_cuadrados + diferencia * diferencia
            varianza = suma_de_cuadrados / self.contar_días_registrados()
            desviación_estándar = sqrt(varianza)
        return desviación_estándar

    def calcular_fecha_de_un_día(self, índice: int) -> date:
        fecha = self.fecha_de_inicio + timedelta(days=índice)
        return fecha

    def buscar_fecha_del_día_de_más_pasajeros(self) -> date | None:
        días_registrados = self.contar_días_registrados()
        # Decisión: se empieza con el primer día y no con mayor_pasajeros = 0,
        # porque un día con 0 pasajeros es válido: si todos los días tienen 0,
        # con > nunca cambiaría el resultado y se retornaría None aunque hay días.
        if días_registrados == 0:
            fecha_de_más_pasajeros = None
        else:
            índice_de_más_pasajeros = 0
            mayor_pasajeros = self.pasajeros_por_día[0]
            for índice in range(1, días_registrados):
                # Decisión: con > estricto, en un empate se queda el primer día.
                if self.pasajeros_por_día[índice] > mayor_pasajeros:
                    mayor_pasajeros = self.pasajeros_por_día[índice]
                    índice_de_más_pasajeros = índice
            fecha_de_más_pasajeros = self.calcular_fecha_de_un_día(índice_de_más_pasajeros)
        return fecha_de_más_pasajeros

    def buscar_fecha_del_día_de_menos_pasajeros(self) -> date | None:
        días_registrados = self.contar_días_registrados()
        if días_registrados == 0:
            fecha_de_menos_pasajeros = None
        else:
            índice_de_menos_pasajeros = 0
            menor_pasajeros = self.pasajeros_por_día[0]
            for índice in range(1, días_registrados):
                # Decisión: con < estricto, en un empate se queda el primer día.
                if self.pasajeros_por_día[índice] < menor_pasajeros:
                    menor_pasajeros = self.pasajeros_por_día[índice]
                    índice_de_menos_pasajeros = índice
            fecha_de_menos_pasajeros = self.calcular_fecha_de_un_día(índice_de_menos_pasajeros)
        return fecha_de_menos_pasajeros

    def clasificar_nivel_de_ocupación(self, pasajeros: int) -> str:
        porcentaje_ocupado = pasajeros / self.cupos_por_día * PORCENTAJE
        if porcentaje_ocupado < LÍMITE_NIVEL_BAJO:
            nivel = NIVEL_CRÍTICO
        elif porcentaje_ocupado < LÍMITE_NIVEL_ADECUADO:
            nivel = NIVEL_BAJO
        elif porcentaje_ocupado < LÍMITE_NIVEL_LLENO:
            nivel = NIVEL_ADECUADO
        else:
            nivel = NIVEL_LLENO
        return nivel

    def contar_días_en_nivel(self, nivel: str) -> int:
        días_en_nivel = 0
        for pasajeros in self.pasajeros_por_día:
            if self.clasificar_nivel_de_ocupación(pasajeros) == nivel:
                días_en_nivel = días_en_nivel + 1
        return días_en_nivel

    def contar_días_críticos_seguidos(self, índice_de_inicio: int) -> int:
        días_seguidos = 0
        índice = índice_de_inicio
        racha_terminada = False
        while not racha_terminada:
            # Decisión: la condición del índice va primero; si ya se pasó del
            # último día, el and no evalúa la segunda parte y no hay IndexError.
            if índice < self.contar_días_registrados() and self.clasificar_nivel_de_ocupación(self.pasajeros_por_día[índice]) == NIVEL_CRÍTICO:
                días_seguidos = días_seguidos + 1
                índice = índice + 1
            else:
                racha_terminada = True
        return días_seguidos

    def buscar_inicio_de_la_racha_crítica_más_larga(self) -> int | None:
        índice_de_inicio_más_larga = None
        días_de_la_más_larga = 0
        anterior_es_crítico = False
        for índice in range(self.contar_días_registrados()):
            actual_es_crítico = self.clasificar_nivel_de_ocupación(self.pasajeros_por_día[índice]) == NIVEL_CRÍTICO
            # Una racha empieza en un día crítico cuyo día anterior no lo fue.
            if actual_es_crítico and not anterior_es_crítico:
                días_de_la_racha = self.contar_días_críticos_seguidos(índice)
                # Decisión: con > estricto, en un empate se queda la racha que empezó primero.
                if días_de_la_racha > días_de_la_más_larga:
                    días_de_la_más_larga = días_de_la_racha
                    índice_de_inicio_más_larga = índice
            anterior_es_crítico = actual_es_crítico
        return índice_de_inicio_más_larga

    def revisar_pasajeros(self, pasajeros: int):
        if pasajeros < PASAJEROS_MÍNIMOS or pasajeros > self.cupos_por_día:
            raise ValueError(f"Los pasajeros van de {PASAJEROS_MÍNIMOS} a {self.cupos_por_día}")

    def convertir_pasajeros(self, texto_pasajeros: str) -> int:
        pasajeros = convertir_a_entero(texto_pasajeros, "Los pasajeros deben ser un número entero")
        self.revisar_pasajeros(pasajeros)
        return pasajeros

    def simular_días(self, cantidad_de_días: int, pasajeros_mínimos: int, pasajeros_máximos: int):
        # Decisión: todas las condiciones se revisan antes del for, para que un
        # dato inválido no deje la mitad de los días agregados.
        if cantidad_de_días < DÍAS_MÍNIMOS_A_SIMULAR:
            raise ValueError("Se debe simular al menos un día")
        self.revisar_pasajeros(pasajeros_mínimos)
        self.revisar_pasajeros(pasajeros_máximos)
        if pasajeros_mínimos > pasajeros_máximos:
            raise ValueError("El mínimo no puede ser mayor que el máximo")
        for número_de_día in range(cantidad_de_días):
            pasajeros = randint(pasajeros_mínimos, pasajeros_máximos)
            self.agregar_pasajeros(pasajeros)

    def calcular_fecha_del_último_día_registrado(self) -> date | None:
        días_registrados = self.contar_días_registrados()
        if días_registrados == 0:
            fecha_del_último_día = None
        else:
            fecha_del_último_día = self.calcular_fecha_de_un_día(días_registrados - 1)
        return fecha_del_último_día

    def contar_días_sin_registrar(self, fecha_actual: date) -> int:
        # Los días por registrar van del día siguiente al último registrado
        # hasta el anterior a la fecha actual, que es la resta de las dos fechas.
        fecha_siguiente = self.calcular_fecha_del_día_siguiente()
        días_sin_registrar = (fecha_actual - fecha_siguiente).days
        # Decisión: si el registro llega hasta ayer o más allá (días simulados en
        # el futuro), la resta da 0 o un número negativo, y el registro está al día.
        if días_sin_registrar < 0:
            días_sin_registrar = 0
        return días_sin_registrar


class Cooperativa:
    def __init__(self):
        self.lanchas = []

    def agregar_lancha(self, lancha: Lancha):
        self.lanchas.append(lancha)

    def buscar_lancha(self, nombre: str) -> Lancha | None:
        nombre_limpio = nombre.strip()
        lancha_encontrada = None
        for lancha in self.lanchas:
            if lancha_encontrada is None and lancha.nombre == nombre_limpio:
                lancha_encontrada = lancha
        return lancha_encontrada

    # Decisión: las cuatro condiciones se revisan aquí y no en Lancha, porque el
    # requisito fija un orden (nombre, cupos enteros, al menos un cupo, fecha) y
    # el nombre repetido solo lo puede revisar la cooperativa, que tiene la lista.
    def crear_lancha(self,
                     nombre: str,
                     texto_cupos: str,
                     texto_año: str,
                     texto_mes: str,
                     texto_día: str) -> Lancha:
        # Decisión: el nombre se guarda sin los espacios del principio y del final,
        # igual que se compara en buscar_lancha.
        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            raise ValueError("El nombre no puede estar vacío")
        if self.buscar_lancha(nombre_limpio) is not None:
            raise ValueError("Ya existe una lancha con ese nombre")
        cupos_por_día = convertir_a_entero(texto_cupos, "Los cupos por día deben ser un número entero")
        if cupos_por_día < CUPOS_MÍNIMOS:
            raise ValueError("La lancha debe ofrecer al menos un cupo por día")
        fecha_de_inicio = construir_fecha(texto_año, texto_mes, texto_día)
        lancha = Lancha(nombre_limpio, cupos_por_día, fecha_de_inicio)
        self.agregar_lancha(lancha)
        return lancha

    # Decisión: el resultado empieza en None y se compara con "is None or", y no
    # con el patrón mayor = 0 del curso ni empezando con la primera lancha:
    # - con mayor = 0 y >, si todas las lanchas tienen factor 0.0 (días con 0
    #   pasajeros), nunca se cumpliría la condición y se retornaría None;
    # - la primera lancha puede no tener días registrados, y no se compara.
    def buscar_lancha_de_factor_más_alto(self) -> Lancha | None:
        lancha_de_factor_más_alto = None
        factor_más_alto = 0.0
        for lancha in self.lanchas:
            factor_de_ocupación = lancha.calcular_factor_de_ocupación()
            if factor_de_ocupación is not None:
                # Decisión: con > estricto y sin redondear, en un empate se queda
                # la lancha que se creó o se cargó primero.
                if lancha_de_factor_más_alto is None or factor_de_ocupación > factor_más_alto:
                    factor_más_alto = factor_de_ocupación
                    lancha_de_factor_más_alto = lancha
        return lancha_de_factor_más_alto

    def buscar_lancha_de_factor_más_bajo(self) -> Lancha | None:
        lancha_de_factor_más_bajo = None
        factor_más_bajo = 0.0
        for lancha in self.lanchas:
            factor_de_ocupación = lancha.calcular_factor_de_ocupación()
            if factor_de_ocupación is not None:
                if lancha_de_factor_más_bajo is None or factor_de_ocupación < factor_más_bajo:
                    factor_más_bajo = factor_de_ocupación
                    lancha_de_factor_más_bajo = lancha
        return lancha_de_factor_más_bajo

    def revisar_que_no_tenga_lanchas(self):
        if len(self.lanchas) > 0:
            raise ValueError("La carga solo se hace con el programa sin lanchas")

    def contar_lanchas(self) -> int:
        cantidad_de_lanchas = len(self.lanchas)
        return cantidad_de_lanchas

    def contar_días_registrados_en_total(self) -> int:
        total_de_días = 0
        for lancha in self.lanchas:
            total_de_días = total_de_días + lancha.contar_días_registrados()
        return total_de_días

    # Recorrido por índices: el número de cada línea (índice + 1) va en el
    # mensaje de las líneas descartadas. El índice 0 es el encabezado.
    def cargar_lanchas(self, ruta: str) -> list:
        self.revisar_que_no_tenga_lanchas()
        líneas = leer_líneas_de_archivo(ruta)
        líneas_descartadas = []
        for índice in range(1, len(líneas)):
            línea = líneas[índice]
            número_de_línea = índice + 1
            # Decisión: una línea vacía (o con solo espacios) se salta sin aviso.
            if línea.strip() != "":
                campos = línea.split(SEPARADOR_DE_CAMPOS)
                if len(campos) != CAMPOS_DEL_ARCHIVO_DE_LANCHAS:
                    líneas_descartadas.append(f"Línea {número_de_línea} descartada. La línea no tiene cinco campos")
                else:
                    # Decisión: se reutiliza crear_lancha, que revisa las condiciones
                    # en el mismo orden que al crear la lancha desde el teclado. Su
                    # error se captura para descartar la línea y seguir con la carga.
                    try:
                        self.crear_lancha(campos[0], campos[1].strip(), campos[2].strip(), campos[3].strip(), campos[4].strip())
                    except ValueError as error:
                        líneas_descartadas.append(f"Línea {número_de_línea} descartada. {error}")
        return líneas_descartadas

    def cargar_pasajeros(self, ruta: str) -> list:
        líneas = leer_líneas_de_archivo(ruta)
        líneas_descartadas = []
        for índice in range(1, len(líneas)):
            línea = líneas[índice]
            número_de_línea = índice + 1
            if línea.strip() != "":
                campos = línea.split(SEPARADOR_DE_CAMPOS)
                if len(campos) != CAMPOS_DEL_ARCHIVO_DE_PASAJEROS:
                    líneas_descartadas.append(f"Línea {número_de_línea} descartada. La línea no tiene dos campos")
                else:
                    lancha = self.buscar_lancha(campos[0])
                    if lancha is None:
                        líneas_descartadas.append(f"Línea {número_de_línea} descartada. No hay una lancha con ese nombre")
                    else:
                        # Cada línea agrega el día que sigue en el registro de su lancha.
                        try:
                            lancha.registrar_día(campos[1].strip())
                        except ValueError as error:
                            líneas_descartadas.append(f"Línea {número_de_línea} descartada. {error}")
        return líneas_descartadas
