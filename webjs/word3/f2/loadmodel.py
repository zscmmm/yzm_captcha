from src.method.GTClick import GTClick
from src.method.GTnine import GTnine




gt3word = GTClick(
    path_yolo_detect = "model/g3word6300/detect.pt",
    path_per = "model/g3word6300/simvgg19.onnx",
    path_yolo_class = "model/g3word6300/muti.pt",
    detectclass = ["char", "target"],
    chars_issorted = False,
    rmalpha = True,
)

gt3nine = GTnine(path_yolo_class="model/nine3/best.pt")

gt4icon = GTClick(
    path_yolo_detect = "model/icon4mi800/detect.pt",
    path_per = "model/icon4mi800/simvgg19.onnx",
    path_yolo_class = "model/icon4mi800/muti.pt", 
    detectclass = ["target"],
    chars_issorted = True,
    rmalpha = True,
)