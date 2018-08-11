"""Константы и настройки"""

ENCODE = 'utf-8'

# Ключи протокола (действия)

ACTION = 'action'
TIME = 'time'
USER = 'user'
ERROR = 'error'
ACCOUNT_NAME = 'account_name'
RESPONSE = 'response'
REQUIRED_MESSAGE_KEYS = (ACTION, TIME)
REQUIRED_RESPONSE_KEYS = (RESPONSE,)

# Значения протокола

PRESENCE = 'presence'
MSG = 'msg'
QUIT = 'quit'
ACTIONS = (PRESENCE, MSG, QUIT)

# Коды ответов сервера

BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400
SERVER_ERROR = 500
RESPONSE_CODES = (BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR)