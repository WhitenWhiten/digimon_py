from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from .Battle import *
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)


def hatch(gamer_id: str) -> str:
    if add_gamer(gamer_id):
        return f'你孵化出的是{get_Monster_by_gamer_id(gamer_id).get_concreate_name()}!一起成为最强的搭档吧！'
    else:
        return '错误的！你已经有了自己的数码宝贝哦!'


def care(gamer_id: str) -> str:
    if not is_gamer(gamer_id):
        return '请先孵蛋!'
    else:
        get_Monster_by_gamer_id(gamer_id).care()
        return f'照顾成功！和{get_Monster_by_gamer_id(gamer_id).get_concreate_name()}的关系更亲密了！'


def set_nickname(gamer_id: str, new_nickname: str) -> str:
    if not is_gamer(gamer_id):
        return '请先孵蛋'
    else:
        get_Monster_by_gamer_id(gamer_id).set_nickname(new_nickname)
        return f'成功将{get_Monster_by_gamer_id(gamer_id).get_concreate_name()}的昵称设定为{new_nickname}'


def feed(gamer_id: str) -> str:
    if not is_gamer(gamer_id):
        return '请先孵蛋'
    else:
        get_Monster_by_gamer_id(gamer_id).eat()
        return '喂食成功！精神满满！'


def info(gamer_id: str) -> str:
    if not is_gamer(gamer_id):
        return '请先孵蛋'
    else:
        return get_Monster_by_gamer_id(gamer_id).get_info()


alias = {'数码宝贝'}
digimon = on_command(cmd='digimon', aliases=alias, priority=15)

help_msg = '暂时懒得写，反正有孵蛋、照顾、喂食、查看昵称、修改昵称、信息这些功能，战斗还没写'


@digimon.handle()
async def _(event: MessageEvent, matcher=Matcher, msg: Message = CommandArg()):
    command = str(msg[0]) if msg[0].is_text() else None
    if command is None:
        await matcher.finish("错误的命令哦！请查看帮助orz", at_sender=True)
    else:
        reply = ''
        user_id = str(event.user_id)
        if command == '孵蛋' or command == 'hatch':
            reply = hatch(user_id)
        elif command == '照顾' or command == 'care':
            reply = care(user_id)
        elif command == '喂食' or command == 'feed':
            reply = feed(user_id)
        elif command == '昵称' or command == 'nickname':
            nickname = get_Monster_by_gamer_id(user_id).get_nickname()
            reply = '没有昵称哦~' if nickname == '' else nickname
        elif command == '信息' or command == 'info':
            reply = info(user_id)
        elif command == '帮助' or command == 'help':
            reply = help_msg
        elif command == '对战' or command == 'fight':
            reply = '暂未支持,忙完这几天写'
        elif command == '图片' or command == 'photo':
            if not is_gamer(user_id):
                reply = '请先孵蛋'
            else:
                pic_path = get_Monster_by_gamer_id(user_id).get_concreate_digimon().get_colorful_path()
                await matcher.finish(MessageSegment.image(pic_path), at_sender=True)
        elif command == 'remake' or command == '重开':
            remake(user_id)
            reply = '重开成功,去孵蛋吧~'
        else:
            reply = '暂未支持'
        await matcher.finish(reply, at_sender=True)


digimon_nickname_changer = on_command('修改昵称', aliases={'change_nickname', 'nickname_change'}, priority=15)


@digimon_nickname_changer.handle()
async def nick_handler(event: MessageEvent, msg: Message = CommandArg(), matcher=Matcher):
    user_id = str(event.user_id)
    if not is_gamer(user_id):
        await matcher.finish('请先孵蛋', at_sender=True)
    else:
        plain_text = msg.extract_plain_text()
        if plain_text:
            get_Monster_by_gamer_id(user_id).set_nickname(plain_text)
            await matcher.finish(f'现在你的数码宝贝的昵称是{plain_text}', at_sender=True)
        else:
            await matcher.finish('请给出正确的昵称', at_sender=True)


digimon_battle = on_command('battle-with', aliases={'与敌对峙', '数码对战'}, priority=15)


@digimon_battle.handle()
async def battle_handle(event: MessageEvent, msg: Message = CommandArg(), matcher=Matcher):
    user_id = str(event.user_id)
    if not is_gamer(user_id):
        await matcher.finish('请先孵蛋', at_sender=True)
    elif len(msg) != 1 and msg[0].type != 'at':
        await matcher.finish('请@一位群成员', at_sender=True)
    else:
        the_other_id = msg[0].data['qq']    # 被对战者的qq
        battle_field = register_battle(user_id, the_other_id)
        if battle_field == -1:
            await matcher.finish('分配战场失败，可能有人没血、没孵化', at_sender=True)
        else:
            await matcher.finish(generate_process(battle_field), at_sender=True)
