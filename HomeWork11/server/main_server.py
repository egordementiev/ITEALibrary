import socket
import asyncio
from time import time
from Networking.msgutils import send_msg, recv_msg, default_encoding
from threading import Thread, Lock
from sympy import isprime

sock = socket.socket()
sock.bind(('localhost', 5500))
sock.listen(1)


# def is_prime(num):
#     for i in range(2, int(num / 2) + 1):
#         if (num % i) == 0:
#             return False
#     else:
#         return True


def load_num_to_file(num):
    with open('numbers.txt', 'a+') as file:
        file.write(f'{num}\n')


# async def work_with_client(conn):
#     while True:
#         msg, msg_type = recv_msg(conn)
#         if not msg:
#             continue
#         msg = msg.decode(default_encoding)
#         if msg == 'finish':
#             conn.close()
#             break
#
#         if not msg.isnumeric():
#             continue
#
#         if is_prime(int(msg)):
#             loop = asyncio.get_event_loop()
#             await loop.run_in_executor(None, load_num_to_file, msg)
#
#             # tr = Thread(target=load_num_to_file, args=(msg,))
#             # tr.start()
#
#             # with open('numbers.txt', 'a+') as file:
#             #     file.write(f'{msg}\n')

# 1 = долго
# 2 = time = 1.5221538543701172

def work_with_client(conn):
    msg, msg_type = recv_msg(conn)
    msg = msg.decode(default_encoding)
    print('recv_msg')

    for i in msg.split(','):
        if not i.isnumeric():
            break
        if isprime(int(i)):
            tr = Thread(target=load_num_to_file, args=(i,))
            tr.start()

            # with open('numbers.txt', 'a+') as file:
            #     file.write(f'{msg}\n')

    send_msg('F'.encode(default_encoding), conn)
    conn.close()


def start_server():
    with open('numbers.txt', 'w') as file:
        file.write('')
    while True:
        conn, _ = sock.accept()
        print('new connection')
        start_time = time()
        work_with_client(conn)
        finish_time = time()
        print(f"time = {finish_time-start_time}")


start_server()
sock.close()
