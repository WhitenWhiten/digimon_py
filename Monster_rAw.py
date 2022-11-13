from Monster import *
import json
import os

from Monster import Monster


def read_monster_from_save_files(owner: str, dir: str) -> Monster | None:
    save_path = dir + '/' + owner + '.json'
    if not os.path.exists(save_path):
        return None
    else:
        with open(save_path, 'r') as save_file:
            temp: dict = json.load(save_file)
        return Monster(int(temp['id']), temp['birthday'], temp['nickname'], int(temp['last_fed']),
                       int(temp['last_care']), int(temp['hp']), int(temp['max_hp']),
                       int(temp['min_dmg']), int(temp['max_dmg']), int(temp['wins']),
                       int(temp['losses']), temp['owner'])


def monster_to_dict(monster: Monster) -> dict:
    ret: dict = {'id': monster.get_id(), 'birthday': monster.get_birthday(),
                 'nickname': monster.get_nickname(), 'last_fed': monster.get_last_fed_time_stamp(),
                 'last_care': monster.get_last_care_time_stamp(), 'hp': monster.get_hp(),
                 'max_hp': monster.get_max_hp(), 'min_dmg': monster.get_min_damage(),
                 'max_dmg': monster.get_max_damage(), 'wins': monster.get_wins(),
                 'losses': monster.get_losses(), 'owner': monster.get_owner()}
    return ret


def write_monster_to_save_file(monster: Monster, dir: str) -> None:
    save_path = dir + '/' + monster.get_owner() + '.json'
    with open(save_path, 'w') as save_file:
        json.dump(monster_to_dict(monster), save_file)
