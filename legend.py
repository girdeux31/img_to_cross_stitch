from pathlib import Path

from legend_composer import LegendComposer

SVG_UNIT_SIZE = 40
COLUMN_WIDTHS = [SVG_UNIT_SIZE, 10*SVG_UNIT_SIZE, 3*SVG_UNIT_SIZE]



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
        x_pos = [0] + [sum(COLUMN_WIDTHS[:i+1]) for i in range(len(COLUMN_WIDTHS[:-1]))]
        widths = COLUMN_WIDTHS
        height = SVG_UNIT_SIZE
        self.width = sum(COLUMN_WIDTHS)
        self.height = n_colors*SVG_UNIT_SIZE
        self.legend_composer.add_header(self.width, self.height)
        for idx, color_info in enumerate(palette):
            y_pos = idx*SVG_UNIT_SIZE
            self.legend_composer.add_symbol(x_pos[0], y_pos, widths[0], height, idx, color_info)
            self.legend_composer.add_color_name(x_pos[1], y_pos, widths[1], height, color_info)
            self.legend_composer.add_color_code(x_pos[2], y_pos, widths[2], height, color_info)
            # TODO add column with number of stitches
        self.legend_composer.add_tail()

    def save(self, out_file: Path, formats: list[str]=['pdf'], png_scale: float=1.0) -> None:
        self.legend_composer.save(out_file, formats, png_scale)