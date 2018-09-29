from basic_functions import BasicFunctions
from constants import Constants

d = BasicFunctions.d

class Person:

    def __init__(self, icon, name,
                 hp, str, dex, int,
                 base_ac, base_er, base_mr, base_doping,
                 x, y):
        self.icon = icon
        self.name = name
        self.hp = hp
        self.VIT = hp
        self.fp = 0
        self.bp = 0
        self.aware = 0
        self.str = str
        self.dex = dex
        self.int = int
        self.base_ac = base_ac
        self.base_er = base_er
        self.base_mr = base_mr
        self.base_doping = base_doping
        self.wield = Constants.NULL_WEAPON
        self.shield = Constants.NULL_SHIELD
        self.wear = Constants.NULL_ARMOR
        self.dual_wield = 0
        self.status = Constants.STATUS_TEMPLATE.copy()
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
    def hand_ac(self):
        return (self.wield.ac + self.shield.ac * self.dual_wield)\
               * (not self.status['stun'])

    @property
    def ac(self):
        return self.base_ac + self.wear.ac + self.hand_ac

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
        self.hp = min(self.hp+amount, self.VIT)