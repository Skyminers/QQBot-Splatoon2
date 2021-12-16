import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

cur_path = os.getcwd()
image_folder = os.path.join(cur_path, 'ImageData')
ttf_path = os.path.join(cur_path, 'font', 'SplatoonFontFix.otf')


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()


def get_file(name):
    # img = Image.open(os.path.join(cur_path, 'src', 'plugins', 'splatnet', 'ImageData', '{}.png'.format(name)))
    img = Image.open(os.path.join(image_folder, '{}.png'.format(name)))
    return img


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


def get_stage_card(name1, name2, contest_mode, game_mode, start_time, end_time):
    _, image_background = circle_corner(get_file('background').resize((2048, 680)), radii=20)
    image_left = get_file(name1).resize((980, 480), Image.ANTIALIAS)
    image_right = get_file(name2).resize((980, 480), Image.ANTIALIAS)
    _, image_alpha = circle_corner(image_left, radii=16)
    image_icon = get_file(contest_mode)

    image_background.paste(image_left, (20, 180), mask=image_alpha)
    image_background.paste(image_right, (1040, 180), mask=image_alpha)
    _, _, _, a = image_icon.convert('RGBA').split()
    image_background.paste(image_icon, (20, 40), mask=a)
    drawer = ImageDraw.Draw(image_background)
    ttf = ImageFont.truetype(ttf_path, 40)
    drawer.text((50, 110), contest_mode, font=ttf, fill=(255, 255, 255))
    ttf = ImageFont.truetype(ttf_path, 80)
    drawer.text((400, 20), game_mode, font=ttf, fill=(255, 255, 255))
    ttf = ImageFont.truetype(ttf_path, 60)
    drawer.text((1600, 30), '{} - {}'.format(start_time, end_time), font=ttf, fill=(255, 255, 255))

    return image_background


if __name__ == '__main__':
    img = get_stage_card('Ancho-V Games', 'Arowana Mall', 'Regular', 'Turf War', '08:00', '10:00')
    img.show()
