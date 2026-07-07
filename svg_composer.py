from pathlib import Path

from svg import SVG


class SVGComposer:

    # TODO: move to constatns
    font_size = '20px'
    symbol_color = 'black'
    symbol_width = 1
    svg_fill = 'none'

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
            'svg_txt': {        # TODO: svg_txt not used
                'font-size': self.font_size,
            },
            'glyph': {
                'stroke': self.symbol_color,
                'stroke-width': self.symbol_width,
            }
        }
        self.svg.add_xml_header(width, height, style)
        self.svg.add_xml_style(classes)

    def save(self, svg_file: Path) -> None:
        self.svg.save(svg_file)