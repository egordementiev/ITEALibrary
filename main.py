import socket
from Networking.msgutils import send_msg, recv_msg, default_encoding


sock = socket.socket()
sock.bind(('localhost', 1234))

sock.listen(1)

conn, addr = sock.accept()

# print(f'Connected client: {addr}')
#
# data = recv_msg(conn)
# if data:
#     send_msg(data.upper(), conn)
#
# send_msg('hello from server'.encode(default_encoding), conn)
# data = recv_msg(conn)
# if data:
#     print(data)

data = recv_msg(conn)
print(data.decode(default_encoding))

send_msg('Thanks'.encode(default_encoding), conn)

conn.close()