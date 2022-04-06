import httpx
import json
from .utils import *
from .imageProcesser import get_stages


def get_schedule():
    with httpx.Client() as client:
        result = client.get('https://splatoon2.ink/data/schedules.json')
        return json.load(result)


def get_coop_schedule():
    with httpx.Client() as client:
        result = client.get('https://splatoon2.ink/data/coop-schedules.json')
        return json.load(result)


def get_coop_info():
    schedule = get_coop_schedule()

    def get_info(res):
        return {
            'stage': trans_to_chinese(res['stage']['name']),
            'start_time': res['start_time'],
            'end_time': res['end_time'],
            'weapons': [trans_to_chinese(w['weapon']['name']) for w in res['weapons']]
        }

    first_info = get_info(schedule['details'][0])
    second_info = get_info(schedule['details'][1])

    is_cooping = time.time() >= first_info['start_time']
    if is_cooping:
        is_cooping = '现在工的时间'
    else:
        is_cooping = '下一次工的时间'

    result_string = '{}为：\n{} - {}\n地图为：{}\n武器为：{}, {}, {}, {}\n接下来工的时间为：\n{} - {}\n地图为：{}\n武器为：{}, {}, {}, {}'.format(
        is_cooping, time_converter_day(first_info['start_time']), time_converter_day(first_info['end_time']),
        first_info['stage'],
        first_info['weapons'][0], first_info['weapons'][1], first_info['weapons'][2], first_info['weapons'][3],
        time_converter_day(second_info['start_time']), time_converter_day(second_info['end_time']),
        second_info['stage'],
        second_info['weapons'][0], second_info['weapons'][1], second_info['weapons'][2], second_info['weapons'][3],
        )
    return result_string


def get_stage_info(num_list=None):
    if num_list is None:
        num_list = [0]
    schedule = get_schedule()
    return get_stages(schedule, num_list)


def random_image():
    return 'https://1mg.obfs.dev/'


if __name__ == '__main__':
    # get_stage_info().show()
    print(get_coop_info())
