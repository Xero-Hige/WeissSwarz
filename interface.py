import tkMessageBox

__author__ = 'hige'

from Tkinter import Tk
import tkSimpleDialog


class WindowInterface(object):
    def __init__(self):
        self.tk_window = Tk()

    def get_integer(self, message, title="", number_range=[]):
        """ """
        if not number_range:
            return tkSimpleDialog.askinteger(title, message, parent=self.tk_window)
        return tkSimpleDialog.askinteger(title, message, parent=self.tk_window, minvalue=number_range[0],
                                         maxvalue=number_range[1])

    def show_info(self, message, title=""):
        tkMessageBox.askquestion(title, message, type=tkMessageBox.OK, icon="info")

    def ask_yesno(self, message, title=""):
        result = tkMessageBox.askquestion(title, message, type=tkMessageBox.YESNO)
        return result == "yes"
