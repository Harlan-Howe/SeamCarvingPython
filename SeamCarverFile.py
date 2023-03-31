import numpy as np
import cv2
import math
from tkinter import *
from tkinter import filedialog
from typing import List,Tuple

from PIL import Image, ImageTk

class SeamCarver:

    def __init__(self):
        self.buildGUI()


    def buildGUI(self):
        """
        sets up the window and the buttons' commands
        :return:
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

    def build_button_frame(self,frm_buttons):
        """
        builds the buttons for the GUI, including binding the buttons to methods.
        :param frm_buttons: the frame where we are putting the buttons.
        :return: None
        """
        btn_load = Button(master=frm_buttons, text="Load Image", command=self.do_load_image)
        btn_load.grid (row=0, column = 0, padx=20)

        btn_find_seam = Button(master=frm_buttons, text="Find Seam", command=self.do_find_seam)
        btn_find_seam.grid (row=0, column = 1, padx=20)

        btn_remove_seam = Button(master=frm_buttons, text="Remove Seam", command=self.do_remove_seam)
        btn_remove_seam.grid (row=0, column = 2, padx=20)

        btn_copy_to_source = Button(master=frm_buttons, text="Copy To Source", command=self.do_copy_to_source)
        btn_copy_to_source.grid (row=0, column = 3, padx=20)

        btn_do_cycle = Button(master=frm_buttons, text="Do N Cycles", command=self.do_n_cycles)
        btn_do_cycle.grid (row=0, column = 4, padx=20)

        # btn_do_ten_cycles = Button(master=frm_buttons, text="Do Ten Cycles", command=self.do_ten_cycles)
        # btn_do_ten_cycles.pack(side='left')
        self.n_spinner = Spinbox(master = frm_buttons, from_=1, to=25)
        self.n_spinner.grid (row=0, column = 5, padx=20)

    def build_image_frame(self,frm_images):
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

        self.original_image_panel = self.update_panel(self.original_image_panel, cvImage=self.source_cv_image, master=frm_org)
        self.source_image_panel = self.update_panel(self.source_image_panel, cvImage=self.source_cv_image, master=frm_source)
        self.edge_image_panel = self.update_panel(self.edge_image_panel, cvImage=self.energy_image, master=frm_energy)
        self.seam_image_panel = self.update_panel(self.seam_image_panel, cvImage=self.seam_cv_image, master=frm_seam)
        self.result_image_panel = self.update_panel(self.result_image_panel, cvImage=self.result_cv_image, master=frm_result)

        frm_org.grid(row=0, column=0, rowspan=2)
        frm_source.grid(row=0, column=1)
        frm_energy.grid(row=0, column=2)
        frm_seam.grid(row=1, column=1)
        frm_result.grid(row=1, column=2)

    def update_panel(self,panel:Label, cvImage:np.ndarray, master = None)->Label:
        """
        refreshes the image that we have put into a panel.
        :param panel: which panel to update or create
        :param cvImage: the cv2 image to show in the panel
        :param master: if we are creating this panel, what frame or window is holding it?
        :return: the panel in question.
        """
        img = self.convert_cv_to_Tk(cvImage)
        if panel is None:
            print("Making new panel.")
            if master is None:
                panel = Label(master=self.root, image = img)
            else:
                panel = Label(master=master, image = img)
            panel.image = img
            panel.pack(side = "bottom")
        else:
            panel.configure(image = img)
            panel.image = img

        return panel

    def convert_cv_to_Tk(self,img:np.ndarray)->ImageTk.PhotoImage:
        """
        Open CV images are incompatible with being shown in TK windows. This does the conversion
        :param img: and image in OpenCV
        :return: the equivalent image in Tkinter
        """
        color_reversed = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        PIL_version = Image.fromarray(color_reversed)
        return ImageTk.PhotoImage(PIL_version)



    def do_load_image(self):
        """
        The user has just pressed the load image button - display a file dialog and open an image file, updating the
        "source" and "edge" panels.
        :return:  None
        """
        path = filedialog.askopenfilename(message="Find the source image.")
        if len(path)>0:
            self.source_cv_image = cv2.imread(path)
            self.update_source_and_energy()
            self.update_panel(self.original_image_panel, self.source_cv_image)


    def do_find_seam(self):
        """
        The user has just pressed the "Find Seam" button. Calculate the seam location and update the "Seam" panel.
        :return: None
        """
        self.seam_list, self.seam_cv_image = self.find_seam()
        self.update_panel(self.seam_image_panel, self.seam_cv_image)

    def do_remove_seam(self):
        """
        The user has just pressed the "remove seam" button. Create the image for the "result" panel - one pixel narrower
        than the source image, as it has had the seam pixels removed.
        :return: None
        """
        if len(self.seam_list) != self.source_cv_image.shape[0]:
            print("Error - seam list is different height than image.")
            print(f"{len(self.seam_list)=}\t{self.source_cv_image.shape[0]=}")
            return
        self.result_cv_image =self.source_cv_image.copy()
        for r in range(self.source_cv_image.shape[0]):
            self.result_cv_image[r,self.seam_list[r]:-1] = self.result_cv_image[r,self.seam_list[r]+1:]
        self.result_cv_image = self.result_cv_image[:,:-1]
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
        self.energy_image = cv2.Sobel(self.source_cv_image.astype(float), ddepth=cv2.CV_16S, dx=1, dy=0, ksize=3,
                                      borderType=cv2.BORDER_REFLECT)
        self.energy_image = (np.abs(self.energy_image)).astype(np.uint8)
        self.energy_image = cv2.cvtColor(self.energy_image, cv2.COLOR_BGR2GRAY)
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


    def find_seam(self)->Tuple[List[int],np.ndarray]:
        """
        Use Dynamic Programming to find the seam from the top of the image to the bottom that has the least total energy.
        :return: an array of integers, listing the x-coordinate of the seam at each row (from top to bottom); also a
        cv2 image describing the seam, to display.
        """
        cumulative = np.zeros(self.energy_image.shape, dtype=float)

        #---------------------
        #TODO: Build up the cumulative grid, showing the least total energy to reach each pixel from the top edge of the
        # self.edge_cv_image.
        #   make sure you have a starting point, and a recursive statement.



        #---------------------
        # Finds the x-position of the minimum value in the bottom row of "cumulative." (This is faster than looping
        # through it, yourself.
        minstart_x = np.argmin(cumulative[-1,:])

        seam_image = self.source_cv_image.copy()
        seam_values = []

        # TODO: work back up the cumulative image to find the path. Each step of the way, set the corresponding pixel in
        #   self.seam_cv_image to be red ([0,0,255])  - backwards from what you are used to; open CV is BGR, not RGB.
        #  - also, add the x value to the seam_values list, so that the first item on the list is the x coordinate of the seam
        #    on the top row, the next value on the list is the x coordinate of the next row and so forth.


        #------------------------

        return seam_values, seam_image





if __name__ == "__main__":
    sc = SeamCarver()


