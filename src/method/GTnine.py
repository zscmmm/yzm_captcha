from src.utils.YoloOnnx import YoloC
from src.utils.utils import open_image, find_max_probability
from typing import Optional, Union
from PIL import Image
from src.utils.outdata import Coordination
from src.utils.SiameseOnnx import SiameseOnnx
from src.utils.nine import crop_nine, flatten
import os
import pandas as pd




class GTnine():
    def __init__(
            self,
            path_yolo_class: Optional[str] = None,
            path_per: Optional[str] = None,
            conf=0.65, 
            rmalpha: bool = True, 
            verbose=False,
        ) -> None:
        '''
        暂时实现 yolo 分类模型, 感觉孪生神经网络模型不太适合
        '''
        assert path_yolo_class or path_per, "path_yolo_class and path_per is None"
        self.path_yolo_class = path_yolo_class
        self.path_per = path_per


        self.modeltype = None
        self.conf = conf 
        self.verbose = verbose
        self.rmalpha = rmalpha

        if self.path_yolo_class and not self.path_per:
            self.modeltype = 1
            self.modelyoloc = YoloC(self.path_yolo_class, task="classify", verbose=self.verbose)
        elif self.path_per and not self.path_yolo_class:
            self.modeltype = 2
            self.modelpre = SiameseOnnx(self.path_per, providers=['CPUExecutionProvider'])
        else:
            self.modeltype = 3
            self.modelyoloc = YoloC(self.path_yolo_class, task="classify", verbose=self.verbose)
            self.modelpre = SiameseOnnx(self.path_per, providers=['CPUExecutionProvider'])
    


    def _preprocess(self, charimg: Union[list, str], background:str)-> tuple[list[Image.Image], list[Image.Image]]:
        if isinstance(charimg, str):
            # 如果是 str 则表面是路径,一定要存在
            assert os.path.exists(charimg), f"{charimg} not exists"
            charimg = [charimg]
        
        charimg = [open_image(i, rmalpha=self.rmalpha) for i in charimg]
        
        if isinstance(background, str):
            assert os.path.exists(background), f"{background} not exists"
            self._image_path = background
        elif isinstance(background, Image.Image):
            self._image_path = None
        else:
            assert False, "background type is not supported"
        
        self._img = open_image(background)
        self._bgsize = self._img.size
        crop_nine_list = crop_nine(background)

        return charimg, crop_nine_list
    def _get_similarity_byper(self, charimg: list, crop_nine_list: list, num: int = None):
        mat = []
        for index, i in enumerate(charimg):
            for index_j, j in enumerate(crop_nine_list):
                prob = self.modelpre.predict(i, j)
                mat.append({
                    "index": index,
                    "name": None,
                    "conf": prob,
                    "msilce": index_j
                })
        # 从 mat 中找出 conf > self.conf 的元素
        df = pd.DataFrame(mat)
        # 按照 conf 降序排列
        df = df.sort_values(by="conf", ascending=False)
        if num:
            df = df.head(num)
        else:
            df = df[df["conf"] > self.conf]
        
        # 按照 index 分组,
        dfg = df.groupby("index")
        silece_list = []
        for name, group in dfg:
            silece_list.append(group["msilce"].tolist())
        return silece_list, None
    
    def _get_similarity_byyolo(self, charimg: list, crop_nine_list: list, num: int = None):
        mat = []
        for index, i in enumerate(charimg):
            results_char = self.modelyoloc.predict(i, 
                conf=self.conf,  
                imgsz=self.modelyoloc.imgsz,
                verbose= self.verbose,  
                device = self.modelyoloc._device
            )

            ic_top1name,  ic_top1conf, ic_top5name, ic_top5conf = self.modelyoloc.extract_info(results_char)
            for index_j, j in enumerate(crop_nine_list):
                results = self.modelyoloc.predict(j,
                    conf=self.conf,  
                    imgsz=self.modelyoloc.imgsz,
                    verbose= self.verbose,  
                    device = self.modelyoloc._device
                )
                it_top1name,  it_top1conf, it_top5name, it_top5conf = self.modelyoloc.extract_info(results)
                
                imax_name, imax_prob = find_max_probability([ic_top1name], [ic_top1conf] , it_top5name, it_top5conf)
                # 返回的概率至少都是大于 0.5 的. 
                mat.append({
                        "index": index, 
                        "top1name": ic_top1name,
                        "top1conf": ic_top1conf,
                        "name": imax_name,
                        "conf": imax_prob,
                        "msilce": index_j
                })


        # 从 mat 中找出 conf > self.conf 的元素
        df = pd.DataFrame(mat)
        # 按照 conf 降序排列
        df = df.sort_values(by="conf", ascending=False)
        if num:
            df = df.head(num)
        else:
            df = df[df["conf"] > self.conf]
        
        # 按照 index 分组,
        dfg = df.groupby("index")
        silece_list = []
        name_list = []
        for name, group in dfg:
            silece_list.append(group["msilce"].tolist())
            name_list.append(group["name"].tolist())
        return silece_list, name_list

 
    def reset_outdata(self):
        self.coordination = Coordination()


    def run(self, background: Union[ str , list, Image.Image] , charimg: Union[str, list]) -> Coordination:
        """
        background: 背景图,即大图, 如果是 list,只支持一个元素
        charimg: 具有顺序的小图标
        """
        assert background, "background is None"
        if isinstance(background, list) and len(background) > 1:
            print("Warning: background is list, only support one element")  
            background = background[0]
        elif isinstance(background, list) and len(background) == 1:
            background = background[0]
        

        self.reset_outdata()
        charimg, crop_nine_list = self._preprocess(charimg, background)

        self.coordination.set_value("charsImage", flatten(charimg))

        if self.modeltype == 1:
            indices, names = self._get_similarity_byyolo(charimg, crop_nine_list)
        elif self.modeltype == 2:
            indices, names = self._get_similarity_byper(charimg, crop_nine_list)
        else:
            indices1, names1 = self._get_similarity_byyolo(charimg, crop_nine_list)
            indices2, names2 = self._get_similarity_byper(charimg, crop_nine_list)
            # 可以用来查找两个模型的差异
            indices = indices1
        
        
        rowcol = self.get_rowcol(indices)
        xyxy = self.get_xyxy(indices, self._bgsize)
        self.coordination.set_value("nine_rowcol",  rowcol)
        # 展平
        xyxy = flatten(xyxy)
        names = flatten(names)
        self.coordination.set_value("targets_xyxy", xyxy)
        self.coordination.set_value("targets_name", names)

        return self.coordination
    def get_rowcol(self, indices: list):
        res = []
        maplist = {
            "0": [1,1],
            "1": [1,2],
            "2": [1,3],
            "3": [2,1],
            "4": [2,2],
            "5": [2,3],
            "6": [3,1],
            "7": [3,2],
            "8": [3,3],
        }
        res = [maplist[str(i)] for i in indices[0]]
        return res
    def get_xyxy(self, indices: list, size: tuple):
        res = []
        width, height = size
        h = height // 3 - 1
        w = width // 3 - 1
        for ind in range(len(indices)):
            row = []
            for j in indices[ind]:
                x = (j % 3) * w
                y = (j // 3) * h
                row.append([x, y, x+w, y+h])
            res.append(row)
        return res



if __name__ == "__main__":
    gt = GTnine(path_yolo_class="model/nine3/best.pt")
    charimg = "assets/nine3/ques_00000_37458.png"
    background = "assets/nine3/img_00000_37458.png"
    out = gt.run(background, charimg)
    from src.utils.outdata import Outfile
    Outfile.draw_image(background, 
                       chars_xyxy= out.get_value("charsImage"),
                       targets_xyxy = out.get_value("targets_xyxy"), 
                       out_path="temp3/temp1.png"
                       )




