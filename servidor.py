#!/usr/bin/env python3
"""
SERVIDOR - Laboratorio de Redes
Servidor HTTP (TCP) con carga computacional.

Su unica funcion es: recibir una peticion, TRABAJAR (gastar CPU) y
responder con un volumen de datos.

Este programa NO mide tiempos. Las mediciones se hacen con Wireshark.

Uso:  python servidor.py
"""

import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PUERTO = 8080

# Se genera una sola vez al arrancar para que el tiempo de respuesta
# corresponda al procesamiento y no a la creacion de los datos.
BLOQUE_1MB = (b'A' * 1024) * 1024


class Manejador(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"      # HTTP 1.1 sobre TCP, sin TLS

    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)

        req_id = q.get('id', ['0'])[0]
        n_iter = int(q.get('n', ['200000'])[0])
        mb = int(q.get('mb', ['50'])[0])

        # ---- CARGA: el servidor procesa antes de contestar ----
        h = hashlib.sha256(req_id.encode())
        for _ in range(n_iter):
            h = hashlib.sha256(h.digest())
        # -------------------------------------------------------

        cuerpo = BLOQUE_1MB * mb

        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', str(len(cuerpo)))
        # Viaja en texto plano -> permite identificar la respuesta en Wireshark
        self.send_header('X-Req-Id', req_id)
        self.end_headers()
        self.wfile.write(cuerpo)

        print(f'  atendida peticion id={req_id}', flush=True)

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    servidor = ThreadingHTTPServer(('0.0.0.0', PUERTO), Manejador)
    print(f'Servidor escuchando en el puerto {PUERTO} (TCP)')
    print('Ctrl+C para detener\n')
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor detenido.')
