from Tkinter import Tk, Label
import pygame
from time import sleep
import tkMessageBox
import tkSimpleDialog

import card_maker

RESOLUTION = (1600, 1000)

ANCHO_PUNTO = 20

ALTO_CARTA_TABLERO = 10 *ANCHO_PUNTO
ANCHO_CARTA_TABLERO = 7 *ANCHO_PUNTO

LADO_AREA_CARTA = 12 * ANCHO_PUNTO

ALTO_BACKGROUND = LADO_AREA_CARTA * 5
ANCHO_BACKGROUND = LADO_AREA_CARTA * 8

POSICION_ANCHO_LABEL_PODER = ANCHO_CARTA_TABLERO / 4
POSICION_ALTO_LABEL_PODER = ALTO_CARTA_TABLERO / 2


__author__ = 'hige'


class WindowInterface(object):
    def __init__(self):
        pygame.init()
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

    def dibujar_front_stage(self, background, posicion_izquierda_front, rotacion, front_stage):
        position = [posicion_izquierda_front, LADO_AREA_CARTA+LADO_AREA_CARTA/12]

        for card in front_stage:
            myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 30)

            if card:
                card_surface = card_maker.generate_card_image(card)
                card_surface = pygame.transform.scale(card_surface, (ANCHO_CARTA_TABLERO, ALTO_CARTA_TABLERO))

                power_label = myfont.render(str(card.get_power()), 1, (0, 0, 0))
                card_surface.blit(power_label, (POSICION_ANCHO_LABEL_PODER, POSICION_ALTO_LABEL_PODER))

                card_surface = pygame.transform.rotate(card_surface, rotacion)
                background.blit(card_surface, position)

            position[1] += LADO_AREA_CARTA + LADO_AREA_CARTA/6

    def ganerate_board(self, gameboard):
        background = pygame.image.load("resources/background.png")
        background = pygame.transform.scale(background,(ANCHO_BACKGROUND,ALTO_BACKGROUND))

        front_stage = gameboard.get_front_stage_cards()

        weiss_front_stage = front_stage[:3]
        schwarz_front_stage = front_stage[3:]
        schwarz_front_stage = schwarz_front_stage[::-1]

        posicion_izquierda_front = 3*LADO_AREA_CARTA #3 areas anteriores (clock climax y back
        self.dibujar_front_stage(background, posicion_izquierda_front, -90, weiss_front_stage)
        self.dibujar_front_stage(background, posicion_izquierda_front+LADO_AREA_CARTA, 90, schwarz_front_stage)


        return pygame.transform.scale(background, RESOLUTION)

    def update_board(self, gameboard):
        board_surface = self.ganerate_board(gameboard)

        screen = pygame.display.set_mode(board_surface.get_size())
        screen.blit(board_surface, (0, 0))
        pygame.display.set_caption("Board")
        pygame.display.flip()