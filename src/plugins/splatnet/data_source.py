import time
import os
from PIL import Image
import base64
from io import BytesIO

cur_path = os.getcwd()


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


def get_file(name):
    img = Image.open(os.path.join(cur_path, 'src', 'plugins', 'splatnet', 'ImageData', '{}.png'.format(name)))
    return img


class StageInfoImage:
    def __init__(self):
        self.time = time.time()

    def get_stage_info(self):
        image1 = get_file('Ancho-V Games')
        return image_to_base64(image1)
