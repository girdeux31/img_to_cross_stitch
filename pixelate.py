import sys
from pathlib import Path

from legend import Legend
from pattern import Pattern


if __name__ == '__main__':

    # Process user arguments

    # if(len(sys.argv)<3):
    #     print("function requires an input filename, number of colors, stitch count and mode")
    #     sys.exit(0)

    # input_file = Path(sys.argv[1])       # input file name, has to be a jpg
    # n_colors = int(sys.argv[2])    # number of colors to use in the pattern
    # n_stitches_per_row = int(sys.argv[3])   # stitch count, number of stitches in x axis

    # Just for debugging
    input_file = Path('examples/bird.jpg')
    n_colors = 3
    n_stitches_per_row = 50

    if not input_file.exists():
        raise FileNotFoundError(f'File \'{input_file}\' not found')

    # Generate file paths

    out_path = input_file.parent
    out_name = input_file.stem
    svg_pattern_file = out_path / f'{out_name}_pattern.svg'
    svg_legend_file = out_path / f'{out_name}_legend.svg'
    png_pattern_file = svg_pattern_file.with_suffix('.png')

    # Generate pattern svg

    pattern = Pattern(color=True, symbols=True)
    pattern.process_image(input_file, n_colors, n_stitches_per_row)
    pattern.generate()
    pattern.save(svg_pattern_file, png_pattern_file, export_png=True)

    # Generate legend svg

    legend = Legend(color=True, symbols=True)
    legend.generate(pattern.get_palette())
    legend.save(svg_legend_file)
