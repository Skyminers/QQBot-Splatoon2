# import nonebot
from nonebot import get_driver
from nonebot import on_command, on_regex
from nonebot.typing import T_State
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Bot, MessageSegment, exception
from .config import Config
from .data_source import *
from .utils import *
from .imageProcesser import *
from .json_struct import JsonStruct

global_config = get_driver().config
config = Config(**global_config.dict())

# 群

matcher_select_stage = on_regex('[0-9]+图')
matcher_weapon_power = on_command('主强')
matcher_skill_forward = on_command('品牌倾向')
matcher_weapon_distance = on_command('武器射程')
matcher_weapon_infomation = on_command('武器详情')
matcher_kill = on_command('伪确')
matcher_coop = on_command('工')
matcher_pool = on_command('开泉')
matcher_stage_group = on_command('图')
matcher_stage_group2 = on_command('图图')
matcher_stage_next1 = on_command('下图')
matcher_stage_next12 = on_command('下图图')
matcher_random = on_command('色图')


@matcher_weapon_distance.handle()
async def _(bot: Bot, event: Event):
    await matcher_weapon_distance.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Weapons Distance', format_name='jpg')),
            cache=False,
        )
    )


@matcher_weapon_infomation.handle()
async def _(bot: Bot, event: Event):
    await matcher_weapon_infomation.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Weapons Information', format_name='jpg')),
            cache=False,
        )
    )


@matcher_weapon_power.handle()
async def _(bot: Bot, event: Event):
    await matcher_weapon_power.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Weapon Plus Power', format_name='jpg')),
            cache=False,
        )
    )


@matcher_skill_forward.handle()
async def _(bot: Bot, event: Event):
    await matcher_skill_forward.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Skill Forward', format_name='jpg')),
            cache=False,
        )
    )


@matcher_select_stage.handle()
async def _(bot: Bot, event: Event):
    msg = list(set([int(x) for x in event.get_message().extract_plain_text()[:-1]]))
    img = get_stage_info(msg)
    await matcher_select_stage.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


@matcher_kill.handle()
async def _(bot: Bot, event: Event):
    await matcher_kill.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Suspected Kill', format_name='jpg')),
            cache=False,
        )
    )


@matcher_coop.handle()
async def _(bot: Bot, event: Event):
    res = get_coop_info()
    await matcher_coop.send(
        res
    )


@matcher_pool.handle()
async def _(bot: Bot, event: Event):
    res = get_file(get_info(get_coop_schedule()['details'][0])['stage'] + ' Pool', format_name='jpg')
    await matcher_pool.send(
        MessageSegment.image(
            file=image_to_base64(res),
            cache=False
        )
    )


@matcher_stage_group.handle()
async def _(bot: Bot, event: Event):
    img = get_stage_info()
    await matcher_stage_group.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


@matcher_stage_group2.handle()
async def _(bot: Bot, event: Event):
    img = get_stage_info([0, 1])
    await matcher_stage_group2.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


@matcher_stage_next1.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).strip()
    img = get_stage_info([1])
    await matcher_stage_next1.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


@matcher_stage_next12.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).strip()
    img = get_stage_info([1, 2])
    await matcher_stage_next12.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


# 随机图片


@matcher_random.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    try:
        if check_group_id(group_id):
            if check_personal_id(personal_id):
                send_msg = MessageSegment.image(file=random_image(), cache=False, timeout=10)
            else:
                send_msg = '今天已经色过了，明天再来吧！'
        else:
            send_msg = '几点啦，还不睡觉，等着猝死吧你们！'
        await matcher_random.send(send_msg)
    except exception.NetworkError:
        await matcher_random.send(
            '超时了>_<, 没能拿到图片'
        )

