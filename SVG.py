from pathlib import Path


class SVG:
    
    idx_to_code = {
        0: "M4 4L16 16", # backslash
        1: "M4 16L16 4M4 10L 16 10", # forward slash
        2: "M7 7L7 13 13 13 13 7Z' fill='black", # little square, filled black
        3: "M4 4L10 16L16 4 Z", # triangle, upside down
        4: "M4 4L16 16M4 16 L16 4", # diagonal cross
        5: "M4 4L4 16 16 16 16 4Z", # square
        6: "M4 4L10 16L16 4 Z' fill='black", # triangle, upside down, filled black
        7: "M10 4L6 10 10 16 14 10Z' fill='black", # diamond, filled black
        8: "M8 8L8 12 12 12 12 8Z", # little square
        9: "M4 4L16 16M4 16 L16 4M10 4L10 16M4 10L16 10", # 8 way cross
        10: "M4 4L4 16 16 16 16 4Z' fill='black", # square, filled black
    }
    font_size = '20px'
    font_color = 'black'
    symbol_color = 'black'
    symbol_width = 1
    arrow_color = 'black'
    arrow_width = 2
    arrow_fill = 'none'
    major_grid_color = 'black'
    major_grid_width = 2
    minor_grid_color = 'rgb(20,20,20)'
    minor_grid_width = 1
    legend_fill_color = 'white'
    legend_stroke_color = 'black'
    legend_stroke_width = 1
    svg_fill = 'none'
    
    def __init__(self, color: bool=True, symbols: bool=True):
        """Init object"""
        self.color = color
        self.symbols = symbols
        self.xml = ''

    def _write_xml_line(self, xml: str, indent: int=0) -> None:
        """Add xml code as string"""
        self.xml += indent*'\t' + xml + '\n'

    def _add_xml_rect(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        style_dict: dict[str, str]
    ) -> None:
        """Add xml rect tag"""
        xml_code = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" style="'
        for style_arg, style_value in style_dict.items():
            xml_code += f'{style_arg}:{style_value};'
        xml_code += '"/>'
        self._write_xml_line(xml_code, indent=1)

    def _add_xml_header(
        self,
        width: int | float,
        height: int | float,
        style_dict: dict[str, dict[str, str]],
    ) -> None:
        """Add xml svg tag"""
        xml_code = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="'
        for style_arg, style_value in style_dict.items():
            xml_code += f'{style_arg}:{style_value};'
        xml_code += '">'
        self._write_xml_line(xml_code)

    def _add_xml_style(self, class_dict: dict[str, dict[str, str]]) -> None:
        """Add xml style tag"""
        xml_code = '<style>'
        for class_name, class_style in class_dict.items():
            xml_code += f'.{class_name}{{'
            for style_arg, style_value in class_style.items():
                xml_code += f'{style_arg}:{style_value};'
            xml_code += '}'
        xml_code += '</style>'
        self._write_xml_line(xml_code, indent=1)

    def _add_xml_path(self, code: str, style_dict: dict[str, str], transform: str) -> None:
        """Add xml path tag"""
        xml_code = f'<path d="{code}"'
        for style_arg, style_value in style_dict.items():
            xml_code += f' {style_arg}="{style_value}"'
        xml_code += f" transform='{transform}'/>"
        self._write_xml_line(xml_code, indent=1)

    def _add_xml_symbol(self, idx: int, x: int | float, y: int | float, size: int) -> str:
        """Add xml symbol according to idx value, position (x, y) and size"""
        scale = size / 20.0
        xml_code = "<path class='glyph' d='"
        xml_code += self.idx_to_code[idx] if idx in self.idx_to_code else ''
        xml_code += f"' transform='translate({x} {y}) scale({scale})'/>"
        self._write_xml_line(xml_code, indent=1)

    def _add_xml_text(self, x: int | float, y: int | float, style_dict: dict[str, str], text: str) -> None:
        """Add xml text tag"""
        xml_code = f'<text x="{x}" y="{y}"'
        for style_arg, style_value in style_dict.items():
            xml_code += f' {style_arg}="{style_value}"'
        xml_code += f'>{text}</text>'
        self._write_xml_line(xml_code, indent=1)

    def _add_xml_line(self, x1: int | float, y1: int | float, x2: int | float, y2: int | float, style_dict: dict[str, str]) -> None:
        """Add xml line tag"""
        xml_code = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="'
        for style_arg, style_value in style_dict.items():
            xml_code += f'{style_arg}:{style_value};'
        xml_code += '"/>'
        self._write_xml_line(xml_code, indent=1)

    def add_color(self, palette: list[dict[str, tuple | str]], idx: int, x: int, y: int, size: int) -> None:
        """Add colors as "pixels" """
        r, g, b = palette[idx]['rgb'] if self.color else (255, 255, 255)
        style = {
            'fill': f'rgb({r},{g},{b})',
            'stroke': 'none',
        }
        self._add_xml_rect(x, y, size, size, style)

    def add_symbol(self, idx: int, x: int, y: int, size: int) -> None:
        """Add symbols"""
        if self.symbols:
            self._add_xml_symbol(idx, x, y, size)
        
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
        self._add_xml_header(width, height, style)
        self._add_xml_style(classes)
    
    def add_arrows(self, size: int, width: int, height: int) -> None:
        """Add midpoint arrows"""
        h = str(size/2)
        f = str(size)
        style = {
            'stroke': self.arrow_color,
            'stroke-width': self.arrow_width,
            'fill': self.arrow_fill,
        }
        # vertical arrow looking down
        code = f'M0 {h}L{f} {h}M{h} 0L{f} {h} {h} {f}'
        transform = f'translate(0 {height/2})'
        self._add_xml_path(code, style, transform)
        # horizontal arrow looking right
        code = f'M{h} 0L{h} {f} M{f} {h}L{h} {f} 0 {h}'
        transform = f'translate({width/2} 0)'
        self._add_xml_path(code, style, transform)
    
    def add_gridlines(self, size: int, width: int, height: int) -> None:
        """Add major and minor gridlines"""
        self._add_minor_gridlines(size, width, height)
        self._add_major_gridlines(size, width, height)

    def _add_major_gridlines(self, size: int, width: int, height: int) -> None:
        """Add major gridlines"""
        style = {
            'stroke': self.major_grid_color,
            'stroke-width': self.major_grid_width,
        }
        for x in range(11*size, width, 10*size):
            self._add_xml_line(x, size, x, height, style)
        for y in range(11*size, height, 10*size):
            self._add_xml_line(size, y, width, y, style)

    def _add_minor_gridlines(self, size: int, width: int, height: int) -> None:
        """Add minor gridlines"""
        style = {
            'stroke': self.minor_grid_color,
            'stroke-width': self.minor_grid_width,
        }
        for x in range(2*size, width, size):
            self._add_xml_line(x, size, x, height, style)
        for y in range(2*size, height, size):
            self._add_xml_line(size, y, width, y, style)

    def add_legend(self, y: int, size: int, idx: int, color: dict[str, tuple | str]):
        """Add legend"""
        x = 0
        # symbol
        r, g, b = color['rgb'] if self.color else (255, 255, 255)
        style = {
            'fill': f'rgb({r},{g},{b})',
            'stroke': self.minor_grid_color,
            'stroke-width': self.minor_grid_width,
        }
        self._add_xml_rect(x, y, size, size, style)
        if self.symbols:
            self._add_xml_symbol(idx, x, y, size)
        # color name
        rect_style = {
            'fill': self.legend_fill_color,
            'stroke': self.legend_stroke_color,
            'stroke-width': self.legend_stroke_width,
        }
        text_style = {
            'fill': self.font_color,
        }
        self._add_xml_rect(size, y, 10*size, size, rect_style)
        self._add_xml_text(x + 1.5*size, y + size/2.0, text_style, color['name'])
        # color code
        self._add_xml_rect(11*size, y, 2*size, size, rect_style)
        self._add_xml_text(11.5*size, y + size/2.0, text_style, color['code'])
        
    def save(self, filename: Path) -> None:
        """Save as svg file"""
        self._write_xml_line('</svg>')
        f = open(filename,'w')
        f.write(self.xml)
        f.close()
        