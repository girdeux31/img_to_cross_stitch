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
    # colors = int(sys.argv[2])    # number of colors to use in the pattern
    # stitches_per_row = int(sys.argv[3])   # stitch count, number of stitches in x axis

    # Just for debugging
    input_file = Path('examples/bird.jpg')
    colors = 3
    stitches_per_row = 50
    scale = 2.0

    # TODO: check if stitches_per_row is more then pixels in row or column
    if not input_file.exists():
        raise FileNotFoundError(f'File \'{input_file}\' not found')
    if not 2 <= colors <= 256:
        raise ValueError('Parameter \'colors\' must be in range [2, 256]')

    # Generate file paths

    out_pattern_file = input_file.with_stem(f'{input_file.stem}_pattern').with_suffix('')
    out_legend_file = input_file.with_stem(f'{input_file.stem}_legend').with_suffix('')

    # Generate pattern svg

    pattern = Pattern(color=True, symbols=True)
    pattern.process_image(input_file, colors, stitches_per_row)
    pattern.generate()
    pattern.save(out_pattern_file, formats=['svg', 'png', 'pdf'], png_scale=scale)

    # # Generate legend svg

    legend = Legend(color=True, symbols=True)
    legend.generate(pattern)
    legend.save(out_legend_file)
