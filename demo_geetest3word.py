from src.method.GTClick import GTClick
from src.utils.outdata import Outfile
from pathlib import Path

path_yolo_detect = "model/g3word6300/detect.pt"
path_per = "model/g3word6300/simvgg19.onnx"
path_yolo_class = "model/g3word6300/muti.pt"
detectclass = ["char", "target"] #当有两个标签的时候,具有顺序的一定要放在第一个
gtclick = GTClick(
    path_yolo_detect = path_yolo_detect,
    path_per = path_per,
    path_yolo_class = path_yolo_class,
    detectclass = detectclass,
    chars_issorted = False,
    rmalpha = True,
)


if __name__ == '__main__':
    i = "assets/word3/pic_00356_20119.png"
    outdir = "example/temp1"
    Path(outdir).mkdir(exist_ok=True)
    out = gtclick.run(i)
    # 高 * 宽
    Outfile.to_labelme(i, out, size=(384, 344), output_dir=outdir )
    charsImage = out.charsImage
    targetsImage = out.targetsImage
    for index, temp in enumerate(charsImage):
        temp.save(f"{outdir}/char_{index}.png")
    for index, temp in enumerate(targetsImage):
        temp.save(f"{outdir}/target_{index}.png")
    
    Outfile.draw_image(i, out.chars_xyxy, out.targets_xyxy , f"{outdir}/output.png")
    exit()

