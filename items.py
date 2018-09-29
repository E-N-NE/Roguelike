from constants import Constants


class Item:

    def __init__(self, icon, name, location=(0, 0)):
        self.icon = icon
        self.name = name
        self.location = location


class Potion(Item):

    def __init__(self, name,
                 number, location=(0, 0)):
        self.number = number
        super().__init__(self, Constants.ICONS['potion'], name, location)


class Weapon(Item):

    def __init__(self, name, type,
                 str_multiply, dex_multiply, int_multiply,
                 ac, er, mr,
                 dual=1, doping=[], location=(0, 0)):
        self.type = type
        self.str_multiply = str_multiply
        self.dex_multiply = dex_multiply
        self.int_multiply = int_multiply
        self.ac = ac
        self.er = er
        self.mr = mr
        self.dual = dual
        self.doping = doping
        super().__init__(self, Constants.ICONS['weapon'], name, location)


class Armor(Item):

    def __init__(self, name,
                 ac, er, mr,
                 doping=[], location=(0, 0)):
        self.ac = ac
        self.er = er
        self.mr = mr
        self.doping = doping
        super().__init__(self, Constants.ICONS['armor'], name, location)


class Food(Item):

    def __init__(self, name,
                 nutrition, side_effects=None, location=(0, 0)):
        self.nutrition = nutrition
        self.side_effects = side_effects
        super().__init__(self, Constants.ICONS['food'], name, location)