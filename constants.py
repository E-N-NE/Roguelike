from basic_functions import BasicFunctions

d = BasicFunctions.d

class Constants:

    def __init__(self):
        pass

    ER_UNNOMINATOR = 2
    STR_UNNOMINATOR = 4
    EVASION_THRESHOLD = 4

    class AttackType:

        def __init__(self, **kwargs):
            for arg, value in kwargs.items():
                setattr(self, arg, value)

        # def __init__(self, name,
        #              attack_flavour1, attack_flavour2, attack_flavour3,
        #              offense_power, defense_power,
        #              accuracy_power, dodge_power,
        #              block_power, graze_power, hit_power):
        #     self.name = name
        #     self.attack_flavour1 = attack_flavour1
        #     self.attack_flavour2 = attack_flavour2
        #     self.attack_flavour3 = attack_flavour3
        #     self.offense_power = offense_power
        #     self.defense_power = defense_power
        #     self.accuracy_power = accuracy_power
        #     self.dodge_power = dodge_power
        #     self.block_power = block_power
        #     self.graze_power = graze_power
        #     self.hit_power = hit_power

    ATTACK_HIT = AttackType(name='hit',
                            attack_flavour1='fp',
                            attack_flavour2='hp',
                            attack_flavour3='bp',
                            offense_power=
       lambda person           : (person.full_str + person.full_dex//2) // 2,
                            defense_power=
       lambda person           : person.ac,
                            accuracy_power=
       lambda person, distance : person.int//2 + person.dex + person.str//2,
                            dodge_power=
       lambda person           : d(person.int+person.dex-person.encumbrance),
                            block_power=
       lambda person, damage   :  max(0, person.str + min(0, damage)),
                            graze_power=
       lambda person, damage   : damage,
                            hit_power=
       lambda person, damage   : person.int + person.dex//2 + damage
                            )

    ATTACK_FLAVOURS = {
                       'hit'   : ('hp', 'bp', 'fp'),
                       'poke'  : ('hp','bp','fp'),
                       'crush' : ('hp','stun','fp'),
                       'hex'   : ('mp','fp','none')
                       }
    ATTACK_POWERS = {
                     'hit'   : (lambda x: (x.str*x.wield.str_multiply
                                + x.dex*x.wield.dex_multiply//2)//2,
                                lambda x: (d(x.int + x.dex
                                             - x.encumbrance())),
                                )
                     }
    # Those three return new instance of a class by template.
    @staticmethod
    def NULL_WEAPON():
        return Weapon('''Something''')


class Icons:

    def __init__(self):
        pass

    WEAPON_ICON = '!'
    POTION_ICON = '?'
    FOOD_ICON = '%'
    ARMOR_ICON = '['
    SHIELD_ICON = ']'
    ACCESSORY_ICON = '"'
    WALL_ICON = '#'
    DOOR_ICON = '+'


class StageInfo:

    def __init__(self, map):
        self.map = map

