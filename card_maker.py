from time import sleep

__author__ = 'hige'

from cards import CharacterCard
import pygame

pygame.init()
w = 448
h = 626
screen = pygame.display.set_mode((w, h))


def render_card(card):
    image_file = card.get_name().replace(' ', '_') + ".png"

    layout_file = card.get_color()[0] + str(card.get_soul_points()) + "s.png"

    if card.get_level() != 0:
        level_file = card.get_color()[0] + "l" + str(card.get_level()) + ".png"
    else:
        level_file = "l0.png"

    cost_file = "c" + str(card.get_cost()) + ".png"
    image = pygame.image.load("resources/card_images/" + image_file)
    i_w, i_h = image.get_size()
    if i_w > i_h:
        i_w = h * i_w / i_h
        i_h = h
        if (i_w < w):
            i_h = w * i_h / i_w
            i_w = w

    else:
        i_h = w * i_h / i_w
        i_w = w
        if (i_h < h):
            i_w = h * i_w / i_h
            i_h = h

    image = pygame.transform.scale(image, (i_w, i_h))
    horizontal_adjust = (w - i_w) / 2
    vertical_adjust = (h - i_h) / 2

    screen.blit(image, (horizontal_adjust, vertical_adjust))

    image = pygame.image.load("resources/card_layouts/character/" + layout_file)
    screen.blit(image, (0, 0))

    image = pygame.image.load("resources/card_layouts/level/" + level_file)
    screen.blit(image, (0, 0))

    image = pygame.image.load("resources/card_layouts/cost/" + cost_file)
    screen.blit(image, (0, 60))

    trigger_icon = card.get_trigger_icon()
    if trigger_icon == 0:
        image = pygame.image.load("resources/card_layouts/triggers/none.png")
        screen.blit(image, (w-image.get_size()[0],0))
    else:
        image = pygame.image.load("resources/card_layouts/triggers/soul.png")
        screen.blit(image, (w-image.get_size()[0],0))

        if trigger_icon == 2:
            screen.blit(image, (w-image.get_size()[0],image.get_size()[1]))

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 27)

    label = myfont.render(str(card.name), 1, (255, 255, 255))
    center_horizontal = 115 + ((435 - 155) - label.get_size()[0]) / 2
    screen.blit(label, (center_horizontal, 554))  # Min 155 - Max 350 || #Min 555 - Max 575

    label = myfont.render(str(card.power), 1, (255, 255, 255))
    center_horizontal = 32 + ((116 - 32) - label.get_size()[0]) / 2
    screen.blit(label, (center_horizontal, 567))  # Min 32 - Max 116

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 11)
    trait_x = 212
    for trait in card.get_traits():
        label = myfont.render(trait, 1, (0, 0, 0))
        center_horizontal = trait_x + (90 - label.get_size()[0]) / 2
        screen.blit(label, (center_horizontal, 587))
        trait_x += 100

    pygame.display.flip()


def main():
    cards = []
    cards.append(CharacterCard("Shiro", "green", 1, None, 0, 0, 1000, 1, ("Warrior", "Mage")))
    cards.append(CharacterCard("Illya", "blue", 0, None, 1, 1, 5500, 1, ("Mage", "Loli")))
    cards.append(CharacterCard("Archer", "red", 1, None, 2, 0, 8000, 1, ("Archer", "Heroic")))
    cards.append(CharacterCard("Elegant Lily", "yellow", 2, None, 2, 2, 11000, 2, ("Warrior", "Heroic")))

    for card in cards:
        render_card(card)
        sleep(10)


main()