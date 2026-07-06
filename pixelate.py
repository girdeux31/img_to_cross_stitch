import sys
import cairosvg
from PIL import Image
from DMC import DMC
from SVG import SVG
from pathlib import Path


def svg_to_png(svg_file: Path):
    """Read svg file and save it as png"""
    if not svg_file.exists():
        raise FileNotFoundError(f'File \'{svg_file}\' not found')
    
    png_file = svg_file.with_suffix('.png')
    with open(svg_file, "rb") as f:
        svg_bytes = f.read()
    png_bytes = cairosvg.svg2png(bytestring=svg_bytes)
    with open(png_file, 'wb') as f:
        f.write(png_bytes)

def get_neighbours(pos, matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    width = 1
    for i in range(max(0, pos[0] - width), min(rows, pos[0] + width + 1)):
        for j in range(max(0, pos[1] - width), min(cols, pos[1] + width + 1)):
            if not (i == pos[0] and j == pos[1]):
                yield matrix[i][j]

if __name__ == '__main__':

    # process arguments

    # if(len(sys.argv)<3):
    #     print("function requires an input filename, number of colors, stitch count and mode")
    #     sys.exit(0)

    # input_file = Path(sys.argv[1])       # input file name, has to be a jpg
    # n_colors = int(sys.argv[2])    # number of colors to use in the pattern
    # n_squares = int(sys.argv[3])   # stitch count, number of stitches in x axis

    # Just for debugging
    input_file = Path('examples/bird.jpg')
    n_colors = 3
    n_squares = 50

    if not input_file.exists():
        raise FileNotFoundError(f'File \'{input_file}\' not found')

    # init svg objects
        
    svg_rgb = SVG(color=True)
    svg_bw = SVG(color=False)
    svg_legend = SVG(color=True)

    # read and resize image

    img = Image.open(input_file).convert('RGB')  # make sure to read it in RGM mode
    new_width  = 1000
    pixel_size = int(new_width / int(n_squares))
    new_height = int(new_width * img.size[1] / img.size[0])
    img = img.resize((new_width, new_height), Image.NEAREST)

    # get 2d list with DMC colors (each element is a RGB tuple)

    dmc = DMC()
    dmc_spaced = [
        [
            dmc.get_most_similar_rgb_by_rgb(img.getpixel((x, y))) 
            for x in range(0, img.size[0], pixel_size)
        ]
        for y in range(0, img.size[1], pixel_size)
    ]

    # create a new image with previous RGB colors

    dmc_image = Image.new('RGB', (len(dmc_spaced[0]), len(dmc_spaced))) #h, w
    dmc_image.putdata([value for row in dmc_spaced for value in row])

    # quantize the image with the required number of colors

    dmc_image = dmc_image.convert('P', palette=Image.ADAPTIVE, colors=n_colors)
    x_count = dmc_image.size[0]
    y_count = dmc_image.size[1]
    svg_pattern = [[dmc_image.getpixel((x, y)) for x in range(x_count)] for y in range(y_count)]

    # get image palette (list of colors)

    palette_list = []
    palette = dmc_image.getpalette()
    for idx in range(n_colors):
        rgb = tuple(palette[idx*3:idx*3+3])
        code = dmc.get_most_similar_code_by_rgb(rgb, corrected=True)
        name = dmc.get_color_name_by_code(code)
        palette_list.append(
            {
                'rgb': rgb,
                'code': code,
                'name': name,
            }
        )

    # remove isolated pixels with a local color average

    for x in range(0, x_count):
        for y in range(0, y_count):
            gen = get_neighbours([y, x], svg_pattern)
            neighbours = []
            for n in gen:
                neighbours += [n]
            if svg_pattern[y][x] not in neighbours:
                mode = max(neighbours, key=neighbours.count)
                svg_pattern[y][x] = mode

    # create images:
    #  - B&W wo symbols
    #  - RGB w symbols
    #  - RGB wo symbols
    # then, extra features are added:
    #  - midpoint arrows
    #  - major and minor grids
    #  - symbols

    svg_cell_size = 10
    width = x_count * svg_cell_size
    height = y_count * svg_cell_size
    svg_rgb.add_header(width, height)
    svg_rgb.add_arrows(svg_cell_size, width, height)
    svg_bw.add_header(width, height)
    svg_bw.add_arrows(svg_cell_size, width, height)
    x = y = svg_cell_size # to allow drawing of midpoint arrows
    for row in svg_pattern:
        for c_idx in row:
            svg_rgb.add_color(palette_list, c_idx, x, y, svg_cell_size)
            svg_rgb.add_symbol(c_idx, x, y, svg_cell_size)
            svg_bw.add_color(palette_list, c_idx, x, y, svg_cell_size)
            svg_bw.add_symbol(c_idx, x, y, svg_cell_size)
            x += svg_cell_size
        y += svg_cell_size
        x = svg_cell_size
    svg_bw.add_gridlines(svg_cell_size, width, height)
    svg_rgb.add_gridlines(svg_cell_size, width, height)

    # generate the legend image

    size = 40
    svg_legend.add_header(size*13, size*n_colors)
    y = 0
    for idx in range(n_colors):
        svg_legend.add_legend(y, size, idx, palette_list[idx])
        y += size

    # save all images

    out_path = input_file.parent
    out_name = input_file.stem
    svg_rgb.save(out_path / f'{out_name}_rgb.svg')
    svg_bw.save(out_path / f'{out_name}_bw.svg')
    svg_legend.save(out_path / f'{out_name}_legend.svg')
    svg_to_png(out_path / f'{out_name}_rgb.svg')