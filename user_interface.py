from datetime import date
from os import system

from business_logic import (NIVEL_ADECUADO, NIVEL_BAJO, NIVEL_CRÍTICO, NIVEL_LLENO, Cooperativa,
                            calcular_día_anterior, convertir_días_a_simular)

cooperativa = Cooperativa()
salir = False

while not salir:
    system("cls")
    print("=====================================")
    print("Cooperativa de Lancheros de Taganga")
    print("=====================================")
    print("1. Crear una lancha")
    print("2. Registrar los pasajeros del día siguiente")
    print("3. Simular días")
    print("4. Ver el informe de una lancha")
    print("5. Ver la lancha con el factor de ocupación más alto y la del más bajo")
    print("6. Cargar las lanchas y los pasajeros desde archivos")
    print("7. Salir")
    opción = input("Opción: ").strip()

    if opción == "1":
        print("\n--- Crear una lancha ---")
        nombre = input("Nombre de la lancha: ")
        texto_cupos = input("Cupos por día: ")
        texto_año = input("Año de inicio del registro: ")
        texto_mes = input("Mes de inicio del registro: ")
        texto_día = input("Día de inicio del registro: ")
        try:
            lancha = cooperativa.crear_lancha(nombre, texto_cupos, texto_año, texto_mes, texto_día)
            print(f"Lancha {lancha.nombre} creada, sin días registrados")
        except ValueError as error:
            print(error)
    elif opción == "2":
        print("\n--- Registrar los pasajeros del día siguiente ---")
        nombre = input("Nombre de la lancha: ")
        lancha = cooperativa.buscar_lancha(nombre)
        if lancha is None:
            print("No hay una lancha con ese nombre")
        else:
            fecha_siguiente = lancha.calcular_fecha_del_día_siguiente()
            día_registrado = False
            while not día_registrado:
                try:
                    texto_pasajeros = input(f"Pasajeros del {fecha_siguiente}: ")
                    lancha.registrar_día(texto_pasajeros)
                    día_registrado = True
                except ValueError as error:
                    print(error)
            print("Día registrado")
    elif opción == "4":
        print("\n--- Informe de una lancha ---")
        nombre = input("Nombre de la lancha: ")
        lancha = cooperativa.buscar_lancha(nombre)
        if lancha is None:
            print("No hay una lancha con ese nombre")
        else:
            print(f"\nLancha: {lancha.nombre}")
            print(f"Cupos por día: {lancha.cupos_por_día}")
            días_registrados = lancha.contar_días_registrados()
            if días_registrados == 0:
                print("La lancha no tiene días registrados")
            else:
                pasajeros_totales = lancha.calcular_pasajeros_totales()
                promedio = lancha.calcular_promedio_de_pasajeros()
                factor_de_ocupación = lancha.calcular_factor_de_ocupación()
                desviación_estándar = lancha.calcular_desviación_estándar()
                print(f"Días registrados: {días_registrados}")
                print(f"Pasajeros totales: {pasajeros_totales}")
                print(f"Promedio de pasajeros por día: {round(promedio, 2)}")
                print(f"Factor de ocupación: {round(factor_de_ocupación, 2)} %")
                print(f"Desviación estándar de los pasajeros: {round(desviación_estándar, 2)}")

                fecha_de_más_pasajeros = lancha.buscar_fecha_del_día_de_más_pasajeros()
                fecha_de_menos_pasajeros = lancha.buscar_fecha_del_día_de_menos_pasajeros()
                print(f"Día de más pasajeros: {fecha_de_más_pasajeros}")
                print(f"Día de menos pasajeros: {fecha_de_menos_pasajeros}")

                días_críticos = lancha.contar_días_en_nivel(NIVEL_CRÍTICO)
                días_bajos = lancha.contar_días_en_nivel(NIVEL_BAJO)
                días_adecuados = lancha.contar_días_en_nivel(NIVEL_ADECUADO)
                días_llenos = lancha.contar_días_en_nivel(NIVEL_LLENO)
                print("Días en cada nivel de ocupación:")
                print(f"  {NIVEL_CRÍTICO}: {días_críticos}")
                print(f"  {NIVEL_BAJO}: {días_bajos}")
                print(f"  {NIVEL_ADECUADO}: {días_adecuados}")
                print(f"  {NIVEL_LLENO}: {días_llenos}")

                índice_de_inicio_de_racha = lancha.buscar_inicio_de_la_racha_crítica_más_larga()
                if índice_de_inicio_de_racha is None:
                    print("La lancha no tuvo ningún día en nivel crítico")
                else:
                    días_de_la_racha = lancha.contar_días_críticos_seguidos(índice_de_inicio_de_racha)
                    fecha_de_inicio_de_racha = lancha.calcular_fecha_de_un_día(índice_de_inicio_de_racha)
                    if días_de_la_racha == 1:
                        print(f"Racha más larga en nivel crítico: 1 día, el {fecha_de_inicio_de_racha}")
                    else:
                        print(f"Racha más larga en nivel crítico: {días_de_la_racha} días, desde el {fecha_de_inicio_de_racha}")

                # Decisión: la fecha actual se toma del computador aquí, en la
                # interfaz, y entra a la lógica por parámetro.
                fecha_actual = date.today()
                fecha_del_último_día = lancha.calcular_fecha_del_último_día_registrado()
                días_sin_registrar = lancha.contar_días_sin_registrar(fecha_actual)
                print(f"Último día registrado: {fecha_del_último_día}")
                if días_sin_registrar == 0:
                    print("El registro está al día")
                else:
                    primer_día_sin_registrar = lancha.calcular_fecha_del_día_siguiente()
                    último_día_sin_registrar = calcular_día_anterior(fecha_actual)
                    print(f"Días por registrar: {días_sin_registrar}, del {primer_día_sin_registrar} al {último_día_sin_registrar}")
    elif opción == "3":
        print("\n--- Simular días ---")
        nombre = input("Nombre de la lancha: ")
        lancha = cooperativa.buscar_lancha(nombre)
        if lancha is None:
            print("No hay una lancha con ese nombre")
        else:
            # Decisión: un solo try sin ciclo. Si un dato no es válido, el error
            # salta al except sin leer los datos que faltan, y se vuelve al menú.
            try:
                texto_días = input("Número de días a simular: ")
                cantidad_de_días = convertir_días_a_simular(texto_días)
                texto_mínimos = input("Pasajeros mínimos: ")
                pasajeros_mínimos = lancha.convertir_pasajeros(texto_mínimos)
                texto_máximos = input("Pasajeros máximos: ")
                pasajeros_máximos = lancha.convertir_pasajeros(texto_máximos)
                fecha_del_primer_día_simulado = lancha.calcular_fecha_del_día_siguiente()
                lancha.simular_días(cantidad_de_días, pasajeros_mínimos, pasajeros_máximos)
                fecha_del_último_día_simulado = lancha.calcular_fecha_del_último_día_registrado()
                print(f"Días simulados: {cantidad_de_días}, del {fecha_del_primer_día_simulado} al {fecha_del_último_día_simulado}")
            except ValueError as error:
                print(error)
    elif opción == "5":
        print("\n--- Factor de ocupación más alto y más bajo ---")
        lancha_más_alta = cooperativa.buscar_lancha_de_factor_más_alto()
        lancha_más_baja = cooperativa.buscar_lancha_de_factor_más_bajo()
        if lancha_más_alta is None:
            print("Ninguna lancha tiene días registrados")
        else:
            factor_más_alto = lancha_más_alta.calcular_factor_de_ocupación()
            factor_más_bajo = lancha_más_baja.calcular_factor_de_ocupación()
            print(f"Lancha con el factor de ocupación más alto: {lancha_más_alta.nombre}, con {round(factor_más_alto, 2)} %")
            print(f"Lancha con el factor de ocupación más bajo: {lancha_más_baja.nombre}, con {round(factor_más_bajo, 2)} %")
    elif opción == "6":
        print("\n--- Cargar las lanchas y los pasajeros desde archivos ---")
        # Decisión: un solo try sin ciclo, como al simular días. Si el programa ya
        # tiene lanchas, no se lee ninguna ruta; si el archivo de lanchas no existe,
        # no se lee la ruta del archivo de pasajeros.
        try:
            cooperativa.revisar_que_no_tenga_lanchas()
            ruta_de_lanchas = input("Ruta del archivo de lanchas: ")
            líneas_descartadas = cooperativa.cargar_lanchas(ruta_de_lanchas)
            for mensaje in líneas_descartadas:
                print(mensaje)
            lanchas_cargadas = cooperativa.contar_lanchas()
            print(f"Lanchas cargadas: {lanchas_cargadas}")

            ruta_de_pasajeros = input("\nRuta del archivo de pasajeros: ")
            líneas_descartadas = cooperativa.cargar_pasajeros(ruta_de_pasajeros)
            for mensaje in líneas_descartadas:
                print(mensaje)
            # Decisión: como la carga empieza sin lanchas, todos los días que hay
            # en la cooperativa son los que se cargaron del archivo.
            días_cargados = cooperativa.contar_días_registrados_en_total()
            print(f"Días cargados: {días_cargados}")
        except ValueError as error:
            print(error)
    elif opción == "7":
        salir = True
    else:
        print("La opción no es válida")

    if not salir:
        input("\nPresione Enter para volver al menú...")
