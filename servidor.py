#!/usr/bin/env python3
"""
SERVIDOR - Laboratorio de Redes
Servidor HTTP (TCP) con carga computacional.

Recibe una peticion, TRABAJA (gasta CPU) y responde con un volumen
de datos. No mide tiempos: las mediciones se hacen con Wireshark.

Uso:  python servidor.py
"""

import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PUERTO = 8080

# Cache de cuerpos de respuesta.
# Se construyen UNA sola vez por tamano solicitado. Sin esto, reservar
# y copiar decenas de MB en cada peticion introduce una variacion de
# cientos de ms que contamina el tiempo de respuesta del servidor.
_CACHE = {}
_BLOQUE_1MB = (b'A' * 1024) * 1024


def cuerpo_de(mb):
    if mb not in _CACHE:
        _CACHE[mb] = _BLOQUE_1MB * mb
    return _CACHE[mb]


class Manejador(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"      # HTTP 1.1 sobre TCP, sin TLS

    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)

        req_id = q.get('id', ['0'])[0]
        n_iter = int(q.get('n', ['100000'])[0])
        mb = int(q.get('mb', ['20'])[0])

        cuerpo = cuerpo_de(mb)         # ya esta en memoria, costo ~0

        # ---- CARGA: unico trabajo real antes de contestar ----
        h = hashlib.sha256(req_id.encode())
        for _ in range(n_iter):
            h = hashlib.sha256(h.digest())
        # ------------------------------------------------------

        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', str(len(cuerpo)))
        # Viaja en texto plano -> identifica la respuesta en Wireshark
        self.send_header('X-Req-Id', req_id)
        self.end_headers()
        self.wfile.write(cuerpo)

        print(f'  atendida peticion id={req_id}', flush=True)

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    # Precarga los tamanos habituales para que la primera peticion
    # no pague el costo de construir el cuerpo.
    for _mb in (20, 50):
        cuerpo_de(_mb)

    servidor = ThreadingHTTPServer(('0.0.0.0', PUERTO), Manejador)
    print(f'Servidor escuchando en el puerto {PUERTO} (TCP)')
    print('Ctrl+C para detener\n')
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor detenido.')
