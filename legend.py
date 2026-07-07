from pathlib import Path

from legend_composer import LegendComposer

SVG_UNIT_SIZE = 40


class Legend:

    def __init__(self, color: bool=True, symbols: bool=True) -> None:
        """Init object"""
        self.color = color
        self.symbols = symbols
        self.width = 0
        self.height = 0
        self.legend_composer = LegendComposer(color, symbols)

    def generate(self, palette: list[dict[str, tuple | str]]) -> None:
        n_colors = len(palette)
        self.width = 13*SVG_UNIT_SIZE
        self.height = n_colors*SVG_UNIT_SIZE
        self.legend_composer.add_header(self.width, self.height)
        y = 0
        for idx, color_info in enumerate(palette):
            self.legend_composer.add_symbol(y, SVG_UNIT_SIZE, idx, color_info)
            self.legend_composer.add_color_name(y, SVG_UNIT_SIZE, color_info)
            self.legend_composer.add_color_code(y, SVG_UNIT_SIZE, color_info)
            y += SVG_UNIT_SIZE

    def save(self, svg_file: Path, png_file: Path=None, export_png: bool=False) -> None:
        self.legend_composer.save(svg_file, png_file, export_png)