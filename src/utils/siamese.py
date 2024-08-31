"""
来自项目: _
"""

from PIL import Image
from PIL.PngImagePlugin import PngImageFile
import numbers
import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))



def cvtColor(image):
    if len(np.shape(image)) == 3 and np.shape(image)[2] == 3:
        return image 
    else:
        image = image.convert('RGB')
        return image 
    
def preprocess_input(x):
    x /= 255.0
    return x

def resize(img, size, interpolation=Image.BILINEAR):
    if isinstance(size, int):
        w, h = img.size
        if (w <= h and w == size) or (h <= w and h == size):
            return img
        if w < h:
            ow = size
            oh = int(size * h / w)
            return img.resize((ow, oh), interpolation)
        else:
            oh = size
            ow = int(size * w / h)
            return img.resize((ow, oh), interpolation)
    else:
        return img.resize(size[::-1], interpolation)

def crop(img, i, j, h, w):
    return img.crop((j, i, j + w, i + h))

def center_crop(img, output_size):
    if isinstance(output_size, numbers.Number):
        output_size = (int(output_size), int(output_size))
    w, h = img.size
    th, tw = output_size
    i = int(round((h - th) / 2.))
    j = int(round((w - tw) / 2.))
    return crop(img, i, j, th, tw)

def letterbox_image(image, size, letterbox_image):
    w, h = size
    iw, ih = image.size
    if letterbox_image:
        '''resize image with unchanged aspect ratio using padding'''
        scale = min(w/iw, h/ih)
        nw = int(iw*scale)
        nh = int(ih*scale)

        image = image.resize((nw,nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    else:
        if h == w:
            new_image = resize(image, h)
        else:
            new_image = resize(image, [h ,w])
        new_image = center_crop(new_image, [h ,w])
    return new_image



def detect_image(image_1:PngImageFile, image_2:PngImageFile, image_width:int =60, image_height:int = 60):
    """
    输入图片的路径，做预处理,返回预处理后的图片
    image_1: PngImageFile数据类型, 由 PIL.Image.open() 读取的图片
    image_2: PngImageFile数据类型
    image_width: 图片的宽
    image_height: 图片的高
    return: photo_1, photo_2
    """
    assert isinstance(image_1, Image.Image), "image_1 should be a Image.Image"
    #---------------------------------------------------------#
    #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
    #---------------------------------------------------------#
    image_1 = cvtColor(image_1)
    image_2 = cvtColor(image_2)
    
    #---------------------------------------------------#
    #   对输入图像进行不失真的resize
    #---------------------------------------------------#
    image_1 = letterbox_image(image_1, [image_width, image_height],False)   
    image_2 = letterbox_image(image_2, [image_width, image_height],False)
    #---------------------------------------------------------#
    #   归一化+添加上batch_size维度
    #---------------------------------------------------------#
    photo_1  = preprocess_input(np.array(image_1, np.float32))
    photo_2  = preprocess_input(np.array(image_2, np.float32))

 
    #---------------------------------------------------#
    #   添加上 batch 维度，才可以放入网络中预测
    #---------------------------------------------------#
    photo_1 = np.expand_dims(np.transpose(photo_1, (2, 0, 1)), 0).astype(np.float32)
    photo_2 = np.expand_dims(np.transpose(photo_2, (2, 0, 1)), 0).astype(np.float32)

    return photo_1, photo_2



if __name__ == '__main__':
    image_1 = "testimg/pic_00273_99704_target0.png"
    image_2 = "testimg/pic_00273_99704_target0.png"
    image_1 = Image.open(image_1)
    image_2 = Image.open(image_2)
    image_width = 60
    image_height = 60

    photo_1, photo_2 = detect_image(image_1, image_2, image_width, image_height)



