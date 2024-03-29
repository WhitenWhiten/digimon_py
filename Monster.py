# Monster class Converted from java version
from .Digimon_concreate import *
import arrow
import random

random.seed()


class Monster(object):
    def __init__(self, digimon_id: int, birthday: str, nickname: str, last_fed_time_stamp: int,
                 last_care_time_stamp: int, hp: int, max_hp: int, min_damage: int,
                 max_damage: int, wins: int, losses: int, owner: str):
        self.__nickname = nickname
        self.__id = digimon_id
        self.__birthday = birthday
        self.__last_fed_time_stamp = last_fed_time_stamp
        self.__last_care_time_stamp = last_care_time_stamp
        self.__hp = hp
        self.__max_hp = max_hp
        self.__min_damage = min_damage
        self.__max_damage = max_damage
        self.__wins = wins
        self.__losses = losses
        self.__owner = owner

    def get_concreate_digimon(self) -> Digimon:
        return digimons[self.__id]

    def get_id(self) -> int:
        return self.__id

    def get_owner(self) -> str:
        return self.__owner

    def get_birthday(self) -> str:
        return self.__birthday

    def get_days_old(self) -> int:
        birthday_stamp = arrow.get(self.__birthday).timestamp()
        now_stamp = arrow.utcnow().timestamp()
        return int((birthday_stamp - now_stamp) / (1000 * 60 * 60 * 24))

    def get_last_fed_time_stamp(self) -> int:
        return self.__last_fed_time_stamp

    def get_last_care_time_stamp(self) -> int:
        return self.__last_care_time_stamp

    def get_hours_since_last_cared(self) -> int:
        diff = self.get_last_care_time_stamp() - arrow.utcnow().timestamp()
        return int(diff / (1000 * 60 * 60))

    def get_nickname(self) -> str:
        return self.__nickname

    def set_nickname(self, new_name: str) -> None:
        self.__nickname = new_name

    def get_hp(self) -> int:
        return self.__hp

    def get_max_hp(self) -> int:
        return self.__max_hp

    def get_min_damage(self) -> int:
        return self.__min_damage

    def get_max_damage(self) -> int:
        return self.__max_damage

    def get_wins(self) -> int:
        return self.__wins

    def get_losses(self) -> int:
        return self.__losses

    def care(self) -> None:
        self.__last_care_time_stamp = int(arrow.utcnow().timestamp())

    def update_hp(self, new_hp: int) -> None:
        self.__hp = new_hp
        if self.__hp > self.__max_hp:
            self.__hp = self.__max_hp
        elif self.__hp < 0:
            self.__hp = 0

    def eat(self) -> None:
        self.update_hp(self.get_max_hp())
        self.__last_fed_time_stamp = int(arrow.utcnow().timestamp())

    def starve(self) -> None:
        self.update_hp(self.get_hp() - 1)

    def victory(self) -> None:
        self.__wins += 1

    def defeated(self) -> None:
        self.__losses += 1

    def can_fight(self) -> bool:
        return self.get_hp != 0

    def get_exp(self) -> float:
        return float(self.__wins) + 0.5 * float(self.__losses)

    def can_evolve(self) -> bool:
        if self.get_exp() > 8.0 and self.get_id() < 10:
            return True
        elif self.get_exp() > 15.0 and 10 <= self.get_id() < 20:
            return True
        elif self.get_exp() > 27.0 and 20 <= self.get_id() < 30:
            return True
        elif self.get_exp() > 35.0 and 30 <= self.get_id() < 40:
            return True
        elif self.get_exp() > 50.0 and 40 <= self.get_id() < 50:
            return True
        else:
            return False

    # 成功进化则返回True
    def evolve(self) -> bool:
        if not self.can_evolve():
            return False
        else:
            self.__id += 10  # 对应图片中下一列同一行的digimon,即现在的digimon的进化体
            self.__max_hp += random.randint(3, 5)  # 最大hp随机增加
            self.__hp = self.__max_hp  # 回满hp
            self.__max_damage += random.randint(1, 2)
            self.__min_damage += 1
            return True

    def get_concreate_name(self) -> str:
        return self.get_concreate_digimon().get_name_cn()

    def get_info(self) -> str:
        c_digimon = self.get_concreate_digimon()
        ret = f'Digimon: {self.get_concreate_name()}\n等级:{c_digimon.get_level()}\n昵称：{self.get_nickname()}\n'
        ret += f'初次登场:{c_digimon.get_first_take()}\n技能:{c_digimon.get_skills_str()}\n信息:{c_digimon.get_intro()[0]}'
        return ret
