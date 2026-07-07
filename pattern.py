from pathlib import Path

from image import Image
from pattern_composer import PatternComposer

SVG_UNIT_SIZE = 10


class Pattern:

    def __init__(self, color: bool=True, symbols: bool=True) -> None:
        """Init object"""
        self.color = color
        self.symbols = symbols
        self.palette = None
        self.rgb_2d_list = None
        self.width = 0
        self.height = 0
        self.pattern_composer = PatternComposer(color, symbols)

    def process_image(self, img_file: Path, n_colors: int, n_pixels_per_row: int) -> None:

        image = Image(img_file)
        image.process(n_colors, n_pixels_per_row)
        self.palette = image.get_palette()
        self.idx_2d_list = image.get_values_as_2d_list()
        self.width = len(self.idx_2d_list[0])
        self.height = len(self.idx_2d_list)

    def get_palette(self) -> list[dict[str, tuple | str]]:
        """Return image palette with color indexes"""
        if self.palette is None:
            raise ValueError('To obtain a palette first call process_image method')
        return self.palette
    
    def generate(self):
        """Generate SVG info"""
        width = self.width * SVG_UNIT_SIZE
        height = self.height * SVG_UNIT_SIZE
        self.pattern_composer.add_header(width, height)
        self.pattern_composer.add_arrows(SVG_UNIT_SIZE, width, height)
        x = y = SVG_UNIT_SIZE # to allow drawing of midpoint arrows
        for row in self.idx_2d_list:
            for c_idx in row:
                self.pattern_composer.add_color(self.palette, c_idx, x, y, SVG_UNIT_SIZE)
                self.pattern_composer.add_symbol(c_idx, x, y, SVG_UNIT_SIZE)
                x += SVG_UNIT_SIZE
            y += SVG_UNIT_SIZE
            x = SVG_UNIT_SIZE
        self.pattern_composer.add_gridlines(SVG_UNIT_SIZE, width, height)

    def save(self, svg_file: Path, export_to: list[str]=[], scale: float=1.0) -> None:
        self.pattern_composer.save(svg_file, export_to, scale)