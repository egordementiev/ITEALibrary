import socket
from Networking.msgutils import send_msg, recv_msg, default_encoding
from time import time
from sympy import isprime

sock = socket.socket()
sock.connect(('127.0.0.1', 5500))


# def is_prime(num):
#     for i in range(2, int(num / 2) + 1):
#         if (num % i) == 0:
#             return False
#     else:
#         return True


start_time = time()
msg = ''
for i in range(2000000):
    if isprime(i):
        msg += f'{i},'
send_msg(msg.encode(default_encoding), sock)
msg = recv_msg(sock)
finish_time = time()
print(f'time = {finish_time-start_time}')

sock.close()
