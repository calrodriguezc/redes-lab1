#!/usr/bin/env python3
"""
CLIENTE - Laboratorio de Redes
Genera N peticiones TCP al servidor.

Su unica funcion es producir trafico identificable.
Este programa NO mide tiempos ni calcula estadisticas: eso se hace
con Wireshark sobre las capturas del cliente y del servidor.

Cada peticion lleva un id incremental visible en texto plano, para
poder ubicarla en ambas capturas con el filtro:

    http.request.uri contains "id=42"

Uso:  python cliente.py <IP_DEL_SERVIDOR>
Ej:   python cliente.py 192.168.1.45
"""

import sys
import time
import urllib.request

# ---------------- CONFIGURACION ----------------
PUERTO = 8080
REPETICIONES = 200      # cuantas peticiones generar
ITERACIONES = 100000    # carga de trabajo en el servidor
MEGABYTES = 20          # tamano de la respuesta
PAUSA = 0.5             # segundos entre peticiones (separa las
                        # transacciones en la captura y facilita
                        # emparejarlas a mano)
# -----------------------------------------------


def main():
    if len(sys.argv) < 2:
        print('Uso: python cliente.py <IP_DEL_SERVIDOR>')
        sys.exit(1)

    host = sys.argv[1]

    print(f'Servidor: {host}:{PUERTO}')
    print(f'{REPETICIONES} peticiones | n={ITERACIONES} | {MEGABYTES} MB')
    print(f'Pausa entre peticiones: {PAUSA} s\n')

    ok = 0
    for i in range(1, REPETICIONES + 1):
        url = (f'http://{host}:{PUERTO}/trabajo'
               f'?id={i}&n={ITERACIONES}&mb={MEGABYTES}')
        try:
            resp = urllib.request.urlopen(url)
            datos = resp.read()
            ok += 1
            print(f'  [{i}/{REPETICIONES}] id={i}  '
                  f'{len(datos)} bytes recibidos')
        except Exception as e:
            print(f'  [{i}/{REPETICIONES}] ERROR: {e}')

        if i < REPETICIONES:
            time.sleep(PAUSA)

    print(f'\nListo. {ok}/{REPETICIONES} peticiones completadas.')
    print('Detener ahora las capturas de Wireshark en ambas maquinas.')


if __name__ == '__main__':
    main()
