import json
from .config import *
from .errors import RequiredKeyError, ResponseCodeError, ResponseCodeLenError


class BaseJimMessage:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __bytes__(self):
        message_json = json.dumps(self.__dict__)
        message_bytes = message_json.encode(encoding='utf-8')
        return message_bytes

    @classmethod
    def create_from_bytes(cls, message_bytes):
        message_json = message_bytes.decode(encoding='utf-8')
        message_dict = json.loads(message_json)
        return cls(**message_dict)

    def __str__(self):
        return str(self.__dict__)


class JimMessage(BaseJimMessage):
    def __init__(self, **kwargs):
        if ACTION not in kwargs:
            raise RequiredKeyError(ACTION)
        if TIME not in kwargs:
            raise RequiredKeyError(TIME)
        super().__init__(**kwargs)


class JimResponse(BaseJimMessage):
    def __init__(self, **kwargs):
        if RESPONSE not in kwargs:
            raise RequiredKeyError(RESPONSE)
        code = kwargs[RESPONSE]
        if len(str(code)) != 3:
            raise ResponseCodeLenError(code)
        if code not in RESPONSE_CODES:
            raise ResponseCodeError(code)
        super().__init__(**kwargs)