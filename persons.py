from constants import Constants


class Person:

    def __init__(self, icon, name,
                 vit, str, dex, int,
                 sight, hear, shout,
                 base_ac, base_er, base_mr, base_doping,
                 x, y):
        self.icon = icon
        self.name = name
        self.title = name
        self.hp = vit
        self.vit = vit
        self.sp = vit
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
    def transparency(self):
        return True

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
        return + self.base_ac + self.wear.ac\
               + (self.wield.ac + self.shield.ac*self.dual_wield)\
               * (not self.status['stun'])

    @property
    def er(self):
        return + self.base_er + self.wear.er\
               + self.wield.er + self.shield.er*self.dual_wield

    @property
    def mr(self):
        return + self.base_mr + self.wear.mr\
               + self.wield.mr + self.shield.mr*self.dual_wield

    @property
    def doping(self):
        return + self.wield.doping + self.shield.doping*(1-self.dual_wield)\
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

    @property
    def human_readable_stats(self):
        return \
    ("{}\n"
     "HP:{}/{}\n"
     "MP:{}/{}\n"
     "SP:{}/{}\n"
     "BP:{:<7}SP:{:<7}XP:{}\n"
     "AC:{:<7}ER:{:<7}MR:{}\n"
     "STR:{:<6}DEX:{:<6}INT:{}\n"
     "Wear:{}\n"
     "Wield:{}\n"
     "Shield:{}\n").format(
        self.title,
        self.hp, self.vit,
        self.mp, self.max_mp,
        self.sp, self.vit,
        self.bp, self.sp, self.xp,
        self.ac, self.er, self.mr,
        self.full_str, self.full_dex, self.full_int,
        self.wear.human_readable_stats,
        self.wield.human_readable_stats,
        '-' if self.dual_wield == 1 else self.shield.human_readable_stats
    )

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.vit)

    def meal(self, amount):
        self.mp = min(self.mp + amount, self.max_mp)

    def seal(self, amount):
        self.sp = min(self.sp + amount, self.vit)


class Mob(Person):

    def __init__(self, icon, name, profession, trait,
                 vit, str, dex, int,
                 sight, hear, shout,
                 base_ac, base_er, base_mr, base_doping,
                 x, y):
        self.profession = profession
        self.trait = trait
        self.vit = vit
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
        super().__init__(icon, name,
                         self.profession.vit_modifier(self),
                         self.profession.str_modifier(self),
                         self.profession.dex_modifier(self),
                         self.profession.int_modifier(self),
                         self.profession.sight_modifier(self),
                         self.profession.hear_modifier(self),
                         self.profession.shout_modifier(self),
                         self.profession.base_ac_modifier(self),
                         self.profession.base_er_modifier(self),
                         self.profession.base_mr_modifier(self),
                         self.profession.base_doping_modifier(self),
                         x, y)
        self.title = "{} {}".format(self.name, self.profession.name)
