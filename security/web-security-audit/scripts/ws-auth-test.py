#!/usr/bin/env python3
"""WebSocket auth probe — checks whether a socket server accepts unauthenticated connections.

Usage: python3 ws-auth-test.py <host> [path]
Path defaults to /socket.io/?EIO=4&transport=websocket (Socket.IO).
Other common paths: /ws

What a GOOD (authenticated) server does after 101:
  - sends an error/close packet (e.g. 4{"message":"Authentication required"})
  - or closes the connection
What a BAD server does:
  - issues a session id: {"sid":"...","pingInterval":...}  <- auth gap confirmed

Exit: 0 = auth enforced (error/close), 1 = auth gap (sid issued), 2 = connection failed
"""
import socket, ssl, base64, os, time, select, sys

def probe(host, path, port=443):
    ctx = ssl.create_default_context()
    raw = socket.create_connection((host, port), timeout=8)
    s = ctx.wrap_socket(raw, server_hostname=host)
    key = base64.b64encode(os.urandom(16)).decode()
    req = (f'GET {path} HTTP/1.1\r\n'
           f'Host: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
           f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n'
           f'Origin: https://{host}\r\n\r\n')
    s.sendall(req.encode())
    resp = s.recv(2048).decode(errors='replace')
    status = resp.split('\r\n')[0]
    time.sleep(1)
    s.setblocking(False)
    r, _, _ = select.select([s], [], [], 3)
    payload = ''
    if r:
        try:
            payload = s.recv(4096).decode(errors='replace')
        except Exception:
            pass
    s.close()
    return status, payload

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    host = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else '/socket.io/?EIO=4&transport=websocket'
    status, payload = probe(host, path)
    print('status:', status)
    print('server sent:', repr(payload[:200]))
    if '101' not in status:
        print('RESULT: connection rejected before upgrade (or non-WS path)')
        sys.exit(2)
    if '"sid"' in payload:
        print('RESULT: AUTH GAP — server issued session id without a token')
        sys.exit(1)
    print('RESULT: auth enforced — no session issued to unauthenticated client')
    sys.exit(0)
