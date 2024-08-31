from src.utils.utils import open_image
from PIL import Image

def flatten(lst, num=1):
    """
    将嵌套的列表展开
    :param lst: 嵌套的列表
    :param num: 展开的层数
    :return: 展开后的列表
    """
    flattened_list = []
    for item in lst:
        if isinstance(item, list) and num > 0:
            flattened_list.extend(flatten(item, num - 1))
        else:
            flattened_list.append(item)
    return flattened_list


def crop_nine(input_file: str) -> list[Image.Image]:
    """
    将图片裁剪成九宫格
    :param input_file: 输入图片路径
    :return: 九宫格图片列表, 按照从左到右，从上到下的顺序排列
    """

    img = open_image(input_file)
    width, height = img.size
    h = height // 3
    w = width // 3
    crop_img_list = []
    for i in range(3):
        for j in range(3):
            x = j * w
            y = i * h
            crop_img = img.crop((x, y, x+w, y+h))
            crop_img_list.append(crop_img)
    return crop_img_list