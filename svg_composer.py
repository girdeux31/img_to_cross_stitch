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

    def save(self, svg_file: Path, export_to: list[str]=[], scale: float=1.0) -> None:
        """Save / export output as svg, png or pdf, scale is only applied to pngs"""
        self.svg.save(svg_file)
        for format_ in export_to:
            if format_ == 'png':
                self.svg.svg_to_png(svg_file, svg_file.with_suffix('.png'), scale)
            elif format_ == 'pdf':
                self.svg.svg_to_pdf(svg_file, svg_file.with_suffix('.pdf'))
            else:
                raise ValueError(f'Format file \'{format_}\' not supported')