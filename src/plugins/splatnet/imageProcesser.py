import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .utils import *

cur_path = os.getcwd()
image_folder = os.path.join(cur_path, 'src', 'plugins', 'splatnet', 'ImageData')
ttf_path = os.path.join(cur_path, 'src', 'plugins', 'splatnet', 'font', 'SplatoonFontFix.otf')

# local
# image_folder = os.path.join(cur_path, 'ImageData')
# ttf_path = os.path.join(cur_path, 'font', 'SplatoonFontFix.otf')


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()


def get_file(name, format_name='png'):
    img = Image.open(os.path.join(image_folder, '{}.{}'.format(name, format_name)))
    return img


def get_file_path(name, format_name='png'):
    return os.path.join(image_folder, '{}.{}'.format(name, format_name))


def circle_corner(img, radii):
    """
    圆角处理
    :param img: 源图象。
    :param radii: 半径，如：30。
    :return: 返回一个圆角处理后的图象。
    """
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    # 原图
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return alpha, img


def paste_with_a(image_background, image_pasted, pos):
    _, _, _, a = image_pasted.convert('RGBA').split()
    image_background.paste(image_pasted, pos, mask=a)


def get_stage_card(name1, name2, contest_mode, game_mode, start_time, end_time, img_size=(1024, 340)):
    _, image_background = circle_corner(get_file('background').resize(img_size), radii=20)

    stage_size = (int(img_size[0]*0.48), int(img_size[1]*0.7))
    image_left = get_file(name1).resize(stage_size, Image.ANTIALIAS)
    image_right = get_file(name2).resize(stage_size, Image.ANTIALIAS)
    _, image_alpha = circle_corner(image_left, radii=16)

    width_between_stages = int((img_size[0] - 2*stage_size[0])/3)
    start_stage_pos = (width_between_stages, int((img_size[1]-stage_size[1])/8*7))
    image_background.paste(image_left, start_stage_pos, mask=image_alpha)
    next_stage_pos = (start_stage_pos[0] + width_between_stages + stage_size[0], start_stage_pos[1])
    image_background.paste(image_right, next_stage_pos, mask=image_alpha)

    stage_mid_pos = (img_size[0]//2 - 60, img_size[1]//2 - 20)
    image_icon = get_file(contest_mode)
    paste_with_a(image_background, image_icon, stage_mid_pos)

    blank_size = (img_size[0], start_stage_pos[1])
    drawer = ImageDraw.Draw(image_background)
    ttf = ImageFont.truetype(ttf_path, 40)
    drawer.text((40, start_stage_pos[1]-60), contest_mode, font=ttf, fill=(255, 255, 255))
    ttf = ImageFont.truetype(ttf_path, 50)
    drawer.text((blank_size[0]//4, 4), game_mode, font=ttf, fill=(255, 255, 255))
    ttf = ImageFont.truetype(ttf_path, 40)
    drawer.text((blank_size[0]*2//3, 20), '{} - {}'.format(start_time, end_time), font=ttf, fill=(255, 255, 255))

    return image_background


def get_stages(schedule, num_list, contest_match=None, rule_match=None):
    regular = schedule['regular']
    ranked = schedule['gachi']
    league = schedule['league']
    cnt = 0
    for idx in num_list:
        if contest_match is None or contest_match == 'Turf War':
            if rule_match is None or rule_match == regular[idx]['rule']['name']:
                cnt += 1

        if contest_match is None or contest_match == 'Ranked':
            if rule_match is None or rule_match == ranked[idx]['rule']['name']:
                cnt += 1

        if contest_match is None or contest_match == 'League':
            if rule_match is None or rule_match == league[idx]['rule']['name']:
                cnt += 1

    background = Image.new('RGB', (1044, 340*cnt), (41, 36, 33))
    pos = 0
    for idx in num_list:
        if contest_match is None or contest_match == 'Turf War':
            if rule_match is None or rule_match == regular[idx]['rule']['name']:
                regular_card = get_stage_card(
                    regular[idx]['stage_a']['name'],
                    regular[idx]['stage_b']['name'],
                    'Regular',
                    regular[idx]['rule']['name'],
                    time_converter(regular[idx]['start_time']),
                    time_converter(regular[idx]['end_time']),
                )
                paste_with_a(background, regular_card, (10, pos))
                pos += 340

        if contest_match is None or contest_match == 'Ranked':
            if rule_match is None or rule_match == ranked[idx]['rule']['name']:
                ranked_card = get_stage_card(
                    ranked[idx]['stage_a']['name'],
                    ranked[idx]['stage_b']['name'],
                    'Ranked',
                    ranked[idx]['rule']['name'],
                    time_converter(ranked[idx]['start_time']),
                    time_converter(ranked[idx]['end_time']),
                )
                paste_with_a(background, ranked_card, (10, pos))
                pos += 340

        if contest_match is None or contest_match == 'League':
            if rule_match is None or rule_match == league[idx]['rule']['name']:
                league_card = get_stage_card(
                    league[idx]['stage_a']['name'],
                    league[idx]['stage_b']['name'],
                    'League',
                    league[idx]['rule']['name'],
                    time_converter(league[idx]['start_time']),
                    time_converter(league[idx]['end_time']),
                )
                paste_with_a(background, league_card, (10, pos))
                pos += 340
    return image_to_base64(background)


if __name__ == '__main__':
    img = get_stage_card('Ancho-V Games', 'Arowana Mall', 'Regular', 'Turf War', '08:00', '10:00', (1024, 340))
    # img = get_file('background').resize((2048, 680))
    # drawer = ImageDraw.Draw(img)
    # ttf = ImageFont.truetype(ttf_path, 40)
    # drawer.text((50, 110), '喷', font=ttf, fill=(255, 255, 255))
    img.show()
