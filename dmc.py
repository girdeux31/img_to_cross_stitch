#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import math

class DMC:

    csv_file = 'dmc_colors.csv'
    
    def __init__(self):
        """Init object"""
        self.dmc_dict = self._read_info_from_csv(self.csv_file)

    def _read_info_from_csv(self, csv_file: str) -> dict[str, dict[str, tuple | str]]:
        """Read CSV file with DMC info"""
        dmc_dict = {}
        with open(csv_file, mode='r') as f:

            reader = csv.reader(f)
            for row in reader:
                if len(row) != 5:
                    raise ValueError(f'Bad format while reading \'{self.csv_file}\' file')
                
                code = row[0]
                rgb = (int(row[1]), int(row[2]), int(row[3]))
                name = row[4]
                dmc_dict[code] = {'rgb': rgb, 'name': name}

        return dmc_dict

    def _euclidean_distance(self, c1: tuple[int], c2: tuple[int], corrected: bool) -> float:
        """Compute euclidean distance between two RGB colors w or wo 'correction'"""
        r1, g1, b1 = c1
        r2, g2, b2 = c2
        mr, mg, mb = (2, 4, 3) if corrected else (1, 1, 1)

        return math.sqrt(mr*((r1-r2)**2) + mg*((g1-g2)**2) + mb*((b1-b2)**2))

    def get_most_similar_code_by_rgb(self, rgb: tuple[int], corrected: bool=True) -> str:
        """Get DMC color code from an RGB tuple. To get the code, the closest rgb is chosen from the list,
        correction to the distance can be applied with corrected bool argument"""
        temp_dist = 99999999
        for code, info in self.dmc_dict.items():
            dist = self._euclidean_distance(info['rgb'], rgb, corrected)
            if dist < temp_dist:
                temp_dist = dist
                new_code = code

        return new_code
    
    def get_color_name_by_code(self, code: str) -> str:
        """Get the exact color name by code"""
        if code not in self.dmc_dict:
            raise KeyError(f'Code {code} not found in \'{self.csv_file}\' file')
        return self.dmc_dict[code]['name']
    
    def get_most_similar_rgb_by_rgb(self, rgb: tuple[int], corrected: bool=True) -> tuple[int]:
        """"""
        code = self.get_most_similar_code_by_rgb(rgb, corrected=corrected)
        return self.dmc_dict[code]['rgb']
