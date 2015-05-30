from time import sleep

__author__ = 'hige'

from cards import CharacterCard, ClimaxCard, EventCard
import pygame

pygame.init()
CHARACTER_WIDTH = 448
CHARACTER_HEIGHT = 626

CLIMAX_WIDTH = 626
CLIMAX_HEIGHT = 448


def generate_character_image(card):
    result = pygame.Surface((CHARACTER_WIDTH, CHARACTER_HEIGHT))
    result.fill((255, 255, 255))

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
        result.blit(image, (CHARACTER_WIDTH - image.get_size()[0], 0))
    else:
        image = pygame.image.load("resources/card_layouts/triggers/soul.png")
        result.blit(image, (CHARACTER_WIDTH - image.get_size()[0], 0))

        if trigger_icon == 2:
            result.blit(image, (CHARACTER_WIDTH - image.get_size()[0] * 2, 0))

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

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 16)

    labels = []
    for line in card.get_flavor_text().split('\n'):
        labels.append(myfont.render(line, 1, (0, 0, 0)))

    line_height = labels[0].get_size()[1]

    text_box = pygame.Surface((CHARACTER_WIDTH - CHARACTER_WIDTH / 8, line_height * len(labels)), pygame.SRCALPHA)
    text_box.fill((255, 255, 255, 150))
    position = 550
    result.blit(text_box, (CHARACTER_WIDTH / 16, position - text_box.get_size()[1]))

    for label in labels[::-1]:
        position -= line_height
        result.blit(label, (CHARACTER_WIDTH / 16, position))

    if (card.get_ability()):
        labels = []
        for line in card.get_ability().get_text().split('\n'):
            labels.append(myfont.render(line, 1, (0, 0, 0)))

        line_height = labels[0].get_size()[1]

        text_box = pygame.Surface((CHARACTER_WIDTH - CHARACTER_WIDTH / 8, line_height * len(labels)), pygame.SRCALPHA)
        text_box.fill((255, 255, 255, 150))
        position -= 5
        result.blit(text_box, (CHARACTER_WIDTH / 16, position - text_box.get_size()[1]))

        for label in labels[::-1]:
            position -= line_height
            result.blit(label, (CHARACTER_WIDTH / 16, position))

    return result


def generate_event_image(card):
    result = pygame.Surface((CHARACTER_WIDTH, CHARACTER_HEIGHT))
    result.fill((255, 255, 255))

    image_file = card.get_name().replace(' ', '_') + ".png"

    layout_file = card.get_color() + ".png"

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

    image = pygame.image.load("resources/card_layouts/event/" + layout_file)
    result.blit(image, (0, 0))

    image = pygame.image.load("resources/card_layouts/level/" + level_file)
    result.blit(image, (0, 0))

    image = pygame.image.load("resources/card_layouts/cost/" + cost_file)
    result.blit(image, (0, 60))

    trigger_icon = card.get_trigger_icon()
    if trigger_icon == 0:
        image = pygame.image.load("resources/card_layouts/triggers/none.png")
        result.blit(image, (CHARACTER_WIDTH - image.get_size()[0], 0))
    else:
        image = pygame.image.load("resources/card_layouts/triggers/soul.png")
        result.blit(image, (CHARACTER_WIDTH - image.get_size()[0], 0))

        if trigger_icon == 2:
            result.blit(image, (CHARACTER_WIDTH - image.get_size()[0] * 2, 0))

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 25)

    label = myfont.render(str(card.get_name()), 1, (255, 255, 255))
    center_horizontal = 115 + ((435 - 155) - label.get_size()[0]) / 2
    result.blit(label, (center_horizontal, 570))  # Min 155 - Max 350 || #Min 555 - Max 575

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 16)

    labels = []
    for line in card.get_flavor_text().split('\n'):
        labels.append(myfont.render(line, 1, (0, 0, 0)))

    line_height = labels[0].get_size()[1]

    text_box = pygame.Surface((CHARACTER_WIDTH - CHARACTER_WIDTH / 8, line_height * len(labels)), pygame.SRCALPHA)
    text_box.fill((255, 255, 255, 150))
    position = 565
    result.blit(text_box, (CHARACTER_WIDTH / 16, position - text_box.get_size()[1]))

    for label in labels[::-1]:
        position -= line_height
        result.blit(label, (CHARACTER_WIDTH / 16, position))

    if (card.get_ability()):
        labels = []
        for line in card.get_ability().get_text().split('\n'):
            labels.append(myfont.render(line, 1, (0, 0, 0)))

        line_height = labels[0].get_size()[1]

        text_box = pygame.Surface((CHARACTER_WIDTH - CHARACTER_WIDTH / 8, line_height * len(labels)), pygame.SRCALPHA)
        text_box.fill((255, 255, 255, 150))
        position -= 5
        result.blit(text_box, (CHARACTER_WIDTH / 16, position - text_box.get_size()[1]))

        for label in labels[::-1]:
            position -= line_height
            result.blit(label, (CHARACTER_WIDTH / 16, position))

    return result


def generate_climax_image(card):
    result = pygame.Surface((CLIMAX_WIDTH, CLIMAX_HEIGHT))
    result.fill((255, 255, 255))

    image_file = card.get_name().replace(' ', '_') + ".png"

    layout_file = card.get_color() + ".png"

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
        image = pygame.transform.rotate(image, 90)
        result.blit(image, (0, 0))
    else:
        image = pygame.image.load("resources/card_layouts/triggers/soul.png")
        image = pygame.transform.rotate(image, 90)
        result.blit(image, (0, 0))

        if trigger_icon == 2:
            result.blit(image, (0, image.get_size()[1]))

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 22)

    label = myfont.render(str(card.get_name()), 1, (255, 255, 255))
    center_horizontal = 380 + ((580 - 380) - label.get_size()[0]) / 2
    result.blit(label, (center_horizontal, 394))

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 16)

    labels = []
    for line in card.get_flavor_text().split('\n'):
        labels.append(myfont.render(line, 1, (0, 0, 0)))

    line_height = labels[0].get_size()[1]

    text_box = pygame.Surface((339, line_height * len(labels)), pygame.SRCALPHA)
    text_box.fill((255, 255, 255, 150))
    position = 390
    result.blit(text_box, (CLIMAX_WIDTH - 372, position - text_box.get_size()[1]))

    for label in labels[::-1]:
        position -= line_height
        result.blit(label, (CLIMAX_WIDTH - 372, position))

    myfont = pygame.font.Font("resources/agfarotissemiserif.ttf", 12)

    labels = []
    for line in card.get_ability().get_text().split('\n'):
        labels.append(myfont.render(line, 1, (0, 0, 0)))

    line_height = labels[0].get_size()[1]

    text_box = pygame.Surface((225, line_height * len(labels)), pygame.SRCALPHA)
    text_box.fill((255, 255, 255, 150))
    position = 445
    result.blit(text_box, (8, position - text_box.get_size()[1]))

    for label in labels[::-1]:
        position -= line_height
        result.blit(label, (10, position))

    return pygame.transform.rotate(result, -90)

def generate_card_image(card):
    if isinstance(card, ClimaxCard):
        return generate_climax_image(card)

    elif isinstance(card, CharacterCard):
        return generate_character_image(card)

    elif isinstance(card, EventCard):
        return generate_event_image(card)

    else:
        raise TypeError , "Eso no es una carta, no se generar una imagen"

def show_card(card,text="",showtime=2):
    if isinstance(card, ClimaxCard):
        screen = pygame.display.set_mode((CLIMAX_WIDTH, CLIMAX_HEIGHT))
        card_image = generate_climax_image(card)

    elif isinstance(card, CharacterCard):
        screen = pygame.display.set_mode((CHARACTER_WIDTH, CHARACTER_HEIGHT))
        card_image = generate_character_image(card)

    elif isinstance(card, EventCard):
        screen = pygame.display.set_mode((CHARACTER_WIDTH, CHARACTER_HEIGHT))
        card_image = generate_event_image(card)

    else:
        raise TypeError , "Eso no es una carta, no se puede mostrar"

    screen.blit(card_image, (0, 0))
    pygame.display.set_caption(text)
    pygame.display.flip()
    sleep(showtime)

def main():
    cards = []
    cards.append(CharacterCard("Illya", "blue", 0, None, "\"Good night\"", 1, 1, 5500, 1, ("Mage", "Loli")))
    cards.append(CharacterCard("Archer", "red", 1, None,
                               "\"But it's all a fake. Such hypocrisy cannot save anything.\nNo, first of all, I did not know what I wanted to save!\"",
                               2, 0, 8000, 1, ("Archer", "Heroic")))
    cards.append(CharacterCard("Elegant Lily", "yellow", 2, None,
                               "\"Even if he is not a Master, our contract will not go away.\nI have sworn to protect him and to be his sword.\"",
                               2, 2, 11000, 2, ("Warrior", "Heroic")))
    cards.append(
        CharacterCard("Bride Saber", "green", 2, None, "\"Answer me:\n   Are you my Praetor?.\"", 3, 1, 15000, 2,
                      ("Warrior", "Heroic")))
    cards.append(CharacterCard("Shiro", "green", 1, None, "\"People die when they are killed\"", 0, 0, 1000, 1,
                               ("Warrior", "Mage")))

    screen = pygame.display.set_mode((CHARACTER_WIDTH, CHARACTER_HEIGHT))

    for card in cards:
        card_image = generate_character_image(card)
        screen.blit(card_image, (0, 0))
        pygame.display.flip()
        sleep(2)

    card = EventCard("Wounded charge", "blue", 0, None, "Believe it till the end, i won't go away\nAnd won't say never",
                     1, 2)
    card_image = generate_event_image(card)
    screen.blit(card_image, (0, 0))
    pygame.display.flip()
    sleep(6)

    pygame.display.set_mode((CLIMAX_WIDTH, CLIMAX_HEIGHT))

    card_image = generate_climax_image(ClimaxCard("A fated encounter", "red", 1, None,
                                                  "\"I'm not scared anymore even though it's dark.\n You're strong, Berserker.\n I'm safe if you're there like that.\""))
    screen.blit(card_image, (0, 0))
    pygame.display.flip()
    sleep(2)

if __name__ == "__main__":
    main()