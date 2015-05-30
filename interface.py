from Tkinter import Tk, Label
import pygame
from time import sleep
import tkMessageBox
import tkSimpleDialog

import card_maker

__author__ = 'hige'


class WindowInterface(object):
    def __init__(self):
        self.tk_window = Tk()
        self.image_label = Label();

    def get_integer(self, message, title="", number_range=[]):
        """ """
        if not number_range:
            return tkSimpleDialog.askinteger(title, message, parent=self.tk_window)
        return tkSimpleDialog.askinteger(title, message, parent=self.tk_window, minvalue=number_range[0],
                                         maxvalue=number_range[1])

    def show_info(self, message, title=""):
        tkMessageBox.askquestion(title, message, type=tkMessageBox.OK, icon="info")

    def ask_yesno(self, message, title=""):
        """

        :param message:
        :param title:
        :return:
        """
        result = tkMessageBox.askquestion(title, message, type=tkMessageBox.YESNO)
        return result == "yes"

    def show_card(self, card, title=""):
        """


        :rtype : None
        :param card:
        :param title:
        """
        self.image_label.destroy()

        c = card_maker.generate_card_image(card)
        from PIL import Image, ImageTk

        image = Image.fromstring('RGBA', c.get_rect()[2:], pygame.image.tostring(c, "RGBA"))
        photo = ImageTk.PhotoImage(image)

        self.image_label = Label(image=photo)
        self.image_label.image = photo  # keep a reference!
        self.image_label.pack()
        self.tk_window.title(title)

        self.tk_window.update()
        sleep(2)
