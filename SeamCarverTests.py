import unittest

import SeamCarverFile


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.energy = [[73, 51, 79, 46, 23, 32, 77, 39],
 [22, 66, 80, 48, 54, 72, 46, 40],
 [38, 42, 26, 29, 51, 78, 60, 80],
 [61, 64, 61, 20, 60, 23, 41, 79],
 [55, 52, 66, 51, 66, 76, 44, 67],
 [50, 32, 57, 34, 44, 69, 74, 22],
 [31, 72, 64, 44, 22, 47, 31, 52],
 [26, 60, 62, 79, 73, 28, 72, 26]]


    def test_something(self):
        expected_cumulative = [[73, 51, 79, 46, 23, 32, 71, 39],
        [73, 117, 126, 71, 77, 95, 78, 79],
        [111, 115, 97, 100, 122, 156, 138, 158],
        [172, 161, 158, 117, 160, 145, 179, 212],
        [216, 210, 183, 168, 183, 221, 189, 246],
        [260, 215, 225, 202, 210, 252, 263, 211],
        [246, 287, 266, 246, 224, 257, 242, 263],
        [272, 306, 308, 303, 297, 252, 314, 289]]

        sc0 = SeamCarverFile.SeamCarver()
        sc0.energy_image = self.energy
        self.assertListEqual(expected_cumulative, sc0.generate_cumulative_grid())

if __name__ == '__main__':
    unittest.main()
