from src.method.GTClick import GTClick
from src.utils.outdata import Outfile

from pathlib import Path
from conf.config import gtconf

gtclick = GTClick(
    pdetect = gtconf['icon4mi']['pdetect'],
    per = gtconf['icon4mi']['per'],
    pclass = gtconf['icon4mi']['pclass'],
    pclasstags = gtconf['icon4mi']['pclasstags'],
    chars_issorted = True,
    rmalpha = True,
)
if __name__ == '__main__':
    i = "assets/icon4/imgs_00142_59845.png"
    extraicon = ["assets/icon4/3f9cdf.png", "assets/icon4/c59e7a.png", "assets/icon4/94cb8d.png"]
    outdir = "example/temp2"
    Path(outdir).mkdir(parents=True, exist_ok=True)
    Path(outdir).parent.mkdir(exist_ok=True)
    out = gtclick.run(i, extraicon)
    # 高 * 宽
    Outfile.to_labelme(i, out, size = (200,300),  output_dir = outdir )
    
    targetsImage = out.targetsImage
    for index, temp in enumerate(targetsImage):
        temp.save(f"{outdir}/target_{index}.png")
    Outfile.draw_image(i, out.charsImage, out.targets_xyxy , f"{outdir}/output.png")
    exit()

