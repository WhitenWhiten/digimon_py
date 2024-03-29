import math
import json
from PIL import Image

digimon_tiles_image = Image.open('./digimon_resources/monsters.png')
with open('./digimon_resources/digimon_db/db.json', 'r', encoding='utf-8') as db:
    digimon_db = json.load(db)

num_cols: int = 10
num_rows: int = 6
tile_width: int = int(480 / num_cols)
tile_height: int = int(384 / num_rows)


class Digimon(object):
    # the tile is tile_width * tile_height sized
    def load_tile(self) -> None:
        col: int = self.__digimon_id % num_cols
        row: int = int(math.floor(float(self.__digimon_id) / float(num_cols)))
        box = (col * tile_width, row * tile_height, (col + 1) * tile_width, (row + 1) * tile_height)
        self.__digimon_tile = digimon_tiles_image.crop(box)

    def __init__(self, gamer_id: int):
        map_val = digimon_db[str(gamer_id)]
        self.__digimon_id = gamer_id
        self.__digimon_name_cn = map_val['name_cn']
        self.__digimon_name_en = map_val['name_en']
        self.__digimon_skills = map_val['ultimate']
        self.__digimon_intro = map_val['introduction']
        self.__digimon_level = map_val['level']
        self.__digimon_attribute = map_val['attribute']
        self.__digimon_type = map_val['digimon_type']
        self.__digimon_first_take = map_val['first_take']
        self.__digimon_colorful = f'./digimon_resources/digimon_db/{self.__digimon_name_en}.jpg'
        self.load_tile()

    def get_first_take(self) -> str:
        return self.__digimon_first_take

    def get_type(self) -> str:
        return self.__digimon_type

    def get_attribute(self) -> str:
        return self.__digimon_attribute

    def get_level(self) -> str:
        return self.__digimon_level

    def get_tile(self) -> Image:
        return self.__digimon_tile

    def get_skills(self) -> list:
        return self.__digimon_skills

    def get_skills_str(self) -> str:
        ret = ''
        for skill in self.__digimon_skills:
            ret += skill + '、'
        return ret[:-1]

    def get_name_cn(self) -> str:
        return self.__digimon_name_cn

    def get_name_en(self) -> str:
        return self.__digimon_name_en

    def get_colorful_path(self) -> str:
        return self.__digimon_colorful

    def get_intro(self) -> list:
        return self.__digimon_intro


digimons: dict = {}
for i in range(0, 60):
    digimons[i] = Digimon(i)

digimon_tiles_image = None  # 释放原图片资源
digimon_db = None
for digimon in digimons.keys():
    print(str(digimon) + ': ' + digimons[digimon].get_name_cn() + ' loaded.')
