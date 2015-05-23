from time import sleep

__author__ = 'hige'

from cards import CharacterCard
import pygame

pygame.init()
w=448
h=626
screen = pygame.display.set_mode((w,h))


def main():
    card = CharacterCard("Elegant Lily", "yellow", 0, None, 2, 1, 2000, 1, ("Warrior", "Mage"))

    image_file = card.name.replace(' ', '_') + ".png"
    layout_file = card.get_color()[0] + str(card.soul_points) + "s.png"
    if card.get_level() != 0:
        level_file = card.get_color()[0] +"l" + str(card.get_level())+ ".png"
    else:
        level_file = "l0.png"

    cost_file = "c" + str(card.get_cost()) + ".png"

    image = pygame.image.load("resources/card_images/"+image_file)

    i_w,i_h = image.get_size()

    if i_w > i_h:
        i_w = h*i_w/i_h
        i_h = h
        if (i_w < w):
            i_h = w*i_h/i_w
            i_w = w


    else:
        i_h = w*i_h/i_w
        i_w = w
        if(i_h < h):
            i_w = h*i_w/i_h
            i_h = h



    image = pygame.transform.scale(image,(i_w,i_h))

    horizontal_adjust = (w-i_w)/2
    vertical_adjust = (h-i_h)/2

    screen.blit(image,(horizontal_adjust,vertical_adjust))

    image = pygame.image.load("resources/card_layouts/character/"+layout_file)
    screen.blit(image,(0,0))

    image = pygame.image.load("resources/card_layouts/level/"+level_file)
    screen.blit(image,(0,0))

    image = pygame.image.load("resources/card_layouts/cost/"+cost_file)
    screen.blit(image,(0,60))

    pygame.display.flip()


    sleep(10)



main()