from basic_functions import d
from constants import Constants


class Person:

    def __init__(self, icon, name,
                 hp, str, dex, int,
                 base_ac, base_er, base_mr, base_doping,
                 sight, hear, shout,
                 x, y):
        self.icon = icon
        self.name = name
        self.title = name
        self.hp = hp
        self.vit = hp
        self.sp = hp
        self.xp = 0
        self.fp = 0
        self.bp = 0
        self.aware = 0
        self.str = str
        self.dex = dex
        self.int = int
        self.sight = sight
        self.hear = hear
        self.shout = shout
        self.base_ac = base_ac
        self.base_er = base_er
        self.base_mr = base_mr
        self.base_doping = base_doping
        self.wield = Constants.NULL_WEAPON
        self.shield = Constants.NULL_SHIELD
        self.wear = Constants.NULL_ARMOR
        self.mp = self.max_mp
        self.dual_wield = 0
        self.status = Constants.STATUS_TEMPLATE
        self.x = x
        self.y = y

    @property
    def max_mp(self):
        return self.full_int\
               * Constants.ER_UNNOMINATOR\
               // (Constants.ER_UNNOMINATOR+self.er)

    @property
    def encumbrance(self):
        return self.er\
               * Constants.STR_UNNOMINATOR\
               // (Constants.STR_UNNOMINATOR + self.str)

    @property
    def ac(self):
        return self.base_ac + self.wear.ac\
               + (self.wield.ac + self.shield.ac * self.dual_wield)\
               * (not self.status['stun'])

    @property
    def er(self):
        return self.base_er + self.wear.er\
               + self.wield.er + self.shield.er*self.dual_wield

    @property
    def mr(self):
        return self.base_mr + self.wear.mr\
               + self.wield.mr + self.shield.mr*self.dual_wield

    @property
    def doping(self):
        return self.wield.doping + self.shield.doping*(1-self.dual_wield)\
               + self.wear.doping + self.base_doping

    @property
    def full_str(self):
        return self.str * self.wield.str_multiply

    @property
    def full_dex(self):
        return self.dex * self.wield.dex_multiply

    @property
    def full_int(self):
        return self.int * self.wield.int_multiply

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.vit)

    def meal(self, amount):
        self.mp = min(self.mp + amount, self.max_mp)

    def seal(self, amount):
        self.sp = min(self.sp + amount, self.vit)


class Mob(Person):

    def __init__(self, icon, name, profession, trait,
                 hp, str, dex, int,
                 base_ac, base_er, base_mr, base_doping,
                 sight, hear, shout,
                 x, y):
        super().__init__(self, icon, name,
                         hp, str, dex, int,
                         base_ac, base_er, base_mr, base_doping,
                         sight, hear, shout,
                         x, y)
        self.profession = profession
        self.trait = trait
        self.modify()

    def modify(self):  # NOOOOOOOOO THIS DOESN'T WORK, CRAAAAAAAAP!!!!
        if self.profession.name:
            self.str = self.profession.str_modifier(self)
            self.dex = self.profession.dex_modifier(self)
            self.int = self.profession.int_modifier(self)
            self.vit = self.profession.vit_modifier(self)
            self.base_ac = self.profession.base_ac_modifier(self)
            self.base_er = self.profession.base_er_modifier(self)
            self.base_mr = self.profession.base_mr_modifier(self)
            self.base_doping = self.profession.base_doping_modifier(self)
            self.sight = self.profession.sight_modifier(self)
            self.hear = self.profession.hear_modifier(self)
            self.shout = self.profession.shout_modifier(self)
            self.title = "{} {}".format(self.name, self.profession.name)
