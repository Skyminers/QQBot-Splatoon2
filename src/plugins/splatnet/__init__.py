# import nonebot
import re
import time

from nonebot import get_driver
from nonebot import on_command, on_regex, on_startswith
from nonebot.typing import T_State
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Bot, MessageSegment, exception
from nonebot import require
from .config import Config
from .data_source import *
from .utils import *
from .imageProcesser import *
from .json_struct import JsonStruct

global_config = get_driver().config
config = Config(**global_config.dict())
scheduler = require("nonebot_plugin_apscheduler").scheduler


# Scheduler

def clear_every_day_from_program_start():
    image_json_lock.acquire()  # Multiprocess image access should be considered
    jsonStruct = JsonStruct('ImagePersonalIdList')
    jsonStruct.clear()
    image_json_lock.release()


scheduler.add_job(clear_every_day_from_program_start, trigger='cron', hour='2')
scheduler.add_job(clear_every_day_from_program_start, trigger='cron', hour='14')
# TODO: 定时删除的功能未经测试

# Response

matcher_select_stage = on_regex('[0-9]+图')
matcher_select_stage_mode_rule = on_regex('[0-9]+(区域|推塔|蛤蜊|抢鱼)(单|组)排')
matcher_select_stage_mode = on_regex('[0-9]+(单排|组排|涂地)')
matcher_select_all_mode_rule = on_regex('全部(区域|推塔|蛤蜊|抢鱼)(单|组)排')
matcher_select_all_mode = on_regex('全部(单排|组排|涂地)')
matcher_time = on_startswith('几点啦')
matcher_rush = on_command('rush')
matcher_weapon_power = on_command('主强')
matcher_skill_forward = on_command('品牌倾向')
matcher_weapon_distance = on_command('武器射程')
matcher_weapon_information = on_command('武器详情')
matcher_kill = on_command('伪确')
matcher_coop = on_command('工')
matcher_pool = on_command('开泉')
matcher_stage_group = on_command('图')
matcher_stage_group2 = on_command('图图')
matcher_stage_next1 = on_command('下图')
matcher_stage_next12 = on_command('下图图')
matcher_random = on_command('色图')
matcher_random_xjj = on_command('小姐姐')
matcher_random_background = on_command('壁纸')
matcher_random_background_mobile = on_command('手机壁纸')


@matcher_select_all_mode.handle()
async def _(bot: Bot, event: Event):
    plain_text = event.get_message().extract_plain_text()
    msg = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    img = get_stage_info(msg, stage_mode=plain_text[-2:])
    await matcher_select_all_mode.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


@matcher_select_all_mode_rule.handle()
async def _(bot: Bot, event: Event):
    plain_text = event.get_message().extract_plain_text()
    msg = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    img = get_stage_info(msg, stage_mode=plain_text[-4:])
    await matcher_select_all_mode_rule.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


@matcher_select_stage_mode_rule.handle()
async def _(bot: Bot, event: Event):
    plain_text = event.get_message().extract_plain_text()
    msg = list(set([int(x) for x in plain_text[:-4]]))
    msg.sort()
    img = get_stage_info(msg, stage_mode=plain_text[-4:])
    if img is None:
        msg = '好像没有符合要求的地图模式>_<'
    else:
        msg = MessageSegment.image(
            file=img,
            cache=False,
        )
    await matcher_select_stage_mode_rule.send(msg)


@matcher_select_stage_mode.handle()
async def _(bot: Bot, event: Event):
    plain_text = event.get_message().extract_plain_text()
    msg = list(set([int(x) for x in plain_text[:-2]]))
    msg.sort()
    img = get_stage_info(msg, stage_mode=plain_text[-2:])
    if img is None:
        msg = '好像没有符合要求的地图模式>_<'
    else:
        msg = MessageSegment.image(
            file=img,
            cache=False,
        )
    await matcher_select_stage_mode.send(msg)


@matcher_rush.handle()
async def _(bot: Bot, event: Event):
    await matcher_rush.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Rush', format_name='jpg')),
            cache=False,
        )
    )


@matcher_weapon_distance.handle()
async def _(bot: Bot, event: Event):
    await matcher_weapon_distance.send(
        MessageSegment.image(
            file=image_to_base64(get_file('Weapons Distance', format_name='jpg')),
            cache=False,
        )
    )


@matcher_weapon_information.handle()
async def _(bot: Bot, event: Event):
    await matcher_weapon_information.send(
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
    msg.sort()
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


@matcher_time.handle()
async def _(bot: Bot, event: Event):
    await matcher_time.send(
        time_converter_display(time.time())
    )


# 随机图片


@matcher_random.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    try:
        if check_group_id(group_id):
            if check_personal_id(personal_id):
                send_msg = MessageSegment.image(file=random_image(), cache=False)
            else:
                send_msg = '今天已经色过了，明天再来吧！'
        else:
            send_msg = '几点啦，还不睡觉，等着猝死吧你们！'
        if send_msg is None:
            send_msg = '获取失败了，重来一遍吧！'
        else:
            record_times(personal_id, 1)
        await matcher_random.send(send_msg)
    except exception.NetworkError:
        print('timeout')
        # await matcher_random.send('我一定会修好这个鬼东西的！')


@matcher_random_background.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    try:
        send_msg = MessageSegment.image(file=random_image_background(), cache=False)
        if send_msg is None:
            send_msg = '获取失败了，重来一遍吧！'
        else:
            record_times(personal_id, 1)
        await matcher_random_background.send(send_msg)
    except exception.NetworkError:
        print('timeout')
        # await matcher_random.send('我一定会修好这个鬼东西的！')


@matcher_random_background_mobile.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    try:
        send_msg = MessageSegment.image(file=random_image_background(zd='mobile'), cache=False)
        if send_msg is None:
            send_msg = '获取失败了，重来一遍吧！'
        else:
            record_times(personal_id, 1)
        await matcher_random_background_mobile.send(send_msg)
    except exception.NetworkError:
        print('timeout')
        # await matcher_random.send('我一定会修好这个鬼东西的！')


@matcher_random_xjj.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    try:
        send_msg = MessageSegment.image(file=random_image_background(zd='zd', fl='meizi'), cache=False)
        if send_msg is None:
            send_msg = '获取失败了，重来一遍吧！'
        else:
            record_times(personal_id, 1)
        await matcher_random_background_mobile.send(send_msg)
    except exception.NetworkError:
        print('timeout')
        # await matcher_random.send('我一定会修好这个鬼东西的！')
