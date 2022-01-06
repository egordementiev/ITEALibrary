from socket import socket

default_msg_type = 'question'
default_header_size = 10
default_msg_type_size = 10
default_pack_size = 5
default_encoding = '866'


def send_msg(msg: bytes, conn: socket, msg_type: str = default_msg_type, header_size: int = default_header_size,
             msg_type_size: int = default_msg_type_size) -> bool:
    # определяем размер сообщения, готовим заголовок
    msg_size = f'{len(msg):{header_size}}'

    # отправляем заголовок
    if conn.send(msg_size.encode(default_encoding)) != header_size:
        print(f'ERROR: can\'t send size message')
        return False

    msg_type = f'{msg_type:{msg_type_size}}'

    # отправляем тип сообщения (вопрос/утверждение)
    if conn.send(msg_type.encode(default_encoding)) != msg_type_size:
        print(f'ERROR: can\'t send size message')
        return False

    # отправляем сообщение
    if conn.send(msg) != len(msg):
        print(f'ERROR: can\'t send message')
        return False

    return True


def recv_msg(conn: socket, header_size: int = default_header_size,
             pack_size: int = default_pack_size,
             msg_type_size: int = default_msg_type_size) -> [bytes, str]:

    # читаем заголовок, в котором размер последующего сообщения
    data = conn.recv(header_size)
    if not data or len(data) != header_size:
        print(f'ERROR: can\'t read size message')
        return [None, None]

    size_msg = int(data.decode(default_encoding))

    # читаем заголовок, в котором  тип последующего сообщения
    msg_type = conn.recv(msg_type_size).decode(default_encoding)
    if not msg_type or len(msg_type) != msg_type_size:
        print(f'ERROR: can\'t read size message')
        return [None, None]

    msg_type = msg_type.replace(' ', '')

    msg = b''

    while True:
        if size_msg <= pack_size:
            pack = conn.recv(size_msg)
            if not pack:
                return [None, None]

            msg += pack
            break

        pack = conn.recv(pack_size)
        if not pack:
            return [None, None]

        size_msg -= pack_size
        msg += pack

    return [msg, msg_type]
