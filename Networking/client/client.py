import socket
from Networking.msgutils import send_msg, recv_msg, default_encoding

sock = socket.socket()
sock.connect(('127.0.0.1', 5050))

while True:
    msg, msg_type = recv_msg(sock)
    if not msg:
        continue
    msg = msg.decode(default_encoding)
    print(msg)
    if msg_type == 'statement':
        continue

    # узер вводит комманду
    while True:
        msg = input('')
        if not msg:
            continue
        break

    if msg in ['end_connection', 'stop_server']:
        send_msg(msg.encode(default_encoding), sock)
        msg, msg_type = recv_msg(sock)
        if not msg:
            continue
        msg = msg.decode(default_encoding)
        print(msg)
        break
    send_msg(msg.encode(default_encoding), sock)

sock.close()
