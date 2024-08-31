from ultralytics import YOLO
from src.utils.utils import get_onnx_shape
from ultralytics.utils.checks import cuda_is_available


class YoloD(YOLO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        tempmodel = self.model
        if isinstance(tempmodel, str) and tempmodel.endswith(".onnx"):
            self.imgsz = get_onnx_shape(tempmodel)
        else:
            self.imgsz = self.model.args["imgsz"]
            if isinstance(self.imgsz, (int, float)):
                self.imgsz = [self.imgsz, self.imgsz]
            elif isinstance(self.imgsz, (list, tuple)) and len(self.imgsz) == 1:
                self.imgsz = [self.imgsz[0], self.imgsz[0]]
        if cuda_is_available():
            self._cuda = True
            self._device = 'cuda:0'
        else:
            self._cuda = None  
            self._device = None  


    def extract_info(self, results)-> tuple[list[list], list[list], list[str], list[dict]]:
        """
        只对单张图片进行检测处理
        返回的是 xyxy, xywh, box_name, info
        xyxy: [[x1, y1, x2, y2], [x1, y1, x2, y2], ...]
        xywh: [[x, y, w, h], [x, y, w, h], ...]
        box_name: ["A", "B", ...]
        info: [
            {
                "classes": "A", 
                "prob": 0.9,
                "xyxy": [x1, y1, x2, y2],
                "xywh": [x, y, w, h]
            }, 
            ...
        ]

        """
        assert self.task == "detect", "detect only support detect task"
        assert len(results) == 1, "detect only support single image"
        xyxy_all = []
        xywh_all = []
        name_all = results[0].names
        #取出name_all 的 value
        box_name = []
        info = []
        for result in results:
            box_cls = result.boxes.cls.tolist()
            xyxy = result.boxes.xyxy.tolist()
            xywh = result.boxes.xywh.tolist()
            probs = result.probs
            for i in range(len(box_cls)):
                box_name.append(name_all[box_cls[i]])
                info.append({
                    "classes": name_all[box_cls[i]], 
                    "prob": 1 if not probs else round(probs[i].item(), 2),
                    "xyxy": xyxy[i],
                    "xywh": xywh[i],
                })
            xyxy_all.append(xyxy)
            xywh_all.append(xywh)
            break   # 只对单张图片进行检测处理
        
        return xyxy_all[0], xywh_all[0], box_name, info



class YoloC(YOLO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tempmodel = self.model
        if isinstance(tempmodel, str) and tempmodel.endswith(".onnx"):
            self.imgsz = get_onnx_shape(tempmodel)
        else:
            self.imgsz = self.model.args["imgsz"]
            if isinstance(self.imgsz, (int, float)):
                self.imgsz = [self.imgsz, self.imgsz]
            elif isinstance(self.imgsz, (list, tuple)) and len(self.imgsz) == 1:
                self.imgsz = [self.imgsz[0], self.imgsz[0]]
        if cuda_is_available():
            self._cuda = True
            self._device = 'cuda:0'
        else:
            self._cuda = None  
            self._device = None    

    def extract_info(self, result)  -> tuple[str, float, list[str], list[float]]:
        """ 
        对结果进行分类
        :param result: 识别结果
        :return: top1name, top1conf, top5name, top5conf
        top1name: 最大概率对应的类别
        top1conf: 最大概率
        top5name: 前五的类别
        top5conf: 前五的概率
        """
        assert self.task == "classify", "classify only support classify task"
        assert len(result) == 1, "classify only support single image"
        all_names = result[0].names ##  类别字典
        top1 = result[0].probs.top1 #最大概率对应的索引
        top1name = all_names[top1] #最大概率对应的类别
        top1conf = result[0].probs.top1conf.tolist() #最大概率
        top5 = result[0].probs.top5 #前五的索引
        top5conf = result[0].probs.top5conf.tolist() #前五的概率
        top5name = [all_names[i] for i in top5]
        # info = {   
        #     "top1": top1,
        #     "top1name": top1name,
        #     "top1conf": top1conf,
        #     "top5": top5,
        #     "top5name": top5name,
        #     "top5conf": top5conf
        # }
        return top1name,  top1conf, top5name, top5conf


if __name__ == '__main__':
    path_yolo_detect = "model/g3word6300/detect.pt"
    path_per = "model/g3word6300/simvgg19.onnx"
    path_yolo_class = "model/g3word6300/muti.pt"

    ##### 对于检测模型的测试
    # m1 = YoloD(path_yolo_detect, task="detect", verbose=False)
    # m1.imgsz

    # m3 = YOLO(path_yolo_detect, task="detect", verbose=False)
    # m3.model.args["imgsz"]