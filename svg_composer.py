from pathlib import Path

from svg import SVG


class SVGComposer:

    font_size = '20px'
    font_color = 'black'
    symbol_color = 'black'
    symbol_width = 1
    svg_fill = 'none'
    svg_text_class_name = 'text'
    svg_symbol_class_name = 'glyph'

    def __init__(self, color: bool=True, symbols: bool=True) -> None:
        """Init object"""
        self.color = color
        self.symbols = symbols
        self.svg = SVG()

    def add_header(self, width: int, height: int) -> None:
        """Add svg header"""
        style = {
            'fill': self.svg_fill,
        }
        classes = {
            self.svg_text_class_name: {
                'font-size': self.font_size,
                'fill': self.font_color,
            },
            self.svg_symbol_class_name: {
                'stroke': self.symbol_color,
                'stroke-width': self.symbol_width,
            }
        }
        self.svg.add_xml_header(width, height, style)
        self.svg.add_xml_style(classes)

    def save(self, svg_file: Path, png_file: Path=None, export_png: bool=False) -> None:
        if export_png and png_file is None:
            raise ValueError('Include \'png_file\' argument if \'export_png\' is True')
        self.svg.save(svg_file)
        if export_png:
            self.svg.svg_to_png(svg_file, png_file)