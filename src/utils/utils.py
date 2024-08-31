from typing import Tuple, Optional
from PIL import Image
from io import BytesIO
import numpy as np
import onnxruntime as ort
import base64
import os
from pathlib import Path
def get_onnx_shape(onnx_model: str) -> tuple:
    providers = ['CPUExecutionProvider']
    options = ort.SessionOptions()
    options.enable_profiling=False
    model = ort.InferenceSession(
        onnx_model, 
        sess_options = options,
        providers=providers
    )
    input_info = model.get_inputs()
    input_shape = input_info[0].shape[2:4] # 先高度后宽度
    del model
    return input_shape


def process_similarity_matrix(similarity_matrix:np.ndarray | list[list[float]]) -> list[tuple[int, int]]:
    """
    处理相似度矩阵, 返回最大值的索引且不重复
    :param similarity_matrix: 相似度矩阵
    :return: 行索引和列索引的列表
    """
    if not isinstance(similarity_matrix, np.ndarray):
        similarity_matrix = np.array(similarity_matrix)
    # rows, cols = similarity_matrix.shape
    final_indices = []
    while True:
        #无参数的时候,把矩阵按行展开成一维数组,然后返回最大值的索引,如果有多个最大值,返回第一个
        max_index = np.argmax(similarity_matrix)
        #根据索引返回行和列
        max_i, max_j = np.unravel_index(max_index, similarity_matrix.shape)
        if similarity_matrix[max_i][max_j] == -np.inf:
            break
        final_indices.append((max_i, max_j))
        similarity_matrix[max_i, :] = -np.inf
        similarity_matrix[:, max_j] = -np.inf

    # 对 final_indices 按照行进行排序
    final_indices.sort(key=lambda x: x[0])
    return final_indices

def is_base64(s: str) -> bool:
    """
    判断字符串是否是 base64 编码
    :param s: 字符串
    :return: 是否是 base64 编码
    """
    try:
        # 如果能解码则返回 True
        base64.b64encode(base64.b64decode(s)) == s
        return True
    except Exception:
        return False

#打开图片
def open_image(file: str, rmalpha:bool = False, output_path: Optional[str] = None) -> Image.Image:
    if isinstance(file, list):
        print("Warning: Multiple images provided")
        img = [open_image(f, rmalpha, output_path) for f in file]
        
    elif isinstance(file, np.ndarray):
        img = Image.fromarray(file)
    elif is_base64(file) and isinstance(file, str):
        img = Image.open(BytesIO(base64.b64decode(file)))
    elif isinstance(file, bytes):
        img = Image.open(BytesIO(file))
    elif isinstance(file, Image.Image):
        img = file
    elif isinstance(file, Path) and file.exists():
        img = Image.open(file)
    elif isinstance(file, str) and os.path.exists(file):
        img = Image.open(file)
    else:
        assert False, "file type is not supported"

    if img.mode == 'RGBA' and rmalpha:
        # 检查图像是否具有 alpha 通道, 创建一个白色背景的图像
        white_bg = Image.new("RGB", img.size, (255, 255, 255))
        # 将原始图像粘贴到白色背景上
        white_bg.paste(img, mask=img.split()[3])        
        img = white_bg
        img = img.convert('RGB')
    elif img.mode == 'RGB':
        pass
    else:
        img = img.convert('RGB')

    if output_path:
        img.save(output_path)
    return img


#调整坐标
def adjust_coordinates(coordinates: list, image_size: Tuple[float, float], toint: bool= True) -> list:
    """
    输入提供的是两个坐标点: 格式为 [[x1, y1], [x2, y2]]，其中 x1, y1 是左上角坐标，x2, y2 是右下角坐标。
    或者是
    四个坐标点: 格式为 [x1, y1, x2, y2]，其中 x1, y1 是左上角坐标，x2, y2 是右下角坐标。
    如果不是左上角和右下角，则进行调整
    :param coordinates: 坐标
    :return: 调整后的坐标,格式为 [x1, y1, x2, y2]
    """
    # 确保提供的坐标是一个包含两个点的列表
    if len(coordinates) == 2:
        # 获取坐标点的 x 和 y 值
        x1, y1, x2, y2 = coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1]
    elif len(coordinates) == 4:
        x1, y1, x2, y2 = coordinates
    else:
        raise ValueError("Invalid coordinates format. It should be either [[x1, y1], [x2, y2]] or [x1, y1, x2, y2]")

    width, height = image_size
    # 确保坐标在图像范围内
    x1 = min(x1, width)
    x2 = min(x2, width)
    y1 = min(y1, height)
    y2 = min(y2, height)

    # 判断是否是左上角和右下角，如果不是则进行调整
    if x1 > x2 or y1 > y2:
        print("Warning: Input coordinates do not match the expected format, adjusting coordinates.")
        # 交换 x 和 y 值，以确保左上角和右下角的关系
        x1, y1, x2, y2 = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        # print("Adjusted coordinates to match the expected format.")
    # 返回调整后的坐标
    if toint:
        return [int(x1), int(y1), int(x2), int(y2)]
    else:
        return [x1, y1, x2, y2]


# 根据坐标进行裁剪
def crop_and_save_image(input_path, coordinates:list, output_path:str):
    # 打开图像
    original_image = Image.open(input_path)
    image_size = original_image.size
    x1, y1, x2,y2 = adjust_coordinates(coordinates, image_size, toint=False)
    # 裁剪图像
    cropped_image = original_image.crop((x1, y1, x2, y2))
    # 保存图像
    cropped_image.save(output_path)


def find_max_probability(ichars_five_name, ichars_five_prob, itargets_five_name, itargets_five_prob):
    # 创建字典将名称和概率关联起来
    ichars_dict = dict(zip(ichars_five_name, ichars_five_prob))
    itarget_dict = dict(zip(itargets_five_name, itargets_five_prob))
    
    merged_dict = ichars_dict.copy()
    for key, value in itarget_dict.items():
        if key in merged_dict:
            merged_dict[key] += value
        else:
            merged_dict[key] = value
    # 找到概率最大的名称
    max_name = max(merged_dict, key=merged_dict.get)
    max_prob = merged_dict[max_name]
    return max_name, round(max_prob / 2, 2)

        
if __name__ == '__main__':
    
    similarity_matrix = [
        [0.1, 0, 0.5],
        [0.7, 1, 0.8],
        [1, 0.6, 1],
    ]

    # 调用函数处理相似度矩阵
    final_indices = process_similarity_matrix(similarity_matrix)

    # 打印处理后的索引列表
    print(final_indices)

    ichars_three_name = ['a', 'b', 'c']
    ichars_three_prob = [0.1, 0.2, 0.3]
    itargets_three_name = ['b1', 'c1', 'd1']
    itargets_three_prob = [0.2, 0.3, 0.4]

    # 调用函数
    max_name, max_prob = find_max_probability(ichars_three_name, ichars_three_prob, itargets_three_name, itargets_three_prob)

    # 打印结果
    print("最大概率对应的名称:", max_name)
    print("最大概率:", max_prob)





