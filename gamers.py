from Monster import *
import json

class Gamer(object):
    __gamer_id: str
    __gamer_nickname: str
    
    def __init__(self, id: str, nickname: str):
        self.__gamer_id = id
        self.__gamer_nickname = str