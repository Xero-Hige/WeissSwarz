__author__ = 'hige'


class Card(object):
    """ Simulates a card  """

    def __init__(self, name, color, trigger_icon, hability):
        self.name = name
        self.color = color
        self.trigger_icon = trigger_icon
        self.hability = hability

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + "(" + self.color + ")"

    def get_color(self):
        return self.name + "(" + self.color + ")"

class CharacterCard(Card):
    """Simulates a character card"""

    def __init__(self, name, color, trigger_icon, hability, level, cost, power, soul_points, trait):
        """ Creates a card with the info  """
        super(self.__class__, self).__init__(name, color, trigger_icon, hability)
        self.level = level
        self.cost = cost
        self.power = power
        self.soul_points = soul_points
        self.trait = trait

    def get_level(self):
        return self.level

    def get_cost(self):
        return self.cost

class ClimaxCard(Card):
    """ """
    pass
