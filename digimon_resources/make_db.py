import json
from bs4 import BeautifulSoup
from PIL import Image


class Digimon_entry(object):
    name_cn: str = ''   # 中文名
    name_en: str = ''   # 英文名
    level: str  = ''    # 幼年型-成熟型-究极体
    digimon_type: str = ''   # 病毒型、改造型
    attribute: str = '' # 自由、疫苗等等
    first_take: str = '' # 初次登场
    ultimate: list = None  #必杀技
    introduction: list = None # 6种语言的介绍
    
    def __init__(self):
        self.ultimate = []
        self.introduction = []

with open('./correct_name_set.json','r') as ns:
    digimon_names = json.load(ns)

entries: dict = []

def entry_to_dict(entry: Digimon_entry) -> dict:
    return {'name_cn':entry.name_cn, 'name_en':entry.name_en,
            'level':entry.level, 'digimon_type':entry.digimon_type,
            'attribute':entry.attribute, 'first_take':entry.first_take,
            'ultimate':entry.ultimate, 'introduction':entry.introduction
            }


url = './digimons/{}/'    
for name in digimon_names:
    temp_entry = Digimon_entry()
    html_url_concreate = url.format(name) + f'{name}.html'
    image_url_concreate = url.format(name) + f'{name}.jpg'
    Image.open(image_url_concreate).save(f'./digimon_db/{name}.jpg')
    with open(html_url_concreate, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
    temp_entry.name_en = name
    temp_entry.name_cn = soup.article.h2.text.split(" ",1)[0]
    table_nodes = soup.find_all('td')
    temp_entry.level = table_nodes[0].text  # 比如，完全体
    temp_entry.digimon_type = table_nodes[1].text # 比如，改造型
    temp_entry.attribute = table_nodes[2].text # 比如，疫苗
    temp_entry.first_take = table_nodes[5].text
    for i in range(7,100,3):
        if i < len(table_nodes):
            temp_entry.ultimate.append(table_nodes[i].text)
        else:
            break
        
    for language in ['简体中文', '繁體中文', '日本語', 'English', '한국어', 'Deutsch']:
        tag_set = soup.find_all(attrs={'data-tab': language})
        if len(tag_set):
            temp_entry.introduction.append(tag_set[0].text[1:-1])
            
    entries.append({str(digimon_names.index(name)):entry_to_dict(temp_entry)})
    
with open('./digimon_db/db.json','w',encoding='utf-8') as db:
    json.dump(entries, db, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)    
    
