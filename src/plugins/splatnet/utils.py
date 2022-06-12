import time
from .json_struct import JsonStruct
from multiprocessing import Lock

trans_map = {
    'Sploosh-o-matic': '喇叭',
    'Splattershot Jr.': '新叶',
    'Splash-o-matic': '针管',
    'Aerospray MG': '银喷',
    'Splattershot': '小绿',
    '.52 Gal': '52',
    'N-ZAP \'85': '85',
    'Splattershot Pro': '精英枪',
    '.96 Gal': '96',
    'Jet Squelcher': '蓝管',
    'Luna Blaster': '白泡',
    'Blaster': '热泡',
    'Range Blaster': '长热泡',
    'Clash Blaster': '蜡笔泡',
    'Rapid Blaster': '红泡',
    'Rapid Blaster Pro': '长红泡',
    'L-3 Nozzlenose': 'L3',
    'H-3 Nozzlenose': 'H3',
    'Squeezer': '香槟',
    'Carbon Roller': '碳刷',
    'Splat Roller': '中刷',
    'Dynamo Roller': '重刷',
    'Flingza Roller': '钢笔刷',
    'Inkbrush': '毛笔',
    'Octobrush': '北斋',
    'Classic Squiffer': '洁厕灵',
    'Splat Charger': '绿狙',
    'Splatterscope': '镜狙',
    'E-liter 4K': '4K',
    'E-liter 4K Scope': '镜4K',
    'Bamboozler 14 Mk I': '竹狙',
    'Goo Tuber': '水管狙',
    'Slosher': '红桶',
    'Tri-Slosher': '绿桶',
    'Sloshing Machine': '洗衣机',
    'Bloblobber': '澡盆',
    'Explosher': '重桶',
    'Mini Splatling': '轻加',
    'Heavy Splatling': '中加',
    'Hydra Splatling': '消防栓',
    'Ballpoint Splatling': '圆珠笔',
    'Nautilus 47': '鹦鹉螺',
    'Dapple Dualies': '牙刷',
    'Splat Dualies': '双枪',
    'Glooga Dualies': '525',
    'Dualie Squelchers': '红双',
    'Dark Tetra Dualies': '气垫',
    'Splat Brella': '伞',
    'Tenta Brella': '重伞',
    'Undercover Brella': '间谍伞',
    'Grizzco Blaster': '熊泡',
    'Grizzco Brella': '熊伞',
    'Grizzco Charger': '熊狙',
    'Grizzco Slosher': '熊桶',
    'Spawning Grounds': '大坝',
    'Marooner\'s Bay': '废船',
    'Salmonid Smokeyard': '工坊',
    'Ruins of Ark Polaris': '方舟',
    'Lost Outpost': '厕所（集落）',
    'Random': '随机'
}

map_contest = {'涂地': 'Turf War', '单排': 'Ranked', '组排': 'League'}
map_rule = {'区域': 'Splat Zones', '推塔': 'Tower Control', '蛤蜊': 'Clam Blitz', '抢鱼': 'Rainmaker'}

white_list = ['458482582', '792711635', '835723997']

image_json_lock = Lock()

def time_converter(time_stamp):
    return time.strftime('%H:%M', time.localtime(time_stamp))


def time_converter_day(time_stamp):
    return time.strftime('%m-%d %H:%M', time.localtime(time_stamp))


def time_converter_display(time_stamp):
    return time.strftime('20%y年%m月%d日 %H:%M:%S', time.localtime(time_stamp))


def trans_to_chinese(input_english):
    if input_english in trans_map:
        return trans_map[input_english]
    else:
        return input_english


def check_group_id(group_id):
    # if group_id == '616533832':
    #     return False
    return True


def check_personal_id(personal_id):
    if personal_id in white_list:
        return True
    image_json_lock.acquire()  # Multiprocess image access should be considered
    jsonStruct = JsonStruct('ImagePersonalIdList')
    id_list = jsonStruct.readFile()
    if personal_id in id_list:
        res = False
    else:
        id_list[personal_id] = 0
        res = True
    jsonStruct.save(id_list)
    image_json_lock.release()
    return res


def record_times(personal_id, x):
    image_json_lock.acquire()  # Multiprocess image access should be considered
    jsonStruct = JsonStruct('ImagePersonalIdList')
    id_list = jsonStruct.readFile()
    if personal_id in id_list:
        id_list[personal_id] += x
    else:
        id_list[personal_id] = x
    jsonStruct.save(id_list)
    image_json_lock.release()