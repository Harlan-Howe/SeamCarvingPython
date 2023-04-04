import numpy as np
import cv2
from typing import List, Tuple

class Carver:

    def __init__(self):
        pass
    def calculate_energy(self, source_image) -> np.ndarray:
        energy_image = cv2.Sobel(source_image.astype(float),
                                      ddepth=cv2.CV_16S,
                                      dx=1,
                                      dy=0,
                                      ksize=3,
                                      borderType=cv2.BORDER_REFLECT)
        energy_image = (np.abs(energy_image)).astype(np.uint8)
        energy_image = cv2.cvtColor(energy_image, cv2.COLOR_BGR2GRAY)
        return energy_image

    def generate_cumulative_energy_grid(self, energy_image) -> np.ndarray:
        """
        Based on the information in self.energy_image, constructs the cumulative grid
        :return: the cumulative grid that goes with this energy grid.
        """
        # start the cumulative grid off as a grid of zeros, the same size as the energy grid, with a copy of the top row
        #    of energy in its top row. So if "energy" is
        #    1 2 3 4
        #    5 6 7 8
        #    9 1 2 3
        #    4 5 6 7
        # then "cumulative" _starts_off_ as
        #    1 2 3 4
        #    0 0 0 0
        #    0 0 0 0
        #    0 0 0 0

        cumulative_energy_image = np.zeros(energy_image.shape, dtype=float)
        cumulative_energy_image[0, :] = energy_image[0, :]

        # TODO: Fill in cumulative grid, showing the least total energy to reach each pixel from the top edge (row 0)
        #  of the self.edge_cv_image. Each pixel is based on cumulative information from the row above it (row-1) and
        #  the value of the energy for this pixel.




        return cumulative_energy_image

    def find_seam_locations(self,
                            energy_image: np.ndarray,
                            cumulative_energy_image: np.ndarray) -> List[int]:
        """
        Given a filled-in cumulative grid, finds the vertical seam corresponding to the least energy used.
        :param energy_image: the energy image for the source image.
        :param cumulative_energy_image: a filled-in cumulative grid
        :return: a list of the column numbers for seam location of each row. So seam_values = [ 12, 13, 13, 14, 15, 14]
        would correspond to a seam consisting of (r, c) points (0, 12), (1, 13), (2, 13), (3, 14), (4, 15), (5, 14).
        """

        # Finds the index of the lowest item in the bottom row of the graphic.
        # I THINK YOU'LL FIND THIS HANDY.
        minstart_x: int = int(np.argmin(cumulative_energy_image[-1, :]))

        # TODO: work back up the cumulative image to find the path. Add the x value to the seam_values list, so that the
        #  first item on the list is the x coordinate of the seam on the top row, the next value on the list is the
        #  x coordinate of the next row and so forth. The minstart_x that was calculated above will be the last number
        #  on the list.
        seam_values = []


        return seam_values

    def build_seam_image_with_path(self, source_image: np.ndarray,
                                seam_values: List[int]) -> np.ndarray:
        """
        given a list of the column numbers for a path from the top row to the bottom row, creates an image with a bw
        copy of the source and a red line representing the seam.
        :param source_image: the color image we will draw this seam onto.
        :param seam_values: a list of integers, corresponding to the horizontal (col) location for each point on a line
        extending from the top of the image to the bottom. (The length of this list should be the same as the height
        of the image.)
        :return: new seam image.
        """
        if len(seam_values) != source_image.shape[0]:
            raise RuntimeError(f"Error - seam list is different height than image. " \
                                 f"{len(seam_values)=}\t{source_image.shape[0]=}")
        seam_image = source_image.copy()
        for r in range(seam_image.shape[0]):
            seam_image[r, seam_values[r]] = (0, 0, 255)
        return seam_image

    def remove_seam_from_image(self, seam_values: List[int],
                                     source_image: np.ndarray) -> np.ndarray:
        if len(seam_values) != source_image.shape[0]:
            raise RuntimeError(f"Error - seam list is different height than image. " \
                                 f"{len(seam_values)=}\t{source_image.shape[0]=}")

        result_image = source_image.copy()
        for r in range(source_image.shape[0]):
            result_image[r, seam_values[r]:-1] = result_image[r, seam_values[r] + 1:]
        result_image = result_image[:, :-1]
        return result_image
