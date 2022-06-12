import random
from enum import Enum
import pickle

from typing import List


class ContestState(Enum):
    Ready = 1
    Gaming = 2
    End = 3


class MemberInfo:
    def __init__(self, game_ID, call_name, QQ_ID):
        self.game_ID = game_ID
        self.call_name = call_name
        self.QQ_ID = QQ_ID
        self.right_vote_count = 0

    def right_vote(self):
        self.right_vote_count += 1


class FindSpyContestModule:
    def __init__(self, member):
        self.member = member
        self.now_member = []
        self.stat = ContestState.Ready
        self.audience = (member and 1) == 1
        self.round = 0
        self.vote_list = {}
        self.id_map = {}
        self.spy = None

    def join(self, ID, name, qID):
        if len(self.now_member) == self.member:
            return 1, None
        for info in self.now_member:
            if qID == info.QQ_ID:
                return 2, info
        # ID: game ID, name: called name, qID: QQ account number
        self.now_member.append(MemberInfo(ID, name, qID))
        return 0, None

    def check_begin(self):
        if len(self.now_member) == self.member:
            for (pos, info) in enumerate(self.now_member):
                self.id_map[info.QQ_ID] = pos
            return True

    def get_display_list(self):
        msg = '此次比赛设定人数为 {} 人, 当前共有 {} 人报名:'.format(self.member, len(self.now_member))
        for (pos, info) in enumerate(self.now_member):
            msg = msg + '\n' + '{}: 游戏名称为 {}, 可以称呼为 {}'.format(pos+1, info.game_ID, info.call_name)
        print(msg)
        return msg

    def get_vote_list(self):
        msg = '请选择你要票的人：'
        for (pos, info) in enumerate(self.now_member):
            msg = msg + '\n' + ' {}: 游戏名称为 {}, 可以称呼为 {}'.format(pos+1, info.game_ID, info.call_name)
        msg = msg + '\n' + '通过 \"/票 编号\" 来进行投票吧！'
        print(msg)
        return msg

    def join_end(self):
        self.stat = ContestState.Gaming

    # Convert to Gaming After This
    def begin_game(self) -> (int, MemberInfo, MemberInfo, List[MemberInfo]):
        self.round += 1
        if self.audience:
            if self.round <= self.member:
                audience_pos = self.round - 1
            else:
                audience_pos = random.randint(0, self.member-1)
            audience = self.now_member[audience_pos]
            tmp_list = self.now_member.copy()
            del tmp_list[audience_pos]
            self.spy = random.choice(tmp_list)
        else:
            audience = None
            self.spy = random.choice(self.now_member)
        self.vote_list = {}
        return self.round, audience, self.spy, self.now_member.copy()

    def record_vote(self, qID, vote_ID):
        if vote_ID < 1 or vote_ID > self.member:
            return False
        if self.id_map[qID] in self.vote_list.keys():
            return False
        self.vote_list[self.id_map[qID]] = vote_ID - 1  # user ID to user ID
        return True

    def get_qID_info(self, qID):
        if qID in self.id_map:
            return self.now_member[self.id_map[qID]]
        else:
            return None

    def end_vote(self):
        if len(self.vote_list.items()) != self.member:
            print('votes {}'.format(len(self.vote_list.items())))
            print(self.vote_list.items())
            return None, None, None, None
        ws_vote = [0 for i in range(self.member)]
        for (x, y) in self.vote_list.items():
            ws_vote[y] += 1
        max_vote = max(ws_vote)
        max_cnt = ws_vote.count(max_vote)
        max_pos = ws_vote.index(max_vote)
        right_list = []
        spy_pos = self.id_map[self.spy.QQ_ID]
        for (x, y) in self.vote_list.items():
            if x == spy_pos:
                continue
            if y == spy_pos:
                right_list.append(self.now_member[x])
                self.now_member[x].right_vote()
        flag = 0
        if max_cnt == 1 and max_pos == spy_pos:
            flag = 1
        elif max_cnt > 1:
            flag = 2
        return flag, right_list, zip(ws_vote, self.now_member), self.spy

    def end(self):
        self.stat = ContestState.End
        return self.now_member









