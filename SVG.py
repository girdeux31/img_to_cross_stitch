#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SVG:
    
    xml = ''
    
    def __init__(self, black_white = False, minor_lines = False, symbols = True):
        self.black_white = black_white
        self.minor_lines = minor_lines
        self.symbols = symbols
        
    def get_rgb_from_dmc_item(self, item):
        return 'rgb('+str(item[0])+','+str(item[1])+','+str(item[2])+');'

    def gen_glyph(self, idx, x, y, size = 1):
        x = str(x)
        y = str(y)
        scale = 'scale(' + str(size) + ')'
        if idx == 0:
            return "<path class='glyph' d='M4 4L16 16' transform='translate("+x+" "+y+") "+scale+"'/>" # backslash
        elif idx == 1:
            return "<path class='glyph' d='M4 16L16 4M4 10L 16 10' transform='translate("+x+" "+y+") "+scale+"'/>" # forward slash
        elif idx == 2:
            return "<path class='glyph' d='M7 7L7 13 13 13 13 7Z' fill='black' transform='translate("+x+" "+y+") "+scale+"'/>" # little square, filled black
        elif idx == 3:
            return "<path class='glyph' d='M4 4L10 16L16 4 Z' transform='translate("+x+" "+y+") "+scale+"'/>" # triangle, upside down
        elif idx == 4:
            return "<path class='glyph' d='M4 4L16 16M4 16 L16 4' transform='translate("+x+" "+y+") "+scale+"'/>" # diagonal cross
        elif idx == 5:
            return "<path class='glyph' d='M4 4L4 16 16 16 16 4Z' transform='translate("+x+" "+y+") "+scale+"'/>" # square
        elif idx == 6:
            return "<path class='glyph' d='M4 4L10 16L16 4 Z' fill='black' transform='translate("+x+" "+y+") "+scale+"'/>" # triangle, upside down, filled black
        elif idx == 7:
            return "<path class='glyph' d='M10 4L6 10 10 16 14 10Z' fill='black' transform='translate("+x+" "+y+") "+scale+"'/>" # diamond, filled black
        elif idx == 8:
            return "<path class='glyph' d='M8 8L8 12 12 12 12 8Z' transform='translate("+x+" "+y+") "+scale+"'/>" # little square
        elif idx == 9:
            return "<path class='glyph' d='M4 4L16 16M4 16 L16 4M10 4L10 16M4 10L16 10' transform='translate("+x+" "+y+") "+scale+"'/>" # 8 way cross
        elif idx == 10:
            return "<path class='glyph' d='M4 4L4 16 16 16 16 4Z' fill='black' transform='translate("+x+" "+y+") "+scale+"'/>" # square, filled black
        else:
            return ''

    def add_rect(self, palette, idx, x, y, size):
        glyph_scale = size / 20.0
        fill = 'fill:rgb(255,255,255);' if self.black_white else 'fill:'+self.get_rgb_from_dmc_item(palette[idx]['rgb'])
        stroke = 'stroke:rgb(20,20,20);stroke-width:1;' if self.minor_lines else 'stroke:none;'
        sym = self.gen_glyph(idx, x, y, glyph_scale) if self.symbols else ''
        self.xml += '<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(size)+'" height="'+str(size)+'" style="'+fill+stroke+'"/>' + sym
        
    def init_svg(self, width, height):
        self.xml += '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(width)+'" height="'+str(height)+'" style ="fill:none;">'
        self.xml += '<style>.svg_txt{font-size:20px;}.glyph{stroke:#000000;stroke-width:1;stroke:1;}</style>'
    
    def add_arrows(self, size, width, height):
        h = str(size/2)
        f = str(size)
        self.xml += "<path d=\"M0 "+h+"L"+f+" "+h+"M"+h+" 0L"+f+" "+h+" "+h+" "+f+"\" stroke=\"black\" stroke-width=\"2\" fill=\"none\" transform='translate(0 " + str(height/2) + ")'/>"
        self.xml += "<path d=\"M"+h+" 0L"+h+" "+f+" M"+f+" "+h+"L"+h+" "+f+" 0 "+h+"\" stroke=\"black\" stroke-width=\"2\" fill=\"none\" transform='translate(" + str(width/2) + " 0)'/>"
    
    def add_major_gridlines(self, size, width, height):
        for x in range(size + size * 10, width, size * 10):
            self.xml += "<line x1=\"" + str(x) + "\" y1=\"" + str(size) + "\" x2=\"" + str(x) + "\" y2=\"" + str(height) + "\" style=\"stroke:black;stroke-width:2\" />"
        for y in range(size + size * 10, height, size * 10):
            self.xml += "<line x1=\"" + str(size) + "\" y1=\"" + str(y) + "\" x2=\"" + str(width) + "\" y2=\"" + str(y) + "\" style=\"stroke:black;stroke-width:2\" />"
            
    def add_key_color(self, y, size, idx, color):
        x = 0
        color_rgb = color['rgb']
        color_name = color['name']
        color_code = color['code']
        # key
        glyph_scale = size / 20.0
        fill = 'fill:rgb(255,255,255);' if self.black_white else 'fill:rgb('+str(color_rgb[0])+', '+str(color_rgb[1])+', '+str(color_rgb[2])+');'
        stroke = 'stroke:rgb(20,20,20);stroke-width:1;' if self.minor_lines else 'stroke:none;'
        sym = self.gen_glyph(idx, x, y, glyph_scale) if self.symbols else ''
        self.xml += '<rect x="0" y="'+str(y)+'" width="'+str(size)+'" height="'+str(size)+'" style="'+fill+stroke+'"/>' + sym
        # color name
        self.xml += '<rect x="'+str(size)+'" y="'+str(y)+'" width="'+str(size* 10)+'" height="'+str(size)+'" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += '<text x = "' + str(x + size * 1.5) + '" y = "' + str(y + size / 2.0) + '" fill="black">' + color_name + '</text>'
        # color code
        self.xml += '<rect x="'+str(size*11)+'" y="'+str(y)+'" width="'+str(size* 2)+'" height="'+str(size)+'" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += '<text x = "' + str(size* 11 + (size/2.0)) + '" y = "' + str(y + size / 2.0) + '" fill="black">' + color_code + '</text>'
        
    def save(self, filename):
        self.xml += '</svg>'
        f = open(filename,'w')
        f.write(self.xml)
        f.close()
        