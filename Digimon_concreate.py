import math
import json
from PIL import Image

digimon_tiles_image = Image.open('./digimon_resources/monsters.png')
with open('./digimon_resources/digimon_db/db.json','r') as db:
    digimon_db: dict = json.load(db)

num_cols: int = 10
num_rows: int = 6
tile_width: int = int(480 / num_cols)
tile_height: int = int(384 / num_rows)

class Digimon(object):
    __digimon_id: int = 0
    __digimon_name_cn: str = ''
    __digimon_name_en: str = ''
    __digimon_skills: str = ''
    __digimon_tile: Image = None
    __digimon_colorful: Image = None
    __digimon_intro: list = None
    __digimon_level: str = ''
    __digimon_attribute: str = ''
    __digimon_type: str = ''
    __digimon_first_take: str = ''
    
    # the tile is tile_width * tile_height sized
    def load_tile(self) -> None:
        col: int = self.__digimon_id % num_cols
        row: int = int(math.floor(float(self.__digimon_id) / float(num_cols)))
        box = (col * tile_width, row * tile_height, (col + 1) * tile_width, (row + 1) * tile_height)
        self.__digimon_tile = digimon_tiles_image.crop(box)
        
    def load_colorful(self) -> None:
        self.__digimon_colorful = Image.open(f'./digimon_resources/digimon_db/{self.get_name_en()}.jpg')
        
    def __init__(self, id: int):
        map_val = digimon_db[str(id)]
        self.__digimon_id = id
        self.__digimon_name_cn = map_val['name_cn']
        self.__digimon_name_en = map_val['name_en']
        self.__digimon_skills = map_val['ultimate']
        self.__digimon_intro = map_val['introduction']
        self.__digimon_level = map_val['level']
        self.__digimon_attribute = map_val['attribute']
        self.__digimon_type = map_val['digimon_type']
        self.__digimon_first_take = map_val['first_take']
        self.load_colorful()
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
    
    def get_skills(self) -> str:
        return self.__digimon_skills
    
    def get_name_cn(self) -> str:
        return self.__digimon_name_cn
    
    def get_name_en(self) -> str:
        return self.__digimon_name_en
    
    def get_colorful(self) -> Image:
        return self.__digimon_colorful
        
    def get_intro(self) -> list:
        return self.__digimon_intro
    
digimons: dict = {}
for i in range(0, 60):
    digimons[i] = Digimon(i)

digimon_tiles_image = None  #释放原图片资源
digimon_db = None