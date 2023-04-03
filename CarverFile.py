import numpy as np
import cv2
import typing

class Carver:

    def __init__(self):
        print ("Building Carver.")
        self.source_image = None
        self.energy_image = None

    def set_source_image(self, source_image: np.ndarray) -> None:
        self.source_image = source_image
    def calculate_energy(self) -> np.ndarray:
        self.energy_image = cv2.Sobel(self.source_image.astype(float),
                                      ddepth=cv2.CV_16S,
                                      dx=1,
                                      dy=0,
                                      ksize=3,
                                      borderType=cv2.BORDER_REFLECT)
        self.energy_image = (np.abs(energy_image)).astype(np.uint8)
        self.energy_image = cv2.cvtColor(energy_image, cv2.COLOR_BGR2GRAY)
        return self.energy_image

    def calculate_cumulative_energy(self) -> np.ndarray:
        cumulative = self.generate_cumulative_grid()

        seam_values = self.find_seam_locations(cumulative)

        self.build_seam_image_with_path(seam_values)

        self.update_panel(self.seam_image_panel, self.seam_cv_image)
