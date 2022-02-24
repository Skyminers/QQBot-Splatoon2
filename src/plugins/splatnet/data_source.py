import httpx
import json
from .imageProcesser import get_stages


def get_schedule():
    with httpx.Client() as client:
        result = client.get('https://splatoon2.ink/data/schedules.json')
        return json.load(result)


def get_stage_info(num_list=None):
    if num_list is None:
        num_list = [0]
    schedule = get_schedule()
    return get_stages(schedule, num_list)


def random_image():
    return 'https://1mg.obfs.dev/'


if __name__ == '__main__':
    get_stage_info().show()
