from src.utils.nine import crop_nine
from src.method.GTnine import GTnine
from src.utils.outdata import Outfile
from pathlib import Path

if __name__ == "__main__":
    gt = GTnine(path_yolo_class="model/nine3/best.pt")
    charimg = ["assets/nine3/ques_00001_54480.png"]
    background = "assets/nine3/img_00000_37458.png"

    outdir = "example/temp3"
    Path(outdir).mkdir(exist_ok=True)
    test_img = crop_nine(background)
    for index, i in enumerate(test_img):
        i.save(f"{outdir}/{index}.png")

    out = gt.run(background, charimg)
    # 高 * 宽
    Outfile.to_labelme(background, out, size = (261, 300),  output_dir = outdir )
    Outfile.draw_image(background, 
                       chars_xyxy= out.get_value("charsImage"),
                       targets_xyxy = out.get_value("targets_xyxy"), 
                       out_path=f"{outdir}/output.png"
                       )
    ## 结果在temp3/output.png 中