# import nonebot
import re
import time

from nonebot import on_command, on_regex, on_startswith
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Bot, MessageSegment, exception
from nonebot import require
from .find_spy_contest import ContestState, FindSpyContestModule
import asyncio
from typing import cast
import traceback

import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from fastapi import Query, FastAPI
from fastapi.responses import UJSONResponse

app = nonebot.get_asgi()
app = cast(FastAPI, app)


# app = FastAPI()

@app.get("/disconnect")
async def disconnect(bot: str = Query(...)) -> UJSONResponse:
    try:
        adapter = nonebot.get_driver()._adapters[Adapter.get_name()]
        adapter = cast(Adapter, adapter)
        ws = adapter.connections[bot]
        await ws.close()
        adapter.connections.pop(bot, None)
        adapter.bot_disconnect(nonebot.get_bot(bot))
        nonebot.logger.info(f"disconnect bot: {bot}")
    except Exception as e:
        return UJSONResponse({"msg": "no such bot", "exc": traceback.format_exc()}, 404)
    else:
        return UJSONResponse({"msg": "ok"}, 200)


contest_module_map = {}
group_binder = {}

# Response

matcher_spy_contest_start = on_command('谁是内鬼', permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)
matcher_spy_contest_join = on_command('报名')
matcher_spy_contest_player_list = on_command('选手列表')
matcher_spy_contest_join_end = on_command('报名结束', permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)
matcher_spy_contest_begin_game = on_command('对局开始', permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)
matcher_spy_contest_vote = on_command('票')
matcher_spy_contest_vote_end = on_command('投票结束', permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)
matcher_spy_contest_end = on_command('游戏结束', permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)


@matcher_spy_contest_start.handle()
async def _(bot: Bot, event: Event, state: T_State):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    await matcher_spy_contest_start.send('谁是内鬼比赛即将开始')
    contest_module_map[group_id] = None
    args = str(event.get_message()).strip()
    if args:
        try:
            member = int(args)
            state['member'] = member
        except Exception as e:
            pass


@matcher_spy_contest_start.got('member', prompt='请输入比赛人数')
async def _(bot: Bot, event: Event, state: T_State):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    member = str(state['member']).strip()
    if member.isdigit():
        member = int(member)
        if 1 <= member <= 9:
            pass
        else:
            await matcher_spy_contest_start.send('人数应该在 4~9 范围内！')
            return
    else:
        await matcher_spy_contest_start.send('请输入 4~9 之间的数字')
        return

    module = FindSpyContestModule(member=member)
    contest_module_map[group_id] = module
    await matcher_spy_contest_start.send('比赛已成功创建，请各位选手以：\n \"/报名 游戏内名称 可以称呼的ID\" \n的格式在群内发送消息来进行注册')


@matcher_spy_contest_join.handle()
async def _(bot: Bot, event: Event):
    global group_binder
    group_id, personal_id = event.get_session_id().split('_')[1:]
    args = str(event.get_message()).strip()
    module = contest_module_map[group_id]
    if not module:
        await matcher_spy_contest_join.send('该群没有正在进行中的比赛')
        return
    if module.stat != ContestState.Ready:
        await matcher_spy_contest_join.send('比赛正在进行中，不能报名哦')
        return
    try:
        _, ID, name = args.split(' ')
    except ValueError as e:
        await matcher_spy_contest_join.send('格式错误，请按照 \"/报名 游戏内名称 可以称呼的ID\" 的格式输入')
        return
    ret, info = module.join(ID, name, personal_id)
    if ret == 1:
        await matcher_spy_contest_join.send('报名人数已满 QwQ，{}下次再来吧！'.format(name))
    elif ret == 2:
        await matcher_spy_contest_join.send('{}你已经报过名啦！不能再报了哦'.format(info.call_name))
    else:
        await matcher_spy_contest_join.send('{}报名成功！'.format(name))
        group_binder[personal_id] = group_id


@matcher_spy_contest_player_list.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    module = contest_module_map[group_id]
    if not module:
        await matcher_spy_contest_player_list.send('该群没有正在进行中的比赛')
        return
    await matcher_spy_contest_player_list.send(module.get_display_list())


@matcher_spy_contest_join_end.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    module = contest_module_map[group_id]
    if not module:
        await matcher_spy_contest_join_end.send('该群没有正在进行中的比赛')
        return
    if module.stat != ContestState.Ready:
        await matcher_spy_contest_join_end.send('该群没有正在进行报名的比赛')
        return
    if not module.check_begin():
        await matcher_spy_contest_join_end.send('比赛还没有就绪\n' + module.get_display_list())
        return
    await matcher_spy_contest_join_end.send('比赛报名结束！')
    module.join_end()


@matcher_spy_contest_begin_game.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    module = contest_module_map[group_id]
    if not module:
        await matcher_spy_contest_begin_game.send('该群没有正在进行中的比赛')
        return
    if module.stat != ContestState.Gaming:
        await matcher_spy_contest_begin_game.send('比赛仍未就绪或已经结束')
        return
    round_num, audience, spy, all_member = module.begin_game()
    if audience is not None:
        print('第 {} 局游戏开始，各位本局身份已通过私聊通知，若未接到 bot 私聊请及时联系主办方！\n本局观众为：{}({})\n 此刻起参赛选手可以私聊 Bot进行投票，命令为 \"/票\"'
                .format(round_num, audience.game_ID, audience.call_name))
        await matcher_spy_contest_begin_game.send(
            '第 {} 局游戏开始，各位本局身份已通过私聊通知，若未接到 bot 私聊请及时联系主办方！\n本局观众为：{}({})\n 此刻起参赛选手可以私聊 Bot进行投票，命令为 \"/票\"'
                .format(round_num, audience.game_ID, audience.call_name))
        all_member.remove(audience)
        all_member.remove(spy)
        await bot.send_private_msg(user_id=audience.QQ_ID, message='本局游戏你是观众')
        await bot.send_private_msg(user_id=spy.QQ_ID, message='本局游戏你是内鬼！隐藏好自己并输掉比赛吧！')
        for member in all_member:
            await bot.send_private_msg(user_id=member.QQ_ID, message='本局游戏你没有特殊任务，尽力赢得比赛并找出内鬼！')
    else:
        print('第 {} 局游戏开始，各位本局身份已通过私聊通知，若未接到 bot 私聊请及时联系主办方！\n 此刻起参赛选手可以私聊 Bot进行投票，命令为 \"/票\"'
              .format(round_num))
        await matcher_spy_contest_begin_game.send('第 {} 局游戏开始，各位本局身份已通过私聊通知，若未接到 bot 私聊请及时联系主办方！\n 此刻起参赛选手可以私聊 '
                                                  'Bot进行投票，命令为 \"/票\" '
              .format(round_num))
        all_member.remove(spy)
        await bot.send_private_msg(user_id=spy.QQ_ID, message='本局游戏你是内鬼！隐藏好自己并输掉比赛吧！')
        for member in all_member:
            await bot.send_private_msg(user_id=member.QQ_ID, message='本局游戏你没有特殊任务，尽力赢得比赛并找出内鬼！')




@matcher_spy_contest_vote.handle()
async def _(bot: Bot, event: Event):
    ids = event.get_session_id()
    if ids.startswith("group"):
        await matcher_spy_contest_vote.send('请私聊机器人来进行投票！')
        return
    qID = ids
    if qID not in group_binder:
        await matcher_spy_contest_vote.send('你好像没有在群内报名比赛？')
        return
    group_ID = group_binder[qID]
    module = contest_module_map[group_ID]
    if module.stat != ContestState.Gaming:
        await matcher_spy_contest_vote.send('你报名的比赛仍未开始或已结束')
        return

    args = str(event.get_message()).strip()

    try:
        _, vote_id = args.split(' ')
        vote_id = int(vote_id)
    except Exception as e:
        await matcher_spy_contest_vote.send(module.get_vote_list())
        return

    if module.record_vote(qID, vote_id):
        send_msg = '投票成功'
        await bot.send_group_msg(group_id=group_ID, message='{} 已投票'.format(module.get_qID_info(qID).call_name))
    else:
        send_msg = '输入有误或已经投过票了'
    await matcher_spy_contest_vote.send(send_msg)


@matcher_spy_contest_vote_end.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    module = contest_module_map[group_id]
    if not module:
        await matcher_spy_contest_vote_end.send('该群没有正在进行中的比赛')
        return
    if module.stat != ContestState.Gaming:
        await matcher_spy_contest_vote_end.send('比赛仍未就绪或已经结束')
        return
    flag, right_list, vote_info, spy = module.end_vote()
    if flag is None:
        await matcher_spy_contest_vote_end.send('有人没投票，我不说是谁')
        print(module.vote_list.items())
        return
    if flag == 0:
        send_msg = '内鬼没有被票出！'
    elif flag == 1:
        send_msg = '内鬼被票出了！'
    elif flag == 2:
        send_msg = '出现了平票，没有人被票出！'
    print(send_msg + '内鬼是 {}({})'.format(spy.game_ID, spy.call_name))
    send_msg2 = '\n'.join(
        ['{}({}) 得票 {}'.format(member.game_ID, member.call_name, v) for (v, member) in vote_info])
    print(send_msg2)
    if len(right_list) == 0:
        print('没有人投中内鬼！')
    else:
        print(' '.join([member.call_name for member in right_list]) + ' 正确地票选了内鬼')

    await matcher_spy_contest_vote_end.send(send_msg + '内鬼是 {}({})'.format(spy.game_ID, spy.call_name))
    await matcher_spy_contest_vote_end.send(send_msg2)

    if len(right_list) == 0:
        await matcher_spy_contest_vote_end.send('没有人投中内鬼！')
    else:
        await matcher_spy_contest_vote_end.send(' '.join([member.call_name for member in right_list]) + ' 正确地票选了内鬼')


@matcher_spy_contest_end.handle()
async def _(bot: Bot, event: Event):
    group_id, personal_id = event.get_session_id().split('_')[1:]
    module = contest_module_map[group_id]
    if not module:
        await matcher_spy_contest_end.send('该群没有正在进行中的比赛')
        return
    info = module.end()
    send_msg = '比赛结束\n' + '\n'.join(
        ['{}({}) 投中内鬼 {} 次'.format(member.game_ID, member.call_name, member.right_vote_count) for member in info])
    print(send_msg)
    await matcher_spy_contest_end.send(send_msg)

