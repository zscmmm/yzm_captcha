from typing import Tuple, Optional, Union
from PIL import Image, ImageDraw, ImageFont
import os

class MakeCharImage:

    def __init__(
        self,
        text: str, 
        image_size: Tuple[int, int] = (120, 120),
        offset: Union[int, float] = 0,
        font_path: str = None,
        output_path: Union[str, None] = None
    ) -> None:
        assert len(text) == 1, "text must be a single character"
        self.text = text
        self.image_size = image_size
        self.offset = offset
        if not font_path:
            font_path = os.path.join(os.path.dirname(__file__), "simsun.ttc")
        self.font_path = font_path
        self.output_path = output_path
        self.generated_image = self.generate_charimage()
        if self.output_path:
            self.generated_image.save(self.output_path)

    @classmethod
    def load_font(cls, font_path: str, font_size: int) -> Optional[ImageFont.FreeTypeFont]:
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception as e:
            # print(f"Error loading font: {e}")
            return None

    def generate_charimage(self) -> Image.Image:
        """
        generate_image generates an image with the given text and size.
        """
        assert len(self.text) == 1, "text must be a single character"
        assert len(self.image_size) == 2, "image_size must be a tuple of 2 integers (width, height)"

        font = self.load_font(self.font_path, min(self.image_size))
        image_width, image_height = self.image_size
        background_color = (255, 255, 255)  # 白色背景
        text_color = (0, 0, 0)  # 黑色文本
        image = Image.new("RGB", (image_width, image_height), background_color)
        draw = ImageDraw.Draw(image)

        # 绘制原始文本
        _, _, width, height = draw.textbbox((0, 0), text=self.text, font=font)
        x = (image_width - width) // 2
        y = (image_height - height) // 2
        draw.text((x, y), self.text, font=font, fill=text_color)

        # 绘制加粗文本（偏移一像素）
        if self.offset > 0:
            draw.text((x - self.offset, y - self.offset), self.text, font=font, fill=text_color)
            draw.text((x + self.offset, y - self.offset), self.text, font=font, fill=text_color)
            draw.text((x - self.offset, y + self.offset), self.text, font=font, fill=text_color)
            draw.text((x + self.offset, y + self.offset), self.text, font=font, fill=text_color)

        return image



if __name__ == "__main__":
    text = "利"
    image_size = (120, 120)
    aa = MakeCharImage(text, image_size, 0.9, output_path="output.png")
