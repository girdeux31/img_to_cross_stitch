from pathlib import Path

from PIL import Image as PILImage

from dmc import DMC

RESIZE_WIDTH  = 1000
MASK_SIZE = 1


class Image:

    def __init__(self, img_file: Path) -> None:
        """"""
        self.img_file = img_file
        self.pil_image = self._import_image(img_file)  # pil_image is always width,height / cols,rows / x,y

    @property
    def width(self) -> int:
        return self.pil_image.size[0]
    
    @property
    def height(self) -> int:
        return self.pil_image.size[1]

    @staticmethod
    def _import_image(img_file: Path) -> PILImage:
        """Read image as (cols,rows,rgb)"""
        if not img_file.exists():
            raise FileNotFoundError(f'File \'{img_file}\' not found')
        return PILImage.open(img_file).convert('RGB')  # make sure to read it in RGB mode

    def _resize(self) -> None:
        """Resize image as (res_cols,res_rows,rgb)"""
        resize_height = int(RESIZE_WIDTH * self.height / self.width)
        self.pil_image = self.pil_image.resize((RESIZE_WIDTH, resize_height), PILImage.NEAREST)
    
    def _pixelate(self, n_pixels_per_row: int) -> None:
        """Resize image as (pix_cols,pix_rows,rgb)"""
        dmc = DMC()
        pixel_size = int(RESIZE_WIDTH / int(n_pixels_per_row))
        rgb_2d_list = self.get_values_as_2d_list(step=pixel_size)
        n_rows, n_cols = (len(rgb_2d_list[0]), len(rgb_2d_list))  # rows, columns
        rgb_2d_list = [
            [
                dmc.get_most_similar_rgb_by_rgb(rgb_2d_list[y][x]) 
                for x in range(0, n_rows)
            ]
            for y in range(0, n_cols)
        ]
        
        self.pil_image = PILImage.new('RGB', (n_rows, n_cols))
        self.pil_image.putdata([rgb for row in rgb_2d_list for rgb in row])

    def _quantize(self, n_colors: int) -> None:
        """Resize image as (pix_cols,pix_rows,color_idx)"""
        self.pil_image = self.pil_image.convert('P', palette=PILImage.ADAPTIVE, colors=n_colors)

    def _clean(self) -> None:
        # TODO move to pattern?
        """Remove isolated pixels and replace by majority neighborhood color
        Resulting image is still (pix_cols,pix_rows,color_idx)"""
        # TODO: remove pixel if only one neighbor is present in a diagonal?
        idx_2d_list = self.get_values_as_2d_list()

        for x in range(0, self.width):
            for y in range(0, self.height):
                neighbors = self._get_neighbors_in_coords([y, x], idx_2d_list)
                if idx_2d_list[y][x] not in neighbors:
                    rgb = max(neighbors, key=neighbors.count)
                    idx_2d_list[y][x] = rgb

    @staticmethod
    def _get_neighbors_in_coords(coords, image_2d_list) -> list[tuple[int]]:
        neighbors = []
        rows = len(image_2d_list)
        cols = len(image_2d_list[0]) if rows else 0
        mask_half_width = int(MASK_SIZE/2)
        for i in range(max(0, coords[0] - mask_half_width), min(rows, coords[0] + mask_half_width + 1)):
            for j in range(max(0, coords[1] - mask_half_width), min(cols, coords[1] + mask_half_width + 1)):
                if i != coords[0] and j != coords[1]:
                    neighbors.append(image_2d_list[i][j])

        return neighbors

    def process(self, n_colors: int, n_pixels_per_row: int):
        self._resize()
        self._pixelate(n_pixels_per_row)
        self._quantize(n_colors)

    def get_palette(self) -> list[dict[str, tuple | str]]:

        if self.pil_image.mode != 'P':
            raise ValueError('To obtain a palette first quantize the image with _quantize method')
        
        dmc = DMC()
        palette_list = []
        palette = self.pil_image.getpalette()
        for idx in range(0, len(palette), 3):
            rgb = tuple(palette[idx:idx+3])
            code = dmc.get_most_similar_code_by_rgb(rgb, corrected=True)
            name = dmc.get_color_name_by_code(code)
            palette_list.append(
                {
                    'rgb': rgb,
                    'code': code,
                    'name': name,
                }
            )

        return palette_list

    def get_values_as_2d_list(self, step: int=1) -> list[list[tuple | int]]:
        """Get image values as a 2d list, either rgb or color index values"""
        return [
            [
                self.pil_image.getpixel((x, y)) 
                for x in range(0, self.width, step)
            ] for y in range(0, self.height, step)
        ]