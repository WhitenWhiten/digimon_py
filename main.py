from Monster import *
from Monster_rAw import *

save_path: str = './save_files'

if __name__ == '__main__':
    # monster = Monster(123,'2020.11.3 13:09:08', '皮卡丘！', 5, 9, 1, 4, 9, 2, 0, 0, '周可儿')
    # write_monster_to_save_file(monster, './save_files/')
    monster: Monster = read_monster_from_save_files('周可儿', save_path)
    print(monster_to_dict(monster))
    monster.eat()
    print(monster_to_dict(monster))
    monster.eat()
    monster.eat()
    monster.eat()
    monster.care()
    print(monster_to_dict(monster))
    write_monster_to_save_file(monster, save_path)
