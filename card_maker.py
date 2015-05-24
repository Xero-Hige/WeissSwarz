from time import sleep

__author__ = 'hige'

from cards import CharacterCard
import pygame

pygame.init()
CHARACTER_WIDTH = 448
CHARACTER_HEIGHT = 626

CLIMAX_WIDTH = 626
CLIMAX_HEIGHT = 448


def generate_character_image(card):

    result = pygame.Surface((CHARACTER_WIDTH,CHARACTER_HEIGHT))
    result.fill((255,255,255))

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
        i_w = CHARACTER_HEIGHT * i_w / i_h
        i_h = CHARACTER_HEIGHT
        if (i_w < CHARACTER_WIDTH):
            i_h = CHARACTER_WIDTH * i_h / i_w
            i_w = CHARACTER_WIDTH

    else:
        i_h = CHARACTER_WIDTH * i_h / i_w
        i_w = CHARACTER_WIDTH
        if (i_h < CHARACTER_HEIGHT):
            i_w = CHARACTER_HEIGHT * i_w / i_h
            i_h = CHARACTER_HEIGHT

    image = pygame.transform.scale(image, (i_w, i_h))
    horizontal_adjust = (CHARACTER_WIDTH - i_w) / 2
    vertical_adjust = (CHARACTER_HEIGHT - i_h) / 2

    result.blit(image, (horizontal_adjust, vertical_adjust))

    image = pygame.image.load("resources/card_layouts/character/" + layout_file)
    result.blit(image, (0, 0))

    image = pygame.image.load("resources/card_layouts/level/" + level_file)
    result.blit(image, (0, 0))

    image = pygame.image.load("resources/card_layouts/cost/" + cost_file)
    result.blit(image, (0, 60))

    trigger_icon = card.get_trigger_icon()
    if trigger_icon == 0:
        image = pygame.image.load("resources/card_layouts/triggers/none.png")
        result.blit(image, (CHARACTER_WIDTH-image.get_size()[0],0))
    else:
        image = pygame.image.load("resources/card_layouts/triggers/soul.png")
        result.blit(image, (CHARACTER_WIDTH-image.get_size()[0],0))

        if trigger_icon == 2:
            result.blit(image, (CHARACTER_WIDTH-image.get_size()[0]*2,0))

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 27)

    label = myfont.render(str(card.get_name()), 1, (255, 255, 255))
    center_horizontal = 115 + ((435 - 155) - label.get_size()[0]) / 2
    result.blit(label, (center_horizontal, 554))  # Min 155 - Max 350 || #Min 555 - Max 575

    label = myfont.render(str(card.get_power()), 1, (255, 255, 255))
    center_horizontal = 32 + ((116 - 32) - label.get_size()[0]) / 2
    result.blit(label, (center_horizontal, 567))  # Min 32 - Max 116

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 11)
    trait_x = 212
    for trait in card.get_traits():
        label = myfont.render(trait, 1, (0, 0, 0))
        center_horizontal = trait_x + (90 - label.get_size()[0]) / 2
        result.blit(label, (center_horizontal, 587))
        trait_x += 100

    return result

def generate_climax_image(card):

    result = pygame.Surface((CLIMAX_WIDTH,CLIMAX_HEIGHT))
    result.fill((255,255,255))

    image_file = card.get_name().replace(' ', '_') + ".png"

    layout_file = card.get_color()+".png"

    if card.get_level() != 0:
        level_file = card.get_color()[0] + "l" + str(card.get_level()) + ".png"
    else:
        level_file = "l0.png"

    cost_file = "c" + str(card.get_cost()) + ".png"
    image = pygame.image.load("resources/card_images/" + image_file)
    i_w, i_h = image.get_size()
    if i_w > i_h:
        i_w = CLIMAX_HEIGHT * i_w / i_h
        i_h = CLIMAX_HEIGHT
        if (i_w < CLIMAX_WIDTH):
            i_h = CLIMAX_WIDTH * i_h / i_w
            i_w = CLIMAX_WIDTH

    else:
        i_h = CLIMAX_WIDTH * i_h / i_w
        i_w = CLIMAX_WIDTH
        if (i_h < CLIMAX_HEIGHT):
            i_w = CLIMAX_HEIGHT * i_w / i_h
            i_h = CLIMAX_HEIGHT

    image = pygame.transform.scale(image, (i_w, i_h))
    horizontal_adjust = (CLIMAX_WIDTH - i_w) / 2
    vertical_adjust = (CLIMAX_HEIGHT - i_h) / 2

    result.blit(image, (horizontal_adjust, vertical_adjust))

    image = pygame.image.load("resources/card_layouts/climax/" + layout_file)
    result.blit(image, (0, 0))

    trigger_icon = card.get_trigger_icon()
    if trigger_icon == 0:
        image = pygame.image.load("resources/card_layouts/triggers/none.png")
        image = pygame.transform.rotate(image,90)
        result.blit(image, (0,0))
    else:
        image = pygame.image.load("resources/card_layouts/triggers/soul.png")
        image = pygame.transform.rotate(image,90)
        result.blit(image, (0,0))

        if trigger_icon == 2:
            result.blit(image, (0,image.get_size()[1]))

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 22)

    label = myfont.render(str(card.get_name()), 1, (255, 255, 255))
    center_horizontal = 115 + ((435 - 155) - label.get_size()[0]) / 2
    result.blit(label, (380, 394))  # Min 155 - Max 350 || #Min 555 - Max 575

    label = myfont.render(str(card.get_power()), 1, (255, 255, 255))
    center_horizontal = 32 + ((116 - 32) - label.get_size()[0]) / 2
    result.blit(label, (center_horizontal, 567))  # Min 32 - Max 116

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 11)
    trait_x = 212
    for trait in card.get_traits():
        label = myfont.render(trait, 1, (0, 0, 0))
        center_horizontal = trait_x + (90 - label.get_size()[0]) / 2
        result.blit(label, (center_horizontal, 587))
        trait_x += 100

    return result

def main():
    cards = []
    #cards.append(CharacterCard("Illya", "blue", 0, None, 1, 1, 5500, 1, ("Mage", "Loli")))
    #cards.append(CharacterCard("Archer", "red", 1, None, 2, 0, 8000, 1, ("Archer", "Heroic")))
    cards.append(CharacterCard("Elegant Lily", "yellow", 2, None, 2, 2, 11000, 2, ("Warrior", "Heroic")))
    #cards.append(CharacterCard("Shiro", "green", 1, None, 0, 0, 1000, 1, ("Warrior", "Mage")))


    screen = pygame.display.set_mode((CHARACTER_WIDTH, CHARACTER_HEIGHT))

    for card in cards:
        card_image = generate_character_image(card)
        screen.blit(card_image,(0,0))
        pygame.display.flip()
        sleep(2)

    pygame.display.set_mode((CLIMAX_WIDTH, CLIMAX_HEIGHT))

    card_image = generate_climax_image(CharacterCard("Illya", "red", 2, None, 2, 2, 5500, 2, ("Mage", "Loli")))
    screen.blit(card_image,(0,0))
    pygame.display.flip()
    sleep(2)



main()