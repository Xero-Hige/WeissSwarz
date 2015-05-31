from Tkinter import Tk, Label
import pygame
import random
from time import sleep
import tkMessageBox
import tkSimpleDialog
import board

import card_maker

CRUZ = "cruz"

CARA = "cara"

RESOLUTION = (1600, 1000)

ANCHO_PUNTO = 20

ALTO_CARTA_TABLERO = 10 * ANCHO_PUNTO
ANCHO_CARTA_TABLERO = 7 * ANCHO_PUNTO

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
        self.image_label = Label()

        self.cards_surface = {}

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

        c = self.__get_card_surface(card)
        from PIL import Image, ImageTk

        image = Image.fromstring('RGBA', c.get_rect()[2:], pygame.image.tostring(c, "RGBA"))
        photo = ImageTk.PhotoImage(image)

        self.image_label = Label(image=photo)
        self.image_label.image = photo  # keep a reference!
        self.image_label.pack()
        self.tk_window.title(title)

        self.tk_window.update()
        sleep(2)

    def __get_card_surface(self, card):
        card_str = str(card)
        if not self.cards_surface.has_key(card_str):
            self.cards_surface[card_str] = card_maker.generate_card_image(card)

        return self.cards_surface[card_str]


    def __dibujar_cartas_personaje(self, background, stage, position, rotacion):
        for card in stage:
            myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 30)

            if card:
                card_surface = self.__get_card_surface(card)
                card_surface = pygame.transform.scale(card_surface, (ANCHO_CARTA_TABLERO, ALTO_CARTA_TABLERO))

                power_label = myfont.render(str(card.get_power()), 1, (0, 0, 0))
                card_surface.blit(power_label, (POSICION_ANCHO_LABEL_PODER, POSICION_ALTO_LABEL_PODER))

                card_surface = pygame.transform.rotate(card_surface, rotacion)
                background.blit(card_surface, position)

            position[1] += LADO_AREA_CARTA

    def __dibujar_front_stage(self, background, posicion_izquierda_front, rotacion, front_stage):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 12, LADO_AREA_CARTA + (5 * LADO_AREA_CARTA) / 24]

        self.__dibujar_cartas_personaje(background, front_stage, position, rotacion)

    def __dibujar_back_stage(self, background, posicion_izquierda_front, rotacion, front_stage):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 12,
                    (3 * LADO_AREA_CARTA) / 2 + (5 * LADO_AREA_CARTA) / 24]

        self.__dibujar_cartas_personaje(background, front_stage, position, rotacion)

    def __dibujar_climax_card(self, background, posicion_izquierda_front, rotacion, climax_card):
        position = [posicion_izquierda_front + (5 * LADO_AREA_CARTA) / 24, 2 * LADO_AREA_CARTA + LADO_AREA_CARTA / 12]

        if not climax_card:
            return

        self.__dibujar_carta_individual(background, climax_card, position, rotacion)

    def __dibujar_discard_weiss(self, background, posicion_izquierda_front, rotacion, discard_top):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 12, 4 * LADO_AREA_CARTA + (5 * LADO_AREA_CARTA) / 24]

        if not discard_top:
            return

        self.__dibujar_carta_individual(background, discard_top, position, rotacion)

    def __dibujar_carta_individual(self, background, discard_top, position, rotacion):
        card_surface = self.__get_card_surface(discard_top)
        card_surface = pygame.transform.scale(card_surface, (ANCHO_CARTA_TABLERO, ALTO_CARTA_TABLERO))
        card_surface = pygame.transform.rotate(card_surface, rotacion)
        background.blit(card_surface, position)

    def __dibujar_discard_schwarz(self, background, posicion_izquierda_front, rotacion, discard_top):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 12, (5 * LADO_AREA_CARTA) / 24]

        if not discard_top:
            return

        self.__dibujar_carta_individual(background, discard_top, position, rotacion)

    def __dibujar_clock_weiss(self, background, posicion_izquierda_front, rotacion, clock):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 12, LADO_AREA_CARTA + (3 * LADO_AREA_CARTA) / 24]

        for card in clock:
            if card:
                self.__dibujar_carta_individual(background, card, position, rotacion)

            position[1] += (3 * ANCHO_CARTA_TABLERO) / 4

    def __dibujar_clock_schwarz(self, background, posicion_izquierda_front, rotacion, clock):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 12,
                    4 * LADO_AREA_CARTA - (3 * LADO_AREA_CARTA) / 24 - ANCHO_CARTA_TABLERO]

        for card in clock:
            if card:
                self.__dibujar_carta_individual(background, card, position, rotacion)

            position[1] -= (3 * ANCHO_CARTA_TABLERO) / 4

    def __dibujar_level_weiss(self, background, posicion_izquierda_front, rotacion, level):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 12, LADO_AREA_CARTA / 12]

        for card in level:
            if card:
                self.__dibujar_carta_individual(background, card, position, rotacion)

            position[0] += ANCHO_CARTA_TABLERO / 3

    def __dibujar_level_schwarz(self, background, posicion_izquierda_front, rotacion, level):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 3, 4 * LADO_AREA_CARTA + LADO_AREA_CARTA / 12]

        for card in level:
            if card:
                self.__dibujar_carta_individual(background, card, position, rotacion)

            position[0] -= ANCHO_CARTA_TABLERO / 3

    def __dibujar_stock_weiss(self, background, posicion_izquierda_front, rotacion, stock):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 4, LADO_AREA_CARTA / 12]

        for card in stock:
            if card:
                self.__dibujar_carta_individual(background, card, position, rotacion)

            position[0] -= ANCHO_CARTA_TABLERO / 3

    def __dibujar_stock_schwarz(self, background, posicion_izquierda_front, rotacion, stock):
        position = [posicion_izquierda_front + LADO_AREA_CARTA / 5, 4 * LADO_AREA_CARTA + LADO_AREA_CARTA / 12]

        for card in stock:
            if card:
                self.__dibujar_carta_individual(background, card, position, rotacion)

            position[0] += ANCHO_CARTA_TABLERO / 3

    def __ganerate_board(self, gameboard):
        background = pygame.image.load("resources/background.png")
        background = pygame.transform.scale(background, (ANCHO_BACKGROUND, ALTO_BACKGROUND))

        front_stage = gameboard.get_all_front_stage_cards()

        posicion_izquierda_front = 0
        self.__dibujar_clock_weiss(background, posicion_izquierda_front, -90,
                                   gameboard.get_clock_cards(board.WEISS_SIDE))
        self.__dibujar_level_weiss(background, posicion_izquierda_front, 0, gameboard.get_level_cards(board.WEISS_SIDE))

        posicion_izquierda_front += LADO_AREA_CARTA
        self.__dibujar_climax_card(background, posicion_izquierda_front, 0, gameboard.get_climax_card(board.WEISS_SIDE))
        self.__dibujar_discard_weiss(background, posicion_izquierda_front, -90,
                                     gameboard.get_top_discard_pile(board.WEISS_SIDE))

        posicion_izquierda_front += LADO_AREA_CARTA
        self.__dibujar_back_stage(background, posicion_izquierda_front, -90,
                                  gameboard.get_back_stage_cards(board.WEISS_SIDE))

        posicion_izquierda_front += LADO_AREA_CARTA
        self.__dibujar_stock_weiss(background, posicion_izquierda_front, 0, gameboard.get_stock_cards(board.WEISS_SIDE))
        self.__dibujar_front_stage(background, posicion_izquierda_front, -90,
                                   gameboard.get_front_stage_cards(board.WEISS_SIDE))

        posicion_izquierda_front += LADO_AREA_CARTA
        self.__dibujar_front_stage(background, posicion_izquierda_front, 90,
                                   gameboard.get_front_stage_cards(board.SCHWARZ_SIDE)[::-1])
        self.__dibujar_stock_schwarz(background, posicion_izquierda_front, 180,
                                     gameboard.get_stock_cards(board.SCHWARZ_SIDE))

        posicion_izquierda_front += LADO_AREA_CARTA
        self.__dibujar_back_stage(background, posicion_izquierda_front, 90,
                                  gameboard.get_back_stage_cards(board.SCHWARZ_SIDE)[::-1])

        posicion_izquierda_front += LADO_AREA_CARTA
        self.__dibujar_discard_schwarz(background, posicion_izquierda_front, 90,
                                       gameboard.get_top_discard_pile(board.SCHWARZ_SIDE))
        self.__dibujar_climax_card(background, posicion_izquierda_front, 180,
                                   gameboard.get_climax_card(board.SCHWARZ_SIDE))

        posicion_izquierda_front += LADO_AREA_CARTA
        self.__dibujar_clock_schwarz(background, posicion_izquierda_front, 90,
                                     gameboard.get_clock_cards(board.SCHWARZ_SIDE))
        self.__dibujar_level_schwarz(background, posicion_izquierda_front, 180,
                                     gameboard.get_level_cards(board.SCHWARZ_SIDE))

        return pygame.transform.scale(background, RESOLUTION)

    def update_board(self, gameboard):
        board_surface = self.__ganerate_board(gameboard)

        screen = pygame.display.set_mode(board_surface.get_size())
        screen.blit(board_surface, (0, 0))
        pygame.display.set_caption("Board")
        pygame.display.flip()

    def lanzar_dado(self):
        resultado = random.randrange(1, 6)
        self.show_info("Salio: " + str(resultado), "Dado lanzado")
        return resultado

    def lanzar_moneda(self):
        resultado = random.choice(CARA, CRUZ)
        self.show_info("Salio: " + resultado, "Moneda lanzada")
        return resultado