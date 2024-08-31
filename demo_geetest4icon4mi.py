from src.method.GTClick import GTClick
from src.utils.outdata import Outfile

from pathlib import Path


path_yolo_detect = "model/icon4mi800/detect.pt"
path_per = "model/icon4mi800/simvgg19.onnx"
path_yolo_class = "model/icon4mi800/muti.pt"
detectclass = ["target"] #当有两个标签的时候,具有顺序的一定要放在第一个
gtclick = GTClick(
    path_yolo_detect = path_yolo_detect,
    path_per = path_per,
    path_yolo_class = path_yolo_class,
    detectclass = detectclass,
    chars_issorted = True,
    rmalpha = True,
)


if __name__ == '__main__':
    i = "assets/icon4/imgs_00142_59845.png"
    extraicon = ["assets/icon4/3f9cdf.png", "assets/icon4/c59e7a.png", "assets/icon4/94cb8d.png"]
    outdir = "example/temp2"
    Path(outdir).mkdir(exist_ok=True)
    out = gtclick.run(i, extraicon)
    # 高 * 宽
    Outfile.to_labelme(i, out, size = (200,300),  output_dir = outdir )
    
    targetsImage = out.targetsImage
    for index, temp in enumerate(targetsImage):
        temp.save(f"{outdir}/target_{index}.png")
    Outfile.draw_image(i, out.charsImage, out.targets_xyxy , f"{outdir}/output.png")
    exit()

