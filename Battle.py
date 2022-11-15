from .Gamers import *

in_battle: set = set()
battle_fields: dict = {}
battle_id: int = 1


def register_battle_field(id1: str, id2: str) -> int:
    global battle_id
    battle_field_id = battle_id
    battle_id += 1
    battle_fields[battle_field_id] = (id1, id2)
    return battle_field_id


def clean_battle_field(b_id: int) -> None:
    (id1, id2) = battle_fields.pop(b_id)
    in_battle.remove(id1)
    in_battle.remove(id2)


def get_fighters(b_id: int):
    battle = battle_fields[b_id]
    return battle[0], battle[1]


# 返回战场编号，如果两者在战斗中或者无法战斗或者还没获得数码宝贝则返回-1
def register_battle(id1: str, id2: str) -> int:
    if id1 is id2:
        return -1
    elif (id1 in in_battle) or (id2 in in_battle):  # in battle
        return -1
    elif (not is_id_registered(id1)) or (not is_id_registered(id2)):  # not registered
        return -1
    elif (get_Monster_by_gamer_id(id1).get_hp() == 0) or (get_Monster_by_gamer_id(id2).get_hp() == 0):  # no hp
        return -1
    else:
        in_battle.add(id1)
        in_battle.add(id2)  # 将两个用户id注册到in_battle集合中
        return register_battle_field(id1, id2)  # 分配战场


def generate_process(b_id: int) -> str:
    id1, id2 = get_fighters(b_id)
    mon1 = get_Monster_by_gamer_id(id1)
    mon2 = get_Monster_by_gamer_id(id2)
    nickname1 = mon1.get_nickname()
    nickname2 = mon2.get_nickname()
    digimon_name1 = nickname1 if nickname1 != '' else mon1.get_concreate_digimon().get_name_cn()
    digimon_name2 = nickname2 if nickname2 != '' else mon2.get_concreate_digimon().get_name_cn()
    hp1 = [mon1.get_hp()]
    hp2 = [mon2.get_hp()]  # 用[]包装成对象，方便后面用eval操作
    dmg1 = (mon1.get_min_damage(), mon1.get_max_damage())
    dmg2 = (mon2.get_min_damage(), mon2.get_max_damage())
    skills1 = mon1.get_concreate_digimon().get_skills()
    skills2 = mon2.get_concreate_digimon().get_skills()
    faster = random.choice((1, 2))  # 随机选择更快的
    slower = ({1, 2} - {faster}).pop()  # 通过集合操作获取较慢的一个
    process = f'这是属于{id1}的{digimon_name1}和{id2}的{digimon_name2}的战斗:\n'
    process += '速度更快的是' + eval('digimon_name' + str(faster)) + '\n'
    actor = faster
    waiter = slower
    while True:
        dmg = eval('dmg' + str(actor))
        damage = random.randint(dmg[0], dmg[1])
        skill = random.choice(eval('skills' + str(actor)))
        acter_name = eval('digimon_name' + str(actor))
        process += f'{acter_name}使用了{skill},造成了{damage}点伤害！\n'
        eval('hp' + str(waiter))[0] = eval('hp' + str(waiter))[0] - damage
        if eval('hp' + str(waiter))[0] <= 0:
            break
        temp = actor  # 回合更替
        actor = waiter
        waiter = temp

    # 退出while时，acter是谁，谁就是winner(因为退出条件是waiter血量<=0)
    winner = eval('mon' + str(actor))
    winner_name = eval('digimon_name' + str(actor))
    loser = eval('mon' + str(waiter))
    loser_name = eval('digimon_name' + str(waiter))
    process += f'{winner_name}({winner.get_owner()})击败了{loser_name}({loser.get_owner()})! 恭喜！'
    winner.victory()  # 更新胜者胜利数
    loser.defeated()  # 更新败者战败数
    winner.update_hp(eval('hp' + str(actor))[0])  # 胜者血量即为战斗结束后的血量
    loser.update_hp(0)  # 败者血量可能为负，此时将其更新为0即可
    win_evolve_or_not = winner.evolve()  # 胜利者尝试进化
    lose_evolve_or_not = loser.evolve()  # 败者尝试进化
    process += f'\n{winner_name}进化了！' if win_evolve_or_not else ''
    process += f'\n{loser_name}进化了！' if lose_evolve_or_not else ''
    clean_battle_field(b_id)
    return process
