'''
Функции сервера:
-Встает на прослушку
-Отправляет принимает сообщения

'''

import sys
from socket import socket, AF_INET, SOCK_STREAM
import select
import logging
import log.log_config as log_config
from log.log import Log
from jim.config import *
from jim.protocol import JimMessage, JimResponse


logger = logging.getLogger('server')
log = Log(logger)


class Server:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.socket = self.launch()
        self.clients = []

    def launch(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.addr, self.port))
        sock.listen(30)
        sock.settimeout(0.2)
        return sock

    @log
    def read_requests(self, read_clients):
        all_messages = []
        for sock in read_clients:
            try:
                bytemsg = sock.recv(1024)
                jimmsg = JimMessage.create_from_bytes(bytemsg)
                all_messages.append(jimmsg)
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                self.clients.remove(sock)
        return all_messages

    @log
    def write_responses(self, messages, write_clients):
        for sock in write_clients:
            for message in messages:
                try:
                    sock.send(bytes(message))
                except:
                    print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    self.clients.remove(sock)

    def get_connection(self):
        try:
            conn, addr = self.socket.accept()
            presence_msg_bytes = conn.recv(1024)
            presence_msg = JimMessage.create_from_bytes(presence_msg_bytes)
            if presence_msg.action == PRESENCE:
                presence_response = JimResponse(**{RESPONSE: OK})
                conn.send(bytes(presence_response))
            else:
                presence_response = JimResponse(**{RESPONSE: WRONG_REQUEST})
                conn.send(bytes(presence_response))
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение от {}".format(str(addr)))
            self.clients.append(conn)
        finally:
            wait = 0
            read = []
            write = []
            try:
                read, write, e = select.select(self.clients, self.clients, [], wait)
            except:
                pass

            requests = self.read_requests(read)
            self.write_responses(requests, write)


if __name__ == '__main__':
    print('сервер запущен и вроде работает')
    addr = 'localhost'
    port = 8888
    server = Server(addr, port)
    while True:
        server.get_connection()