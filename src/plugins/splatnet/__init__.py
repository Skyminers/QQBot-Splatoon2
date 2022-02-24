# import nonebot
from nonebot import get_driver
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Bot, MessageSegment, exception
from .config import Config
from nonebot_guild_patch import GuildMessageEvent
from .data_source import get_stage_info
from .data_source import random_image

global_config = get_driver().config
config = Config(**global_config.dict())

# 群

matcher_stage_group = on_command('图')


@matcher_stage_group.handle()
async def _(bot: Bot, event: Event):
    img = get_stage_info()
    await matcher_stage_group.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


matcher_stage_group2 = on_command('图图')


@matcher_stage_group2.handle()
async def _(bot: Bot, event: Event):
    img = get_stage_info([0,1])
    await matcher_stage_group2.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


matcher_stage_next1 = on_command('下图')


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

matcher_stage_next12 = on_command('下图图')


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


matcher_stage_next2 = on_command('下下图')


@matcher_stage_next2.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).strip()
    img = get_stage_info([2])
    await matcher_stage_next2.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


matcher_stage_next3 = on_command('下下下图')


@matcher_stage_next3.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).strip()
    img = get_stage_info([3])
    await matcher_stage_next3.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


matcher_stage_next4 = on_command('下下下图')


@matcher_stage_next4.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).strip()
    img = get_stage_info([4])
    await matcher_stage_next4.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


matcher_stage_next5 = on_command('下下下下图')


@matcher_stage_next5.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).strip()
    img = get_stage_info([5])
    await matcher_stage_next5.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


# 随机图片
matcher_random = on_command('色图')


@matcher_random.handle()
async def _(bot: Bot, event: Event):
    try:
        await matcher_random.send(
            MessageSegment.image(
                file=random_image(),
                cache=False,
            ))
        # await matcher_random.send(
        #     '这个功能没有了！'
        # )
    except exception.NetworkError:
        await matcher_random.send(
            '超时了>_<, 没能拿到图片'
        )


# 频道

# 获取所有地图

matcher_all_stage = on_command('所有图图')


@matcher_all_stage.handle()
async def _(bot: Bot, event: GuildMessageEvent):
    for i in range(6):
        img = get_stage_info([i])
        await matcher_all_stage.send(
            MessageSegment.image(
                file=img,
                cache=False,
            )
        )


# 获取地图
matcher_stage = on_command('图')


@matcher_stage.handle()
async def _(bot: Bot, event: GuildMessageEvent):
    img = get_stage_info()
    await matcher_stage.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )


matcher_stage_next = on_command('下图')


@matcher_stage_next.handle()
async def _(bot: Bot, event: GuildMessageEvent):
    args = str(event.get_message()).strip()
    img = get_stage_info([1])
    await matcher_stage_next.send(
        MessageSegment.image(
            file=img,
            cache=False,
        )
    )



# 复读机功能
matcher_repeat = on_command('复读')


@matcher_repeat.handle()
async def _(bot: Bot, event: GuildMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['msg'] = args


@matcher_repeat.got('msg', prompt='人类的本质就是我')
async def _(bot: Bot, event: GuildMessageEvent, state: T_State):
    msg = state['msg']
    await matcher_repeat.send(msg)
