__author__ = 'hige'


class Ability(object):
    def __init__(self):
        """ """

    def apply_on_card(self, card):
        pass

    def apply_on_board(self, gameboard,side):
        pass

    def revert_on_card(self, card):
        pass

    def revert_on_board(self, gameboard,side):
        pass

    def _get_base_text(self):
        return "ABILITY:\n"

    def get_text(self):
        pass


class PowerModifyAbility(Ability):
    def __init__(self, power_modify):
        self.modify = power_modify

    def apply_on_card(self, card):
        card.power += self.modify

    def get_text(self):
        text = self._get_base_text()
        if (self.modify > 0):
            text += "Increments "
        else:
            text += "Reduces "

        text += "character power points in " + str(abs(self.modify))
        return text


class TemporalModifyAbility(PowerModifyAbility):
    def revert_on_card(self, card):
        card.power -= self.modify

    def get_text(self):
        return super(self.__class__, self).get_text() + " during this turn"


class Card(object):
    """ Simulates a card  """

    def __init__(self, name, color, trigger_icon, ability, flavor_text):
        self.name = name
        self.color = color
        self.trigger_icon = trigger_icon
        self.ability = ability
        self.flavor_text = flavor_text

    def get_color(self):
        return self.color

    def get_trigger_icon(self):
        return self.trigger_icon

    def get_name(self):
        return self.name

    def get_flavor_text(self):
        return self.flavor_text

    def get_ability(self):
        return self.ability


class CharacterCard(Card):
    """Simulates a character card"""

    def __init__(self, name, color, trigger_icon, ability, flavor_text, level, cost, power, soul_points, traits):
        """ Creates a card with the info  """
        super(self.__class__, self).__init__(name, color, trigger_icon, ability, flavor_text)
        self.level = level
        self.cost = cost
        self.power = power
        self.soul_points = soul_points
        self.traits = traits

    def get_level(self):
        return self.level

    def get_cost(self):
        return self.cost

    def get_power(self):
        return self.power

    def get_soul_points(self):
        return self.soul_points

    def get_traits(self):
        return self.traits

    def __str__(self):
        return self.name + " (" + str(self.level) + "," + str(self.cost) + " " + self.color + ")"

    def __repr__(self):
        return self.name + " (" + str(self.level) + "," + str(self.cost) + " " + self.color + ")"


class EventCard(Card):
    """Simulates a character card"""

    def __init__(self, name, color, trigger_icon, ability, flavor_text, level, cost):
        """ Creates a card with the info  """
        super(self.__class__, self).__init__(name, color, trigger_icon, ability, flavor_text)
        self.level = level
        self.cost = cost

    def get_level(self):
        return self.level

    def get_cost(self):
        return self.cost

    def __str__(self):
        return self.name + " (" + str(self.level) + "," + str(self.cost) + " " + self.color + ")"

    def __repr__(self):
        return self.name + " (" + str(self.level) + "," + str(self.cost) + " " + self.color + ")"


class ClimaxCard(Card):
    """ """
    pass


    def __str__(self):
        return self.name + " (" + self.color + " CLIMAX)"

    def __repr__(self):
        return self.name + " (" + self.color + " CLIMAX)"