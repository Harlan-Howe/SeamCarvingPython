import numpy as np
import cv2
import math # you may want this... I don't know.
from tkinter import *
from tkinter import filedialog
from typing import List, Tuple

from PIL import Image, ImageTk #Must install "Pillow"
from numpy import ndarray

from CarverFile import Carver


def convert_cv_to_Tk(img: np.ndarray) -> ImageTk.PhotoImage:
    """
    Open CV images are incompatible with being shown in TK windows. This does the conversion
    :param img: and image in OpenCV
    :return: the equivalent image in Tkinter
    """
    color_reversed = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    PIL_version = Image.fromarray(color_reversed)
    return ImageTk.PhotoImage(PIL_version)


class SeamCarver:

    def __init__(self):

        self.n_spinner = None
        self.result_cv_image = None
        self.seam_cv_image = None
        self.energy_image = None
        self.source_cv_image = None
        self.result_image_panel = None
        self.seam_image_panel = None
        self.edge_image_panel = None
        self.source_image_panel = None
        self.original_image_panel = None
        self.seam_list = None
        self.root = None
        self.carver = Carver()
        self.build_GUI()



    def build_GUI(self) -> None:
        """
        sets up the window and the buttons' commands
        :return:None
        """
        self.root = Tk()
        self.seam_list = []
        self.original_image_panel = None
        self.source_image_panel = None
        self.edge_image_panel = None
        self.seam_image_panel = None
        self.result_image_panel = None

        frm_buttons = Frame(self.root)
        frm_images = Frame(self.root)

        self.build_button_frame(frm_buttons)
        self.build_image_frame(frm_images)

        frm_buttons.pack(side="top")
        frm_images.pack(side="bottom")

        self.root.mainloop()

    def build_button_frame(self, frm_buttons):
        """
        builds the buttons for the GUI, including binding the buttons to methods.
        :param frm_buttons: the frame where we are putting the buttons.
        :return: None
        """
        btn_load = Button(master=frm_buttons, text="Load Image", command=self.do_load_image)
        btn_load.grid(row=0, column=0, padx=20)

        btn_find_seam = Button(master=frm_buttons, text="Find Seam", command=self.do_find_seam)
        btn_find_seam.grid(row=0, column=1, padx=20)

        btn_remove_seam = Button(master=frm_buttons, text="Remove Seam", command=self.do_remove_seam)
        btn_remove_seam.grid(row=0, column=2, padx=20)

        btn_copy_to_source = Button(master=frm_buttons, text="Copy To Source", command=self.do_copy_to_source)
        btn_copy_to_source.grid(row=0, column=3, padx=20)

        btn_do_cycle = Button(master=frm_buttons, text="Do N Cycles", command=self.do_n_cycles)
        btn_do_cycle.grid(row=0, column=4, padx=20)

        # btn_do_ten_cycles = Button(master=frm_buttons, text="Do Ten Cycles", command=self.do_ten_cycles)
        # btn_do_ten_cycles.pack(side='left')
        self.n_spinner = Spinbox(master=frm_buttons, from_=1, to=25)
        self.n_spinner.grid(row=0, column=5, padx=20)

    def build_image_frame(self, frm_images):
        """
        generates the image panels at the bottom of the window, starting them off with small black boxes.
        :param frm_images: the frame where these panels will go.
        :return: None
        """
        self.source_cv_image = np.ones([50, 50, 3], dtype='uint8')
        self.energy_image = np.ones([50, 50, 3], dtype='uint8')
        self.seam_cv_image = np.zeros([50, 50, 3], dtype="uint8")
        self.result_cv_image = np.zeros([50, 50, 3], dtype="uint8")

        frm_org = Frame(master=frm_images, relief=RAISED, borderwidth=1)
        lbl_org = Label(master=frm_org, text="Original")
        lbl_org.pack(side="top")

        frm_source = Frame(master=frm_images, relief=RAISED, borderwidth=1)
        lbl_source = Label(master=frm_source, text="Source")
        lbl_source.pack(side="top")

        frm_energy = Frame(master=frm_images, relief=RAISED, borderwidth=1)
        lbl_energy = Label(master=frm_energy, text="Energy")
        lbl_energy.pack(side="top")

        frm_seam = Frame(master=frm_images, relief=RAISED, borderwidth=1)
        lbl_seam = Label(master=frm_seam, text="Seam")
        lbl_seam.pack(side="top")

        frm_result = Frame(master=frm_images, relief=RAISED, borderwidth=1)
        lbl_result = Label(master=frm_result, text="Result")
        lbl_result.pack(side="top")

        self.original_image_panel = self.update_panel(self.original_image_panel, cv_image=self.source_cv_image,
                                                      master=frm_org)
        self.source_image_panel = self.update_panel(self.source_image_panel, cv_image=self.source_cv_image,
                                                    master=frm_source)
        self.edge_image_panel = self.update_panel(self.edge_image_panel, cv_image=self.energy_image,
                                                  master=frm_energy)
        self.seam_image_panel = self.update_panel(self.seam_image_panel, cv_image=self.seam_cv_image,
                                                  master=frm_seam)
        self.result_image_panel = self.update_panel(self.result_image_panel, cv_image=self.result_cv_image,
                                                    master=frm_result)

        frm_org.grid(row=0, column=0, rowspan=2)
        frm_source.grid(row=0, column=1)
        frm_energy.grid(row=0, column=2)
        frm_seam.grid(row=1, column=1)
        frm_result.grid(row=1, column=2)

    def update_panel(self, panel: Label, cv_image: np.ndarray, master=None) -> Label:
        """
        refreshes the image that we have put into a panel.
        :param panel: which panel to update or create
        :param cv_image: the cv2 image to show in the panel
        :param master: if we are creating this panel, what frame or window is holding it?
        :return: the panel in question.
        """
        img = convert_cv_to_Tk(cv_image)
        if panel is None:
            print("Making new panel.")
            if master is None:
                panel = Label(master=self.root, image=img)
            else:
                panel = Label(master=master, image=img)
            panel.image = img
            panel.pack(side="bottom")
        else:
            panel.configure(image=img)
            panel.image = img

        return panel

    def do_load_image(self):
        """
        The user has just pressed the load image button - display a file dialog and open an image file, updating the
        "source" and "edge" panels.
        :return:  None
        """
        path = filedialog.askopenfilename(title="Find the source image.")
        if len(path) > 0:
            self.source_cv_image = cv2.imread(path)
            self.update_source_and_energy()
            self.update_panel(self.original_image_panel, self.source_cv_image)

    def do_find_seam(self) -> None:
        """
        The user has just pressed the "Find Seam" button. Calculate the seam location and update the "Seam" panel.
        :return: None
        """
        cumulative = self.carver.generate_cumulative_energy_grid(self.energy_image)

        self.seam_values = self.carver.find_seam_locations(self.energy_image,
                                               cumulative)

        self.seam_cv_image = self.carver.build_seam_image_with_path(self.source_cv_image,
                                                               self.seam_values)

        self.update_panel(self.seam_image_panel, self.seam_cv_image)

    def do_remove_seam(self):
        """
        The user has just pressed the "remove seam" button. Create the image for the "result" panel - one pixel narrower
        than the source image, as it has had the seam pixels removed.
        :return: None
        """
        self.result_cv_image = self.carver.remove_seam_from_image(self.seam_values, self.source_cv_image)
        self.update_panel(self.result_image_panel, self.result_cv_image)

    def do_copy_to_source(self):
        """
        The user has just pressed the "copy to source" button. Copies the "result" image into the "Source" image,
        updating the source and edge images and panels.
        :return: None
        """
        self.source_cv_image = self.result_cv_image.copy()
        self.update_source_and_energy()

    def update_source_and_energy(self):
        self.energy_image = self.carver.calculate_energy(self.source_cv_image)
        self.update_panel(self.source_image_panel, self.source_cv_image)
        self.update_panel(self.edge_image_panel, self.energy_image)

    def do_cycle(self):
        """
        The user has just pressed the "do cycle" button - equivalent to pressing "find seam," "remove seam" and "copy"
        buttons, in sequence.
        :return: None
        """
        self.do_find_seam()
        self.do_remove_seam()
        self.do_copy_to_source()

    def do_n_cycles(self):
        """
        the user has just pressed the "do ten cycles" button, equivalent to pressing "do cycle" ten times.
        :return:
        """
        n = int(self.n_spinner.get())
        print(f"Cycling {n} times.")
        for i in range(n):
            print(i)
            self.do_cycle()

if __name__ == "__main__":
    sc = SeamCarver()
