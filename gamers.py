from Monster import *
import json
import os
import random
import arrow
from timeloop import Timeloop
from datetime import timedelta
import threading

# 用于定时调用save_gamers
timer = Timeloop()
# 用于保护gamers的锁
lock = threading.Lock()
# 初始化种子
random.seed()
save_path = './gamers.json'


def read_gamers() -> dict | None:
    if not os.path.exists(save_path):
        return None
    else:
        with open(save_path, 'r', encoding='utf-8') as save_file:
            temp: dict = json.load(save_file)
        ret = {}
        if len(temp) == 0:
            return ret
        for k in temp.keys():
            val = temp[k]
            ret[str(k)] = Monster(int(val['id']), val['birthday'], val['nickname'],
                                  int(val['last_fed']), int(val['last_care']),
                                  int(val['hp']), int(val['max_hp']),
                                  int(val['min_dmg']), int(val['max_dmg']),
                                  int(val['wins']), int(val['losses']),
                                  val['owner'])
        return ret


# 从id(str)到Monster对象的映射
gamers: dict = read_gamers()


def get_Monster_by_id(gamer_id: str) -> Monster:
    lock.acquire()
    ret = gamers[gamer_id]
    lock.release()
    return ret


def get_all_id():
    lock.acquire()
    ret = gamers.keys()
    lock.release()
    return ret


def is_id_registered(gamer_id: str) -> bool:
    return gamer_id in get_all_id()


# maps attribute of a monster to a seq dict
def monster_to_dict(monster: Monster) -> dict:
    ret: dict = {'id': monster.get_id(), 'birthday': monster.get_birthday(),
                 'nickname': monster.get_nickname(), 'last_fed': monster.get_last_fed_time_stamp(),
                 'last_care': monster.get_last_care_time_stamp(), 'hp': monster.get_hp(),
                 'max_hp': monster.get_max_hp(), 'min_dmg': monster.get_min_damage(),
                 'max_dmg': monster.get_max_damage(), 'wins': monster.get_wins(),
                 'losses': monster.get_losses(), 'owner': monster.get_owner()}
    return ret


# 保存gamers，每5min自动调用一次
@timer.job(interval=timedelta(minutes=5))
def save_gamers() -> None:
    lock.acquire()
    to_save = {}
    for gamer in gamers.keys():
        to_save[gamer] = monster_to_dict(gamers[gamer])
    lock.release()
    with open(save_path, 'w', encoding='utf-8') as save_file:
        json.dump(to_save, save_file, indent=4, separators=(',', ': '), ensure_ascii=False)


def random_monster(monster_owner: str) -> Monster:
    now = arrow.utcnow()
    random_id = random.randint(0, 9)
    random_max_hp = random.randint(9, 12)
    random_max_dmg = random.randint(3, 5)
    return Monster(id=random_id, birthday=str(now), nickname='',
                   last_care_time_stamp=int(now.timestamp()), last_fed_time_stamp=int(now.timestamp()),
                   hp=random_max_hp, max_hp=random_max_hp, max_damage=random_max_dmg,
                   min_damage=random_max_dmg - 3, wins=0, losses=0, owner=monster_owner)


# if the gamer has existed, return false
def add_gamer(gamer_id: str) -> bool:
    lock.acquire()
    if not (gamers.get(gamer_id) is None):
        lock.release()
        return False
    else:
        gamers[gamer_id] = random_monster(gamer_id)
        lock.release()
        return True
