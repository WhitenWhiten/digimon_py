import io
import json
import requests
import time
import os
from PIL import Image

with open('./correct_name_set.json','r') as digifile:
    digimons = json.load(digifile)
print(f'{len(digimons)} digimons are loaded.')

url_text = 'http://www.digimons.net/digimon/{}/index.html'
url_image = 'http://www.digimons.net/digimon/{}/{}.jpg'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

for k in digimons:
    os.mkdir('./digimons/' + k)
    url_text_concreate = url_text.format(k)
    url_image_concreate = url_image.format(k,k)
    image_response = requests.get(url_image_concreate)
    if(not image_response.status_code == 200):
        print(f'{k}:fail to fetch, maybe the name is false.\n')
        continue
    try:
        image = Image.open(io.BytesIO(image_response.content))
        image.save(f'./digimons/{k}/{k}.jpg')
    finally:
        image = None
    
    with open(f'./digimons/{k}/{k}.html','w', encoding='utf-8') as towrite:    
        x = requests.get(url_text_concreate,headers=header)
        x.encoding='utf-8'
        towrite.write(x.text)
    time.sleep(3)    