from src.method.GTClick import GTClick
from src.utils.outdata import Outfile
from pathlib import Path
from conf.config import gtconf

gtclick = GTClick(
    pdetect = gtconf["word"]['pdetect'],
    per = gtconf["word"]['per'],
    pclass = gtconf["word"]['pclass'],
    pclasstags =gtconf["word"]['pclasstags'],
    chars_issorted = False,
    rmalpha = True,
)


if __name__ == '__main__':
    i = "assets/word3/pic_00356_20119.png"
    outdir = "example/temp1"
    Path(outdir).mkdir(parents=True, exist_ok=True)
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

