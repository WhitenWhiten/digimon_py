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

entries: dict = {}

def entry_to_dict(entry: Digimon_entry) -> dict:
    return {'name_cn':entry.name_cn, 'name_en':entry.name_en,
            'level':entry.level, 'digimon_type':entry.digimon_type,
            'attribute':entry.attribute, 'first_take':entry.first_take,
            'ultimate':entry.ultimate, 'introduction':entry.introduction
            }

def is_chinese(s: str) -> bool:
    for c in s:
        if not ('\u4e00' <= c <= '\u9fff'):
            return False
    return True


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
    table_nodes = soup.find_all('tr')
    for tr in table_nodes:
        if not (tr.th is None):
            datatype = tr.th.text
            match datatype:
                case '等级':
                    temp_entry.level = tr.td.text
                case '类型':
                    temp_entry.digimon_type = tr.td.text
                case '属性':
                    temp_entry.attribute = tr.td.text
                case '首次登场':
                    temp_entry.first_take = tr.td.text
            
    h3s = soup.find_all('h3')
    for h3 in h3s:
        match h3.text:
            case '基本资料':
                trs = h3.next_sibling.next_sibling.find_all('tr')
                for tr in trs:
                    if hasattr(tr,'th'):
                        datatype = tr.th.text
                        match datatype:
                            case '等级':
                                temp_entry.level = tr.td.text
                            case '类型':
                                temp_entry.digimon_type = tr.td.text
                            case '属性':
                                temp_entry.attribute = tr.td.text
                            case '首次登场':
                                temp_entry.first_take = tr.td.text
            case '必杀技＆得意技':
                #在这里处理必杀技
                trs = h3.next_sibling.next_sibling.find_all('tr')
                for tr in trs:
                    temp_entry.ultimate.append(tr.td.text)  #只存放打头的中文
            case '设定资料':
                #在这里处理设定
                intros = h3.next_sibling.next_sibling
                for language in ['简体中文', '繁體中文', '日本語', 'English', '한국어', 'Deutsch']:
                    tag_set = intros.find_all(attrs={'data-tab': language})
                    if len(tag_set):
                        temp_entry.introduction.append(tag_set[0].p.text)
    
    entries[str(digimon_names.index(name))] = entry_to_dict(temp_entry)
    
with open('./digimon_db/db.json','w',encoding='utf-8') as db:
    json.dump(entries, db, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)    
    
