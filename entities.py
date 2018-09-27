from basic_functions import BasicFunctions
from constants import Constants, Icons

d = BasicFunctions.d

class Entity:

    def __init__(self, icon, name, x, y):
        self.icon = icon
        self.name = name
        self.x = x
        self.y = y


class Potion(Entity):

    def __init__(self, icon, name, number, x=None, y=None):
        self.number = number
        Entity.__init__(self, icon, name, x, y)


class Weapon(Entity):

    def __init__(self, icon, name, type,
                 str_multiply, dex_multiply, int_multiply,
                 ac, er, mr,
                 dual=1, doping=[], x=None, y=None):
        self.type = type
        self.str_multiply = str_multiply
        self.dex_multiply = dex_multiply
        self.int_multiply = int_multiply
        self.ac = ac
        self.er = er
        self.mr = mr
        self.dual = dual
        self.doping = doping
        Entity.__init__(self, icon, name, x, y)


class Armor(Entity):
    def __init__(self, ac, er, mr, icon, name, doping=[], x=None, y=None):
        self.ac = ac
        self.er = er
        self.mr = mr
        self.doping = doping
        Entity.__init__(self, icon, name, x, y)


class Food(Entity):
    def __init__(self, icon, name, nutrition, side_effects=None, x=None, y=None):
        self.nutrition = nutrition
        self.side_effects = side_effects
        Entity.__init__(self, icon, name, x, y)


class Person(Entity):

    def __init__(self, hp, str, dex, int,
                 base_ac, base_er, base_mr, base_doping,
                 icon, name, x, y):
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
        self.wield = Constants.NULL_WEAPON()
        self.shield = Constants.NULL_SHIELD()
        self.wear = Constants.NULL_ARMOR()
        self.dual_wield = 0
        self.status = Constants.STATUS_TEMPLATE()
        self.recalculate()
        Entity.__init__(self, icon, name, x, y)

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
        return (self.wield.ac
                + self.shield.ac * self.dual_wield) * (not self.status['stun'])

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

    def full_str(self):
        return self.str * self.wield.str_multiply

    def full_dex(self):
        return self.dex * self.wield.dex_multiply

    def full_int(self):
        return self.int * self.wield.int_multiply

    def heal(self, amount):
        self.hp = min(self.hp+amount, self.VIT)

    def offense_power(self, attack_type):
        if attack_type == 'hit':
            return (self.str * self.wield.str_multiply
                    + self.dex * self.wield.dex_multiply // 2) // 2
        elif attack_type == 'poke':
            return (self.dex * self.wield.dex_multiply * 2
                    + self.str * self.wield.str_multiply // 2) // 3
        elif attack_type == 'crush':
            return self.str * self.wield.str_multiply
        elif attack_type == 'hex':
            return self.int * self.wield.int_multiply

    def dodge_power(self, attack_type):
        if attack_type == 'hit':
            return d(self.int + self.dex - self.encumbrance())
        elif attack_type == 'poke':
            return d(self.int + d(self.dex - self.encumbrance()))
        elif attack_type == 'crush':
            return d(self.int + self.dex - d(self.encumbrance()))
        elif attack_type == 'hex':
            return d(self.int * self.wield.int_multiply) + self.mr

    def accuracy_power(self, attack_type):
        if attack_type == 'hit':
            return self.int // 2 + self.dex + self.str // 2
        elif attack_type == 'poke':
            return self.int // 2 + self.dex * 2
        elif attack_type == 'crush':
            return self.int // 4 + self.dex // 2 + self.str
        elif attack_type == 'hex':
            return max(self.int * self.wield.int_multiply,
                       self.int * self.wield.int_multiply * 4 // (self.mr + 1))

    def defense_power(self, attack_type):
        if attack_type == 'hit':
            return self.ac
        elif attack_type == 'poke':
            return self.ac // 2
        elif attack_type == 'crush':
            return self.ac
        elif attack_type == 'hex':
            return self.ac//3 + self.mr*self.int

    def bonus_power(self, attack_type, damage):
        if attack_type == 'hit':
            return self.int + self.dex // 2 + damage
        elif attack_type == 'poke':
            return self.dex * 2 + damage
        elif attack_type == 'crush':
            return 1
        elif attack_type == 'hex':
            return damage * 3

    def block_power(self, attack_type, damage):
        if attack_type == 'hit':
            return max(0, self.str + damage)
        elif attack_type == 'poke':
            return max(0, self.str // 3 + damage)
        elif attack_type == 'crush':
            return self.str
        elif attack_type == 'hex':
            return 0