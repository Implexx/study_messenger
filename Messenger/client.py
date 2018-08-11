import sys
import logging
import time
from socket import socket, AF_INET, SOCK_STREAM
import log.log_config as log_config
from log.log import Log
from errors import WrongModeError
from jim.protocol import JimMessage, JimResponse
from jim.config import *


logger = logging.getLogger('client')
log = Log(logger)


class Client:
    def __init__(self, addr='localhost', port=8888, mode='r'):
        self.addr = addr
        self.port = port
        self.mode = mode
        self.socket = self.__connect()

    @log
    def __connect(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self.addr, self.port))
        return sock

    def main_loop(self):
        presence_msg = JimMessage(action=PRESENCE, time=time.time())
        self.socket.send(bytes(presence_msg))
        presence_response_bytes = self.socket.recv(1024)
        presence_response = JimResponse.create_from_bytes(presence_response_bytes)
        if presence_response.response == OK:
            print('Связь с сервером установлена')
            if self.mode == 'r':
                while True:
                    message_bytes = self.socket.recv(1024)
                    jimmsg = JimMessage.create_from_bytes(message_bytes)
                    print('Вы получили от {} {} сообщеие'.format(self.socket.fileno(),
                                                                 self.socket.getpeername()), jimmsg.message)
            elif self.mode == 'w':
                while True:
                    message = input('Пошлите сообщение в никуда =')
                    msg = JimMessage(action=MSG, time=time.time(), encoding='utf-8', message=message)
                    self.socket.send(bytes(msg))
            else:
                raise WrongModeError(mode)
        elif presence_response.response == SERVER_ERROR:
            print('Ошибка сервера')
        elif presence_response.response == WRONG_REQUEST:
            print('Неверный запрос на сервер')
        else:
            print('Неверный код ответа от сервера')


if __name__ == '__main__':
    addr = 'localhost'
    port = 8888
    try:
        mode = sys.argv[3]
        if mode not in ('r', 'w'):
            print('Режим должен быть или чтение - r, или запись - w')
            sys.exit(0)
    except IndexError:
        mode = 'r'

    client = Client(addr, port, mode)
    client.main_loop()