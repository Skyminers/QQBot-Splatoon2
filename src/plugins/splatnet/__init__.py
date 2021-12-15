# import nonebot
from nonebot import get_driver
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Bot, MessageSegment, exception
from .config import Config
from nonebot_guild_patch import GuildMessageEvent
from .data_source import StageInfoImage

global_config = get_driver().config
config = Config(**global_config.dict())

# 获取地图
matcher_stage = on_command('图')


@matcher_stage.handle()
async def _(bot: Bot, event: GuildMessageEvent):
    img = StageInfoImage().get_stage_info()
    await matcher_random.send(
        MessageSegment.image(
            file=img,
            cache=False,
        ))

# 随机图片
matcher_random = on_command('image')


@matcher_random.handle()
async def _(bot: Bot, event: GuildMessageEvent):
    try:
        await matcher_random.send(
            MessageSegment.image(
                file='https://1mg.obfs.dev/',
                cache=False,
            ))
    except exception.NetworkError:
        await matcher_random.send(
            '超时了>_<, 没能拿到图片'
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
