from constants import Icons


class Item:

    def __init__(self, icon, name, unique=True, location=(0, 0)):
        self.icon = icon
        self.name = name
        self.unique = unique
        self.location = location

    @property
    def transparency(self):
        return True


class Potion(Item):

    def __init__(self, name,
                 number, location=(0, 0)):
        self.number = number
        super().__init__(Icons.POTION, name, False, location)


class Weapon(Item):

    def __init__(self, name, type,
                 str_multiply, dex_multiply, int_multiply,
                 ac, er, mr,
                 dual=1, doping=(), location=(0, 0)):
        self.type = type
        self.str_multiply = str_multiply
        self.dex_multiply = dex_multiply
        self.int_multiply = int_multiply
        self.ac = ac
        self.er = er
        self.mr = mr
        self.dual = dual
        self.doping = doping
        super().__init__(Icons.WEAPON, name, True, location)

    @property
    def human_readable_stats(self):
        return \
    ("{}\n"
     "AC:{:<7}ER:{:<7}MR:{}\n"
     "STR:{:<6}DEX:{:<6}INT:{}\n").format(
        self.name,
        self.ac, self.er, self.mr,
        self.str_multiply, self.dex_multiply, self.int_multiply
    )


class Armor(Item):

    def __init__(self, name,
                 ac, er, mr,
                 doping=(), location=(0, 0)):
        self.ac = ac
        self.er = er
        self.mr = mr
        self.doping = doping
        super().__init__(Icons.ARMOR, name, True, location)

    @property
    def human_readable_stats(self):
        return \
    ("{}\n"
     "AC:{:<7}ER:{:<7}MR:{}\n").format(
        self.name,
        self.ac, self.er, self.mr
    )


class Food(Item):

    def __init__(self, name,
                 nutrition, side_effects=None, location=(0, 0)):
        self.nutrition = nutrition
        self.side_effects = side_effects
        super().__init__(Icons.FOOD, name, False, location)
