import onnxruntime as ort
from src.utils.siamese import detect_image, sigmoid
from src.utils.utils import  open_image, process_similarity_matrix

class SiameseOnnx():
    def __init__(self, model_path: str, providers: list[str] = ['CPUExecutionProvider']) -> None:
        options = ort.SessionOptions()
        options.enable_profiling=False
        options.add_session_config_entry('session.load_model_format', 'ONNX')
        siamese_model = ort.InferenceSession(
            model_path, 
            sess_options = options,
            providers=providers
        )
        self.model = siamese_model
        input_info = siamese_model.get_inputs()
        self.imgsz = input_info[0].shape[2:4]




    def getmodel_inputname(self):
        """
        获取模型的信息
        """
        input_info = self.model.get_inputs()
        input_name = [input.name for input in input_info]
        # input_shape = [input.shape for input in input_info]
        return input_name
    


    
    def predict_list(self, 
                     img1: list,  
                     img2: list,
                     image_width: int =None,
                     image_height: int =None
                     ) -> list[tuple[int, int]]:
        """
        输入图片, 对 img1 中的每张图片和 img2 中的每张图片进行比较,找出对应最高的相似度图片
        img1: 图片1的路径,是一个 list, 根据 img1 的顺序返回
        img2: 图片2的路径,是一个 list
        image_width: 图片的宽
        image_height: 图片的高
        indices: 是否返回索引
        return: 返回的是 img1 和 img2 的索引,比如: [(0, 1), (1, 0)], 长度为 img1 的长度 
        """
        # 检查 list 中的数据类型
        assert isinstance(img1, list), "img1 should be a list"
        assert isinstance(img2, list), "img2 should be a list"
        assert len(img1) <= len(img2), "img1 should be less than or equal to img2"
        # 补全 image_width 和 image_height
        if image_width is None:
            image_width = self.imgsz[1]
        if image_height is None:
            image_height = self.imgsz[0]

        img1 = [open_image(i) for i in img1]
        img2 = [open_image(i) for i in img2]

        if len(img1) == 0 and len(img2) == 0:
            assert False, "img1 or img2 should not be empty"
        elif len(img1) == 1 and len(img2) == 1:
            return [(0, 0)]
        
        similarity_matrix = []
        for i in img1:
            sim_row = []
            for j in img2:
                sim_row.append(self.predict(i, j, image_width, image_height))
            similarity_matrix.append(sim_row)
        final_indices = process_similarity_matrix(similarity_matrix)
        return final_indices






    def predict(self, img1: str, img2: str, image_width: int = 60, image_height: int = 60)-> float:
        """
        输入图片的路径，做预处理, 然后预测两个图片的相似度
        img1: 图片1的路径 或者 图片1的二进制数据,或者 Image.Image
        img2: 图片2的路径 或者 图片2的二进制数据 或者 Image.Image
        image_width: 图片的宽
        image_height: 图片的高
        return: 相似度, 保留两位小数
        """
        image_1 = open_image(img1)
        image_2 = open_image(img2)

        photo_1, photo_2 = detect_image(image_1, image_2, image_width, image_height)
        inputs_name = self.getmodel_inputname()
        inputs = {
            inputs_name[0]: photo_1,
            inputs_name[1]: photo_2
        }
        outs = self.model.run(None, inputs)
        
        prob = sigmoid(outs[0][0][0])
        return round(prob, 2)
    


# if __name__ == '__main__':
#     siamese = SiameseOnnx("model/g3word6300/simvgg19.onnx")
#     img1 = "testimg/ques_00002_20624_1.png"
#     img2 = "testimg/ques_00003_75122_0.png"
#     result = siamese.predict(img1, img2)
#     print(result)
#     result1,  result2 = siamese.predict_list([img1, img2], [img1, img2])
#     print(result1, result2)
#     print(type(result1[0]), type(result2))