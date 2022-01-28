import socket
from Networking.msgutils import send_msg, recv_msg, default_encoding

sock = socket.socket()
sock.connect(('127.0.0.1', 5050))


def is_prime(num):
    for i in range(2, int(num / 2) + 1):
        if (num % i) == 0:
            return False
    else:
        return True


while True:
    msg = ''
    for i in range(20000):
        if is_prime(i):
            msg += f'{i},'
    send_msg(msg.encode(default_encoding), sock)
    send_msg('finish'.encode(default_encoding), sock)
    break
sock.close()
