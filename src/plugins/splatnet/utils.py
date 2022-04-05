import time

trans_map = {
    'Heavy Splatling': '中加',
    'Splattershot Pro': '精英枪'
}


def time_converter(time_stamp):
    return time.strftime('%H:%M', time.localtime(time_stamp))


def time_converter_day(time_stamp):
    return time.strftime('%m-%d %H:%M', time.localtime(time_stamp))


def trans_to_chinese(input_english):
    if input_english in trans_map:
        return trans_map[input_english]
    else:
        return input_english
