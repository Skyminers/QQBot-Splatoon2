import httpx
import json
from .utils import *
from .imageProcesser import get_stages

schedule_res = None


def check_expire_schedule(schedule):
    st = schedule['regular'][0]['start_time']
    ed = schedule['regular'][0]['end_time']
    nw = time.time()
    if st < nw < ed:
        return False
    return True


def get_schedule():
    global schedule_res
    if schedule_res is None or check_expire_schedule(schedule_res):
        print('Re-get schedule')
        with httpx.Client() as client:
            result = client.get('https://splatoon2.ink/data/schedules.json')
            schedule_res = json.load(result)
            return schedule_res
    else:
        return schedule_res


def get_coop_schedule():
    with httpx.Client() as client:
        result = client.get('https://splatoon2.ink/data/coop-schedules.json')
        return json.load(result)


def get_weapon_name(res):
    if 'weapon' not in res:
        return res['coop_special_weapon']['name']
    else:
        return res['weapon']['name']


def get_info(res):
    return {
        'stage': res['stage']['name'],
        'start_time': res['start_time'],
        'end_time': res['end_time'],
        'weapons': [get_weapon_name(w) for w in res['weapons']]
    }


def get_coop_info():
    schedule = get_coop_schedule()

    first_info = get_info(schedule['details'][0])
    second_info = get_info(schedule['details'][1])

    is_cooping = time.time() >= first_info['start_time']
    if is_cooping:
        is_cooping = '现在工的时间'
    else:
        is_cooping = '下一次工的时间'

    result_string = '{}为：\n{} - {}\n地图为：{}\n武器为：{}, {}, {}, {}\n接下来工的时间为：\n{} - {}\n地图为：{}\n武器为：{}, {}, {}, {}'.format(
        is_cooping, time_converter_day(first_info['start_time']), time_converter_day(first_info['end_time']),
        trans_to_chinese(first_info['stage']),
        trans_to_chinese(first_info['weapons'][0]),
        trans_to_chinese(first_info['weapons'][1]),
        trans_to_chinese(first_info['weapons'][2]),
        trans_to_chinese(first_info['weapons'][3]),
        time_converter_day(second_info['start_time']), time_converter_day(second_info['end_time']),
        trans_to_chinese(second_info['stage']),
        trans_to_chinese(second_info['weapons'][0]),
        trans_to_chinese(second_info['weapons'][1]),
        trans_to_chinese(second_info['weapons'][2]),
        trans_to_chinese(second_info['weapons'][3]),
    )
    return result_string


def get_stage_info(num_list=None, stage_mode=None):
    if num_list is None:
        num_list = [0]
    schedule = get_schedule()
    if stage_mode is not None:
        if len(stage_mode) == 2:
            return get_stages(schedule, num_list, map_contest[stage_mode[:2]])
        elif len(stage_mode) == 4:
            return get_stages(schedule, num_list, map_contest[stage_mode[2:]], map_rule[stage_mode[:2]])
        else:
            raise NameError()
    return get_stages(schedule, num_list)


def random_image():
    # return 'https://1mg.obfs.dev/'
    # return 'https://pximg2.rainchan.win/rawimg'
    # return 'https://rc-pximg.glitch.me/rawimg'
    # return 'https://pximg.rainchan.win/rawimg'
    # return 'https://api.pixiv.cx/rand/?mode=1/2/3'
    # return 'http://www.dmoe.cc/random.php'
    return 'https://imgapi.cn/api.php?zd=zd&fl=dongman'


def random_image_background(zd='pc', fl='fengjing'):
    return 'https://imgapi.cn/api.php?&zd={}&fl={}&gs=images'.format(zd, fl)


if __name__ == '__main__':
    # get_stage_info().show()
    print(get_coop_info())
