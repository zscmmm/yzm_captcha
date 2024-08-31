
from src.utils.SiameseOnnx import SiameseOnnx
from src.utils.YoloOnnx import YoloD, YoloC
from src.utils.utils import open_image, find_max_probability, process_similarity_matrix
from typing import Optional, Union
from PIL import Image
from src.utils.outdata import Coordination
import numpy as np
from pathlib import Path


class GModel(object):
    def __init__(
            self, 
            pdetect: str,
            per: str,
            pclass: Optional[str] = None,
            pclasstags: list[str] = ["icon"], #会根据这个类别来进行分类, 最多支持两个类别, 如果是两个,则第一个是具有顺序的字符类别,第二个是目标类别
            chars_issorted: bool = False, # 当 chars_issorted 为 True 时, 表示手动输入chars 类别,并且具有顺序, 只有 pclasstags 为1时才有效
            rmalpha: bool = False, # 只有在 chars_issorted 为 True 时才有效
            conf=0.65, 
            verbose=False,
            **kwargs
        ):
        """
        实现图像点选功能, 通过 yolo 检测模型找到目标,然后利用孪生神经网络对图片进行排序, 找出对应相似度最高的图片,最后利用 yolo 分类模型进行字符识别
        参数:
        - pdetect: str, yolo 检测模型路径
        - per: str, 孪生神经网络模型路径
        - pclass: Optional[str], yolo 分类模型路径
        - pclasstags: list[str], 会根据这个类别来进行分类, 最多支持两个类别, 如果是两个,则第一个是具有顺序的字符类别,第二个是目标类别
        - chars_issorted: bool, 当 chars_issorted 为 True 时, 表示手动输入chars 类别,并且具有顺序, 只有 pclasstags 为1时才有效
        - rmalpha: bool, 只有在 chars_issorted 为 True 时才有效, 表示是否去除图片的透明度
        - verbose: bool, 是否打印详细信息
        """
        self.pdetect = pdetect
        self.per = per
        self.pclass = pclass
        self.pclasstags = pclasstags
        self.conf = conf 
        self.verbose = verbose
        self.rmalpha = rmalpha
        self.chars_issorted = chars_issorted
        self.modeltype = None
        if len(self.pclasstags) == 1 and self.chars_issorted:
            self._chars_issorted = True
        else:
            self._chars_issorted = False
        assert len(self.pclasstags) in [1, 2], f"pclasstags length is not in [1, 2], but {len(self.pclasstags)}"

        self.modelyolod = YoloD(self.pdetect, task="detect", verbose=self.verbose, **kwargs)
        # 检查输入的类别是否在模型中
        if not self.per  and not self.pclass:
            assert False, f"per and pclass is None"
        elif not self.per and self.pclass:
            self.modeltype = 1
            self.modelyoloc = YoloC(self.pclass, task="classify", verbose=self.verbose, **kwargs)
        elif self.per and not self.pclass:
            self.modeltype = 2
            self.modelpre = SiameseOnnx(self.per, providers=['CPUExecutionProvider'])
        else:
            self.modeltype = 3
            self.modelyoloc = YoloC(self.pclass, task="classify", verbose=self.verbose, **kwargs)
            self.modelpre = SiameseOnnx(self.per, providers=['CPUExecutionProvider'])

        self._img = None
        self._image_path = None
        self.extraicon = None


    ### ### 1. 利用 yolo 检测模型进行检测找到目标并返回具有顺序的坐标
    def detect_objects(self, img, **kwargs) -> tuple:
        """
        利用 yolo 检测模型进行检测找到目标并返回具有顺序的坐标
        参数:
        - img: PIL.Image.Image, 图片对象
        - kwargs: dict, 其他参数
        返回:
        - tuple: (chars_xyxy, targets_xyxy)
        img: PIL.Image.Image, 图片对象
        chars_xyxy: list, 字符坐标, [[x1, y1, x2, y2], [x1, y1, x2, y2], ...]
        targets_xyxy: list, 目标坐标 [[x1, y1, x2, y2], [x1, y1, x2, y2], ...]
        """
        assert isinstance(img, Image.Image), f"img type is not Image.Image, but {type(img)}"
        imgsz1 = kwargs.get("imgsz", None)
        imgsz = imgsz1 if imgsz1 else self.modelyolod.imgsz

        results = self.modelyolod.predict(img, imgsz = imgsz,  device = self.modelyolod._device, **kwargs)
        xyxy, xywh, box_name, info = self.modelyolod.extract_info(results)
        
        ### 2. 根据目标按照坐标进行分类 (这里为验证模型, 直接采用模型预测的类别进行分类过滤)
        assert self.pclasstags[-1] in box_name, f"pclasstags[-1]: {self.pclasstags[-1]} not in box_name: {box_name}"
        targets_xyxy = [i.get("xyxy") for i in info if i.get("classes") == self.pclasstags[-1]]
        chars_xyxy= None 
        if not self._chars_issorted:
            assert len(self.pclasstags) == 2, f"pclasstags length is not 2, but {len(self.pclasstags)}"
            assert self.pclasstags[0] in box_name, f"pclasstags[0]: {self.pclasstags[0]} not in box_name: {box_name}"
            chars_xyxy = [i.get("xyxy") for i in info if i.get("classes") == self.pclasstags[0]]
            chars_xyxy.sort(key=lambda x: x[0])
            if len(chars_xyxy) != len(targets_xyxy):
                min_len = min(len(chars_xyxy), len(targets_xyxy))
                chars_xyxy = chars_xyxy[:min_len]
                targets_xyxy = targets_xyxy[:min_len]
        return chars_xyxy, targets_xyxy

    def per_sortimages(self, 
                    charsImage: list[Image.Image],
                    targetsImage: list[Image.Image],
                    **kwargs
        ) -> list[tuple[int, int]]:
        """
        利用孪生神经网络对图片进行排序, 找出对应相似度最高的图片
        :param img: PIL.Image.Image, 图片对象
        """
        imgsz1 = kwargs.get("imgsz", None)
        if isinstance(imgsz1, (int, float)):
            imgsz = [imgsz1, imgsz1]
        elif isinstance(imgsz1, (list, tuple)) and len(imgsz1) == 1:
            imgsz = [imgsz1[0], imgsz1[0]]
        else:
            imgsz = imgsz1 if imgsz1 else self.modelpre.imgsz

        indices = self.modelpre.predict_list(charsImage, targetsImage, *imgsz)
        # 返回的是图片对象
        return indices 
            

    def yolo_classify(self, charsImage, targetsImage, **kwargs):
        imax_name_list = []
        imax_prob_list = []
        prob_matrix =  np.zeros((len(charsImage), len(targetsImage)))
        for i in range(len(charsImage)):
            row_name = []
            row_prob = []
            for j in range(len(charsImage)):
                result_char = self.modelyoloc.predict(
                    charsImage[i], 
                    conf=self.conf,  
                    imgsz=self.modelyoloc.imgsz,
                    verbose=self.verbose,  
                    device = self.modelyoloc._device,
                    **kwargs
                )
                result_target = self.modelyoloc.predict(
                    targetsImage[j], 
                    conf=self.conf, 
                    imgsz=self.modelyoloc.imgsz,
                    device = self.modelyoloc._device,
                    verbose=self.verbose, 
                    **kwargs
                )
                _, _, ic_top5name, ic_top5conf = self.modelyoloc.extract_info(result_char)
                _, _, it_top5name, it_top5conf = self.modelyoloc.extract_info(result_target)
                imax_name, imax_prob = find_max_probability(ic_top5name, ic_top5conf, it_top5name, it_top5conf)
                row_name.append(imax_name)
                row_prob.append(imax_prob)
            imax_name_list.append(row_name)
            imax_prob_list.append(row_prob)
            prob_matrix[i] = row_prob
        
        final_indices = process_similarity_matrix(prob_matrix)
        char_name = [imax_name_list[i][j] for i, j in final_indices]
        target_name = [imax_name_list[i][j] for i, j in final_indices]
        return final_indices, char_name, target_name





class GTClick(GModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def openimage(self, image_path:  Union[str, Path, Image.Image]):
        if isinstance(image_path, str) or isinstance(image_path, Path):
            assert Path(image_path).exists(), f"image_path: {image_path} is not exists"
            self._image_path = image_path
        elif isinstance(image_path, Image.Image):
            self._image_path = None
        else:
            assert False, f"image_path type is not str or Image.Image, but {type(image_path)}"
        self._img = open_image(image_path)

    def reset_outdata(self):
        self.coordination = Coordination()
        
    def run(self, image_path: Union[str, Path, Image.Image], extraicon:list[str, Image.Image] = None,  **kwargs) -> Coordination:
        """
        根据图片路径进行返回结果
        :param image_path: str, 图片路径
        :param extraicon: list[str], 额外的图片路径, 用于排序
        """
        self.openimage(image_path)
        self.reset_outdata()
        
        self.coordination.set_value("extraicon", extraicon)
        ## 1. 利用 yolo 检测模型进行检测找到目标,并返回具有顺序的坐标
        chars_xyxy, targets_xyxy = self.detect_objects(self._img, conf=self.conf,  verbose=self.verbose, **kwargs)
        
        self.coordination.set_value("chars_xyxy", chars_xyxy) # 返回的 chars_xyxy 是按照顺序排列的
        self.coordination.set_value("targets_xyxy", targets_xyxy)      
        self.coordination.set_value("targetsImage", [self._img.crop(xyxy) for xyxy in targets_xyxy])
        if self._chars_issorted:
            charsImage_temp = [open_image(i, rmalpha=self.rmalpha) for i in self.coordination.get_value("extraicon")]
            self.coordination.set_value("charsImage", charsImage_temp)
        else:
            self.coordination.set_value("charsImage", [self._img.crop(xyxy) for xyxy in chars_xyxy])

        charsImage, targetsImage = self.coordination.get_value("charsImage"), self.coordination.get_value("targetsImage")
        if self.modeltype in [2]:
            indices = self.per_sortimages(charsImage, targetsImage)
            char_name= None
            target_name = None
        elif self.modeltype in [1]:
            indices, char_name, target_name = self.yolo_classify(charsImage, targetsImage)
        else:
            indices0 = self.per_sortimages(charsImage, targetsImage)
            indices, char_name, target_name = self.yolo_classify(charsImage, targetsImage)
            # 如果不一样,应该以谁为准呢? --- 可以用来判断这张图片是否需要人工干预
            if indices0 != indices:
                self.coordination.set_value("exist_error", True)
                print(f"image_path: {image_path} indices0: {indices0} indices: {indices}")
        self.coordination.set_value("chars_name", char_name)
        self.coordination.set_value("targets_name", target_name)
        self.coordination.set_value("indices", indices)
        self.coordination.rank()
        return self.coordination



