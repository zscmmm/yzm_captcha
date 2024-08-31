from typing import Tuple, Optional, List, Union
from dataclasses import dataclass
from src.utils.yoloclass import Shape, Labelme
from pathlib import Path
import os
from PIL import Image, ImageDraw, ImageFont
@dataclass
class Coordination:
    charsImage: List[Image.Image] = None
    targetsImage: List[Image.Image] = None
    chars_xyxy: List[List[float]] = None
    targets_xyxy: List[List[float]] = None
    chars_name: List[str]  = None
    targets_name: List[str] = None
    extraicon: Optional[Union[str,Image.Image]] = None
    indices: Optional[Tuple[int, int]] = None
    exist_error: Optional[bool] = None
    nine_rowcol: Optional[Tuple[int, int]] = None
    chars_xywh: Optional[List[List[float]]] = None
    targets_xywh: Optional[List[List[float]]] = None
    def set_value(self, key, value):
        assert hasattr(self, key), f"key {key} not in Coordination"
        setattr(self, key, value)

    def get_value(self, key):
        assert hasattr(self, key), f"key {key} not in Coordination"
        return getattr(self, key)
    
    def rank(self):  
        assert self.indices is not None, "indices is None"

        self.chars_rank, self.targets_rank = zip(*self.indices)

        self.charsImage = [self.charsImage[i] for i in self.chars_rank] if self.charsImage  else None
        self.targetsImage = [self.targetsImage[i] for i in self.targets_rank] if self.targetsImage  else None
        self.chars_xyxy = [self.chars_xyxy[i] for i in self.chars_rank] if self.chars_xyxy  else None
        self.targets_xyxy = [self.targets_xyxy[i] for i in self.targets_rank] if self.targets_xyxy  else None
        # 保留 2 位小数
        self.chars_xyxy = [[round(j, 2) for j in i] for i in self.chars_xyxy] if self.chars_xyxy  else None
        self.targets_xyxy = [[round(j, 2) for j in i] for i in self.targets_xyxy] if self.targets_xyxy  else None
        self.chars_xywh = self.xyxy2xywh(self.chars_xyxy) if self.chars_xyxy else None
        self.targets_xywh = self.xyxy2xywh(self.targets_xyxy) if self.targets_xyxy else None
    def to_dict(self):
        exclude = ["charsImage", "targetsImage", "indices", "chars_rank", "targets_rank"]
        return {k: v for k, v in self.__dict__.items() if v is not None and k not in exclude}

    def xyxy2xywh(self, xyxy):
        if not xyxy:
            return None
        assert isinstance(xyxy, list), "xyxy should be a list"
        assert all([len(i) == 4 for i in xyxy]), "xyxy should have 4 elements"
        return [[ (i[0] + i[2]) / 2, (i[1] + i[3]) / 2, i[2] - i[0], i[3] - i[1]] for i in xyxy]



@dataclass
class Outfile:

    @staticmethod
    def concatenate_images(images: List[Image.Image]) -> Image.Image:
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        concatenated_image = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in images:
            concatenated_image.paste(img, (x_offset, 0))
            x_offset += img.width

        return concatenated_image

    @staticmethod
    def check_format(data):
        if not isinstance(data, list):
            return False  # 如果不是列表，则格式不符合要求
        
        for sublist in data:
            if not isinstance(sublist, list):
                return False  # 如果子列表不是列表，或者长度不等于4，则格式不符合要求
            for item in sublist:
                if not isinstance(item, (int, float)):
                    return False  # 如果子列表中的元素不是浮点数，则格式不符合要求
        return True

    @staticmethod  
    def load_font(font_path: str, font_size: int) -> Optional[ImageFont.FreeTypeFont]:
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception as e:
            # print(f"Error loading font: {e}")
            return None
        
    @staticmethod       
    def draw_image(image_path:str, chars_xyxy:list =None, targets_xyxy:list = None, out_path=None):
        assert os.path.exists(image_path), f"{image_path} not exists"
        assert chars_xyxy is not None or targets_xyxy is not None, "chars_xyxy or targets_xyxy must be not None"

        img = Image.open(image_path)
        out_path = image_path.replace(".png", "_out.png") if out_path is None else out_path
 
        # ##把坐标在图中画出来
        draw = ImageDraw.Draw(img)
        try:
            font_path = os.path.join(os.path.dirname(__file__), "simsun.ttc")
        except:
            font_path = None

        if Outfile.check_format(chars_xyxy):
            font = Outfile.load_font(font_path, (chars_xyxy[0][2] - chars_xyxy[0][0]) // 2)
            for index, xyxy in enumerate(chars_xyxy):
                
                draw.rectangle(xyxy, outline="red", width=3)
                # draw.text((xyxy[0], xyxy[1]), str(index),  fill="blue", font=font)  
                x = xyxy[0]
                y = xyxy[1]
                text = str(index)
                offset = 0.1
                text_color = "blue"
                draw.text((x, y), text,  fill= text_color, font=font)  
                draw.text((x - offset, y - offset), text, font=font, fill=text_color)
                draw.text((x + offset, y - offset), text, font=font, fill=text_color)
                draw.text((x - offset, y + offset), text, font=font, fill=text_color)
                draw.text((x + offset, y + offset), text, font=font, fill=text_color)

        if chars_xyxy and all([isinstance(i, Image.Image) for i in chars_xyxy]):
            # 把这些图按顺序拼接起来, 放到图的左下角
            concat_image = Outfile.concatenate_images(chars_xyxy)
            # 按比例进行缩放
            concat_image = concat_image.resize((concat_image.width//4, concat_image.height // 4))
            # 将拼接后的图像放到原始图像的左下角
            img.paste(concat_image, (0, img.height - concat_image.height))

        
        if targets_xyxy is not None:
            font = Outfile.load_font(font_path, (targets_xyxy[0][2] - targets_xyxy[0][0]) // 2)
            for index, xyxy in enumerate(targets_xyxy):
                draw.rectangle(xyxy, outline="blue", width=3)
                x = xyxy[0]
                y = xyxy[1]
                text = str(index)
                offset = 0.1
                text_color = "red"
                draw.text((x, y), text,  fill= text_color, font=font)  
                draw.text((x - offset, y - offset), text, font=font, fill=text_color)
                draw.text((x + offset, y - offset), text, font=font, fill=text_color)
                draw.text((x - offset, y + offset), text, font=font, fill=text_color)
                draw.text((x + offset, y + offset), text, font=font, fill=text_color)
        img.save(out_path)
        
    
    @staticmethod
    def word3to_labelme(image_path: str, 
                        chars_xyxy: list,
                        targets_xyxy: list,
                        chars_name: list,
                        targets_name: list,
                        size: Tuple[int, int] = (384, 344),
                        output_dir:str = None,
                        showWarning: bool = True
                    ) -> Labelme:
        if chars_xyxy is None and chars_name is None and showWarning:
            print("Warning: chars_xyxy and chars_name are None")
        assert len(targets_xyxy) == len(targets_name), "targets_xyxy and targets_name should have the same length"
        assert isinstance(targets_xyxy, list), "targets_xyxy should be a list"
        assert isinstance(targets_name, list), "targets_name should be a list"

        os.makedirs(output_dir, exist_ok=True)

        labelme = Labelme()
        labelme.set_size(*size)
        labelme.set_imagePath(os.path.join("../", Path(image_path).parent.stem, Path(image_path).name))
        for i in range(len(targets_xyxy)):
            if chars_xyxy:
                ichar_shape1 = Shape() #创建一个空的shape
                ichar_shape1.set_points(chars_xyxy[i])
                ichar_shape1.set_group_id(int(i))
                ichar_shape1.set_label("char")
                ichar_shape1.set_text(chars_name[i])
                ichar_shape1.set_description(chars_name[i])
                labelme.shapes.append(ichar_shape1.to_dict())
            if targets_xyxy:
                itarget_shape1 = Shape() #创建一个空的shape
                itarget_shape1.set_points(targets_xyxy[i])
                itarget_shape1.set_group_id(int(i))
                itarget_shape1.set_label("target")
                itarget_shape1.set_text(targets_name[i])
                itarget_shape1.set_description(targets_name[i])
                labelme.shapes.append(itarget_shape1.to_dict())

        new_json = os.path.join(output_dir, f"{Path(image_path).stem}.json")
        labelme.to_json_file(new_json)
        return labelme


    @staticmethod
    def to_labelme(image_path:str, info:Coordination,  size: Tuple[int, int] = (384, 344), output_dir:str = None) -> Labelme:
        """
        image_path: 图片路径, 不读取图片, 只是用来生成 json 文件
        info: Coordination 类型, 包含了图片的坐标信息
        output_dir: 输出的文件夹
        """
        assert isinstance(info, Coordination), "input should be Coordination"
        # 调用 word3to_labelme
        return Outfile.word3to_labelme(image_path, 
                                       info.chars_xyxy, info.targets_xyxy, 
                                       info.chars_name, info.targets_name,
                                      size=size,
                                       output_dir=output_dir)


